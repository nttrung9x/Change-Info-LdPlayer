import requests
import json
class OTPHelper:

    def __init__(self, api_VOTP=None, api_CTN=None, api_CTSC=None):

        self.api_VOTP = api_VOTP
        self.api_CTN = api_CTN
        self.api_CTSC = api_CTSC

    def GetNumberVOTP(self):
        get = requests.get(("https://api.viotp.com/request/get?token={0}&serviceId=7").format(self.api_VOTP)).json()

        number = get['data']['phone_number']
        id = get['data']['request_id']

        return number, id

    def GetOTPVOTP(self,id):
        get = requests.get(('https://api.viotp.com/session/get?requestId={0}&token={1}').format(id, self.api_VOTP)).json()
        otp = get['data']['Code']
        return otp

    def GetNumberCTN(self):
        param = "&apikey={0}&action=create-request&serviceId=1&count=1".format(self.api_CTN)
        get = requests.get("http://codetextnow.com/api.php", params=param)
        number = json.loads(get.text)['results']['data'][0]
        return number['sdt'], number['requestId']

    def GetOTPCTN(self, requestid):
        param = "&apikey={0}&action=data-request&requestId={1}".format(self.api_CTN, requestid)
        getCode = requests.get("http://codetextnow.com/api.php", params=param).json()
        otp = getCode['data'][0]['otp']
        return otp

    def GetMailCTN(self):
        param = "&apikey={0}&action=create-request&serviceId=3&count=1".format(self.api_CTN)
        get = requests.get("http://codetextnow.com/api.php", params=param)
        number = json.loads(get.text)['results']['data'][0]
        return number['email'], number['requestId']

    def GetOTPMailCTN(self, requestid):
        param = "&apikey={0}&action=data-request-tempmail&requestId={1}".format(self.api_CTN, requestid)
        getCode = requests.get("http://codetextnow.com/api.php", params=param).json()
        otp = getCode['data'][0]['otp']
        return otp

class ProxyHelper:

    def GetCurrentProxyTM(self,api):
        param = {
            "api_key": api
        }
        request = requests.post("https://tmproxy.com/api/proxy/get-current-proxy", json=param).json()
        return request['data']['https']

    def GetNewProxyTM(self,api):
        param = {
            "api_key": api
        }
        request = requests.post("https://tmproxy.com/api/proxy/get-new-proxy", json=param).json()
        return request['data']['https']