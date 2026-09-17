#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import json
import requests
import time
import random
#import yaml
import datetime
#from bs4 import BeautifulSoup
from lxml import etree
import re
import urllib3
import os
import time
import hashlib
import fcntl
from yy_logger import get_logger

class FkstAPI:
    def __init__(self):
        self.headers = {
            "content-type": "application/x-www-form-urlencoded",
            "accept-encoding": "br, gzip, deflatee",
            "User-Agent": 'iOS 1.11.7',
            #"Cookie": 'XSRF-TOKEN=eyJpdiI6ImJZZ21VNm0xRGhoOUwrWFNqMlQyNlE9PSIsInZhbHVlIjoiQ1hHOHRzcmRvWGVcL1NRS1puQkdOM1R4bklyTXVlTFBtRUx4dTdnanJwUTQ0S0NYRVVVRVVBVkJyZHFyTW44ZytZbTdJQVllTlg5bGJjaUNcL3lLcFlxUT09IiwibWFjIjoiZmY5ZDkxZGY1YjMxZGZiZjg1MzdmMmU5ZTI4YTQ2YmRhNWRkYTdkNzNhNzJjNTM2ODI4MzU5MThlNDhjMzhhNSJ9; yex_session=eyJpdiI6IlwvalBwdXorU094TzJwbTFCUG5zaVB3PT0iLCJ2YWx1ZSI6IlFJZ2d4eHhCaVFaNXdZRG12UThlWTRUaERYK1c1b2FpNHMzZlVKNHpYZDVrd29CamNmNG1EZ2VQT25cL3RJeHZPcjZkMVEwdnZWcUo0akZ2Qnl4VVprQT09IiwibWFjIjoiNjZmNjEyZDI0ZDM1NDBmZjYwNTRkMmY5Zjg2MjRlMDI2Yzg4ODA5YzYzMDZkNTM0MWQ3OTZhNmQ2MDkxYjI5MiJ9',
        }

        self.user_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "fkst.json")
        self.userdata = {}
        self.load_user()

        self.logger = get_logger(os.path.join(os.path.dirname(os.path.realpath(__file__)), "fkst_log.txt"))

    def load_user(self):
        if not os.path.exists(self.user_path):
            '''
            with open(self.user_path, encoding="utf-8", mode='w+') as f:
                fcntl.flock(f, fcntl.LOCK_EX)
                fdata = {}
                json.dump(fdata, f, indent=4)
                fcntl.flock(f, fcntl.LOCK_UN)
            '''
            return True

        with open(self.user_path, encoding="utf-8") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            try:
                self.userdata = json.load(f)
            except Exception as e:
                self.userdata = {}

            fcntl.flock(f, fcntl.LOCK_UN)

        return True

    def save_user(self, mobile, json_obj):
        userdata = {}
        with open(self.user_path, encoding="utf-8", mode='r+') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            try:
                fdata = json.load(f)
            except Exception as e:
                fdata = {}

            fdata[mobile] = json_obj
            f.truncate(0)
            f.seek(0)
            json.dump(fdata, f, indent=4, ensure_ascii=False)
            fcntl.flock(f, fcntl.LOCK_UN)

        return

    def md5_encrypt(self, text):
        # 创建一个MD5对象
        md5 = hashlib.md5()

        # 将文本转换为字节类型并更新到MD5对象中
        md5.update(text.encode('utf-8'))

        # 获取加密后的结果（16位十六进制表示）
        encrypted_result = md5.hexdigest()[:32]

        return encrypted_result

    def get_api_sig(self, data):
        md5str = [f'{k}{v}' for k, v in data.items()]
        md5str = "".join(md5str)
        md5str = md5str + '55531210653ed3c70a819d52b9bbdef3'

        api_sig = self.md5_encrypt(md5str)

        return api_sig

    def get_form_param(self, data):
        # 将字典转换为列表
        items = [f'{k}={v}' for k, v in data.items()]

        # 使用join()函数将列表元素通过"&"连接起来
        datastr = "&".join(items)
        return datastr

    def AddSTCoin(self, json_rsp, openid, unionid):
        """
        签到
        :return:
        """
        coin = [1, 1, 1, 2, 1, 1, 3]

        url = "https://api.yaerxing.com/AddSTCoin"

        data = {}
        data['api_key'] = 'eddc42dcb249716ec2c00b7d5ee665fb'
        data['app_v'] = '1.11.7'
        data['appid'] = 'wx2bd42ba7f4c547f5'
        data['coin'] = coin[int(json_rsp["get_coin_day"])]
        data['day'] = int(json_rsp["get_coin_day"]) + 1
        data['device_id'] = 'iPhone 5s'
        #data['openid'] = '32359ca5aaf89170a4a2f4faa0c94d67'
        data['openid'] = openid
        data['os_v'] = '12.5.5'
        data['platform_id'] = 1
        # data['timestamp'] = 1704790012
        data['timestamp'] = int(time.time())
        #data['unionid'] = '32359ca5aaf89170a4a2f4faa0c94d67'
        data['unionid'] = unionid
        data['api_sig'] = self.get_api_sig(data)

        response = requests.post(url=url, headers=self.headers, data=self.get_form_param(data))
        json_rsp = response.json()

        self.logger.info(json_rsp)

        return True

    def GetSTMyData5(self, openid, unionid):
        """
        获取签到天数
        :return:
        """
        url = "https://api.yaerxing.com/GetSTMyData5"

        data = {}
        data['all_black_member'] = 1
        data['api_key'] = 'eddc42dcb249716ec2c00b7d5ee665fb'
        data['app_v'] = '1.11.7'
        data['appid'] = 'wx2bd42ba7f4c547f5'
        data['device_id'] = 'iPhone 5s'
        #data['openid'] = '32359ca5aaf89170a4a2f4faa0c94d67'
        data['openid'] = openid
        data['os_v'] = '12.5.5'
        data['platform_id'] = 1
        data['timestamp'] = int(time.time())
        #data['unionid'] = '32359ca5aaf89170a4a2f4faa0c94d67'
        data['unionid'] = unionid
        data['api_sig'] = self.get_api_sig(data)

        response = requests.post(url=url, headers=self.headers, data=self.get_form_param(data))
        json_rsp = response.json()

        #self.logger.info(json.dumps(json_rsp, indent=4))
        self.logger.info(json_rsp)

        return json_rsp

    def get_cookie(self):
        """
        获取cookie
        :return:
        """
        url = "https://www.yaerxing.com/shuati/selectDirection3?version=3"

        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "accept-encoding": "br, gzip, deflatee",
            "User-Agent": 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_5_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
        }

        response = requests.post(url=url, headers=self.headers)

    def SendSTCheckCode2(self, phone_number):
        """
        发送校验码
        :return:
        """
        url = "https://api.yaerxing.com/SendSTCheckCode2"

        data = {}
        data['api_key'] = 'eddc42dcb249716ec2c00b7d5ee665fb'
        data['app_v'] = '1.11.7'
        data['appid'] = 'wx2bd42ba7f4c547f5'
        data['check_status'] = '0'
        data['device_id'] = 'iPhone 5s'

        data['os_v'] = '12.5.5'
        data['phone_number'] = phone_number
        data['platform_id'] = 1
        data['timestamp'] = int(time.time())
        data['api_sig'] = self.get_api_sig(data)

        response = requests.post(url=url, headers=self.headers, data=self.get_form_param(data))
        json_rsp = response.json()
        self.logger.info(json_rsp)

        return json_rsp["checkcode"]

    def STAccountLogin3(self, phone_number, password):
        """
        登录
        :return:
        """
        url = "https://api.yaerxing.com/STAccountLogin3"

        data = {}
        data['api_key'] = 'eddc42dcb249716ec2c00b7d5ee665fb'
        data['app_v'] = '1.11.7'
        data['appid'] = 'wx2bd42ba7f4c547f5'
        data['device_id'] = 'iPhone 5s'
        data['os_v'] = '12.5.5'
        data['password'] = password
        data['phone_number'] = phone_number
        data['platform_id'] = 1
        data['timestamp'] = int(time.time())
        data['verify_type'] = 1
        data['api_sig'] = self.get_api_sig(data)

        response = requests.post(url=url, headers=self.headers, data=self.get_form_param(data))
        json_rsp = response.json()
        self.logger.info(json_rsp)

        return json_rsp

    def GetShuaTiTotal6(self, userinfo):
        """
        获取帐户详细信息
        userinfo
        {
            "unionid": "32359ca5aaf89170a4a2f4faa0c94d67",
            "openid": "32359ca5aaf89170a4a2f4faa0c94d67",
            "mid": "17713737",
            "res": 0
        }
        :return:
        """
        url = "https://api.yaerxing.com/GetShuaTiTotal6"

        data = {}
        data['api_key'] = 'eddc42dcb249716ec2c00b7d5ee665fb'
        data['app_v'] = '1.11.7'
        data['appid'] = 'wx2bd42ba7f4c547f5'
        data['device_id'] = 'iPhone 5s'
        data['height'] = 1136
        data['openid'] = userinfo["openid"]
        data['os_v'] = '12.5.5'
        data['platform_id'] = 1
        data['system_version'] = 'IOS12.5.5'
        data['timestamp'] = int(time.time())
        data['unionid'] = userinfo["unionid"]
        data['width'] = '640'
        data['api_sig'] = self.get_api_sig(data)

        response = requests.post(url=url, headers=self.headers, data=self.get_form_param(data))
        json_rsp = response.json()
        self.logger.info(json.dumps(json_rsp, indent=4))

        return json_rsp

    def login(self, phone_number):
        # 获取登录密码
        password = self.SendSTCheckCode2(phone_number)
        json_rsp = self.STAccountLogin3(phone_number, password)
        json_rsp = self.GetShuaTiTotal6(json_rsp)
        self.save_user(phone_number, json_rsp)

        return True

    def qiandao(self):
        for k, v in self.userdata.items():
            self.logger.info("%s %s %s" % (v["member"]["phone_number"], v["member"]["id"], v["member"]["nick_name"]))
            json_rsp = self.GetSTMyData5(v["member"]["openid"], v["member"]["unionid"])
            old_coin_count = json_rsp["coin_count"]

            if json_rsp["get_coin_status"] == 0:
                self.AddSTCoin(json_rsp, v["member"]["openid"], v["member"]["unionid"])

            json_rsp = self.GetSTMyData5(v["member"]["openid"], v["member"]["unionid"])
            new_coin_count = json_rsp["coin_count"]

            self.logger.info("%s %s --> %s" % (v["member"]["phone_number"], old_coin_count, new_coin_count))

        return True

if __name__ == '__main__':
    api = FkstAPI()

    # api.login("18620303906")

    api.qiandao()

