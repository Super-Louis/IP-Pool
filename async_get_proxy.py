import json
import aiohttp
import asyncio
import time
import pika
from pika import exceptions as pika_exception
import logging

class MqSession(object):
    def __init__(self):
        try:
            self.credentials = pika.PlainCredentials(username='***', password='***')
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='***', credentials=self.credentials))
            self.channel = self.connection.channel()
            self.channel.basic_qos(prefetch_count=1)
        except Exception as e:
            logging.error('rabbit mq error : %s' % (str(e)))
            raise

    def put(self, queue, body):
        while True:
            try:
                self.channel.basic_publish(exchange='***', routing_key=queue, body=body.encode('utf-8'))
            except pika_exception.ConnectionClosed:
                self.channel = self.connection.channel()
            except Exception as e:
                logging.error('rabbit mq error : %s' % (str(e)))
                return -1
            else:
                return 0

    def close(self):
        self.connection.close()

class Get_Proxy:
    def __init__(self):
        self._session = None

    @property
    def session(self):
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return self._session

    async def get_proxy(self):
        proxy_list = list()
        res = await self.session.get("******")
        resp = await res.text()
        for p in resp.split("\n"):
            proxy_ip = "http://" + p.strip()
            proxy_list.append(proxy_ip)
        print(len(proxy_list))

        return proxy_list

    async def check_proxy(self,ip):
        url = 'https://www.baidu.com/'

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
        try:
            res = await self.session.get(url,headers=headers,proxy=ip,timeout=5)
            print(ip, 'is ok')
            mq.put(queue='***', body=proxy)
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


    def run(self):
        # gp = Get_Proxy()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.fetch_proxy())
        loop.close()


if __name__=='__main__':
    mq = MqSession()
    gp = Get_Proxy()
    gp.run()
    mq.close()


