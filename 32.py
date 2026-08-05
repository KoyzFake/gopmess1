# -*- coding: utf-8 -*-
import requests
import concurrent.futures
import time
import sys
import io
from datetime import datetime

# Fix encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# URL chua danh sach proxy
PROXY_URL = "https://proxy-gvjp.onrender.com/download/http.txt"

# Timeout cho viec kiem tra proxy (giay)
TIMEOUT = 10

# URL de test proxy
TEST_URL = "http://httpbin.org/ip"

# So luong kiem tra dong thoi
MAX_WORKERS = 50

# Gioi han so proxy kiem tra
MAX_PROXIES = 500


def fetch_proxies():
    """Lay danh sach proxy tu URL"""
    print(f"[*] Dang lay proxy tu: {PROXY_URL}")
    try:
        response = requests.get(PROXY_URL, timeout=30)
        response.raise_for_status()
        proxies = response.text.strip().split('\n')
        proxies = [p.strip() for p in proxies if p.strip()]
        print(f"[+] Tong cong co {len(proxies)} proxy")
        
        # Gioi han so luong proxy
        if len(proxies) > MAX_PROXIES:
            proxies = proxies[:MAX_PROXIES]
            print(f"[*] Chi kiem tra {MAX_PROXIES} proxy dau tien")
        
        return proxies
    except Exception as e:
        print(f"[-] Loi khi lay proxy: {e}")
        return []


def check_proxy(proxy):
    """Kiem tra mot proxy co hoat dong khong"""
    proxy_dict = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    }
    
    try:
        response = requests.get(
            TEST_URL,
            proxies=proxy_dict,
            timeout=TIMEOUT
        )
        if response.status_code == 200:
            return proxy, True
    except:
        pass
    
    return proxy, False


def check_all_proxies(proxies):
    """Kiem tra tat ca proxy voi da luong"""
    live_proxies = []
    dead_count = 0
    total = len(proxies)
    
    print(f"\n[*] Bat dau kiem tra {total} proxy voi {MAX_WORKERS} luong...")
    print("-" * 50)
    
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_proxy = {executor.submit(check_proxy, proxy): proxy for proxy in proxies}
        
        for i, future in enumerate(concurrent.futures.as_completed(future_to_proxy), 1):
            proxy, is_alive = future.result()
            
            if is_alive:
                live_proxies.append(proxy)
                print(f"[{i}/{total}] LIVE: {proxy}")
            else:
                dead_count += 1
                print(f"[{i}/{total}] DEAD: {proxy}")
    
    elapsed_time = time.time() - start_time
    
    print("-" * 50)
    print(f"\n[*] Hoan thanh trong {elapsed_time:.2f} giay")
    print(f"[+] Proxy song: {len(live_proxies)}")
    print(f"[-] Proxy chet: {dead_count}")
    
    return live_proxies


def save_live_proxies(live_proxies):
    """Luu proxy song vao file"""
    filename = "proxy_live.txt"
    
    with open(filename, 'w') as f:
        for proxy in live_proxies:
            f.write(proxy + '\n')
    
    print(f"\n[+] Da luu {len(live_proxies)} proxy song vao file: {filename}")


def main():
    print("=" * 50)
    print("       PROXY CHECKER - AUTO FETCH & CHECK")
    print("=" * 50)
    print(f"[*] Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[*] Gioi han: {MAX_PROXIES} proxy")
    print()
    
    # Lay proxy tu URL
    proxies = fetch_proxies()
    
    if not proxies:
        print("[-] Khong co proxy nao de kiem tra!")
        return
    
    # Kiem tra tat ca proxy
    live_proxies = check_all_proxies(proxies)
    
    # Luu proxy song vao file
    if live_proxies:
        save_live_proxies(live_proxies)
    else:
        print("\n[-] Khong co proxy nao song!")


if __name__ == "__main__":
    main()
