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