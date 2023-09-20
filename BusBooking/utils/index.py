import http.client


def sendOTP(phone_no="+255623317196" , sms="Your OTP is 1234"):

    BASE_URL = "q984r.api.infobip.com"
    API_KEY = "App 59681f69a81b5802b3f7b8383ef65b1d-1d681fa7-8e5a-496a-83c7-b0ce6e678819"

    # SENDER = "Jipime"
    SENDER = "ConnectMoja"
    # SENDER = "AfyaTap"
    RECIPIENT = phone_no
    MESSAGE_TEXT = sms

    conn = http.client.HTTPSConnection(BASE_URL)

    payload1 = "{\"messages\":" \
            "[{\"from\":\"" + SENDER + "\"" \
            ",\"destinations\":" \
            "[{\"to\":\"" + RECIPIENT + "\"}]," \
            "\"text\":\"" + MESSAGE_TEXT + "\"}]}"

    headers = {
        'Authorization': API_KEY,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    conn.request("POST", "/sms/2/text/advanced", payload1, headers)

    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
