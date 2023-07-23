import urllib.parse
import requests
import json
import logging
import base64

import config_loader

try:
    from urllib.parse import quote_plus
except ImportError:
    from urllib import quote_plus

config = config_loader.config

# proxies = {"http": "socks5://127.0.0.1:8888", }


class Gitea():
    """docstring for Gitea."""

    def __init__(self, token: str, host='https://gitea.com'):
        self.host = host
        self.token = token
        self.sess = requests.Session()
        self.headers = {
            "Authorization": "token " + token,
        }

    def webpage_get(self, url, headers=None, allow_redirects=True):
        if headers is None:
            headers = self.headers
        # print("Get: " + url)
        proxies = None
        self.resp = self.sess.get(
            url, headers=headers, allow_redirects=allow_redirects, verify=False, proxies=proxies, timeout=10)
        return self.resp

    def webpage_post(self, url, data=None, json=None, headers=None):
        if headers is None:
            headers = self.headers
        proxies = None
        self.resp = self.sess.post(
            url, headers=headers, data=data, json=json, verify=False, proxies=proxies, timeout=10)
        return self.resp

    def webpage_put(self, url, data=None, json=None, headers=None):
        if headers is None:
            headers = self.headers
        proxies = None
        self.resp = self.sess.put(
            url, headers=headers, data=data, json=json, verify=False, proxies=proxies, timeout=10)
        return self.resp

    def webpage_delete(self, url, headers=None, allow_redirects=True):
        if headers is None:
            headers = self.headers
        proxies = None
        self.resp = self.sess.delete(
            url, headers=headers, allow_redirects=allow_redirects, verify=False, proxies=proxies, timeout=10)
        return self.resp

    def request_api(self, method: str, api_endpoint: str, payload={}) -> str:
        """
            Request Gitea API.
            doc: https://gitea.com/api/swagger

        Args:
            method (str): Request method, one of ("GET", "POST", "DELETE", "PUT")
            api_endpoint (str): api endpoint
            payload (dict): payload in post request

        Returns:
            str: _description_
        """
        url = f'{self.host}/api/v1{api_endpoint}'
        match method:
            case "GET":
                self.resp = self.webpage_get(url, headers=self.headers, allow_redirects=True)
            case "POST":
                self.resp = self.webpage_post(url, headers=self.headers, json=payload)
            case "PUT":
                self.resp = self.webpage_put(url, headers=self.headers, json=payload)
            case "DELETE":
                self.resp = self.webpage_delete(url, headers=self.headers)
        try:
            assert self.resp.status_code in (200, 201)
        except AssertionError as e:
            logging.error('Error request API:')
            logging.error(self.resp.content.decode('unicode-escape'))
            self.resp.raise_for_status()
        return json.loads(self.resp.text)

    def get_file_content(self, owner: str, repo: str, filepath: str) -> dict:
        api_endpoint = f"/repos/{owner}/{repo}/contents/{filepath}"
        result = self.request_api("GET", api_endpoint)
        return result

    def create_file_content(self, owner: str, repo: str, filepath: str, content: str) -> dict:
        payload = {
            "content": base64.b64encode(content.encode()).decode()
        }
        api_endpoint = f"/repos/{owner}/{repo}/contents/{filepath}"
        result = self.request_api("POST", api_endpoint, payload=payload)
        return result

    def update_file_content(self, owner: str, repo: str, filepath: str, content: str) -> dict:
        payload = {
            "content": base64.b64encode(content.encode()).decode(),
            "sha": self.get_file_content(owner, repo, filepath)["sha"],
        }
        logging.debug(' '.join((owner, repo, filepath)))
        logging.debug(json.dumps(payload))
        api_endpoint = f"/repos/{owner}/{repo}/contents/{filepath}"
        result = self.request_api("PUT", api_endpoint, payload=payload)
        return result


if __name__ == "__main__":
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    LOG_FORMAT = '[%(asctime)s] %(levelname)8s - %(name)s - %(message)s'
    formatter = logging.Formatter(LOG_FORMAT)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    # token = ""
    # gitea = Gitea(token=token)
    # owner = "duchenpaul"
    # repo = "mixed_nodes"
    # filepath = "v2board_nodes.txt"
    # print(gitea.update_file_content(owner, repo, filepath, 'teddst'))
    pass
