#!/bin/bash

DOMAIN=""
USERNAME=""
PASSWD=""
WEPUSH="yes"

while getopts "a:u:p:w:" opt; do
    case $opt in
        a)
            DOMAIN=${OPTARG}
            ;;
        u)
            echo -e "选项u的参数是${OPTARG}"
            USERNAME=${OPTARG}
            ;;
        p)
            echo -e "选项p的参数是${OPTARG}"
            PASSWD=${OPTARG}
            ;;
        w)
            echo -e "选项w的参数是${OPTARG}"
            WEPUSH=${OPTARG}
            ;;
        v)
            echo -e "version:1.0"
            ;;
        \?)
            usage
            ;;

    esac
done

echo "域名：${DOMAIN}"
echo "账号：${USERNAME}"
echo "密码：${PASSWD}"


if [ "${DOMAIN}" == "" ] || [ "${USERNAME}" == "" ] || [ "${PASSWD}" == "" ]; then
    echo "环境常量未配置，请正确配置 DOMAIN、USERNAME 和 PASSWD 值" && exit 1
fi

if [ $(command -v jq) == "" ]; then
    echo "依赖缺失: jq，查看 https://github.com/isecret/sspanel-autocheckin/blob/master/README.md 安装" && exit 1
fi

COOKIE_PATH="./.ss-autocheckin.cook"

login=$(curl "${DOMAIN}/auth/login" -d "email=${USERNAME}&passwd=${PASSWD}&code=" -c ${COOKIE_PATH} -L -k -s)

echo "---------"
echo ${login}
 
date=$(date '+%Y-%m-%d %H:%M:%S')
login_status=$(echo ${login} | jq '.msg')

if [ "${login_status}" == "" ]; then
    login_status='"登录失败"'
fi

login_text="[${date}] ${login_status}"

echo ${login_text}

checkin=$(curl -k -s -d "" -b ${COOKIE_PATH} "${DOMAIN}/user/checkin")

rm -rf ${COOKIE_PATH}

date=$(date '+%Y-%m-%d %H:%M:%S')
checkin_status=$(echo ${checkin} | jq '.msg')

if [ "${checkin_status}" == "" ]; then
    checkin_status='"签到失败"'
fi

checkin_text="[${date}] ${checkin_status}"

echo ${checkin_text}

date=$(date '+%Y-%m-%d %H:%M:%S')
if [ "${PUSH_KEY}" == "" ]; then
    push_status='"未配置推送 PUSH_KEY"'
else
    text="SSPanel Auto Checkin 签到结果"
    desp="站点: ${DOMAIN}"+$'\n\n'+"用户名: ${USERNAME}"+$'\n\n'+"${login_text}"+$'\n\n'+"${checkin_text}"+$'\n\n'
    # server酱推送
    push=$(curl -k -s -d "text=${text}&desp=${desp}" "https://sc.ftqq.com/${PUSH_KEY}.send")
    push_code=$(echo ${push} | jq '.errno')

    if [ ${push_code} == 0 ]; then
        push_status='"签到结果推送成功"'
    else
        push_status='"签到结果推送失败"'
    fi
fi

push_text="[${date}] ${push_status}"
echo ${push_text}

login_text=`echo $login_text | sed 's/\"//g'`
checkin_text=`echo $checkin_text | sed 's/\"//g'`
domain_text=`echo $DOMAIN | sed 's/\"//g'`
username_text=`echo $USERNAME | sed 's/\"//g'`
echo $login_text
echo $checkin_text
# wcdesp="站点: ${DOMAIN}"+$'\n\n'+"用户名: ${USERNAME}"+$'\n\n'+"${login_text}"+$'\n\n'+"${checkin_text}"+$'\n\n'
# wcdesp="站点: ${DOMAIN}"$'\n\n'"用户名: ${USERNAME}"$'\n\n'${login_text}$'\n\n'${checkin_text}$'\n\n'
wcdesp="\n站点: ${domain_text}\n\n用户名: ${username_text}\n\n${login_text}\n\n${checkin_text}\n"
# wcdesp="签到成功了"
# 企业微信推送给微信
echo "企业微信开始推送了"
echo $wcdesp
# curl -G --data-urlencode "sendkey=wangyingbo" --data-urlencode "msg_type=text" --data-urlencode "to_user=WangYingBo" --data-urlencode "msg=${wcdesp}" 'https://service-d606bcz6-1304203451.usw.apigw.tencentcs.com/release/wecomchan'

wecomcontent="{\"msgtype\": \"1\",\"key\": \"4ours\",\"num\": \"1\",\"touser\": \"WangYingBo\",\"title\": \"ikuuu签到\",\"content\": \"${wcdesp}\"}"
echo $wecomcontent

if [[ "${WEPUSH}" == "yes" ]]; then
    # echo "需要推送"
    curl -H "Content-Type:application/json" -X POST --data "${wecomcontent}" http://129.148.39.121:5005/wechat
fi

