# coding=utf-8

from flask import Flask,request,make_response
import xmltodict
import hashlib
import time
app = Flask(__name__)

# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')


@app.route('/wechat8009',methods=['GET','POST'])
def wechat_8024():
    if request.method == 'GET':
        token = 'pythonliu'
        signature = request.args.get('signature')
        timestamp = request.args.get('timestamp')
        nonce = request.args.get('nonce')
        echostr = request.args.get('echostr')

        # 校验参数
        temp = [token,timestamp,nonce]
        temp.sort()
        data = ''.join(temp)
        # 调用sha1中的方法进加密，与signature对比
        if hashlib.sha1(data).hexdigest() == signature:
            return make_response(echostr)
        else:
            return 'error',777
        """
        <ToUserName><![CDATA[gh_866835093fea]]></ToUserName>
        <FromUserName><![CDATA[ogdotwSc_MmEEsJs9-ABZ1QL_4r4]]></FromUserName>
        <CreateTime>1478317060</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[你好]]></Content>
        <MsgId>6349323426230210995</MsgId>

        """
    else:
        # 文本消息处理，request有个ｄａｔａ属性，记录请求的数据，并转为字符串
        xml_data = request.data
        # 获取ｘｍｌ格式数据
        req = xmltodict.parse(xml_data)['xml']
        # 获取参数的数据类型
        type = req.get('MsgType')
        if 'text' == type:
            resp = {
                'ToUserName':req.get('FromUserName'),
                'FromUserName':req.get('ToUserName'),
                'CreateTime':int(time.time()),
                'MsgType':'text',
                'Content':req.get('Content')
            }

            # 把响应数据转成ｘｍｌ格式
            data = xmltodict.unparse({'xml':resp})
            print resp['Content']
            print data
            return data

        elif 'voice' == type:
            resp = {
                'ToUserName': req.get('FromUserName'),
                'FromUserName': req.get('ToUserName'),
                'CreateTime': int(time.time()),
                'MsgType': 'text',
                'Content': req.get('Recognition', u'口音比较重')
            }

            data = xmltodict.unparse({'xml':resp})
            return data
        else:
            resp = {
                'ToUserName':req.get('FromUserName'),
                'FromUserName': req.get('ToUserName'),
                'CreateTime': int(time.time()),
                'MsgType': 'text',
                'Content': 'I LOVE PYTHON24'
            }
            data = xmltodict.unparse({'xml':resp})

            return data

if __name__ == '__main__':
    app.run(debug=True,port=8009)
