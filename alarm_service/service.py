#导入发短信相关模块
import twilio.twiml
from flask import Flask, request, redirect
from twilio.rest import Client
from passwords import *
#导入发邮件相关模块
from email import encoders
from email.header import Header
from email.utils import parseaddr, formataddr
from email.mime.text import MIMEText
import smtplib
import time
import threading

#发短信用户id
account_sid = '?'
auth_token = '?'

#建立短信链接
client = Client(account_sid, auth_token)

# 输入SMTP服务器地址:
smtp_server = 'smtp.qq.com'
# 输入Email地址和口令:
from_addr ='1149006285@qq.com'
password_smtp ='?'
# 输入收件人地址:
to_addr4 = '1821321180@qq.com'

def sendMail(TheMessage):
    #连接SMTP服务器
    server_smtp = smtplib.SMTP_SSL(smtp_server, 465) # SMTP协议默认端口是25
    #是否显示调试信息，1显示，0不显示
    server_smtp.set_debuglevel(0)
    #登录
    server_smtp.login(from_addr, password_smtp)
    msg = MailGeneration(TheMessage)
    server_smtp.sendmail(from_addr,to_addr4, msg)

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def MailGeneration(st):
    msg = MIMEText(st, 'plain', 'utf-8')
    #构造头部From信息
    msg['From'] = _format_addr('树莓派邮件警报器 <%s>' % from_addr)
    #构造头部Subject信息
    msg['Subject'] = Header('Alert from raspberry pi', 'utf-8').encode()
    return str(msg)

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def AlertService():
    TheMessage=request.form.get("Body")
    if (TheMessage != None):
        print(TheMessage)
        client.messages.create(to=+8613205031827, from_=+14805259719, body=TheMessage)
        print('\n*****已发送警报短信！*****')
        sendMail(TheMessage)
        print('\n*****已发送警报邮件！*****')
    return str(TheMessage)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
