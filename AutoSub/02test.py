import requests
import json


def baidu_sentiment_analysis(text):
    url = "https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?access_token=24.9712b5e99b1f27ef85c637b8d3157fe6.2592000.1688982761.282335-34644185&charset=UTF-8"

    payload = json.dumps({
        "text": text
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()


def main():
    text = "我不买了"
    response = baidu_sentiment_analysis(text)
    print(response)


if __name__ == '__main__':
    main()
