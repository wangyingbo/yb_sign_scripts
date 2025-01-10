"""
cron: 0 5,17 * * *
"""

import requests ,os,json
from time import sleep

# server酱开关，填0不开启(默认)，填2同时开启cookie失效通知和签到成功通知
sever = 'on'
referer = 'https://glados.rocks/console/checkin'

class Model:
	def __init__(self,name,sckey,wcuser,cookie):
		self.name = name
		self.sckey = sckey
		self.wcuser = wcuser
		self.cookie = cookie

def start():  
    url= "https://glados.rocks/api/user/checkin"
    url2= "https://glados.rocks/api/user/status"
    origin = "https://glados.rocks"
    referer = "https://glados.rocks/console/checkin"
    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
    payload={
        'token': 'glados.one'
    }
        
    # -----------------------通过对象创建----------------------------------
    objArray = []
    # Model("mail","sckey","wechatUserId","cookie")

    # 泽东
    userJZD = Model("zidonj_163","none","WangYingBo","__stripe_mid=9a7bd424-66ba-4812-900c-a871fccb640e0dc722; koa:sess=eyJ1c2VySWQiOjEwMTQ4MywiX2V4cGlyZSI6MTc1NjI1NjUyMDYwNSwiX21heEFnZSI6MjU5MjAwMDAwMDB9; koa:sess.sig=opTl26E1s1Xi7w4zaJkfwsCVa9A; _ga=GA1.2.1926169907.1729136487; _ga_CZFVKMNT9J=GS1.1.1731562164.4.0.1731562166.0.0.0")
    objArray.append(userJZD)

    # 魏总
    userWW = Model("weiwei","none","WangYingBo","koa:sess=eyJ1c2VySWQiOjEwMTk1NywiX2V4cGlyZSI6MTc0NTkwODI3MzYwNSwiX21heEFnZSI6MjU5MjAwMDAwMDB9; koa:sess.sig=5Sbh3vczLPYhEEDLHm1i0wsvQfo; _gid=GA1.2.1598444316.1719988274; _ga=GA1.1.1149206999.1704702146; _ga_CZFVKMNT9J=GS1.1.1719988273.11.1.1719988274.0.0.0")
    objArray.append(userWW)
    

    for obj in objArray:
        sleep(0.5)
        checkin = requests.post(url,headers={'cookie': obj.cookie ,'referer': referer,'origin':origin,'user-agent':useragent,'content-type':'application/json;charset=UTF-8'},data=json.dumps(payload))
        state =  requests.get(url2,headers={'cookie': obj.cookie ,'referer': referer,'origin':origin,'user-agent':useragent})
        # print(res)
        print('-------------step1-----------')
        print(checkin.json())
        print(state.json())
        print('\n')
        if 'message' in checkin.text:
            sckey = obj.sckey
            wcuser = obj.wcuser

            mess = checkin.json()['message']
            code = checkin.json()['code']
            if code<0:
                noticeWC('-999',wcuser,sever,obj.name+str(code)+mess)
                continue
                
            stateObj = state.json()
            if 'data' in stateObj:
                print('')
            else:
                noticeWC('-999',wcuser,sever,'response不存在data')
                continue

            responseData = stateObj['data']
            if 'leftDays' in responseData:
                print('')
            else:
                noticeWC('-999',wcuser,sever,'data不存在leftDays')
                continue

            leftDays = responseData['leftDays']
            if isinstance(leftDays,int):
                time = str(leftDays)
            elif isinstance(leftDays,str):
                time = leftDays.split('.')[0]
            print("---------------------**---------------------")
            print('剩余时长：' + time)
            print(mess)
            messStr = obj.name + ', ' + mess
            if len(sckey) > 0:
                notice(time,sckey,sever,messStr)
            if len(wcuser) > 0:
                noticeWC(time,wcuser,sever,messStr)

    # -----------------------server酱----------------------------------
    dict = {}
    # 以&&分割，前面的是邮箱，后面是推送到微信的server酱的sckey
    # dict['2532084725_qq&&SCT75671TT2h5sM8nwaCPkyBQq6XjxgoL'] = "_ga=GA1.2.1461581697.1631507811; koa:sess=eyJ1c2VySWQiOjk5NTY4LCJfZXhwaXJlIjoxNjU3NDI5MDU5NjM3LCJfbWF4QWdlIjoyNTkyMDAwMDAwMH0=; koa:sess.sig=QsLpz_YI-SjEc-EtaCh4LSyzM0Q; _gid=GA1.2.1728200036.1631673727; _gat_gtag_UA_104464600_2=1"
    
    for key in dict:
        checkin = requests.post(url,headers={'cookie': dict[key] ,'referer': referer,'origin':origin,'user-agent':useragent,'content-type':'application/json;charset=UTF-8'},data=json.dumps(payload))
        state =  requests.get(url2,headers={'cookie': dict[key] ,'referer': referer,'origin':origin,'user-agent':useragent})
        # print(res)

        if 'message' in checkin.text:
            mess = checkin.json()['message']
            if mess == '\u6ca1\u6709\u6743\u9650':
                requests.get('https://sc.ftqq.com/' + sckey + '.send?text=' + key + '账号cookie过期')
            time = state.json()['data']['leftDays']
            time = time.split('.')[0]
            #print(time)
            arr = key.split("&&")
            pre_str = ""
            suf_str = ""
            pre_str = arr[0]
            if len(arr) == 2:
                suf_str = arr[1]
            messStr = pre_str + ', ' + mess
            notice(time,suf_str,sever,messStr)

    # -----------------------企业微信----------------------------------
    dictWC = {}
    # 以&&分割，前面的是邮箱，后面是利用企业微信推送到微信的user
    # dictWC['2532084725_qq&&wangyingbo'] = "_ga=GA1.2.1461581697.1631507811; koa:sess=eyJ1c2VySWQiOjk5NTY4LCJfZXhwaXJlIjoxNjU3NDI5MDU5NjM3LCJfbWF4QWdlIjoyNTkyMDAwMDAwMH0=; koa:sess.sig=QsLpz_YI-SjEc-EtaCh4LSyzM0Q; _gid=GA1.2.1728200036.1631673727; _gat_gtag_UA_104464600_2=1"
    # dictWC['wangyingbo0528_gmail&&wangyingbo'] = "_ga=GA1.2.1461581697.1631507811; _gid=GA1.2.1615168255.1632308837; koa:sess=eyJ1c2VySWQiOjEwMTA1OSwiX2V4cGlyZSI6MTY1ODIzMDI5NDkxNCwiX21heEFnZSI6MjU5MjAwMDAwMDB9; koa:sess.sig=dBFYB29eoIsZh3pdJg4eFhzJpz0"
    # dictWC['wangyingbo528_126&&wangyingbo'] = "_ga=GA1.2.1461581697.1631507811; _gid=GA1.2.2032489875.1632628557; koa:sess=eyJ1c2VySWQiOjEwMjE0MywiX2V4cGlyZSI6MTY1ODcxNjAwNDY2NywiX21heEFnZSI6MjU5MjAwMDAwMDB9; koa:sess.sig=xoW6EP40mx5agTgPW-9xYrwZ3-U"

    for key in dictWC:
        checkin = requests.post(url,headers={'cookie': dictWC[key] ,'referer': referer,'origin':origin,'user-agent':useragent,'content-type':'application/json;charset=UTF-8'},data=json.dumps(payload))
        state =  requests.get(url2,headers={'cookie': dictWC[key] ,'referer': referer,'origin':origin,'user-agent':useragent})
        # print(res)

        if 'message' in checkin.text:
            mess = checkin.json()['message']
            if mess == '\u6ca1\u6709\u6743\u9650':
                requests.get('https://sc.ftqq.com/' + sckey + '.send?text=' + key + '账号cookie过期')
            time = state.json()['data']['leftDays']
            time = time.split('.')[0]
            #print(time)
            arr = key.split("&&")
            pre_str = ""
            suf_str = ""
            pre_str = arr[0]
            if len(arr) == 2:
                suf_str = arr[1]
            messStr = pre_str + ', ' + mess
            noticeWC(time,suf_str,sever,messStr)

        
def notice(time,sc_key,sever,mess):
    if sever == 'off':
        return
    if sc_key == 'none':
        return
    if sever == 'on':
        # 用server酱推送
        requests.get('https://sc.ftqq.com/' + sc_key + '.send?text='+mess+'，you have '+time+' days left')

        # 用企业微信推送
        # gladosStr = mess + '，you have ' + time + ' days left'
        # ftStr = 'https://service-d606bcz6-1304203451.usw.apigw.tencentcs.com/release/wecomchan?sendkey=wangyingbo&msg_type=text&msg=' + gladosStr
        # requests.get(ftStr)
    else:
        # 用server酱推送
        requests.get('https://sc.ftqq.com/' + sc_key + '.send?text=通知没打开')

        # 用企业微信推送
        # ftStr = 'https://service-d606bcz6-1304203451.usw.apigw.tencentcs.com/release/wecomchan?sendkey=wangyingbo&msg_type=text&msg=' + "Notification off"
        # requests.get(ftStr)

# 用企业微信推送
def noticeWC(time,user,sever,mess):
    if sever == 'off':
        return
    if user == 'none':
        return
    requests.adapters.DEFAULT_RETRIES = 5
    if sever == 'on':
        gladosStr = mess + '，you have ' + time + ' days left'
        #ftStr = 'https://service-d606bcz6-1304203451.usw.apigw.tencentcs.com/release/wecomchan?sendkey=wangyingbo&to_user=' + user + '&msg_type=text&msg=' + gladosStr
        ftStr = 'http://129.148.39.121:5005/wechat?msgtype=1&key=4ours&num=1&title=glados签到&touser=' + user + '&content=' + gladosStr
        requests.get(ftStr)
    else:
        #ftStr = 'https://service-d606bcz6-1304203451.usw.apigw.tencentcs.com/release/wecomchan?sendkey=wangyingbo&to_user=' + user + '&msg_type=text&msg=' + "Notification off"
        ftStr = 'http://129.148.39.121:5005/wechat?msgtype=1&key=4ours&num=1&title=glados签到&touser=' + user + '&content=' + "notification off"
        requests.get(ftStr)        
        

def main_handler(event, context):
  return start()

if __name__ == '__main__':
    start()