import requests
import jsondump

class API:
    def __init__(self, apiKey):
        self.apiKey = apiKey

    def setToken(self, apiKey):
        self.apiKey = apiKey

    def getLatestNews(self, limit = 10):
        try:
            url = 'https://chainecho.me/api/v2/article'
            headers = { "Content-Type": "application/json" }
            data = {
                "token": self.apiKey,
                "limit": limit
            }
            resp = requests.post(url, headers=headers, json=data)

            if resp.status_code == 200:
                ret = jsondump.loads(resp.text)
                if ret['success']:
                    return ret['data']
                else:
                    print(ret['error'])
        except Exception as e:
            print(e)

        return []
    
    def getCategories(self):
        try:
            url = 'https://chainecho.me/api/v2/category'
            headers = { "Content-Type": "application/json" }
            data = {
                "token": self.apiKey
            }
            resp = requests.post(url, headers=headers, json=data)

            if resp.status_code == 200:
                ret = jsondump.loads(resp.text)
                if ret['success']:
                    return ret['data']
                else:
                    print(ret['error'])
        except Exception as e:
            print(e)

        return []
