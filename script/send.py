import os

def send(text):

    try:
        LINEAPI_TOKEN = os.environ['LINEAPI_TOKEN']
    except KeyError:
        print("KEY ERROR")
        LINEAPI_TOKEN = "***********"

    test_send_command = f"curl -v -X POST https://api.line.me/v2/bot/message/broadcast \
    -H \'Content-Type: application/json\' \
    -H \'Authorization: Bearer {{ { LINEAPI_TOKEN } }}\' \
    -d \'{{ \
        \"messages\":[ \
            {{ \
                \"type\":\"text\", \
                \"text\":\"{ text } \" \
            }} \
        ] \
    }}\'"


    # print(test_send_command)
    os.popen(test_send_command)


if __name__ == "__main__":
    send("This is a test message.")
