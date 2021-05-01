import requests
import time
import random
import json
import threading
from bs4 import BeautifulSoup
import re
import urllib.parse as parse
import os
import logging


class Box:
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

        self.login()

    def login(self):
        data = {
            'ac': 'login',
            't': time.strftime('%Y-%m-%d'),
            'r': random.random(),
            'scookie': self.scookie,
            'device': self.device,
            'sdevice': self.sdevice
        }
        response = requests.post('https://www.mobayx.com/2016/signcart2/hd_wap_user_e13.php', headers=self.headers,
                                 cookies=self.cookies, data=data)
        content = json.loads(response.text)
        if content['name'] == '':
            logging.error('【' + self.name + '】未获取到有效用户名！')
        else:
            logging.info('【' + self.name + '】用户:{} 调用login成功！'.format(content['name']))
        list = content['config']
        self.names = []
        self.num = []

        for item in list['gameinfo_list']:
            if type(item) == str:
                tmp = list['gameinfo_list']
                tmp = tmp[item]
                cont = tmp['gameinfo']
            elif type(item) == dict:
                cont = item['gameinfo']
            self.num.append(cont['id'])
            self.names.append(cont['packag'])
        self.stat = list['play_stat']
        self.delay_time = list['ios_delay_time']
        self.compare = dict(zip(self.num, self.names))

    def playgame(self):
        flag = 1
        self.login()
        games = ""
        maxsec = 0
        for gid in self.num:
            if self.stat[gid] == '0':
                data = {
                    'ac': 'playgame',
                    'gids': gid,
                    't': time.strftime('%Y-%m-%d'),
                    'r': random.random(),
                    'scookie': self.scookie,
                    'device': self.device,
                    'sdevice': self.sdevice
                }
                response = requests.post('https://www.mobayx.com/2016/signcart2/hd_wap_user_e13.php',
                                         headers=self.headers,
                                         cookies=self.cookies, data=data)
                maxsec = maxsec if maxsec > int(self.delay_time[gid])/1000 else int(self.delay_time[gid])/1000
                logging.info("【" + self.name + "】编号{}，{}:签到发包成功".format(gid, self.compare[gid]))
                time.sleep(1)
            else:
                logging.info('【' + self.name + '】编号{}，{}：该游戏已签到'.format(gid, self.compare[gid]))
            if gid == self.num[-1]:
                games = games + str(gid)
            else:
                games = games + str(gid) + "|"

        logging.info('【' + self.name + '】请等待{}秒'.format(maxsec))
        time.sleep(maxsec)

        data = {
            'ac': 'yesgame',
            'games': games,
            't': time.strftime('%Y-%m-%d'),
            'r': random.random(),
            'scookie': self.scookie,
            'device': self.device,
            'sdevice': self.sdevice
        }
        response = requests.post('https://www.mobayx.com/2016/signcart2/hd_wap_user_e13.php',
                                 headers=self.headers,
                                 cookies=self.cookies, data=data)
        content = json.loads(response.text)

        for gid in self.num:
            if content['play_stat'][gid] == '0':
                flag = 0
        if flag:
            logging.info("【" + self.name + "】所有签到结束！当前积分：{}".format(content['mark']))
            return True
        else:
            logging.error("【" + self.name + "】存在应用签到失败，重新执行签到任务！")
            if self.playgame():
                return True

    def detect_accelerate(self):
        logging.info("【" + self.name + "】启动加速卡监视线程！")
        threading.Thread(target=self.detect_main).start()

    def detect_main(self):
        flag = 1
        self.test_suppleup()
        while True:
            if time.strftime("%H", time.localtime()) == '8' and time.strftime("%M", time.localtime()) == '59':
                threading.Thread(target=self.test_prize).start()
            try:
                response = requests.get("https://www.mobayx.com/2016/signcart2/", timeout=0.5)
                content = response.text
                soup = BeautifulSoup(content, 'html.parser')
                s1 = soup.find('li', class_='cd-2')
                s2 = s1.find_next('a')
            except:
                logging.error("【" + self.name + "】=====网络出错，正在重试=====")
                continue
            else:
                if s2.text == '补仓中':
                    flag = 1
                    time.sleep(1)
                else:
                    if flag:
                        threading.Thread(target=self.test_accelerate).start()
                        logging.info("【" + self.name + "】加速卡补货了！")
                    flag = 0

    def test_accelerate(self):
        # 尝试脚本抢加速卡
        """
        大致逻辑：
        1、发现加速卡补仓
        2、输入验证码（自动识别or人工输入） # 这里发现三个卡只用输一次验证码步骤可以跳过
        3、抢到一张加速卡
        4、立刻前往签到页面使用 # 这个过程可以人工辅助，所以23333
        5、再去接着抢 # 不清楚需不需要延时，不知道是服务器延时还是客户端延时
        """
        data = {
            'ac': 'accelerator',
            't': time.strftime('%Y-%m-%d'),
            'r': random.random(),
            'scookie': self.scookie,
            'device': self.device,
            'sdevice': self.sdevice
        }
        while True:
            try:
                response = requests.post('https://www.mobayx.com/2016/signcart2/hd_wap_user_e13.php',
                                         headers=self.headers,
                                         cookies=self.cookies, data=data)
                content = json.loads(response.text)
                logging.info("【" + self.name + "】"+response.content.decode('unicode-escape'))
                if content['key'] == 'ok':
                    logging.info("【" + self.name + "】抢到一张加速卡，目前共有{}张加速卡".format(content['accelerator_card']))
                    time.sleep(1)
                    threading.Thread(target=self.test_signup).start()
                    time.sleep(2)
                elif content['key'] == 'show_checkLingqu_time':
                    pass
                elif content['key'] == 'error':
                    logging.info("【" + self.name + "】加速卡已抢完！")
                    break
                else:
                    break
            except:
                continue

    def test_supplementary(self):
        # 尝试脚本抢补签卡
        data = {
            'ac': 'supplementary',
            't': time.strftime('%Y-%m-%d'),
            'r': random.random(),
            'scookie': self.scookie,
            'device': self.device,
            'sdevice': self.sdevice
        }
        try:
            response = requests.post('https://www.mobayx.com/2016/signcart2/hd_wap_user_e13.php',
                                     headers=self.headers,
                                     cookies=self.cookies, data=data)
            content = json.loads(response.text)
            logging.info("【" + self.name + "】"+response.content.decode('unicode-escape'))
            if content['key'] == 'ok':
                logging.info("【" + self.name + "】抢到一张补签卡，目前共有{}张补签卡".format(content['accelerator_card']))
                time.sleep(10)
            elif content['key'] == 'show_checkLingqu_time':
                pass
            elif content['key'] == 'error':
                logging.info("【" + self.name + "】补签卡已抢完！")
        except:
            pass

    def test_suppleup(self):
        # 补签+签当天
        hdid = str(self.gameid)  # hdid为游戏编号，3为赛尔号
        flag = 0
        data = {}
        while flag != 1:
            flag = 1
            day_status = []  # range循环是左闭右开的，所以下面totalday要+1，才能令下标到达31（此时共有32项）
            for i in range(0, self.total_day + 1):
                day_status.append(0)
            # 首先需要获取当前已签到日期
            params = (
                ('ac', 'init'),
                ('hdid', hdid),
                ('t', random.random()),
                ('c', ''),
                ('device', self.device),
                ('scookie', self.scookie)
            )
            response = requests.get('https://www.mobayx.com/comm/qdlb/ajax.php', headers=self.headers, params=params,
                                    cookies=self.cookies)
            content = json.loads(response.text)
            logging.info("【" + self.name + "】" + response.content.decode('unicode-escape'))
            signed_day = content['sign_days2'].split(',')
            for item in signed_day:
                day_status[int(item)] = 1
            if day_status[int(time.strftime("%d", time.localtime()))] == 0:
                flag = -1
                t = time.strftime("%d", time.localtime())
            else:
                for i in range(1, int(time.strftime("%d", time.localtime()))):
                    if day_status[i] == 0:
                        flag = 2
                        self.test_supplementary()
                        t = str(i)  # t特指补签日期
            if flag == 1:
                logging.info("【" + self.name + "】没有可签到的日期，签到失败！")
                return False
            else:
                data = {
                    'ac': 'sign' if flag == -1 else 'signPre',
                    'rand': random.random(),
                    'device': self.device,
                    'c': '',
                    'day': t,
                    'hdid': hdid,
                    'gameid': '',
                    'status': 'undefined',
                    'scookie': self.scookie
                }
                logging.info("【" + self.name + "】尝试签到本月{}日。。。".format(t))
                response = requests.post('https://www.mobayx.com/comm/qdlb/ajax.php', headers=self.headers,
                                         cookies=self.cookies,
                                         data=data)
                content = json.loads(response.text)
                if content['pre_cs'] == 0:
                    logging.info("【" + self.name + "】没有补签卡，签到失败！")
                    return False
                time.sleep(0.5)
                data = {
                    'ac': 'sign' if flag == -1 else 'signPre',
                    'rand': random.random(),
                    'device': self.device,
                    'c': '',
                    'day': t,
                    'hdid': hdid,
                    'gameid': '',
                    'status': '1',
                    'scookie': self.scookie
                }
                response = requests.post('https://www.mobayx.com/comm/qdlb/ajax.php', headers=self.headers,
                                         cookies=self.cookies,
                                         data=data)
                content = json.loads(response.text)
                if content['key'] == 300:
                    logging.info("【" + self.name + "】本月{}日签到成功！".format(t))
                else:
                    logging.error("【" + self.name + "】出现问题,{}".format(content['msg']))
                    return False

    def test_signup(self):
        hdid = str(self.gameid)  # hdid为游戏编号，3为赛尔号，22为洛克王国
        day_status = []  # range循环是左闭右开的，所以下面totalday要+1，才能令下标到达31（此时共有32项）
        for i in range(0, self.total_day + 1):
            day_status.append(0)
        # 首先需要获取当前已签到日期
        params = (
            ('ac', 'init'),
            ('hdid', hdid),
            ('t', random.random()),
            ('c', ''),
            ('device', self.device),
            ('scookie', self.scookie)
        )
        response = requests.get('https://www.mobayx.com/comm/qdlb/ajax.php', headers=self.headers, params=params,
                                cookies=self.cookies)
        content = json.loads(response.text)
        logging.info("【" + self.name + "】" + response.content.decode('unicode-escape'))
        signed_day = content['sign_days2'].split(',')
        for item in signed_day:
            day_status[int(item)] = 1
        flag = 1
        for i in range(self.total_day, int(time.strftime("%d", time.localtime())), -1):
            if day_status[i] == 0:
                flag = 0
                t = str(i)  # t特指补签日期
                logging.info("【" + self.name + "】尝试签到本月{}日。。。".format(t))
                break
        if flag:
            logging.info("【" + self.name + "】没有可签到的日期，签到失败！")
        else:
            data = {
                'ac': 'signNext',
                'rand': random.random(),
                'device': self.device,
                'c': '',
                'day': t,
                'hdid': hdid,
                'gameid': '',
                'status': 'undefined',
                'scookie': self.scookie
            }
            response = requests.post('https://www.mobayx.com/comm/qdlb/ajax.php', headers=self.headers,
                                     cookies=self.cookies,
                                     data=data)
            content = json.loads(response.text)
            if content['next_cs'] == 0:
                logging.info("【" + self.name + "】没有加速卡，签到失败！")
                return False
            time.sleep(0.5)
            data = {
                'ac': 'signNext',
                'rand': random.random(),
                'device': self.device,
                'c': '',
                'day': t,
                'hdid': hdid,
                'gameid': '',
                'status': '1',
                'scookie': self.scookie
            }
            response = requests.post('https://www.mobayx.com/comm/qdlb/ajax.php', headers=self.headers,
                                     cookies=self.cookies,
                                     data=data)
            content = json.loads(response.text)
            if content['key'] == 300:
                logging.info("【" + self.name + "】本月{}日签到成功！".format(t))
                return True
            else:
                logging.error("【" + self.name + "】出现问题,{}".format(content['msg']))
                return False

    def test_prize(self):
        """
        大致逻辑：
        1、获取奖品的日期
        2、构造数据包
        """
        hdid = str(self.gameid)  # hdid为游戏编号，3为赛尔号，22为洛克王国
        day_status = []  # range循环是左闭右开的，所以下面totalday要+1，才能令下标到达31（此时共有32项）
        for i in range(0, self.total_day + 1):
            day_status.append(0)
        # 首先需要获取当前已签到日期
        params = (
            ('ac', 'init'),
            ('hdid', hdid),
            ('t', random.random()),
            ('c', ''),
            ('device', self.device),
            ('scookie', self.scookie)
        )
        response = requests.get('https://www.mobayx.com/comm/qdlb/ajax.php', headers=self.headers, params=params,
                                cookies=self.cookies)
        content = json.loads(response.text)
        logging.info("【" + self.name + "】" + response.content.decode('unicode-escape'))
        big_prize = content['prize_rand']
        target = '-1'
        # 这里需要枚举字典
        while True:
            for key in big_prize:
                item = big_prize[key]
                if item['code'] is None:
                    target = item['sign_day']
            if target == '-1':
                logging.info("【" + self.name + "】未找到可抢的礼品,结束进程！")
                return False
            # 默认账户已经提前绑定
            data = {
                'ac': 'prizeRand',
                'rand': random.random(),
                'device': self.device,
                'days': target,
                'c': '',
                'hdid': hdid,
                'scookie': self.scookie
            }
            response = requests.post('https://www.mobayx.com/comm/qdlb/ajax.php', headers=self.headers,
                                     cookies=self.cookies,
                                     data=data)
            content = json.loads(response.text)
            if content['key'] == 200:
                logging.info('【' + self.name + '】成功抢到{}日礼品！'.format(target))
            else:
                logging.error("【" + self.name + "】出现问题,{}".format(content['msg']))
            if time.strftime("%M", time.localtime()) == '5':
                logging.info("【" + self.name + "】补货时间已过,结束进程！")

