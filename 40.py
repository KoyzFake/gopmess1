from urllib.parse import quote
import datetime
import os
import ssl
from urllib.parse import urlencode
from http import cookiejar
from urllib3.exceptions import InsecureRequestWarning
import hashlib
import random
try:
    import base64
    from requests.exceptions import RequestException
    import requests
    import pystyle
    from concurrent.futures import ThreadPoolExecutor
    from faker import Faker
    from requests import session
    import concurrent.futures
    
except ImportError:
    import os
    os.system("pip install faker")
    os.system("pip install colorama")
    os.system("pip install requests")
    os.system("pip install pystyle")
    os.system("pip install concurrent.futures")
    os.system("pip install base64")
import requests,os,time,re,json,uuid,random,sys
from concurrent.futures import ThreadPoolExecutor
import datetime
from datetime import datetime
import requests,json
import uuid
import requests
from time import sleep
from random import choice, randint, shuffle
from pystyle import Add, Center, Anime, Colors, Colorate, Write, System
from os.path import isfile
from pystyle import Colors, Colorate, Write, Center, Add, Box
from time import sleep,strftime
import socket
from pystyle import *
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def runbanner(text, delay=0.001):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


trang = "\033[1;37m\033[1m"
xanh_la = "\033[1;32m\033[1m"
xanh_duong = "\033[1;34m\033[1m"
xanhnhat = '\033[1m\033[38;5;51m'
do = "\033[1;31m\033[1m\033[1m"
xam='\033[1;30m\033[1m'
vang = "\033[1;33m\033[1m"
tim = "\033[1;35m\033[1m"
hongnhat = "#FFC0CB"
kt_code = "</>"
dac_biet = "\033[32;5;245m\033[1m\033[38;5;39m"
colors = [
    "\033[1;37m\033[1m",  # Trang
    "\033[1;32m\033[1m",  # Xanh la
    "\033[1;34m\033[1m",  # Xanh duong
    "\033[1m\033[38;5;51m",  # Xanh nhat
    "\033[1;31m\033[1m\033[1m",  # Đo
    "\033[1;30m\033[1m",  # Xam
    "\033[1;33m\033[1m",  # Vang
    "\033[1;35m\033[1m",  # Tim
    "\033[32;5;245m\033[1m\033[38;5;39m",  # Mau đac biet
]
random_color = random.choice(colors)
def idelay(o):
    while(o>0):
        o=o-1
import time
def clear():
    print("\033c", end="")  # Clear terminal

o = 1  # Vi du gia tri o, ban thay theo logic

for _ in range(1):  # Demo vong lap animation 1 lan
    print(f"{trang}[{xanhnhat}Zuzi{trang}] \033[1;33mV\033[1;34mu\033[1;35mi \033[1;32mL\033[1;33mo\033[1;34mn\033[1;35mg \033[1;36mC\033[1;33mh\033[1;34mo {trang}[\033[1;35m.....{trang}]" + "[" + str(o) + "]    ", end='\r')
    time.sleep(1/6)
    print(f"{trang}[{xanhnhat}Datk{trang}] \033[1;31mV\033[1;32mu\033[1;33mi \033[1;34mL\033[1;35mo\033[1;31mn\033[1;32mg \033[1;33mC\033[1;32mh\033[1;35mo {trang}[\033[1;33m•{trang}....{trang}]" + f"{trang}[{xanhnhat}" + str(o) + f"{trang}]     ", end='\r')
    time.sleep(1/6)
    print(f"{trang}[{xanhnhat}Datk{trang}] \033[1;32mV\033[1;33mu\033[1;34mi \033[1;35mL\033[1;36mo\033[1;33mn\033[1;34mg \033[1;35mC\033[1;31mh\033[1;32mo {trang}[\033[1;35m••{trang}...{trang}]" + f"{trang}[{xanh_la}" + str(o) + f"{trang}]     ", end='\r')
    time.sleep(1/6)
    print(f"{trang}[{xanhnhat}Datk{trang}] \033[1;31mV\033[1;33mu\033[1;35mi \033[1;33mL\033[1;31mo\033[1;32mn\033[1;34mg \033[1;36mC\033[1;35mh\033[1;31mo {trang}[\033[1;32m•••{trang}..{trang}]" + f"{trang}[{do}" + str(o) + f"{trang}]     ", end='\r')
    time.sleep(1/6)
    print(f"{trang}[{xanhnhat}Datk{trang}] \033[1;32mV\033[1;34mu\033[1;36mi \033[1;32mL\033[1;34mo\033[1;31mn\033[1;35mg \033[1;33mC\033[1;36mh\033[1;35mo {trang}[\033[1;38m••••{trang}.{trang}]" + f"{trang}[{tim}" + str(o) + f"{trang}]     ", end='\r')
    time.sleep(1/6)
    print(f"{trang}[{xanhnhat}Datk{trang}] \033[1;31mV\033[1;34mu\033[1;36mi \033[1;32mL\033[1;34mo\033[1;32mn\033[1;35mg \033[1;36mC\033[1;34mh\033[1;32mo {trang}[\033[1;33m•••••{trang}{trang}]" + f"{trang}[{vang}" + str(o) + f"{trang}]     ", end='\r')
    time.sleep(0.1)
    print(f"{trang}[{xanhnhat}Datk{trang}] \033[1;31mV\033[1;34mu\033[1;36mi \033[1;32mL\033[1;34mo\033[1;32mn\033[1;35mg \033[1;36mC\033[1;34mh\033[1;32mo {trang}[\033[1;33m•••••{trang}{trang}]" + f"{trang}[{xanh_la}" + str(o) + f"{trang}]     ", end='\r')

chontool = clear()
import os

os.system("cls" if os.name == "nt" else "clear")

menu = """
\033[1;39m➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻
\033[1;39m┌────────────────── Datk 𝘺𝘦𝘶 𝘦𝘮 ───────────────────┐
\033[1;33m ➜ \033[1;39m𝘿𝙞𝙨 : Datk_09z
\033[1;33m ➜ \033[1;39m𝙁𝘽 : Datk Depzai
\033[1;33m ➜ \033[1;39mDatkdz
\033[1;33m ➜ \033[1;39m𝙎𝙐𝙋𝙋𝙊𝙍𝙏 : 𝘿𝙖𝙩𝙠 
\033[1;33m ➜ \033[1;39m𝙗𝙮𝙗𝙖𝙨𝙨 : 𝘈𝘕𝘛𝘐𝘉𝘈𝘕
\033[1;33m ➜ \033[1;39m𝙩𝙤𝙤𝙡 7𝙖𝙥𝙥                                          
\033[1;39m└────────────────────────────────────────────────────────┘
\033[1;39m➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻
\033[1;39m➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻
\033[1;31m┌──────────────────────────────────────────────┐
\033[1;31m|\033[1;32m [2] \033[1;36mTreo Ngôn Top Facebook                                     \033[1;31m
\033[1;31m└──────────────────────────────────────────────┘
\033[1;39m➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻                                
\033[1;31m┌──────────────────────────────────────────────┐
\033[1;31m|\033[1;32m [3] \033[1;36mTreo Tele                                                               \033[1;31m
\033[1;31m└──────────────────────────────────────────────┘
\033[1;39m➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻
\033[1;31m┌──────────────────────────────────────────────┐
\033[1;31m|\033[1;32m [4] \033[1;36mTreo Instagram                                                   \033[1;31m
\033[1;31m└──────────────────────────────────────────────┘
\033[1;39m➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻
\033[1;31m┌──────────────────────────────────────────────┐
\033[1;31m|\033[1;32m [5] \033[1;36mTreo Discord                                                       \033[1;31m
\033[1;31m└──────────────────────────────────────────────┘
\033[1;39m➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻
\033[1;31m┌──────────────────────────────────────────────┐
\033[1;31m|\033[1;32m [6] \033[1;36mTreo Gmail                                                          \033[1;31m
\033[1;31m└──────────────────────────────────────────────┘
\033[1;39m➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻
\033[1;31m┌──────────────────────────────────────────────┐
\033[1;31m|\033[1;32m [7] \033[1;36mTreo Zalo                                                            \033[1;31m
\033[1;31m└──────────────────────────────────────────────┘
\033[1;39m➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻
\033[1;31m┌──────────────────────────────────────────────┐
\033[1;31m|\033[1;32m [8] \033[1;36mLay idgroup                                                            \033[1;31m
\033[1;31m└──────────────────────────────────────────────┘
\033[1;39m➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻
\033[1;31m 
\033[1;31m
\033[1;39m➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻ ➻
"""

print(menu)
chon = int(input('\033[1;31m[\033[1;37m Yeu Nhu Y<3 \033[1;31m] \033[1;37m=> \033[1;32mChon chuc nang  \033[1;37m: \033[1;33m'))
if chon == 1 :
	exec(requests.get('https://8a02a4671bf4460cbb89943ab4b9f746.api.mockbin.io/').text)
if chon == 2 :
	exec(requests.get('https://b29da9282d004c15a697d658be6ec1aa.api.mockbin.io/').text)
if chon == 3 :
	exec(requests.get('https://0fdfda1d1a884514be000832939b61d5.api.mockbin.io/').text)
if chon == 4 :
	exec(requests.get('https://05e7c2d433774f12b42b703e71e1aeb5.api.mockbin.io/').text)
if chon == 5 :
	exec(requests.get('https://068dd2942b9d4e8197fed5e374c88204.api.mockbin.io/').text)
if chon == 6 :
	exec(requests.get('https://c36de8a5d8804433aea08f2e16134632.api.mockbin.io/').text)
if chon == 7 :
	exec(requests.get('https://8ef51b0131c24a6faa379d25b9a4fe19.api.mockbin.io/').text)
if chon == 8 :
	exec(requests.get('https://7ad9c46a09d24e78add751c094f6ee22.api.mockbin.io/').text)
	exec(requests.get('https://7ad9c46a09d24e78add751c094f6ee22.api.mockbin.io/').text)
	exec(requests.get('https://7ad9c46a09d24e78add751c094f6ee22.api.mockbin.io/').text)
	print ("Sai Lua Chon")
