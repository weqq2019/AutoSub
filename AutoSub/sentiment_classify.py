# -*- coding: utf-8 -*-

import time
import base64
import requests
import json
from datetime import datetime
print(datetime.now())

start = time.time()
# 获取access_token
# client_id 为官网获取的AK， client_secret 为官网获取的SK
appid = "34644185"
client_id = "2vQxvtSwB8BXtuI5BjRfG4if"
client_secret = "mfSN5DPBezD4mwPek2FAD2SRXKys94cp"
print("appid:" + appid)
print("client_id:" + client_id)
print("client_secret:" + client_secret)

token_url = "https://aip.baidubce.com/oauth/2.0/token"
host = f"{token_url}?grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}"

response = requests.get(host)
access_token = response.json().get("access_token")


# 调用情感倾向分析接口
request_url = "https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify"
# 参数text
# 下面文本参数请自行切换为自己环境的文本内容
text="你测试总是不行,为什么？"
body = {
	"text": text,
}
body = json.dumps(body)
headers = {"Content-Type": "application/json"}
request_url = f"{request_url}?access_token={access_token}"
response = requests.post(request_url, headers=headers, data=body)
content = response.json()
# 打印调用结果
print(content)

end = time.time()
print(f"Running time: {(end-start):.2f} Seconds")