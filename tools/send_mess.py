import requests
import random
from send import API_KEY


class YunPian(object):

    def __init__(self, api_key):
        self.api_key = api_key
        # 使用云片网提供的第三方接口完成短信发送
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_message(self, phone, code):
        parmas = {
            'apikey': self.api_key,
            'mobile': phone,
            'text': "【毛信宇test】您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code)
        }
        req = requests.post(self.single_send_url, data=parmas)
        print(req)


if __name__ == '__main__':
    yun_pian = YunPian(API_KEY)
    yun_pian.send_message("17331413566", "123456")
