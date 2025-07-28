#!/bin/zsh

# veloera 签到脚本

# 会话 cookie 和用户 ID（可修改为变量）
SESSION_COOKIE="session=MTc1MzQwOTgwOHxEWDhFQVFMX2dBQUJFQUVRQUFEX2xfLUFBQVVHYzNSeWFXNW5EQVFBQW1sa0EybHVkQVFFQVA0bExnWnpkSEpwYm1jTUNnQUlkWE5sY201aGJXVUdjM1J5YVc1bkRBNEFER3hwYm5WNFpHOWZORGMxT1FaemRISnBibWNNQmdBRWNtOXNaUU5wYm5RRUFnQUNCbk4wY21sdVp3d0lBQVp6ZEdGMGRYTURhVzUwQkFJQUFnWnpkSEpwYm1jTUJ3QUZaM0p2ZFhBR2MzUnlhVzVuREFrQUIyUmxabUYxYkhRPXx74SgdL97oy9aZPZh9rN0V7qtbO25Mq-UgGw5q2EdHUQ==; 0aba66732dc8235fdf212e2032d4ef96=4f920d4c6c111056eae9f0f93d85ca46"
VELOERA_USER="4759"

# 发送签到请求
# curl 'https://zone.veloera.org/api/user/check_in' \
#   -X 'POST' \
#   -H 'accept: application/json, text/plain, */*' \
#   -H 'accept-language: zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7' \
#   -H 'cache-control: no-store' \
#   -H 'content-length: 0' \
#   -H "cookie: $SESSION_COOKIE" \
#   -H 'origin: https://zone.veloera.org' \
#   -H 'priority: u=1, i' \
#   -H 'referer: https://zone.veloera.org/app/me' \
#   -H 'sec-ch-ua: "Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"' \
#   -H 'sec-ch-ua-mobile: ?0' \
#   -H 'sec-ch-ua-platform: "macOS"' \
#   -H 'sec-fetch-dest: empty' \
#   -H 'sec-fetch-mode: cors' \
#   -H 'sec-fetch-site: same-origin' \
#   -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36' \
#   -H "veloera-user: $VELOERA_USER"




check_res=$(curl -s 'https://zone.veloera.org/api/user/check_in' \
  -X POST \
  -H 'accept: application/json, text/plain, */*' \
  -H "cookie: $SESSION_COOKIE" \
  -H "veloera-user: $VELOERA_USER" \
  -H 'origin: https://zone.veloera.org' \
  -H 'referer: https://zone.veloera.org/app/me' \
  -H 'user-agent: Mozilla/5.0')

# 输出结果
echo "签到结果：$check_res"


wcdesp=$(echo "$check_res" | jq -r '.message')

echo "企业微信开始推送了"
echo $wcdesp

wecomcontent="{\"msgtype\": \"1\",\"key\": \"4ours\",\"num\": \"1\",\"touser\": \"WangYingBo\",\"title\": \"zone.veloera.org\",\"content\": \"${wcdesp}\"}"
echo $wecomcontent

curl -H "Content-Type:application/json" -X POST --data "${wecomcontent}" http://129.148.39.121:5005/wechat
  

