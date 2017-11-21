import json
import aiohttp
import asyncio
import time

class Get_Proxy:
    def __init__(self):
        self.ip_list_valid = list()
        self.proxy_list = list()
        self._session = None

    @property
    def session(self):
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return self._session

    async def get_proxy(self):
        res = await self.session.get("http://80161325451205093.standard.hutoudaili.com/"
                                   "?num=500&area_type=1&scheme=0&anonymity=0&order=1")
        resp = await res.text()
        for p in resp.split("\n"):
            proxy_ip = "http://" + p.strip()
            self.proxy_list.append(proxy_ip)
            # print(proxy)
        print(len(self.proxy_list))

        return self.proxy_list

    async def check_proxy(self,ip):
        url = 'https://www.baidu.com/'
        # 创建proxyhandler
        # 添加user_agent
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.baidu.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
        }
        # 安装opener
        try:
            res = await self.session.get(url,headers=headers,proxy=ip,timeout=5)
            print(ip, 'is ok')
            self.ip_list_valid.append(ip)
        except Exception as e:
            print(ip, e)

    async def fetch_proxy(self):
        time1 = time.time()
        list = await self.get_proxy()
        tasks = [self.check_proxy(ip) for ip in list]
        await asyncio.gather(*tasks)
        self.session.close()
        time2 = time.time()
        print(f"total time {time2-time1}s")
        print(f"proxy valid:{len(self.ip_list_valid)}")
        with open('proxy_pool.txt', 'w') as f:
            json.dump(self.ip_list_valid, f)

    def run(self):
        # gp = Get_Proxy()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.fetch_proxy())
        loop.close()


if __name__=='__main__':
    gp = Get_Proxy()
    gp.run()


