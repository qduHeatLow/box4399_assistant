import json
import time
import requests

headers = {
    'authority': 'm.weibo.cn',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'accept': 'application/json, text/plain, */*',
    'mweibo-pwa': '1',
    'x-xsrf-token': '920de5',
    'x-requested-with': 'XMLHttpRequest',
    'user-agent': 'Mozilla/5.0 (Linux; Android 9.0; MI 8 SE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.119 Mobile Safari/537.36',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://m.weibo.cn/search?containerid=100103type%3D1%26q%3D%E8%9B%8B%E5%A3%B3',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cookie': 'SCF=AlSQ8aMlgofViCYSVfHBoqfq_VLKbT6mJZ-2R8LFMJJNi74ljAeEwniK-u1kdsWuPomL_AedMNP-nePb19_xgdw.; WEIBOCN_FROM=1110005030; SUB=_2A25y1MbEDeRhGeBN41YV8SvKzj2IHXVuNuqMrDV6PUJbkdANLW_xkW1NRAnWcn83G83pn29B1vicHH-9jwVd93yW; _T_WM=89292249966; MLOGIN=1; XSRF-TOKEN=920de5; M_WEIBOCN_PARAMS=oid%3D4580178036789997%26luicode%3D10000011%26lfid%3D100103type%253D1%2526q%253D%25E8%259B%258B%25E5%25A3%25B3%26fid%3D100103type%253D1%2526q%253D%25E8%259B%258B%25E5%25A3%25B3%26uicode%3D10000011',
}

ok = 1
page = 1
with open('data.txt','w',encoding='utf-8') as f:
    while ok:
        try:
            params = (
                ('containerid', '100103type=1&q=\u86CB\u58F3\u516C\u5BD3'),
                ('page_type', 'searchall'),
                ('page',page)
            )
            response = requests.get('https://m.weibo.cn/api/container/getIndex', headers=headers, params=params)
            data = json.loads(response.text)
            if data['ok'] == 1:
                for item in data['data']['cards']:
                    if item['card_type'] == 9:
                        if item['mblog']['isLongText'] == False:
                            print(item['mblog']['raw_text'].replace('\n','\t').replace('\r','\t'))
                            f.writelines(str(item['mblog']['raw_text'].replace('\n','\t').replace('\r','\t')))
                            f.writelines('\n')
                        else:
                            params = (
                                ('id', item['mblog']['id']),
                            )
                            response = requests.get('https://m.weibo.cn/statuses/extend', headers=headers, params=params)
                            da = json.loads(response.text)
                            print(da['data']['longTextContent'].replace('\n','\t').replace('\r','\t'))
                            f.writelines(str(da['data']['longTextContent'].replace('\n','\t').replace('\r','\t')))
                            f.writelines('\n')
                page = page + 1
                time.sleep(10)
            else:
                print('没有更新的内容了，当前爬到第{}页'.format(page))
                break
        except:
            print("网络链接出现问题，正在重新尝试请求！")


