import base64
import hmac, hashlib
import time
import os

def generate_random_secret():
    import os
    return base64.b32encode(os.urandom(20)).decode('utf-8').replace('=', '')

def get_totp_token(secret_key, time_step=30):
    t = int(time.time() // time_step)
    key = base64.b32decode(secret_key, casefold=True)
    msg = t.to_bytes(8, 'big')
    hm = hmac.new(key, msg, hashlib.sha1).digest()
    offset = hm[-1] & 0x0f
    code = (hm[offset] & 0x7f) << 24 \
           | (hm[offset+1] & 0xff) << 16 \
           | (hm[offset+2] & 0xff) << 8 \
           | (hm[offset+3] & 0xff)
    return str(code % 10**6).zfill(6)

def verify_token(secret_key, token, time_step=30, window=1):
    token_str = str(token).zfill(6)
    for offset in range(-window, window+1):
        t = int(time.time() // time_step) + offset
        key = base64.b32decode(secret_key, casefold=True)
        msg = t.to_bytes(8, 'big')
        hm = hmac.new(key, msg, hashlib.sha1).digest()
        offset_ = hm[-1] & 0x0f
        code = (hm[offset_] & 0x7f) << 24 \
               | (hm[offset_+1] & 0xff) << 16 \
               | (hm[offset_+2] & 0xff) << 8 \
               | (hm[offset_+3] & 0xff)
        calc = str(code % 10**6).zfill(6)
        if calc == token_str:
            return True
    return False
