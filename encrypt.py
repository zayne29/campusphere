import base64
import json
import uuid
import random
from pyDes import des, CBC, PAD_PKCS5
def DESEncrypt(s,Key="b3L26XNL"):
    iv = b"\x01\x02\x03\x04\x05\x06\x07\x08"
    k = des(Key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    encrypt_str = k.encrypt(s)
    return base64.b64encode(encrypt_str).decode()
extension = {
            "systemName": "android",
            "systemVersion": "11",
            "model": "MI 11",
            "deviceId": str(uuid.uuid4()),
            "appVersion": "9.0.0",
            "lon": 23.0,
            "lat": 116.0,
            "userId": str(random.randint(1,50))+"1133"+str(random.randint(1,50)),
        }
print(DESEncrypt(json.dumps(extension)))