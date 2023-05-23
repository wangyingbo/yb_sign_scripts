"""
cron: 0 3,11 * * *
"""

import requests ,os,json

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
        'token': 'glados.network'
    }
        
    # -----------------------通过对象创建----------------------------------
    objArray = []
    # Model("mail","sckey","none","cookie")

    # 第一个用户
    user1 = Model("2532084725_qq","none","WangYingBo","_ga=GA1.2.2034832508.1661233106; _gid=GA1.2.2011244267.1661233106; __cf_bm=5mMiAlJmxjceRifaWPb.Y4kl0b6.Odp_pHM0fTEG3kw-1661233237-0-AV6dxJV4+TNTdoblgAv+eQcUh/CZIEvFxfM7BGXHoRqWALrrYxe/XipSeYi2SqlsmhJGCYgn4VB2FtNFHEF+LjfRXC7MU1F3HVuqBluyB0t1r76FxNKVvu4pwpAhRbHRYQ==; koa:sess=eyJ1c2VySWQiOjk5NTY4LCJfZXhwaXJlIjoxNjg3MTUzMjc1OTI5LCJfbWF4QWdlIjoyNTkyMDAwMDAwMH0=; koa:sess.sig=IUzGQiQMrlHFdLu39ucJ_klKqlY")
    objArray.append(user1)

    # 第二个用户
    user2 = Model("wangyingbo0528_gmail","none","WangYingBo","_ga=GA1.2.1461581697.1631507811; koa:sess=eyJ1c2VySWQiOjEwMTA1OSwiX2V4cGlyZSI6MTY3NjM3NTM0NDQxNCwiX21heEFnZSI6MjU5MjAwMDAwMDB9; koa:sess.sig=XYdWoN0oz5H0YNQ5frAbQtIKBO8; _gid=GA1.2.474745356.1655349911; _dd_s=logs=1&id=dab57835-60de-4f14-b4f2-c5d6dddd704b&created=1655349910870&expire=1655351623431")
    # objArray.append(user2)

    # 第三个用户
    user3 = user11 = Model("yangqq721","SCT195403Tq8LhDCrPmZNJ7PcaSXf5q7SY","none","_ga=GA1.2.1100215316.1675841868; _gid=GA1.2.762050823.1675841868; koa:sess=eyJ1c2VySWQiOjI3MTgwMSwiX2V4cGlyZSI6MTcwMTc2MjAzNDU4OCwiX21heEFnZSI6MjU5MjAwMDAwMDB9; koa:sess.sig=r3jnaw5sTCJpKLZDkUlanoPaXZs")
    # objArray.append(user3)

    # 第四个用户 苏鲜明
    user4 = Model("1360789864_qq","SCT88569Tk3eHEXVRRgMrLENyPdAzQZkB","none","_ga=GA1.2.1649392190.1635315436; _gid=GA1.2.1937226553.1635315436; koa:sess=eyJ1c2VySWQiOjEwNzA1MSwiX2V4cGlyZSI6MTY2MTIzNTUwMjI5NSwiX21heEFnZSI6MjU5MjAwMDAwMDB9; koa:sess.sig=Xm6BHF0ppnO3dn83oQ0K5Q9nZDk")
    # objArray.append(user4)
    user_xianming_1 = Model("vipjinggege_163","SCT88569Tk3eHEXVRRgMrLENyPdAzQZkB","none","_ga=GA1.2.1649392190.1635315436; _gid=GA1.2.1047252294.1636701711; koa:sess=eyJ1c2VySWQiOjExMDAwNywiX2V4cGlyZSI6MTY2MjYyMjIwNTk2NiwiX21heEFnZSI6MjU5MjAwMDAwMDB9; koa:sess.sig=jLSJ3qWG6A8TE3lQKTao-uKCDos")
    # objArray.append(user_xianming_1)

    # 第五个用户 秦宏伟
    user5 = Model("836495953_qq","SCT90572TacfOhqXgkK45cdyAhvCAsrZk","none","_ga=GA1.2.213997131.1635840772; _gid=GA1.2.796273265.1635840772; koa:sess=eyJ1c2VySWQiOjEwODA0MywiX2V4cGlyZSI6MTY2MTc2MDkxMzg2MywiX21heEFnZSI6MjU5MjAwMDAwMDB9; koa:sess.sig=HWCZub4b6lco-XzR5IXZU6xNNbg")
    # objArray.append(user5)

    # 第6个用户 iOS开发群里的
    user6 = Model("clousnow_vip_qq","SCT91704TVsjHKVHgVG6W8N0HoKrmNQQ1","none","_ga=GA1.2.406575256.1636083487; _gid=GA1.2.1592092324.1636083487; koa:sess=eyJ1c2VySWQiOjEwODU5NywiX2V4cGlyZSI6MTY2MjAwMzUyMDU5MCwiX21heEFnZSI6MjU5MjAwMDAwMDB9; koa:sess.sig=xqflF8MM_k7Cho31MDdzVApTGYc")
    # objArray.append(user6)

    # 第7个用户，郭瑾
    user7 = Model("guojin_163","SCT103954TXryuFzBZxCYxq1ZaNGCtZCaU","none","_ga=GA1.2.1146170739.1639538188; _gid=GA1.2.1372910885.1639538188; koa:sess=eyJ1c2VySWQiOjExNzgyNiwiX2V4cGlyZSI6MTY2NTQ1ODI4NjMwMSwiX21heEFnZSI6MjU5MjAwMDAwMDB9; koa:sess.sig=yNBtiP1ct2Bc9MUhv2sBqqTxVB0")
    # objArray.append(user7)

    # 第8个用户，王琳
    user8 = Model("lin2934748395_163","SCT117311T8yUtyqK6aZd4l4sbD8gFGxtk","none","_ga=GA1.2.2001532657.1656513453; _gid=GA1.2.1982075889.1656513453; __cf_bm=bpNBIPBEuCLPHhuYuZDqhEMDkV4BHuhzE8XRb8_0sVE-1656513481-0-AadCptuUQcN0ZdaITONn8Zyo6BRRUav4p6e/EriOZuvA34Ej5UsAuBOHXqzM1Gna43lEluPXaAqozdgjWWcs2Xtr2IepHIdQBRTkBObBdYBmMxtooi8+myCJaQF78VafSA==; koa:sess=eyJ1c2VySWQiOjEyOTMzMywiX2V4cGlyZSI6MTY4MjQzMzUzNDYzMywiX21heEFnZSI6MjU5MjAwMDAwMDB9; koa:sess.sig=oAagfA59mtVXP4reGx0tBIe8ZCA; _gat_gtag_UA_104464600_2=1")
    # objArray.append(user8)

    # 第9个用户，春阳
    user9 = Model("961429020_qq","SCT96095Tq6JopnCx5Scz9j4cKGKq0Zne","none","_ga=GA1.2.719739536.1657279147; _gid=GA1.2.1832563000.1657279147; __cf_bm=DBzoX_Bmqa4lDOx8n00bq1Sbi68BCSr9fZpRcLbDslE-1657279147-0-Ad9OzwKMSQvIaVCgoGMg6KnChNAsg/BfN81XPm1BHh5DIq6NKAqXEbKK+9jLtiu/1TJyP2pYSVhnxqYINRweveRaZqOgm0LHl4+BMTlummWanJvF9ycLTM94rjsKbfY1Yw==; koa:sess=eyJ1c2VySWQiOjExMTMwMSwiX2V4cGlyZSI6MTY4MzE5OTE5NTkxMiwiX21heEFnZSI6MjU5MjAwMDAwMDB9; koa:sess.sig=KH2j6s6a7-9H4_mMLcVg0HnZhrM")
    # objArray.append(user9)

    for obj in objArray:
        checkin = requests.post(url,headers={'cookie': obj.cookie ,'referer': referer,'origin':origin,'user-agent':useragent,'content-type':'application/json;charset=UTF-8'},data=json.dumps(payload))
        state =  requests.get(url2,headers={'cookie': obj.cookie ,'referer': referer,'origin':origin,'user-agent':useragent})
        # print(res)
        if 'message' in checkin.text:
            mess = checkin.json()['message']
            time = state.json()['data']['leftDays']
            time = time.split('.')[0]
            print("---------------------**---------------------")
            print(time)
            print(mess)
            messStr = obj.name + ', ' + mess
            sckey = obj.sckey
            wcuser = obj.wcuser
            if len(sckey) > 0:
                notice(time,obj.sckey,sever,messStr)
            if len(wcuser) > 0:
                noticeWC(time,obj.wcuser,sever,messStr)

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
        ftStr = 'https://service-d606bcz6-1304203451.usw.apigw.tencentcs.com/release/wecomchan?sendkey=wangyingbo&to_user=' + user + '&msg_type=text&msg=' + gladosStr
        requests.get(ftStr)
    else:
        ftStr = 'https://service-d606bcz6-1304203451.usw.apigw.tencentcs.com/release/wecomchan?sendkey=wangyingbo&to_user=' + user + '&msg_type=text&msg=' + "Notification off"
        requests.get(ftStr)        
        

def main_handler(event, context):
  return start()

if __name__ == '__main__':
    start()