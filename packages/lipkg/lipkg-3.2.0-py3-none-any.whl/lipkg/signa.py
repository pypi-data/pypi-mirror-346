import json
import base64
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


def rsakey(key_file) -> bytes:
    """
    获取rsa密钥
    @param key_file: rsa密钥文件路径
    @return: rsa密钥字节内容
    """
    with open(key_file, mode='rb') as f:
        return RSA.import_key(f.read())


def getSignature(rsa_key_bytes: bytes, data: dict, ensure_ascii=False):
    pkcs = PKCS1_v1_5.new(rsa_key_bytes)
    data_bytes = json.dumps(data, separators=(',', ':'), ensure_ascii=ensure_ascii).encode('utf-8')
    sha256 = SHA256.new(data_bytes)
    signature = base64.b64encode(pkcs.sign(sha256)).decode('utf-8')
    return signature


def verifySignature(rsa_key_bytes: bytes, data: dict, signature: str, ensure_ascii=False):
    pkcs = PKCS1_v1_5.new(rsa_key_bytes)
    signature_hash = base64.b64decode(signature)
    data_bytes = json.dumps(data, separators=(',', ':'), ensure_ascii=ensure_ascii).encode('utf-8')
    sha256 = SHA256.new(data_bytes)
    flag = pkcs.verify(sha256, signature_hash)
    return flag