#!/bin/zsh
# author: yingbo 2025.01.05


# 发送 Telegram 推送通知
TOKEN="8193052405:AAEELfimgNDKZnBWIkSAHVr0m7dC64LLdcY"
CHAT_ID="890158254"


# JSON 文件路径
json_file="./serv00_accounts.json"

# 使用 jq 获取 JSON 文件中的所有记录并遍历
for account in $(jq -c '.[]' "$json_file"); do
    # 从每个 account 中提取相应的字段
    username=$(echo "$account" | jq -r '.username')
    password=$(echo "$account" | jq -r '.password')
    panel=$(echo "$account" | jq -r '.panel')

    # 输出当前的账户信息（可以根据需要修改为实际操作）
    ACCOUNT_INFO="登录信息：用户名=$username, 密码=$password, 主机=$panel"

    echo "开始执行任务..."

    MESSAGE=''
    # 执行远程命令并将输出存储在变量中
    OUTPUT=$(sshpass -p 'hhO!rD@J0n*h1VqQy7MI' ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -tt wybgit@panel14.serv00.com "ps -A; echo $(date) >> auto_sign_in_log.txt; exit" 2>&1)
    if [ $? -ne 0 ]; then
        echo "执行命令失败: $OUTPUT"
        MESSAGE=$OUTPUT
    else
        MESSAGE="任务执行完成\n\n输出:\n用户名：${username}，主机：${panel} 登录成功！\n"
    fi

    # 输出命令的结果
    echo "输出:\n$OUTPUT"


    # 使用 urlencode 对消息进行编码，以便在 URL 中安全传输
    MESSAGE_ENCODED=$(echo -e "$MESSAGE" | jq -sRr @uri)

    curl -s -X POST "https://api.telegram.org/bot$TOKEN/sendMessage" \
         -d "chat_id=$CHAT_ID&text=$MESSAGE_ENCODED"

    echo "任务执行完成"

done


