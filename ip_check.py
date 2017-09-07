from urllib import request
import requests
from bs4 import BeautifulSoup
from lxml import etree
import threading, socket, random
import time
import json
from ip_acquire import get_ips


def ip_test(ip):
	"""检验所获得的免费ip，并将有效的ip保存在本地，方便其他程序使用"""

	socket.setdefaulttimeout(5) #设置全局超时时间
	url = 'https://www.baidu.com/'
	#创建proxyhandler
	proxy_support = request.ProxyHandler(ip)
	#创建opener
	opener = request.build_opener(proxy_support)
	#添加user_agent
	opener.addheaders = [
						('User-Agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36'),
						('Host', 'www.jobbole.com'), 
						('Cookie','wordpress_logged_in_0efdf49af511fd88681529ef8c2e5fbf=super_super%7C1506509213%7CFhFz1N1oeutFfnhbza7zRcyQEk6faVTAxyiWVu2wLOy%7Ca033562741af2c0ebf9f98d97ee74cda70d51addf4e525ce34c32371dda1694f')
						] 
	#安装opener
	request.install_opener(opener)
	try:
		html = opener.open(url).read().decode('utf-8')
		print(ip, 'is ok')
		lock.acquire()
		ip_list_valid.append(ip)
		lock.release()
	except Exception as e:
		print(ip, e)

def check_ip():
	threads = []
	with open('ip_pool.txt', 'r') as f:
		ip_list = json.load(f)
	for i in range(len(ip_list)):
		thread = threading.Thread(target=ip_test, args=(ip_list[i],))
		threads.append(thread)
	for i in range(len(ip_list)):
		threads[i].start()
		time.sleep(0.5)
	for thread in threads:
		thread.join()

# 多线程验证
if __name__ == '__main__':
	# get_ips()
	start_time = time.time()
	ip_list_valid = []
	lock = threading.Lock()
	check_ip()
	print('%d ips are valid.' % len(ip_list_valid))
	end_time = time.time()
	print('多线程ip验证所花时间为：%s seconds' % (end_time-start_time))
	with open('ip_pool.txt', 'w') as f:
		json.dump(ip_list_valid, f)

# # 单线程
# start_time = time.time()
# ip_list_valid = []

# with open('ip_pool.txt', 'r') as f:
# 	ip_list = json.load(f)
# for i in range(len(ip_list)):
# 	ip_test(ip_list[i])
# print('%d ips are valid.' % len(ip_list_valid))
# end_time = time.time()
# print('单线程ip验证所花时间为：%s seconds' % (end_time-start_time))


