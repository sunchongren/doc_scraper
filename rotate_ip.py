import requests
from bs4 import BeautifulSoup
import random

IP_URL = "https://free-proxy-list.net/"

def get_ip(url):
    res = requests.get(url)
    content = BeautifulSoup(res.text, 'lxml')
    table = content.find('table')
    rows = table.find_all('tr')
    cols = [[col.text for col in row.find_all('td')] for row in rows]

    proxies = []
    for col in cols:
        try:
            if col[4] == 'elite proxy' and col[6] == 'yes':
                href = 'http://' + col[0] + ':' + col[1]
                # print(href)
                proxies.append(href)
        except:
            pass
    
    return proxies

def get_random_proxy(proxy_list):
    return {'http': random.choice(proxy_list)}

print(get_ip(IP_URL))