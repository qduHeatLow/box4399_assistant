import requests
import time
import random
import json
from bs4 import BeautifulSoup
from configparser import RawConfigParser
import re
import urllib.parse as parse
import os
import logging
import asyncio
from aiohttp import ClientSession


class Box:
    def __init__(self, path='.\confs'):
        self.cdk = []
        self.prize_target_normal = []
        self.prize_target_rand = []
        self.tasks = []
        self.loop = asyncio.get_event_loop()
        self.path = path
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.getLogger("asyncio").setLevel(logging.WARNING)
        logging.basicConfig(level=logging.DEBUG,  # 控制台打印的日志级别
                            filename=self.path + '\\' + time.strftime("%Y-%m-%d", time.localtime()) + '.log',
                            filemode='a',
                            format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                            )
        # 以下是部分全局变量
        self.num = []
        self.names = []
        # 定义一个月中有多少天
        day_of_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        self.total_day = day_of_month[int(time.strftime("%m", time.localtime()))]

    def read_config(self):
        filelist = []
        self.size = 0
        for root, dirs, files in os.walk(self.path, topdown=False):
            if root == self.path:
                for name in files:
                    if name.split('.')[-1] == 'ini':
                        filelist.append(name)
                        self.size = self.size + 1
        if self.size == 0:
            logging.error('【初始化错误】没有找到配置文件！')
            return False

        self.name = []
        self.cookies = []
        self.headers = []
        self.scookie = []
        self.device = []
        self.sdevice = []
        self.gameid = []

        for item in filelist:
            conf = RawConfigParser()
            conf.read(self.path + '\\' + item)
            cok = re.findall(r'([^=]+)=([^;]+)[ ;]*', parse.unquote(conf.get("essential", "cookies")))
            hed = re.findall(r'([^:]+): ([^\n]+)[\n]*',
                             parse.unquote(conf.get("essential", "headers").replace('。', '\n')))
            cookies_temperoary = {}
            headers_temperoary = {}
            for x in cok:
                cookies_temperoary[x[0]] = x[1]
            for x in hed:
                headers_temperoary[x[0]] = x[1]
            self.name.append(item)
            self.cookies.append(cookies_temperoary)
            self.headers.append(headers_temperoary)
            self.scookie.append(parse.unquote(conf.get("essential", "scookie")))
            self.device.append(parse.unquote(conf.get("essential", "device")))
            self.sdevice.append(parse.unquote(conf.get("essential", "sdevice")))
            self.gameid.append(conf.get("essential", "gameid"))

    async def log(self, msg, t=1):
        if t:
            logging.info(msg)
        else:
            logging.error(msg)

    def detect_accelerator(self):
        self.tasks.append(self.main_detect_accelerator())

    def get_prize_rand(self):
        self.tasks.append(self.main_get_prize_rand())

    def get_prize_normal(self):
        self.tasks.append(self.main_get_prize_normal())

    def main_loop(self):
        self.loop.run_until_complete(asyncio.wait(self.tasks))


    async def main_detect_accelerator(self):
        asyncio.create_task(self.log("【加速卡检测线程】启动加速卡检测功能！"))
        flag = 1
        while True:
            try:
                response = requests.get("https://www.mobayx.com/2016/signcart2/", timeout=0.5)
                content = response.text
                soup = BeautifulSoup(content, 'html.parser')
                s1 = soup.find('li', class_='cd-2')
                s2 = s1.find_next('a')
            except:
                asyncio.create_task(self.log("【加速卡检测线程】=====网络出错，正在重试=====", 0))
                continue
            else:
                if s2.text == '补仓中':
                    flag = 1
                    await asyncio.sleep(1)
                else:
                    if flag:
                        asyncio.create_task(self.log("【加速卡检测线程】加速卡补货了！", 1))
                    flag = 0

    async def main_detect_prize(self):
        """
        主要功能：
        获取可获得奖品的日期
        （建议在获得加速卡之后运行）
        """
        # 这里是要提前做的，防止到时耗时过久
        pattern = re.compile('day(\d+)')
        for x in range(0, self.size):
            self.prize_target_rand.append([])
            self.prize_target_normal.append([])
            self.cdk.append([])
            # hdid = str(self.gameid[x])  # hdid为游戏编号，3为赛尔号，22为洛克王国
            # 首先需要获取当前已签到日期
            params = (
                ('ac', 'init'),
                ('hdid', self.gameid[x]),
                ('t', str(random.random())),
                ('c', ''),
                ('device', self.device[x]),
                ('scookie', self.scookie[x])
            )
            response = requests.get('https://www.mobayx.com/comm/qdlb/ajax_e2.php', headers=self.headers[x], params=params,
                                    cookies=self.cookies[x])
            content = json.loads(response.text)
            asyncio.create_task(
                self.log("【奖品侦测功能-封包记录】【" + self.name[x] + "】" + response.content.decode('unicode-escape'), 1))
            big_prize = content['prize_rand']
            normal_prize = content['prizes']
            for key in normal_prize:
                item = normal_prize[key]
                sign_day = pattern.match(key).group(1)
                if int(sign_day) <= int(content['sign_days']):
                    if item['code'] is None:
                        self.prize_target_normal[x].append(sign_day)
                    else:
                        self.cdk[x].append(item['code'])
            # 这里需要枚举字典
            for key in big_prize:
                item = big_prize[key]
                if int(item['sign_day']) <= int(content['sign_days']):
                    if item['code'] is None:
                        self.prize_target_rand[x].append(item['sign_day'])
                    else:
                        self.cdk[x].append(item['code'])
        for x in range(0, self.size):
            asyncio.create_task(self.log('【奖品侦测功能】【' + self.name[x] + '】目前可获取的限量奖品日期如下：' + str(
                self.prize_target_rand[x]) + '目前可获取的普通奖品日期如下：' + str(
                self.prize_target_normal[x]) + '目前已获得的cdk如下：' + str(self.cdk[x])))
        return self.prize_target_rand,self.prize_target_normal

    async def main_get_prize_rand(self):
        asyncio.create_task(self.log('【奖品自动抢功能】开始等待九点补仓。。。', 1))
        self.prize_target_rand,self.prize_target_normal = await self.main_detect_prize()
        while int(time.strftime("%H", time.localtime())) != 8 or int(time.strftime("%M", time.localtime())) != 58:
            print(self.prize_target_rand)
            await asyncio.sleep(30)
        while True:
            if time.strftime("%H", time.localtime()) == '9' and time.strftime("%M", time.localtime()) == '5':
                break
            for x in range(0, self.size):
                if self.prize_target_rand[x] == []:
                    continue
                data = {
                    'ac': 'prizeRand',
                    'rand': '',
                    'device': self.device[x],
                    'days': '',
                    'c': '',
                    'hdid': self.gameid[x],
                    'scookie': self.scookie[x]
                }

                for j in self.prize_target_rand[x]:
                    data['rand'] = str(random.random())
                    data['days'] = j
                    asyncio.create_task(self.post(x,data))
                    await asyncio.sleep(0.01)

    async def main_get_prize_normal(self):
        self.prize_target_rand, self.prize_target_normal = await self.main_detect_prize()
        print(self.prize_target_normal)
        for x in range(0, self.size):
            if self.prize_target_normal[x] == []:
                continue
            data = {
                'ac': 'prize',
                'rand': '',
                'device': self.device[x],
                'days': '',
                'c': '',
                'hdid': self.gameid[x],
                'scookie': self.scookie[x]
            }

            for j in self.prize_target_normal[x]:
                data['rand'] = str(random.random())
                data['days'] = j
                asyncio.create_task(self.post(x, data))

    async def post(self,x,data):
        response = requests.post('https://www.mobayx.com/comm/qdlb/ajax_e2.php', headers=self.headers[x],
                      cookies=self.cookies[x], data=data)
        print(response.text)