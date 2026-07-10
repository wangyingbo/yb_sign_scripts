#!/usr/bin/env bash
# ikuuu Checkin v3
# Single-file edition
# Features:
# - Multi-account Cookie checkin
# - Retry/timeout
# - Cookie expiry warning
# - Optional ServerChan/WeCom/PushPlus/Telegram/Bark
# - Unified summary
#
# ====== Configuration ======
DOMAIN="https://ikuuu.win"

# Push switches
ENABLE_WECOM=yes
ENABLE_SERVERCHAN=no
ENABLE_PUSHPLUS=no
ENABLE_BARK=no
ENABLE_TELEGRAM=no

# WeCom
WECOM_URL="http://129.148.39.121:5005/wechat"
WECOM_KEY="4ours"
WECOM_TOUSER="WangYingBo"

# ServerChan
SERVERCHAN_KEY=""

# PushPlus
PUSHPLUS_TOKEN=""

# Bark
BARK_URL=""

# Telegram
TG_BOT_TOKEN=""
TG_CHAT_ID=""

# Accounts:
# nickname|email|cookie
USERS=(
'王迎博|2532084725@qq.com|PHPSESSID=b7tlni9dd1f11qdqd234ndgokb; uid=301459; email=2532084725%40qq.com; key=0b7556dea15664befb14b2e99806aadc8197a60b909c1; ip=6e29e5c1d71393fc6a6f6615a460f8c9; expire_in=1784259855'
)

need(){ command -v "$1" >/dev/null || { echo "Missing $1"; exit 1; }; }
need curl
need jq

GREEN="\033[32m"; RED="\033[31m"; YELLOW="\033[33m"; NC="\033[0m"
SUMMARY=""

push_wecom(){
[ "$ENABLE_WECOM" != yes ] && return
local title="$1"; local content="$2"
# json=$(printf '{"msgtype":"1","key":"%s","num":"1","touser":"%s","title":"%s","content":"%s"}' "$WECOM_KEY" "$WECOM_TOUSER" "$title" "$(echo "$content"|sed ':a;N;$!ba;s/\n/\\n/g')")
content_escaped=$(printf '%s' "$content" | awk '{printf "%s\\n",$0}' | sed 's/\\n$//')
json=$(printf '{"msgtype":"1","key":"%s","num":"1","touser":"%s","title":"%s","content":"%s"}' \
"$WECOM_KEY" "$WECOM_TOUSER" "$title" "$content_escaped")
curl -s -H "Content-Type:application/json" -X POST -d "$json" "$WECOM_URL" >/dev/null
}
push_serverchan(){ [ "$ENABLE_SERVERCHAN" != yes ] && return; curl -s -d "title=$1&desp=$2" "https://sctapi.ftqq.com/${SERVERCHAN_KEY}.send" >/dev/null; }
push_pushplus(){ [ "$ENABLE_PUSHPLUS" != yes ] && return; curl -s -H "Content-Type:application/json" -d "{"token":"$PUSHPLUS_TOKEN","title":"$1","content":"$2"}" https://www.pushplus.plus/send >/dev/null; }
push_bark(){ [ "$ENABLE_BARK" != yes ] && return; curl -s "$BARK_URL/$1/$2" >/dev/null; }
push_tg(){ [ "$ENABLE_TELEGRAM" != yes ] && return; curl -s -X POST "https://api.telegram.org/bot${TG_BOT_TOKEN}/sendMessage" -d chat_id="$TG_CHAT_ID" --data-urlencode text="$2" >/dev/null; }

check(){
nick="$1"; mail="$2"; cookie="$3"
echo "==== $nick ===="
headers=$(mktemp)
body=$(curl -sS --retry 3 --connect-timeout 10 --max-time 30 -D "$headers" -X POST -H "X-Requested-With: XMLHttpRequest" -H "Origin:$DOMAIN" -H "Referer:$DOMAIN/user" -b "$cookie" "$DOMAIN/user/checkin")
ret=$(echo "$body"|jq -r '.ret // empty')
msg=$(echo "$body"|jq -r '.msg // "Unknown"')
status=""
if [ "$ret" = "1" ]; then status="SUCCESS"; color=$GREEN
elif echo "$msg"|grep -Eq "已经签到|已签到"; then status="ALREADY"; color=$YELLOW
elif echo "$msg"|grep -Eq "登录|未登录"; then status="COOKIE_EXPIRED"; color=$RED
else status="FAILED"; color=$RED; fi
printf "${color}%s${NC} %s
" "$status" "$msg"

exp=$(echo "$cookie"|tr ';' '\n'|awk -F= '/expire_in/{print $2}')
warn=""
if [ -n "$exp" ]; then
 left=$((exp-$(date +%s)))
 if [ $left -gt 0 ]; then
  d=$((left/86400))
  [ $d -lt 7 ] && warn=" (Cookie ${d} days left)"
 fi
fi

new=$(grep -i '^Set-Cookie:' "$headers"|grep -E 'PHPSESSID='|tail -1|cut -d' ' -f2-|cut -d';' -f1)
rm -f "$headers"
[ -n "$new" ] && echo "Server issued new PHPSESSID: $new"

SUMMARY="${SUMMARY}
[$nick] $status
$msg$warn
"
}

start=$(date +%s)
for u in "${USERS[@]}"; do
 n=$(echo "$u"|cut -d'|' -f1)
 m=$(echo "$u"|cut -d'|' -f2)
 c=$(echo "$u"|cut -d'|' -f3-)
 check "$n" "$m" "$c"
done
cost=$(( $(date +%s)-start ))
SUMMARY="${SUMMARY}
Elapsed: ${cost}s"

echo "$SUMMARY"
push_wecom "ikuuu签到汇总" "$SUMMARY"
push_serverchan "ikuuu签到汇总" "$SUMMARY"
push_pushplus "ikuuu签到汇总" "$SUMMARY"
push_bark "ikuuu签到汇总" "$SUMMARY"
push_tg "ikuuu签到汇总" "$SUMMARY"
