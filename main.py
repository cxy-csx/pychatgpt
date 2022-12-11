from flask import Flask, request
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy import parse_message
from wechatpy.replies import TextReply
import requests

app = Flask(__name__)

TOKEN = "公众号Token"

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer 填写API_KEY'
}


@app.route("/", methods=["GET", "POST"])
def index():
    if (request.method == "GET"):
        signature = request.args.get('signature')
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')
        echostr = request.args.get('echostr')
        token = TOKEN
        try:
            check_signature(token, signature, timestamp, nonce)
        except InvalidSignatureException:
            # 处理异常情况或忽略
            return "校验失败"
        # 校验成功
        return echostr
    if (request.method == "POST"):
        xml_str = request.data
        # 解析xml格式数据
        msg = parse_message(xml_str)
        xml_str = request.data
        # 解析xml格式数据
        msg = parse_message(xml_str)
        # 1.目标用户信息
        target = msg.target
        # 2.发送用户信息
        source = msg.source
        # 3.消息类型
        msgType = msg.type
        # 4.消息内容
        msgCcontent = msg.content

        print(msgCcontent)

        reply = TextReply()
        reply.source = target
        reply.target = source
        # answer = chat.ask(msgCcontent)[0]

        

        json_data = {
            'model': 'text-davinci-003',
            'prompt': msgCcontent,
            'max_tokens': 2000,
            'temperature': 0
        }

        response = requests.post('https://api.openai.com/v1/completions', headers=headers, json=json_data)
        reply.content = response.json()['choices'][0]['text'].strip()
        print(reply.content)
        # 包装成XML格式的数据
        xml = reply.render()
        return xml


if __name__ == '__main__':
    app.run(port=80)
