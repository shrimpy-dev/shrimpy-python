import hmac
import hashlib
import time
import base64
import threading
from requests.auth import AuthBase


class AuthProvider(AuthBase):
    def __init__(self, api_key, secret_key, version):
        self.api_key = api_key
        self.secret_key = secret_key
        self.nonce_lock = threading.Lock()
        self.last_nonce = int(time.time() * 1000)
        self.version = version
    
    def __call__(self, request):
        nonce = self.get_nonce()
        message = f"{request.path_url}{request.method}{nonce}{request.body or ''}"
        headers = get_auth_headers(self.version, nonce, message, self.api_key, self.secret_key)
        request.headers.update(headers)
        return request
    
    def get_nonce(self):
        new_nonce = int(time.time() * 1000)
        with self.nonce_lock:
            if new_nonce <= self.last_nonce:
                new_nonce = new_nonce + 1
            self.last_nonce = new_nonce
        return new_nonce


def get_auth_headers(version, timestamp, message, api_key, secret_key):
    message = message.encode('ascii')
    hmac_key = base64.b64decode(secret_key)
    signature = hmac.new(hmac_key, message, hashlib.sha256)
    signature_b64 = base64.b64encode(signature.digest()).decode('utf-8')
    header_prefix = 'DEV-' if version == 'dev' else ''
    
    return {
        'Content-Type': 'application/json',
        f'{header_prefix}SHRIMPY-API-KEY': api_key,
        f'{header_prefix}SHRIMPY-API-NONCE': timestamp,
        f'{header_prefix}SHRIMPY-API-SIGNATURE': signature_b64
    }
