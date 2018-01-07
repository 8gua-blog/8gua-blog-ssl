#!/usr/bin/env python3

from os.path import join, getmtime, dirname
from json import dump
import time
import requests
from pprint import pprint

class Dnspod:
    _URL = "https://dnsapi.cn/"

    def __init__(self, dns_id, dns_key):
        self._token = f"{dns_id},{dns_key}"

    def api(self, action, data={}):
        url = f"{self._URL}{action}"
        data['login_token'] = self._token
        data['format'] = 'json'
        return requests.post(url, data).json()

def update_host(host, dns_id, dns_key, mtime):
    dnspod = Dnspod(dns_id, dns_key).api
    li = dnspod("Record.List", dict(domain=host))['records']

    for i in li:
        if i['type'] == 'TXT':
            if i['name'] == "ssl-v":
                mtime = str(mtime)
                if mtime != i['value']:
                    print(f'设置DNSPOD记录 {host} {i["name"]} {mtime}')
                    dnspod("Record.Modify", dict(
                        domain=host,
                        record_id=i['id'],
                        sub_domain=i['name'],
                        record_type=i['type'],
                        record_line="默认",
                        value=mtime,
                    ))
                break

def main(root, host, path, dns_id, dns_key):
    key = open(join(root, host, "%s.key"%host)).read()
    cer = join(root, host, 'fullchain.cer')
    mtime = int(time.mktime(time.gmtime(getmtime(cer))))
    cer = open(cer).read()


    with open(join(path,"ssl.json"),"w") as f:
        dump([mtime, key, cer], f)

    update_host(host, dns_id, dns_key, mtime)


if __name__ == "__main__":
    import fire
    fire.Fire(main)
