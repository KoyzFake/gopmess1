import sys
import os
os.system('clear')
import requests
import threading
import time
import json,requests,time
from time import strftime
from pystyle import Colorate, Colors, Write, Add, Center

def codebydzi_banner():
    print(''' 
████████╗░█████╗░░█████╗░██╗░░░░░
╚══██╔══╝██╔══██╗██╔══██╗██║░░░░░
░░░██║░░░██║░░██║██║░░██║██║░░░░░
░░░██║░░░██║░░██║██║░░██║██║░░░░░
░░░██║░░░╚█████╔╝╚█████╔╝███████╗
░░░╚═╝░░░░╚════╝░░╚════╝░╚══════╝
BUFF SHARE FACEBOOK ĐA COOKIE
          ''')
t=("- - - - - - - - - - - - - - - - - - - - - - - - -")
print(t)
def codebydzi_clear():
    if(sys.platform.startswith('win')):
        os.system('cls')
    else:
        os.system('clear')
gome_token = []
def codebydzi_get_token(input_file):
    for cookie in input_file:
        header_ = {
            'authority': 'business.facebook.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
            'cache-control': 'max-age=0',
            'cookie': cookie,
            'referer': 'https://www.facebook.com/',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
        }
        try:
            home_business = requests.get('https://business.facebook.com/content_management', headers=header_).text
            token = home_business.split('EAAG')[1].split('","')[0]
            cookie_token = f'{cookie}|EAAG{token}'
            gome_token.append(cookie_token)
        except:
            pass
    return gome_token

def codebydzi_share(tach, id_share):
    cookie = tach.split('|')[0]
    token = tach.split('|')[1]
    he = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate',
        'connection': 'keep-alive',
        'content-length': '0',
        'cookie': cookie,
        'host': 'graph.facebook.com'
    }
    try:
        res = requests.post(f'https://graph.facebook.com/me/feed?link=https://m.facebook.com/{id_share}&published=0&access_token={token}', headers=he).json()
    except:
        pass
    
def codebydzi_main_share():
    codebydzi_clear()
    codebydzi_banner()
    input_file = open(input("[=.=] => Nhập tên file chứa Cookies: ")).read().split('\n')
    id_share = input("[=.=] => Nhập ID Cần Share: ")
    delay = int(input("[=.=] => Nhập Delay Share: "))
    total_share = int(input("[=.=] => Bao Nhiêu Share Thì Dừng Tool: "))
    all = codebydzi_get_token(input_file)
    total_live = len(all)
    print('────────────────────────────────────────────────────────────')
    if total_live == 0:
        sys.exit()
    stt = 0
    while True:
        for tach in all:
            stt = stt + 1
            threa = threading.Thread(target=codebydzi_share, args=(tach, id_share))
            threa.start()
            print(f'[{stt}] Share thành công bài viết {id_share} \n', end='\r')
            time.sleep(delay)
        if stt == total_share:
            break
    gome_token.clear()
    input('[SUCCESS] Đã Share Thành Công | Nhấn [Enter] Để Chạy Lại ')
while True:
    try:
        codebydzi_main_share()
    except KeyboardInterrupt:
        print('\n[!] Tạm Biệt User Nhé Hhi')
        sys.exit()
