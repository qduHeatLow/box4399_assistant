# -*- coding: utf-8 -*-
import json
from urllib import parse
import base64
import hashlib
import time
import requests
import jsonpath



class Xunfei:
    def __init__(self):
        """
              手写文字识别WebAPI接口调用示例接口文档(必看):https://doc.xfyun.cn/rest_api/%E6%89%8B%E5%86%99%E6%96%87%E5%AD%97%E8%AF%86%E5%88%AB.html
              图片属性：jpg/png/bmp,最短边至少15px，最长边最大4096px,编码后大小不超过4M,识别文字语种：中英文
              webapi OCR服务参考帖子(必看)：http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=39111&highlight=OCR
              (Very Important)创建完webapi应用添加服务之后一定要设置ip白名单，找到控制台--我的应用--设置ip白名单，如何设置参考：http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=41891
              错误码链接：https://www.xfyun.cn/document/error-code (code返回错误码时必看)
              @author iflytek
            """
        # OCR手写文字识别接口地址
        self.URL = "http://webapi.xfyun.cn/v1/service/v1/ocr/handwriting"
        # 应用APPID(必须为webapi类型应用,并开通手写文字识别服务,参考帖子如何创建一个webapi应用：http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=36481)
        self.APPID = "333dd1b6"
        # 接口密钥(webapi类型应用开通手写文字识别后，控制台--我的应用---手写文字识别---相应服务的apikey)
        self.API_KEY = "a76206b351479a985ca9fdb4a4da6f03"
        # 语种设置
        self.language = "en"
        # 是否返回文本位置信息
        self.location = "true"
        # 图片上传接口地址
        self.filepath = "code.jpg"

    def getHeader(self):
        curTime = str(int(time.time()))
        param = "{\"language\":\"" + self.language + "\",\"location\":\"" + self.location + "\"}"
        paramBase64 = base64.b64encode(param.encode('utf-8'))

        m2 = hashlib.md5()
        str1 = self.API_KEY + curTime + str(paramBase64, 'utf-8')
        m2.update(str1.encode('utf-8'))
        checkSum = m2.hexdigest()
        # 组装http请求头
        header = {
            'X-CurTime': curTime,
            'X-Param': paramBase64,
            'X-Appid': self.APPID,
            'X-CheckSum': checkSum,
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        }
        return header

    def getBody(self):
        with open(self.filepath, 'rb') as f:
            imgfile = f.read()
        data = {'image': str(base64.b64encode(imgfile), 'utf-8')}
        return data

    def get_word(self):
        # headers=getHeader(language, location)
        response = requests.post(self.URL, headers=self.getHeader(), data=self.getBody())

        content = json.loads(response.text)
        #print(content)
        word = jsonpath.jsonpath(jsonpath.jsonpath(jsonpath.jsonpath(jsonpath.jsonpath(content, '$.data.block')[0][0], '$.line')[0][0], '$.word')[0][0], '$.content')
        if word[0][:-1].find('×'):
            #print('---')
            #print(word[0][:-1])
            word[0][:-1].replace('×','*')
            #print(word[0][:-1])
        return eval(word[0][:-1])