import hmac
import hashlib
import time
import base64
from requests.auth import AuthBase


class AuthProvider(AuthBase):
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key


    def __call__(self, request):
        timestamp = int(time.time() *  1000)
        message = ''.join([request.path_url, request.method, str(timestamp), (request.body or '')])
        headers = get_auth_headers(timestamp, message, self.api_key, self.secret_key)
        request.headers.update(headers)

        return request
    

def get_auth_headers(timestamp, message, api_key, secret_key):
    message = message.encode('ascii')
    hmac_key = base64.b64decode(secret_key)
    signature = hmac.new(hmac_key, message, hashlib.sha256)
    signature_b64 = base64.b64encode(signature.digest()).decode('utf-8')

    return {
        'Content-Type': 'application/json',
        'DEV-SHRIMPY-API-KEY': api_key,
        'DEV-SHRIMPY-API-NONCE': timestamp,
        'DEV-SHRIMPY-API-SIGNATURE': signature_b64
    }