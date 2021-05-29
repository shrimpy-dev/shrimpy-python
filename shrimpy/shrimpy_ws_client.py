import asyncio
import asyncio.tasks
import json
import websockets
import websockets.client
import websockets.exceptions
import threading


def get_topic(message):
    """
    Gets the topic given a message sent from the client / server
    """
    try:
        # Only ping, error messages have a type
        message_type = message.get('type', None)
        if (message_type is not None) and (message_type.find('subscribe') == -1):
            return message_type.lower()
        
        exchange = message.get('exchange', None)
        pair = message.get('pair', None)
        channel = message['channel']  # Channel must be present
        keys = [exchange, pair, channel]
        keys = filter(lambda k: k is not None, keys)
    except KeyError:
        raise InvalidSubscriptionException()
    
    if not keys:
        raise InvalidSubscriptionException()
    
    return str('-'.join(keys)).lower()


class ConnectionFailureException(Exception):
    pass


class ShrimpyConnectionClosed(Exception):
    pass


class InvalidSubscriptionException(Exception):
    pass


class ShrimpyWsException(Exception):
    
    def __init__(self, shrimpy_ws_error_json):
        super(ShrimpyWsException, self).__init__()
        shrimpy_raw_error = json.loads(shrimpy_ws_error_json)
        self.error_code = shrimpy_raw_error.get('code', None)
        self.error_message = shrimpy_raw_error.get('message', None)


class ShrimpyWsClient:
    """
    The Shrimpy Websocket Client is intended to be used to access the websocket streams
    and manipulate the data received using callbacks.

    It provides reconnection and ping management. Errors received while streaming data
    are routed to the error callbacks defined per subscription. If no callbacks
    are defined, errors must be handled explicitly.
    """
    
    def __init__(self, error_handler=None, token=None):
        self.base_url = 'wss://ws-feed.shrimpy.io'
        self.subscription_handlers = {}
        self.error_handler = error_handler
        self.pending_messages_to_send = []
        self.pending_messages_lock = threading.Lock()
        self.socket_thread = None
        self.is_closed = False
        self.connection = None
        self.connection_close_timeout = 10
        self.token = token
    
    def connect(self):
        self.socket_thread = threading.Thread(target=self._run_socket_thread)
        self.socket_thread.start()
    
    def disconnect(self):
        if self.is_closed:
            # Already closed
            return
        
        self.is_closed = True
        self.socket_thread.join()
    
    def subscribe(self, subscription_data, handler):
        """
            Sending subscription_data to webSocket server
        """
        with self.pending_messages_lock:
            self.pending_messages_to_send.append(subscription_data)
        
        topic = get_topic(subscription_data)
        self.subscription_handlers[topic] = handler
    
    def unsubscribe(self, subscription_data):
        """
            Sending subscription_data to webSocket server
        """
        with self.pending_messages_lock:
            self.pending_messages_to_send.append(subscription_data)
        
        topic = get_topic(subscription_data)
        del self.subscription_handlers[topic]
    
    # noinspection PyBroadException
    def _run_socket_thread(self):
        loop = asyncio.new_event_loop()
        try:
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self._connect())
            loop.run_until_complete(self._receive_message_handler())
            print(loop)
        except Exception:
            # Exceptions must be handled via the error handler
            pass
        finally:
            for task in asyncio.Task.all_tasks():
                task.cancel()
            loop.run_until_complete(self._disconnect())
            loop.stop()
    
    async def _connect(self):
        """
            Handle connecting to shrimpy websocket server
        """
        url = self.base_url
        if self.token:
            url = self.base_url + "?token=" + self.token
        
        self.connection = await websockets.client.connect(url)
        if (self.connection is None) or (not self.connection.open):
            raise ConnectionFailureException('Failed to start the connection. Please reconnect.')
        
        self.is_closed = False
    
    # noinspection PyBroadException
    async def _disconnect(self):
        """
            Disconnect from the shrimpy websocket server
        """
        if self.connection is not None:
            try:
                await self.connection.close()
            except Exception:
                # Exceptions during connection termination aren't very useful
                pass
    
    async def _reconnect(self, token=None):
        self.token = token
        await self._disconnect()
        await self._connect()
    
    async def _receive_message_handler(self):
        """
            The core loop that runs the websocket logic
        """
        while True:
            if self.is_closed:
                return
            
            try:
                # First send pending messages
                
                with self.pending_messages_lock:
                    pending_messages_to_send, self.pending_messages_to_send = self.pending_messages_to_send, []
                
                for pending_message in pending_messages_to_send:
                    await self.connection.send(json.dumps(pending_message))
                
                # Parse message and use handler based on the type
                message = await self.connection.recv()
                parsed_message = json.loads(message)
                topic = get_topic(parsed_message)
                
                if topic == 'ping':
                    await self._pong(parsed_message['data'])
                else:
                    await self._run_handler(topic, parsed_message)
            
            except websockets.exceptions.ConnectionClosed:
                raise ShrimpyConnectionClosed()
    
    async def _run_handler(self, topic, parsed_message):
        try:
            loop = asyncio.get_event_loop()
            if topic == 'error':
                if self.error_handler is not None:
                    loop.run_in_executor(None, self.error_handler, parsed_message)
                else:
                    raise ShrimpyWsException(json.dumps(parsed_message))
            else:
                subscription_handler = self.subscription_handlers[topic]
                loop.run_in_executor(None, subscription_handler, parsed_message)
        except KeyError:
            # The client has unsubscribed from this topic
            pass
    
    async def _pong(self, data):
        """
        Sending heartbeat to server based on data received from the server in the
        ping message to keep the connection alive.
        """
        try:
            pong_data = {
                'type': 'pong',
                'data': data
            }
            await self.connection.send(json.dumps(pong_data))
        except websockets.exceptions.ConnectionClosed:
            raise ShrimpyConnectionClosed()
