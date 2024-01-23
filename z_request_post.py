import requests

if __name__ == '__main__':
    url = "http://127.0.0.1:8000"
    data = "start"
    r = requests.post(url=url, data=data)
    print(r.text)
