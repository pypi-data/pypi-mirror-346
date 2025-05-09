import json
import base64
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


def signer(request: dict, pri_key=""):
    """
    加签
    :param request: 待签名dict对象
    :param pri_key: 密钥路径
    :return: 签名(str)
    """
    if pri_key == "":
        print("请输入密钥路径")
        return
    with open(pri_key, mode='rb') as f:
        rsa_key = RSA.import_key(f.read())
    pkcs = PKCS1_v1_5.new(rsa_key)
    sha256_hash = SHA256.new(json.dumps(request, separators=(',', ':'), ensure_ascii=False).encode('utf-8'))
    return base64.b64encode(pkcs.sign(sha256_hash)).decode('utf-8')


def verifier(response: dict, signature: str, pub_key: str) -> bool:
    """
    验签
    :param response: 待验签的dict对象
    :param signature: 签名
    :param pub_key: 公钥路径
    :return: bool
    """
    if pub_key == "":
        print("请输入密钥路径")
        return
    with open(pub_key, mode='rb') as f:
        rsa_key = RSA.import_key(f.read())
    pkcs = PKCS1_v1_5.new(rsa_key)
    sha256_hash = SHA256.new(json.dumps(response, separators=(',', ':'), ensure_ascii=False).encode('utf-8'))
    signature_hash = base64.b64decode(signature)
    return pkcs.verify(sha256_hash, signature_hash)
