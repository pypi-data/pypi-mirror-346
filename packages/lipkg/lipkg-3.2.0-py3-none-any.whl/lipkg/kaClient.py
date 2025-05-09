import json
import logging
from lipkg import signa
from lipkg.apiUtils import ApiUtils
from lipkg.httpClient import HttpClient


class KaClient(HttpClient):
    
    def __init__(self, *, domain, appid, priKeyPath, pubKeyPath):
        self.appid = appid
        self.priKey = signa.rsakey(priKeyPath)
        self.pubKey = signa.rsakey(pubKeyPath)
        self.logger = logging.getLogger(f'{__name__}')
        super().__init__(domain)

    def _call(self, *, endpoint, method, headers, biz_body):
        """ 调用KA接口, 并进行签名与验证 """
        payload = self._ka_body()
        payload['request']['body'].update(biz_body)
        payload['signature'] = signa.getSignature(rsa_key_bytes=self.priKey, data=payload.get('request')) # type: ignore
        allinfo = super()._call(endpoint=endpoint, method=method, headers=headers, payload=payload)
        ResponseBody = allinfo.get('ResponseBody')
        response = ResponseBody['response'] # type: ignore
        response_signature = ResponseBody['signature'] # type: ignore
        varify_result = signa.verifySignature(rsa_key_bytes=self.pubKey, data=response, signature=response_signature) # type: ignore
        self.logger.info(f'接口报文: \n{json.dumps(allinfo, ensure_ascii=False, indent=4)}\n 接口返回报文签名验证结果: {varify_result}')
        if not varify_result:
            raise Exception('签名验证失败')
        return allinfo
    
    def _ka_body(self):
        """ 生成KA接口报文标准格式 """
        payload = {
            "request": {
                "head": {
                    "version": "1.0.0",
                    "appid": self.appid,
                    "sign_type": "SHA256",
                    "request_time": ApiUtils.now(),
                },
                "body": dict(),
            },
            "signature": ""
        }
        return payload