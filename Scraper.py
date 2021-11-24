from requests_html import AsyncHTMLSession
import asyncio
import time
import pandas as pd
import socket
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import ssl
from bs4 import BeautifulSoup

with open('DIN_first1m.txt', 'r') as file:
    dins = file.read().splitlines()

cookies = {
    'cookiesession1': '678B2874QRSTUVWXYZCDEFHIJKLMCC68',
    'JSESSIONID': '0000ZGKBt5sYWirUgsgcYVm5MNU:1aevghkom',
}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Upgrade-Insecure-Requests': '1',
    'Origin': 'https://mca.gov.in',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://mca.gov.in/mcafoportal/viewCompanyMasterData.do',
    'Accept-Language': 'en-US,en;q=0.9',
}

async def grab(s, din):
    data = {
      'directorName': '',
      'din': din,
      'displayCaptcha': 'false'
    }
    try:
        r = await s.post('https://mca.gov.in/mcafoportal/showdirectorMasterData.do', headers=headers, data=data, cookies=cookies, timeout=(0.5, 3.0), verify=False)
        print(din)
        soup = BeautifulSoup(r.text,'html.parser')
        error = soup.select_one('ul.errorMessage')
        if error:
            failed = open('Not Found.txt', 'a')
            failed.write(din+'\n')
            failed.close()
        else:
            din = str(din)
            info = pd.read_html(r.text)[1]
            info.insert(0, "DIN", din, allow_duplicates=False)
            info.to_csv('Directors Info.csv', mode='a', index=False, header=False)
    except Exception as e:
        with open('Failed.txt', 'a') as file:
            file.write(din+'\n')

async def main(dins):
    s = AsyncHTMLSession()
    tasks = (grab(s, din) for din in dins)
    return await asyncio.gather(*tasks)

start = time.time()
asyncio.run(main(dins))
print(time.time()-start)
