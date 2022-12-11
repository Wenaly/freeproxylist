import threading
import requests

def checker(p):     
    headers = {
         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
     }
    try:
        proxy = {"http": f"http://{p}", "https": f"http://{p}"}
        res = requests.get('https://open.spotify.com/artist/0OjAaymO59uGiFmfpJrQpl', proxies= proxy, timeout= 2, headers= headers)
        if res.status_code == 200:   
            http_live.append(p)
    except:
        try:
            proxy = {"http": f"socks4://{p}", "https": f"socks4://{p}"}
            res = requests.get('https://open.spotify.com/artist/0OjAaymO59uGiFmfpJrQpl', proxies= proxy, timeout= 2, headers= headers)
            if res.status_code == 200:   
                socks4_live.append(p)
        except:
            try:
                proxy = {"http": f"socks5://{p}", "https": f"socks5://{p}"}
                res = requests.get('https://open.spotify.com/artist/0OjAaymO59uGiFmfpJrQpl', proxies= proxy, timeout= 2, headers= headers)
                if res.status_code == 200:   
                    socks5_live.append(p)
            except:
                pass
            pass
        pass

def save_result(mode, live:list):
    with open(f'{mode}.txt', 'w') as file:
        for proxy in live:
            if proxy:
                file.write(proxy + '\n')
http_live = []
socks4_live = []
socks5_live = []
thread = []
with open('not-checked.txt') as file:
    for line in file:
        line = line.strip()
        t = threading.Thread(target=checker, args=(line))
        t.start()
        thread.append(t)
    for j in thread:
        j.join() 
    print('Saved live proxies.')
    save_result('http', http_live)
    save_result('socks4', socks4_live)
    save_result('socks4', socks5_live)
