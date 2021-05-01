import os
import re
import urllib.parse as parse
import time
import logging
import threading


class rush:
    def __init__(self, name, cookies, headers, scookie, device, sdevice, gameid):
        self.name = name
        if os.path.exists('.\confs\logs'):
            pass
        else:
            os.mkdir('.\confs\logs')
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.basicConfig(level=logging.DEBUG,  # 控制台打印的日志级别
                            filename='.\confs\logs\\' + time.strftime("%Y-%m-%d", time.localtime()) + '.log',
                            filemode='a',  ##模式，有w和a，w就是写模式，每次都会重新写日志，覆盖之前的日志
                            # a是追加模式，默认如果不写的话，就是追加模式
                            format=
                            '%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                            # 日志格式
                            )
        logging.info("【" + self.name + "】初始化成功！")
        self.cookies = {}
        self.headers = {}
        cok = re.findall(r'([^=]+)=([^;]+)[ ;]*', parse.unquote(cookies))
        hed = re.findall(r'([^:]+): ([^\n]+)[\n]*', parse.unquote(headers.replace('。', '\n')))
        for item in cok:
            self.cookies[item[0]] = item[1]
        for item in hed:
            self.headers[item[0]] = item[1]
        self.scookie = parse.unquote(scookie)
        self.device = parse.unquote(device)
        self.sdevice = parse.unquote(sdevice)
        self.gameid = gameid
        # 以下是部分全局变量
        self.num = []
        self.names = []
        # 定义一个月中有多少天
        day_of_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        self.total_day = day_of_month[int(time.strftime("%m", time.localtime()))]