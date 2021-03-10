import requests
import json

class weixin(object):

    def __init__(self, ID, Secret):
        self.ID = ID
        self.Secret = Secret


    def get_access_token(self):
        get_token_url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}".format(self.ID, self.Secret)
        r = requests.get(get_token_url)
        r = r.json()
        access_token = r["access_token"]
        return access_token


    def send_message(self, access_token, message, to_user = "@all", agentid = "1"):
        send_message_url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(access_token)
        message_params = {
            "touser": to_user,
            "msgtype": "text",
            "agentid": agentid,
            "text": {
                "content": message
            },
            "safe": "0"
        }
        requests.post(send_message_url, data=json.dumps(message_params))
