'''A template for sending requests to websites'''
import requests

url = 'http://example.com/'

class Example():
    """docstring for Example"""
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.url = 'http://example.com/'
        self.sess = requests.Session()

    def webpage_get(self, url, headers=dict(), allow_redirects=True):
        # print("Get: " + url)
        self.resp = self.sess.get(url, headers=headers, allow_redirects=allow_redirects)
        return self.resp

    def webpage_post(self, url, data, headers=dict()):
        self.sess.post(url, data=data, headers=headers)
        # self.req = requests.Request('POST', url, data=data, headers=headers)
        # self.prepped = self.sess.prepare_request(self.req)
        # self.resp = self.sess.send(self.prepped)
        return self.resp

    def save_page(self, page):
        with open('./test.html', 'w', encoding='utf-8') as f:
                f.write(page)
        print("Page has been saved as " + './test.html')

    def save_json(self, page, file):
        with open(file, 'w', encoding='utf-8') as f:
                f.write(page)
        print("json response been saved as " + file)

    def login(self):
        headers = {
            'Host': 'club.mail.126.com',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        }
        self.resp = self.webpage_get(self.url, headers=headers, allow_redirects=True)
        print(self.resp.content.decode('utf-8').replace('\r\n', '\n'))


if __name__ == '__main__':
    username, password = 'username', 'password'
    exampleins = Example(username, password)