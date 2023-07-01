import time, uuid, hmac, hashlib, base64, os
from requests import request

BASE_URL = 'https://core-vpn.chaordicsystems.com'
API_TOKEN = os.environ['PRITUNL_API_TOKEN']
API_SECRET = os.environ['PRITUNL_API_SECRET']

def base_request(path, method="GET"):
    auth_timestamp = str(int(time.time()))
    auth_nonce = uuid.uuid4().hex
    auth_string = '&'.join([API_TOKEN, auth_timestamp, auth_nonce,
        method, path]).encode("utf-8")
    auth_signature = base64.b64encode(hmac.new(
        str.encode(API_SECRET), auth_string, hashlib.sha256).digest())
    auth_headers = {
        'Auth-Token': API_TOKEN,
        'Auth-Timestamp': auth_timestamp,
        'Auth-Nonce': auth_nonce,
        'Auth-Signature': auth_signature,
        'Content-Type': 'application/json'
    }

    return request(url=BASE_URL+path, headers=auth_headers, method=method)