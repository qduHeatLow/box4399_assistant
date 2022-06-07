from func import Box
from configparser import RawConfigParser
import os
import threading


def run_program(name):
    conf = RawConfigParser()
    conf.read('.\confs\\' + name)
    box = Box(name, conf.get("essential", "cookies"), conf.get("essential", "headers"),
              conf.get("essential", "smid"),
              conf.get("essential", "scookie"),
              conf.get("essential", "device"), conf.get("essential", "sdevice"), conf.get("essential", "gameid"))
    box.hebi()



    #box.detect_accelerate()  # 检查加速卡状态，全自动线程
    #box.playgame()  # 自动签到拿积分
    # con.test_prize()


if __name__ == '__main__':
    filelist = []
    for root, dirs, files in os.walk(".\confs", topdown=False):
        if root == ".\confs":
            for name in files:
                if name.split('.')[-1] == 'ini':
                    filelist.append(name)
    for item in filelist:
        # run_program(item)
        threading.Thread(target=run_program, args=(item,)).start()

