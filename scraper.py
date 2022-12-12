from collections import OrderedDict
from datetime import datetime
import re
import aiohttp
import asyncio
from bs4 import BeautifulSoup, Tag

import requests


g_Tasks = []


async def save_result(result):
    with open('not-checked.txt', 'w') as file:
        for proxy in result:
            if proxy:
                file.write(proxy + '\n')


async def scrape(url, result: list):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
        resp = requests.get(url, headers=headers, timeout=5)
        proxies = resp.text
        pattern = re.compile(r"\d{1,3}(?:\.\d{1,3}){3}(?::\d{1,5})?")
        output = re.findall(pattern, proxies)
        if not output:
            pattern_one(url, result)
        else:
            for s in output:
                result.append(s)
    except:
        pass


def pattern_one(url, result):
    ip_port = re.findall("(\d{,3}\.\d{,3}\.\d{,3}\.\d{,3}:\d{2,5})", url)
    if not ip_port:
        pattern_two(url)
    else:
        for i in ip_port:
            result.append(i)


def pattern_two(url, result):
    ip = re.findall(">(\d{,3}\.\d{,3}\.\d{,3}\.\d{,3})<", url)
    port = re.findall("td>(\d{2,5})<", url)
    if not ip or not port:
        pattern_three(url)
    else:
        for i in range(len(ip)):
            result.append(i)


def pattern_three(url, result):
    ip = re.findall(">\n[\s]+(\d{,3}\.\d{,3}\.\d{,3}\.\d{,3})", url)
    port = re.findall(">\n[\s]+(\d{2,5})\n", url)

    if not ip or not port:
        pattern_four(url)
    else:
        for i in range(len(ip)):
            result.append(i)


def pattern_four(url, result):
    ip = re.findall(">(\d{,3}\.\d{,3}\.\d{,3}\.\d{,3})<", url)
    port = re.findall(">(\d{2,5})<", url)

    if not ip or not port:
        pattern_five(url)
    else:
        for i in range(len(ip)):
            result.append(i)


def pattern_five(url, result):
    ip = re.findall("(\d{,3}\.\d{,3}\.\d{,3}\.\d{,3})", url)
    port = re.findall("(\d{2,5})", url)

    for i in range(len(ip)):
        result.append(i)


dates = []
dateRegex = "[0-9]{4}-[0-9]{2}-[0-9]{2}"
proxyRegex = r"\b(?:(?:2(?:[0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9])\.){3}(?:(?:2([0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9]))\b:[0-9]?[0-9]?[0-9]?[0-9]"


def getDates() -> list[str]:
    request = requests.get("https://checkerproxy.net/api/archive/")
    if request.status_code == 200:
        for date in re.findall(dateRegex, str(request.json()),
                               re.RegexFlag.MULTILINE):
            dates.append(date)
    return dates


async def startCP(result: list):
    for date in getDates():
        sk = datetime.today().strftime('%Y-%m-%d')
        suanki_ay = int(sk.split('-')[1])
        suanki_gun = int(sk.split('-')[2])
        ay = int(date.split('-')[1])
        gun = int(date.split('-')[2])
        if ay >= suanki_ay and gun > suanki_gun - 10:
            request = requests.get(
                "https://checkerproxy.net/api/archive/" + date)
            for proxy in re.finditer(proxyRegex, str(request.json()),
                                     re.RegexFlag.MULTILINE):
                result.append(proxy.group())

def extract(url, result: list):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9'
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    soup_head = soup.find("table").find('thead').find("tr").contents
    soup_row = soup.find("table").find('tbody').contents

    for row_index, row_value in enumerate(soup_row):
        if isinstance(row_value, Tag):
            row_value = row_value.find_all('td')

            detail_row_value = {}
            detail_row_value['id'] = row_index

            for head_index, head in enumerate(soup_head):
                try:
                    result.append(f'{row_value[0].get_text()}:{row_value[1].get_text()}')
                except: # Checkbox aka Select###All###Proxies
                    continue


async def main():
    result = []
    bs_urls = [
    'https://free-proxy-list.net/', 
    'https://www.sslproxies.org/', 
    'https://free-proxy-list.net/anonymous-proxy.html',
    'https://www.socks-proxy.net/',
    'https://www.us-proxy.org/',
    'https://free-proxy-list.net/uk-proxy.html', 
    'https://premproxy.com/socks-list/',
    'https://premproxy.com/list/'
    ]
    
    for bs_url in bs_urls:
        extract(bs_url, result)

    big = [
        'https://github.com/ShiftyTR/Proxy-List/raw/master/socks4.txt',
        'https://github.com/ShiftyTR/Proxy-List/raw/master/socks5.txt',
        'https://github.com/zevtyardt/proxy-list/raw/main/socks5.txt',
        'https://github.com/zevtyardt/proxy-list/raw/main/socks4.txt',
        'https://github.com/BlackSnowDot/proxylist-update-every-minute/raw/main/socks.txt',
        'https://github.com/hookzof/socks5_list/raw/master/proxy.txt',
        'https://github.com/manuGMG/proxy-365/raw/main/SOCKS5.txt',
        'https://github.com/andigwandi/free-proxy/raw/main/proxy_list.txt',
        'https://github.com/monosans/proxy-list/raw/main/proxies/socks5.txt',
        'https://github.com/monosans/proxy-list/raw/main/proxies/socks4.txt',
        'https://github.com/roosterkid/openproxylist/raw/main/SOCKS4_RAW.txt',
        'https://github.com/roosterkid/openproxylist/raw/main/SOCKS5_RAW.txt',
        'https://github.com/hanwayTech/free-proxy-list/raw/main/socks4.txt',
        'https://github.com/hanwayTech/free-proxy-list/raw/main/socks5.txt',
        'https://github.com/Zaeem20/FREE_PROXIES_LIST/raw/master/socks4.txt',
        'https://github.com/Zaeem20/FREE_PROXIES_LIST/raw/master/socks5.txt',
        'https://github.com/almroot/proxylist/raw/master/list.txt',
        'https://github.com/saschazesiger/Free-Proxies/raw/master/proxies/socks4.txt',
        'https://github.com/saschazesiger/Free-Proxies/raw/master/proxies/socks5.txt',
        'https://api.proxyscrape.com/?request=getproxies&proxytype=socks4',
        'https://www.proxy-list.download/api/v1/get?type=socks5',
        'https://api.proxyscrape.com/?request=getproxies&proxytype=socks5',

        'https://sunny9577.github.io/proxy-scraper/proxies.txt',
        'https://spys.one/',
        'https://api.proxyscrape.com/?request=getproxies&proxytype=https&timeout=10000&country=all&ssl=all&anonymity=all',
        'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/proxy.txt',
        'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all',
        'https://github.com/ShiftyTR/Proxy-List/raw/master/https.txt', 'https://github.com/ShiftyTR/Proxy-List/raw/master/http.txt', 'https://raw.githubusercontent.com/hanwayTech/free-proxy-list/main/http.txt', 'https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt', 'https://github.com/BlackSnowDot/proxylist-update-every-minute/raw/main/http.txt', 'https://github.com/BlackSnowDot/proxylist-update-every-minute/raw/main/https.txt', 'https://github.com/andigwandi/free-proxy/raw/main/proxy_list.txt', 'https://github.com/mertguvencli/http-proxy-list/raw/main/proxy-list/data.txt', 'http://alexa.lr2b.com/proxylist.txt', 'https://proxyspace.pro/https.txt', 'https://proxyspace.pro/http.txt', 'http://rootjazz.com/proxies/proxies.txt', 'https://raw.githubusercontent.com/almroot/proxylist/master/list.txt', 'https://raw.githubusercontent.com/aslisk/proxyhttps/main/https.txt', 'https://raw.githubusercontent.com/hanwayTech/free-proxy-list/main/http.txt', 'https://raw.githubusercontent.com/hanwayTech/free-proxy-list/main/https.txt', 'https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-Repo/master/proxy_list.txt', 'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt', 'https://raw.githubusercontent.com/jetkai/proxy-list/main/archive/txt/proxies-http.txt', 'https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt', 'https://raw.githubusercontent.com/mmpx12/proxy-list/master/https.txt', 'https://raw.githubusercontent.com/RX4096/proxy-list/main/online/http.txt', 'https://raw.githubusercontent.com/RX4096/proxy-list/main/online/https.txt', 'https://raw.githubusercontent.com/saisuiu/uiu/main/free.txt', 'https://raw.githubusercontent.com/yemixzy/proxy-list/main/proxy-list/data.txt', 'https://raw.githubusercontent.com/Zaeem20/FREE_PROXY_LIST/master/http.txt', 'https://raw.githubusercontent.com/Zaeem20/FREE_PROXY_LIST/master/https.txt', 'https://rootjazz.com/proxies/proxies.txt', 'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt', 'https://raw.githubusercontent.com/HyperBeats/proxy-list/main/http.txt', 'https://api.openproxylist.xyz/http.txt', 'https://www.proxyscan.io/download?type=http', 'https://www.proxyscan.io/download?type=https']
    for smol in big:
        await scrape(smol, result)
    await scrape('https://api.proxyscrape.com/?request=getproxies&proxytype=http', result)
    await scrape('https://spys.me/proxy.txt', result)
    await scrape('https://raw.githubusercontent.com/hendrikbgr/Free-Proxy-Repo/master/proxy_list.txt', result)
    await scrape('https://www.proxy-list.download/api/v1/get?type=http', result)
    await scrape('https://www.proxy-list.download/api/v1/get?type=https', result)
    await scrape('https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt', result)
    await scrape('https://proxy-daily.com/', result)
    await scrape('https://github.com/proxy4parsing/proxy-list/raw/main/http.txt', result)
    await scrape('https://github.com/rdavydov/proxy-list/raw/main/proxies/http.txt', result)
    await scrape('https://github.com/mmpx12/proxy-list/raw/master/http.txt', result)
    await scrape('https://github.com/mmpx12/proxy-list/raw/master/https.txt', result)
    await scrape('https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/premium.txt', result)
    await scrape('https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/working.txt', result)
    await scrape('https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/http.txt', result)
    await scrape('https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/ultrafast.txt', result)
    await scrape('https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/fast.txt', result)

    await startCP(result)

    new = list(OrderedDict.fromkeys(result))
    print('{0:2d} proxies scraped.'.format(len(new)))
    await save_result(result=new)
    return result


if __name__ == '__main__':  # no need to check it
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(main())
    loop.run_until_complete(asyncio.sleep(0.1))
    loop.close()
