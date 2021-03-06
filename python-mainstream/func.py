from datetime import date, datetime

from ocr import Xunfei
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
    def __init__(self, name, cookies, headers, smid,scookie, device, sdevice, gameid):
        self.xunfei = Xunfei()
        self.url_signchart = 'https://huodong2.4399.com/comm/qdlb/ajax_e3.php'
        self.url_getcard = 'https://huodong2.4399.com/2016/signcart2/hd_wap_user_e13.php?1'
        self.url_hebi = 'https://huodong2.4399.com/comm/playapp2/m/hd_wap_user_e4.php'
        self.url_lingqu_check ="https://huodong2.4399.com/identifying_code/identifyCode.https.api.php?ac=pic&type=4&randkey=lingqu&reflash=1"
        self.url_qingqu_check_upload="https://huodong2.4399.com/comm/playapp2/m/hd_wap_user_e4.php"
        self.url_prize = "https://huodong2.4399.com/comm/qdlb/ajax_e3.php"
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

        # self.headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 11; GM1910 Build/RKQ1.201022.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36 4399GameCenter/6.6.1.31(android;GM1910;11;1440x3060;4G;1747.795;baidu)",
        #                 "Content-Type":"application/x-www-form-urlencoded",
        #                 "Sec-Fetch-Site":"same-origin",
        #                 "Sec-Fetch-Mode": "cors",
        #                 "Sec-Fetch-Dest": "empty",
        #                 "Referer": "https://huodong2.4399.com/2016/signcart2/",
        #                 "Accept-Encoding": "gzip, deflate",
        #                 "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
        #                 }
        self.headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 10; MIX 2S Build/QKQ1.190828.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.101 Mobile Safari/537.36 4399GameCenter/6.4.1.33(android;MIX 2S;10;1080x2030;WIFI;1705.774;wap4399)",
                        "Content-Type":"application/x-www-form-urlencoded",
                        "Sec-Fetch-Site":"same-origin",
                        "Sec-Fetch-Mode": "cors",
                        "Sec-Fetch-Dest": "empty",
                        "Referer": "https://huodong2.4399.com/2016/signcart2/",
                        "Accept-Encoding": "gzip, deflate",
                        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
                        }
        self.headers={}
        cok = re.findall(r'([^=]+)=([^;]+)[ ;]*', parse.unquote(cookies))
        hed = re.findall(r'([^:]+): ([^\n]+)[\n]*', parse.unquote(headers.replace('#', '\n')))
        for item in cok:
            self.cookies[item[0]] = item[1]
        for item in hed:
           self.headers[item[0]] = item[1]
        self.scookie = parse.unquote(scookie)
        #self.scookie = "0%7C644844046%7C05c477b1a39f7b88358b9e02d3627841%7C1a4131816%7C3de356aeebe97d7e0dfcd80026ccb552%7C644844046"
        #self.scookie = parse.unquote(smid)
        # self.smid = "202206041012485a32a4dd22c05b95978ae817551fec59006f26ff7e9ea7c90"
        self.smid = "202206141502325a32a4dd22c05b95978ae817551fec5900bce3108030ca4c0"

        self.device = parse.unquote(device)
        self.sdevice = parse.unquote(sdevice)
        self.gameid = gameid

        #print(self.headers)
        # 以下是部分全局变量
        self.num = []
        self.names = []
        # 定义一个月中有多少天
        day_of_month = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        self.total_day = day_of_month[int(time.strftime("%m", time.localtime()))]

        #self.login()

    def login(self):
        data = {
            'ac': 'login',
            't': time.strftime('%Y-%m-%d'),
            'r': random.random(),
            'scookie': self.scookie,
            'device': self.device,
            'sdevice': self.sdevice
        }
        response = requests.post(self.url_getcard, headers=self.headers,
                                 cookies=self.cookies, data=data)

        print(response.request.headers)
        content = json.loads(response.text)

        if content['name'] == '':
            logging.error('【' + self.name + '】未获取到有效用户名！')
        else:
            logging.info('【' + self.name + '】用户:{} 调用login成功！'.format(content['name']))
        print(content)
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

    def login_with_cid(self,cid):
        data = {
            'ac': 'login',
            'cid':cid,
            't': time.strftime('%Y-%m-%d'),
            'r': random.random(),
            'scookie': self.scookie,
            'device': self.device,
            'sdevice': self.sdevice
        }
        response = requests.post(self.url_hebi, headers=self.headers,
                                 cookies=self.cookies, data=data)

        #print(response.request.headers)
        content = json.loads(response.text)

        # if content['name'] == '':
        #     logging.error('【' + self.name + '】未获取到有效用户名！')
        # else:
        #     logging.info('【' + self.name + '】用户:{} 调用login成功！'.format(content['name']))
        try:
            print('已完成天数：',content['config']['play_day'])
            if (int(content['config']['play_day'])>5):
                return False
            else:
                return True
            # self.names = []
            # self.num = []
        except Exception as e:
                print(content)
                return True




        """for item in list['gameinfo_list']:
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
        """
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
                response = requests.post(self.url_getcard,
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
        response = requests.post(self.url_getcard,
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

    def hebi(self):
        #626 - 640
        #cid = 637


        cid_list=[]
        for cid in range(10,643):
            print("------------------------")
            print("正在执行使用应用id：" , cid)
            if(self.login_with_cid(cid)==False):
                continue
            cid_list.append(cid)
            data = {
                'ac': 'download',
                'cid': cid,
                't': time.strftime('%Y-%m-%d'),
                'r': random.random(),
                'scookie': self.scookie,
                'device': self.device,
                'sdevice': self.sdevice
            }
            response = requests.post(self.url_hebi,
                                     headers=self.headers,
                                     cookies=self.cookies, data=data)
            #print(response.text)

            data = {
                'ac': 'clickplay',
                'cid': cid,
                't': time.strftime('%Y-%m-%d'),
                'r': random.random(),
                'scookie': self.scookie,
                'device': self.device,
                'sdevice': self.sdevice
            }
            response = requests.post(self.url_hebi,
                                     headers=self.headers,
                                     cookies=self.cookies, data=data)
            #print(response.text)

            """
            maxsec = maxsec if maxsec > int(self.delay_time[gid]) / 1000 else int(self.delay_time[gid]) / 1000
            logging.info("【" + self.name + "】编号{}，{}:签到发包成功".format(gid, self.compare[gid]))
            time.sleep(1)
    
                else:
                    logging.info('【' + self.name + '】编号{}，{}：该游戏已签到'.format(gid, self.compare[gid]))
                if gid == self.num[-1]:
                    games = games + str(gid)
                else:
                    games = games + str(gid) + "|"
    
            logging.info('【' + self.name + '】请等待{}秒'.format(maxsec))
            
            """
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        time.sleep(480)

        credit = 0
        for cid in cid_list:
            print("------------------------")
            print("正在执行领取应用id：",cid)
            code, key = self.check()
            data = {
                'ac': 'checkindentify',
                'cid': cid,
                'codekey': key,
                'code': code,
                't': time.strftime('%Y-%m-%d'),
                'r': random.random(),
                'scookie': self.scookie,
                'device': self.device,
                'sdevice': self.sdevice
            }
            response = requests.post(self.url_qingqu_check_upload,
                                     headers=self.headers,
                                     cookies=self.cookies, data=data)
            #print(response.text)


            data = {
                'ac': 'playtime',
                'cid': cid,
                't': time.strftime('%Y-%m-%d'),
                'r': random.random(),
                'scookie': self.scookie,
                'device': self.device,
                'sdevice': self.sdevice
            }
            response = requests.post(self.url_hebi,
                                     headers=self.headers,
                                     cookies=self.cookies, data=data)
            #print(response.text)

            #content = json.loads(response.text)



            data = {
                'ac': 'lingqu',
                'cid': cid,
                't': time.strftime('%Y-%m-%d'),
                'r': random.random(),
                'smid':self.smid,
                'scookie': self.scookie,
                'device': self.device,
                'sdevice': self.sdevice
            }
            response = requests.post(self.url_hebi,
                                     headers=self.headers,
                                     cookies=self.cookies, data=data)
            content = json.loads(response.text)

            try:
                if content['error_msg'][:1].isdigit():
                    result = content['error_msg'][:2]
                    credit = credit + int(content['error_msg'][:2])
                else:
                    result = content['error_msg'].encode('utf-8').decode('unicode-escape')
                print(result)
            except Exception as e:
                print(content)
            time.sleep(1)
        print(credit)
        """
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
        """

    def check(self):
        response = requests.get(self.url_lingqu_check,
                                 headers=self.headers,
                                 cookies=self.cookies)
        print(response.text)
        content = json.loads(response.text)
        url = content['img']
        key = content['key']
        #print(url)

        import urllib.request
        try:
            urllib.request.urlretrieve(url, filename="code.jpg")
        except IOError as e:
            print("IOE ERROR")
        except Exception as e:
            print("Exception")

        try:
            code = self.xunfei.get_word()
            print(code)
            return code, key
        except Exception as e:
            print(e)
            print("重试验证码中")
            return self.check()

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

    def detect_prize_main(self):
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
                response = requests.post(self.url_getcard,
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
            response = requests.post(self.url_getcard,
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
            response = requests.get(self.url_signchart, headers=self.headers, params=params,
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
                response = requests.post(self.url_signchart, headers=self.headers,
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
                response = requests.post(self.url_signchart, headers=self.headers,
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
        response = requests.get(self.url_signchart, headers=self.headers, params=params,
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
            response = requests.post(self.url_signchart, headers=self.headers,
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
            response = requests.post(self.url_signchart, headers=self.headers,
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
        response = requests.get(self.url_signchart, headers=self.headers, params=params,
                                cookies=self.cookies)
        content = json.loads(response.text)
        logging.info("【" + self.name + "】" + response.content.decode('unicode-escape'))
        big_prize = content['prize_rand']
        target = '-1'
        # 这里需要枚举字典
        import datetime
        d1 = date.today()
        t9 = datetime.time(9, 0, 0)
        nine_oclock = datetime.datetime.combine(d1, t9)  # 7点抢座时间

        curr_time = datetime.datetime.now()  # 第一个执行的时候休眠到指定时间执行
        total_seconds = (nine_oclock - curr_time).total_seconds()  # 时间差
        # print(total_seconds)

        time.sleep(total_seconds - 2)  # 休眠到指定时间
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
            response = requests.post(self.url_signchart, headers=self.headers,
                                     cookies=self.cookies,
                                     data=data)
            content = json.loads(response.text)
            if content['key'] == 200:
                logging.info('【' + self.name + '】成功抢到{}日礼品！'.format(target))
            else:
                logging.error("【" + self.name + "】出现问题,{}".format(content['msg']))
            if time.strftime("%M", time.localtime()) == '5':
                logging.info("【" + self.name + "】补货时间已过,结束进程！")
                break

    def firefox_candy(self):


        from selenium import webdriver

        # 头信息
        from selenium.webdriver.firefox.options import Options

        options = Options()
        options.add_argument('--incognito')
        options.add_argument(
             'user-agent="Mozilla/5.0 (Linux; Android 11; GM1910 Build/RKQ1.201022.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.141 Mobile Safari/537.36 4399GameCenter/6.6.1.31(android;GM1910;11;1440x3060;4G;1747.795;baidu)"')
        # options.add_argument(self.headers)
        Path = 'D:/python_tool/geckodriver.exe'
        wb = webdriver.Firefox(options=options, executable_path=Path)
        # 进入网页+登录
        wb.get('https://huodong.4399.cn/game/maintain/game/candyDart/index?hduuid=3yeq5pjyr&id=13630=3#/home')