#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/28 8:41
# @File    : glados.py
# @Software: PyCharm
# @Description:
# @Ref: https://github.com/komori-flag/glados_automation

import json
import os
import requests

# -------------------------------------------------------------------------------------------
# github workflows
# -------------------------------------------------------------------------------------------
if __name__ == '__main__':
    # pushplus秘钥 申请地址 http://www.pushplus.plus
    sckey = os.environ.get("PUSHPLUS_TOKEN", "")
    # 推送内容
    sendContent = ''
    # glados账号cookie
    cookie = os.environ.get("GLADOS_COOKIE", "")
    if cookie == "":
        print('未获取到COOKIE变量')
        exit(0)

    # 定义url等相关变量
    url = "https://glados.cloud/api/user/checkin"
    url2 = "https://glados.cloud/api/user/status"
    referer = 'https://glados.cloud/console/checkin'
    origin = "https://glados.cloud"
    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    payload = {
        'token': 'glados.cloud'
    }
    left_time = ''

    # 发起请求
    checkin = requests.post(url, headers={'cookie': cookie, 'referer': referer, 'origin': origin,
                                          'user-agent': useragent,
                                          'content-type': 'application/json;charset=UTF-8'},
                            data=json.dumps(payload))
    state = requests.get(url2,
                         headers={'cookie': cookie, 'referer': referer, 'origin': origin, 'user-agent': useragent})

    # --------------------------------------------------------------------------------------------------------#
    # 解析请求
    code = state.json()['code']
    if code != 0:
        print(state.json()['message'])
        sendContent += state.json()['message']
    else:
        time = state.json()['data']['leftDays']
        time = time.split('.')[0]
        left_time = time
        email = state.json()['data']['email']
        if 'message' in checkin.text:
            mess = checkin.json()['message']
            if 'Repeats' in mess:
                mess = "Checkin Repeats!"
                print(mess + '--剩余(' + time + ')天\n' + email)  # 日志输出
            sendContent += mess + '--剩余(' + time + ')天\n' + email
        else:
            requests.get('http://www.pushplus.plus/send?token=' + sckey + '&content=' + email + 'cookie已失效')
            print('cookie已失效')  # 日志输出
            sendContent += 'cookie已失效' + '----剩余(' + time + ')天\n' + email
    # --------------------------------------------------------------------------------------------------------#
    if sckey != "":
        requests.get(
            'http://www.pushplus.plus/send?token=' + sckey + '&title=' + '签到成功' + '--剩余(' + left_time + ')天' + '&content=' + sendContent)
