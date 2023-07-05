import os

try:
    LINEAPI_TOKEN = os.environ['LINEAPI_TOKEN']
except KeyError:
    LINEAPI_TOKEN = "***********"

test_send_command = f"curl -v -X POST https://api.line.me/v2/bot/message/broadcast \
-H \'Content-Type: application/json\' \
-H \'Authorization: Bearer {{{LINEAPI_TOKEN}}}\' \
-d \'{{\
    \"messages\":[\
        {{\
            \"type\":\"text\",\
            \"text\":\"Hello, world1\"\
        }},\
        {{\
            \"type\":\"text\",\
            \"text\":\"Hello, world2\"\
        }}\
    ]\
}}\'"

# print(test_send_command)
os.popen(test_send_command)
