# -*- coding: utf8 -*-

import requests
import json
import datetime
 
global contents
contents = ''
 
def sign(): 
    #金山词霸每日一句
    url = "http://open.iciba.com/dsapi/"
    r = requests.get(url)
    r = json.loads(r.text)
    content = r["content"]
    note = r["note"]
    daily_sentence = content + "\n" + note

    #one  接口api
    # http://api.tianapi.com/txapi/one/index?key=06f67dbab9e2610f9a15f44a85540110
    oneUrl = "http://api.tianapi.com/txapi/one/index?key=06f67dbab9e2610f9a15f44a85540110"
    oneResponse = requests.get(oneUrl)
    oneResponse = json.loads(oneResponse.text)
    oneArr = oneResponse["newslist"]
    oneObj = oneArr[0]
    wordfrom = oneObj["wordfrom"]
    word = oneObj["word"]
    if len(wordfrom) == 0:
        wordfrom = "——来源于《one》"
    one_sentence = word + '\n' + wordfrom
    print(one_sentence)
 
    # 获取日期和倒计时    
    a = datetime.datetime.now()  # 实施时间
    y = str(a.year)
    m = str(a.month)
    d = str(a.day)  # 转换为字符串，便于打印
    time = y + '年' + m + '月' + d + '日' + '\n'
    b = datetime.datetime(2013, 5, 28)  # 自己设置的时间
    count_down = (a - b).days  # 差值
    count_down = '我们相爱了{}天，加油哦！'.format(count_down) 

    # 企业微信推送
    serverWechat(count_down + '\n' + '\n' + daily_sentence + '\n' + '\n' + one_sentence)

    # qq推送
    # qqtalk = 'https://qmsg.zendee.cn/send/[qmsgkey码]?msg=' +count_down+'\n' + daily_sentence + '&qq=[qq号]'
    # requests.get(qqtalk)


#企业微信推送
def serverWechat(content):
    # WangYingBo|RouQiuEr
    toUser = "WangYingBo|RouQiuEr"
    # post 
    myContent = "恋爱通知：\n \n" + content
    message = {"key":"4ours","title":"hi","num":"1","msgtype":"1","content":myContent,"touser":toUser}
    # 1、post请求
    r = requests.post("http://129.148.39.121:5005/wechat", data=json.dumps(message))
    if r.status_code == 200:
        print('[+]企业微信已推送，请查收')
    
    # 2、get请求
    myWeather = "" + content
    # ftStr = 'https://service-d606bcz6-1304203451.usw.apigw.tencentcs.com/release/wecomchan?sendkey=wangyingbo&to_user=' + toUser + '&msg_type=text&msg=' + myWeather
    # 不拼接to_user字段时，默认是全部发送
    ftStr = 'http://129.148.39.121:5005/wechat?key=WangYingBo&title=标题&num=1&msgtype=1&content=' + myWeather
    # requests.get(ftStr)



def main():
    sign()
 
def main_handler(event, context):
    return main()
 
if __name__ == '__main__':
    main()