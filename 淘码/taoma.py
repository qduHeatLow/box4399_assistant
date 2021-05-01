import json
import random
import time


import requests

li = []
li_filter = []
cookies_list=[
    #InDream
    {
        'hd_comm_gifts_27_access': '1',
        '_4399stats_vid': '16066962335012535',
        'UM_distinctid': '176168eeb841d4-0b7df6680b96ec-4c3f2779-130980-176168eeb861d',
        'Hm_lvt_334aca66d28b3b338a76075366b2b9e8': '1606696234',
        'Hm_lpvt_334aca66d28b3b338a76075366b2b9e8': '1606696234',
        'Hm_lvt_7fb37cb72d7723dcb46e14756c6b23b6': '1606696241',
        'Hm_lpvt_7fb37cb72d7723dcb46e14756c6b23b6': '1606696541',
        'CNZZDATA30020228': 'cnzz_eid%3D1214487109-1606693487-http%253A%252F%252Fwww.4399.com%252F%26ntime%3D1606693376',
        'CNZZDATA30039538': 'cnzz_eid%3D577125410-1606695535-http%253A%252F%252Fwww.4399.com%252F%26ntime%3D1606694823',
        'USESSIONID': '1e78b503-e023-4aa3-b682-099ee31455af',
        'Uauth': 'ext|In%EF%BC%87Dream|20201130|huodong.|1606696296450|b56823ccc4a8e9304476c6f6bef40782',
        'Pauth': '3009218591|2048496262|t3ce7m0000fbda1408aee90bf4a9fef8|1606696296|10002|6098a2e9050309d3c7fe7c932a082852|0',
        'ck_accname': '2048496262',
        'Puser': '2048496262',
        'Xauth': '69daeb69827f6dc91d6df82169e42c6c',
        'ptusertype': 'huodong.qq_login',
        'Pnick': 'InDream',
        'Qnick': 'In%EF%BC%87Dream',
    },
    {
        'hd_comm_gifts_27_access': '1',
        'Hm_lvt_7fb37cb72d7723dcb46e14756c6b23b6': '1606696449',
        'Hm_lpvt_7fb37cb72d7723dcb46e14756c6b23b6': '1606696487',
        'UM_distinctid': '176169234e287-0521e448b27153-4c3f2779-130980-176169234e341',
        'CNZZDATA30020228': 'cnzz_eid%3D1119339584-1606693487-%26ntime%3D1606693487',
        'CNZZDATA30039538': 'cnzz_eid%3D1662644015-1606695535-%26ntime%3D1606695535',
        'USESSIONID': '28518ec7-8476-4f61-9b13-2b5607ab6d35',
        'Uauth': '4399|1|20201130|huodong.|1606696485946|fbed67144e4275f189450057294c1f8f',
        'Pauth': '3302013609|inxdream|t3ce7n53364cbd3ee12f996dca2042e4|1606696485|10002|896a47607e250debb91a4af58d01ed4f|0',
        'ck_accname': 'inxdream',
        'Puser': 'inxdream',
        'Xauth': '5aefe9a4e3b7a9dc3eb4c7000730d5b2',
        'ptusertype': 'huodong.4399_login',
        'Pnick': 'INXdream',
        'Qnick': '',
    },
    {
        'hd_comm_gifts_27_access': '1',
        'Hm_lvt_7fb37cb72d7723dcb46e14756c6b23b6': '1606696564',
        'Hm_lpvt_7fb37cb72d7723dcb46e14756c6b23b6': '1606696594',
        'UM_distinctid': '1761693f53b91-0a9753c98d9d42-4c3f2779-130980-1761693f53c12b',
        'CNZZDATA30020228': 'cnzz_eid%3D2033822858-1606693376-%26ntime%3D1606693376',
        'CNZZDATA30039538': 'cnzz_eid%3D2000969083-1606694823-%26ntime%3D1606694823',
        'USESSIONID': 'b15d1c66-9b32-4c68-a295-a8335ac86b5a',
        'Uauth': '4399|1|20201130|huodong.|1606696592435|629fac381551dabaf07f59a406cfd32e',
        'Pauth': '3302454069|inxdream001|t3ce7n53364f77aa706704e44d40250c|1606696592|10002|9b9189d1c0bd20e9c57ecd526385c3b2|0',
        'ck_accname': 'inxdream001',
        'Puser': 'inxdream001',
        'Xauth': 'ea778e07a03bae7ed1a867464d7200ab',
        'ptusertype': 'huodong.4399_login',
        'Pnick': '%E6%B8%A9%E6%9F%94%E5%8F%88%E8%90%8C%E8%90%8C%E7%9A%84%E7%9B%92%E9%A5%ADa89a',
        'Qnick': '',
    },
    {
        'hd_comm_gifts_27_access': '1',
        'Hm_lvt_7fb37cb72d7723dcb46e14756c6b23b6': '1606696643',
        'Hm_lpvt_7fb37cb72d7723dcb46e14756c6b23b6': '1606696672',
        'UM_distinctid': '17616952bae62-09fad738fa9f03-4c3f2779-130980-17616952bb07d',
        'CNZZDATA30020228': 'cnzz_eid%3D1206482321-1606693487-%26ntime%3D1606693487',
        'CNZZDATA30039538': 'cnzz_eid%3D1732828796-1606695535-%26ntime%3D1606695535',
        'USESSIONID': '4be14713-d7d6-4065-a303-e04e658c8d99',
        'Uauth': '4399|1|20201130|huodong.|1606696670244|4bd1e1a9fa2d4c94e61192b6dacb950e',
        'Pauth': '3303256566|inxdream002|t3ce7n5336f2aea91cc0409106df6be0|1606696670|10002|48462a0ad2813debf0224a1fd764e853|0',
        'ck_accname': 'inxdream002',
        'Puser': 'inxdream002',
        'Xauth': '27acfd0d26eda04954e997ebe1814d8d',
        'ptusertype': 'huodong.4399_login',
        'Pnick': 'inxdream002',
        'Qnick': '',
    },
    {
        'hd_comm_gifts_27_access': '1',
        'Hm_lvt_7fb37cb72d7723dcb46e14756c6b23b6': '1606696734',
        'Hm_lpvt_7fb37cb72d7723dcb46e14756c6b23b6': '1606696764',
        'UM_distinctid': '17616968e8f62-003163dd0c92d18-4c3f2779-130980-17616968e901b5',
        'CNZZDATA30020228': 'cnzz_eid%3D577534144-1606693487-%26ntime%3D1606693487',
        'CNZZDATA30039538': 'cnzz_eid%3D751903218-1606695535-%26ntime%3D1606695535',
        'USESSIONID': 'bb614a9b-c40a-41f2-8a7f-23ff61e25689',
        'Uauth': '4399|1|20201130|huodong.|1606696762652|d5fcc905ec82d82aa92ac87a4d88a9ae',
        'Pauth': '3305050096|inxdream003|t3ce7n533696e7a2e71c2fcb8c31ac02|1606696762|10002|fc0cb8d7edd9d3b4fbc2bf7cc93fc157|0',
        'ck_accname': 'inxdream003',
        'Puser': 'inxdream003',
        'Xauth': '0bece4a0c662ded8ce5e08c3ce248134',
        'ptusertype': 'huodong.4399_login',
        'Pnick': '%E8%80%90%E5%BF%83%E5%8F%88%E5%B8%85%E6%B0%94%E7%9A%84%E7%9B%92%E9%A5%ADzpda',
        'Qnick': '',
    }
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'http://huodong2.4399.com',
    'Connection': 'keep-alive',
    'Referer': 'http://huodong2.4399.com/gifts/2020tlj_27.html?zt',
}

for i in range(0,5):
    data = {
        'op': 'taoma',
        'hd_id': '27',
        't': random.random()
    }
    try:
        response = requests.post('http://huodong2.4399.com/gifts/ajax.php', headers=headers, cookies=cookies_list[i], data=data)
        data = json.loads(response.text)
        # print(requests.utils.dict_from_cookiejar(response.cookies))
        print(data)
        if data["status"] == "ok":
            for item in data["taomaList"]:
                li.append(item)
                if item[0:4] in ["2SAS","TJCU","DR3Q","PH87"]:
                    #2SAS圣尊，TJCU水晶，DR3Q幻曦,PH87瞬杀
                    li_filter.append(item)
        #time.sleep(5)
        else:
            print("#{}TimeOut".format(i))
    except:
        print("#{}Error".format(i))

for item in li_filter:
    print(item)
