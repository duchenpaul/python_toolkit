'''A template for sending requests to websites'''
import requests
import urllib.parse
try:
    from urllib.parse import quote_plus
except ImportError:
    from urllib import quote_plus

# proxies = { "http": "http://127.0.0.1:8888", }

url = 'http://example.com/'


class Example():
    """docstring for Example"""

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.url = 'http://example.com/'
        self.sess = requests.Session()

    def webpage_get(self, url, headers=None, allow_redirects=True):
        if headers is None:
            headers = dict()
        # print("Get: " + url)
        proxies = None
        self.resp = self.sess.get(
            url, headers=headers, allow_redirects=allow_redirects, verify=False, proxies=proxies, timeout=10)
        # print(self.resp.content.decode('utf-8').replace('\r\n', '\n'))
        return self.resp

    def webpage_post(self, url, data, headers=None):
        if headers is None:
            headers = dict()
        proxies = None
        self.resp = self.sess.post(
            url, data=data, headers=headers, verify=False, proxies=proxies, timeout=10)
        # self.req = requests.Request('POST', url, data=data, headers=headers)
        # self.prepped = self.sess.prepare_request(self.req)
        # self.resp = self.sess.send(self.prepped)
        return self.resp

    def save_page(self, page):
        with open('./test.html', 'w', encoding='utf-8') as f:
            f.write(page)
        print("Page has been saved as " + './test.html')

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
        self.resp = self.webpage_get(
            self.url, headers=headers, allow_redirects=True)

        postDataDict = {
            'username': self.username,
            'password': self.password,
            'url': 'http://club.mail.126.com/jifen/index.do',
            'm-URSlogin-box-form-url2': 'http://club.mail.126.com/jifen/index.do',
        }
        post_data = urllib.parse.urlencode(postDataDict)
        print(post_data)
        self.resp = self.webpage_post(url, post_data, headers=headers)


if __name__ == '__main__':
    username, password = 'username', 'password'
    exampleins = Example(username, password)
