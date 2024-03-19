import requests

api_key = "80ca7c3dab028bba12ff4cd20a8c7884-b02bcf9f-5049817a"


def send_simple_message(to, message):
    return requests.post(
        "https://api.mailgun.net/v3/sandbox1873968e38074f8ba45bcbed4fa857e4.mailgun.org/messages",
        auth=("api", api_key),
        data={"from": "4insta10001@gmail.com",
              "to": [to],
              "subject": "Music Recommender",
              "text": message})
