#!/bin/zsh
# author: yingbo 2025.01.05

echo "开始执行任务..."

# 执行远程命令并将输出存储在变量中
OUTPUT=$(sshpass -p 'hhO!rD@J0n*h1VqQy7MI' ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -tt wybgit@panel14.serv00.com "ps -A; echo $(date) >> auto_sign_in_log.txt; exit" 2>&1)
if [ $? -ne 0 ]; then
    echo "执行命令失败: $OUTPUT"
    exit 1
fi

# 输出命令的结果
echo "输出:\n$OUTPUT"
echo "任务执行完成"

# 发送 Telegram 推送通知
TOKEN="8193052405:AAEELfimgNDKZnBWIkSAHVr0m7dC64LLdcY"
CHAT_ID="890158254"
MESSAGE="任务执行完成\n\n输出:\n$OUTPUT\n"

# 使用 urlencode 对消息进行编码，以便在 URL 中安全传输
MESSAGE_ENCODED=$(echo -e "$MESSAGE" | jq -sRr @uri)

curl -s -X POST "https://api.telegram.org/bot$TOKEN/sendMessage" \
     -d "chat_id=$CHAT_ID&text=$MESSAGE_ENCODED"