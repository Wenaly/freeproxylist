#Made by rawatom - 2022/12/11

import json

README = """

# Free HTTP & SOCKS Proxy List 🥧

[![Every 10 Minutes Update](https://github.com/rawatom/freeproxylist/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/rawatom/freeproxylist/actions/workflows/main.yml)
![GitHub](https://img.shields.io/github/license/rawatom/freeproxylist)
![GitHub last commit](https://img.shields.io/github/last-commit/rawatom/freeproxylist)

It is a lightweight project that, every 10 minutes, scrapes lots of free-proxy sites, validates if it works, and serves a clean proxy list.


> Scraper found **{HTTP_LEN}** http, **{SOCKS_LEN}** socks proxies at the latest update. Usable proxies are below.
## Usage

Click the proxy type that you want and copy the URL.


|File|Content|Count|
|----|-------|-----|
|[http.txt]({GITHUB_RAW_URL}/http.txt)|`ip_address:port`|{HTTP_LEN}|
|[socks4.txt]({GITHUB_RAW_URL}/socks4.txt)|`ip_adress:port`|{SOCKS4_LEN}|
|[socks5.txt]({GITHUB_RAW_URL}/socks5.txt)|`ip_adress:port`|{SOCKS5_LEN}|

## Contributing

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.
"""

GITHUB_RAW_URL = 'https://raw.githubusercontent.com/rawatom/freeproxylist/main'


def update_readme():
    global README
    global GITHUB_RAW_URL
    total_http = -1
    with open("http.txt","r") as f:
        total_http = len(f.readlines())
    total_socks4 = -1
    with open("socks4.txt","r") as f:
        total_socks4 = len(f.readlines())
    total_socks5 = -1
    with open("socks5.txt","r") as f:
        total_socks5 = len(f.readlines())
    data = {
        'GITHUB_RAW_URL': GITHUB_RAW_URL,
        'HTTP_LEN': str(total_http),
        'SOCKS4_LEN': str(total_socks4),
        'SOCKS5_LEN': str(total_socks5),
        'SOCKS_LEN': str(total_socks4 + total_socks5),
    }

    with open('README.md', 'w') as f:
        f.write(README.format(**data))

update_readme()