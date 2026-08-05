import requests
import threading
import time
import os
import random

class GuiTinNhan:
    def __init__(self):
        self.tokens = []
        self.delays = {}
        self.kenh_id = ""
        self.nguoi_tag = []
        self.tin_nhan = []
        self.chi_so_tn = 0
        self.lock = threading.Lock()
        self.fake_typing_enabled = False
    
    def doc_token(self):
        while True:
            file_token = input("Nhap file chua token: ").strip()
            if os.path.exists(file_token):
                with open(file_token, 'r', encoding='utf-8') as f:
                    self.tokens = [line.strip() for line in f if line.strip()]
                break
            print("File khong ton tai")
    
    def nhap_delay(self):
        for token in self.tokens:
            token_hien = token[:4] + "..." + token[-4:]
            while True:
                try:
                    delay = float(input(f"Token {token_hien} > Delay: "))
                    self.delays[token] = delay
                    break
                except:
                    print("Nhap so")
    
    def nhap_kenh(self):
        self.kenh_id = input("Nhap ID kenh: ").strip()
    
    def nhap_tag(self):
        print("Nhap ID nguoi tag (done de dung hoac bo qua):")
        while True:
            user_id = input().strip()
            if user_id.lower() == 'done' or user_id == '':
                break
            self.nguoi_tag.append(f"<@{user_id}>")
    
    def hoi_fake_typing(self):
        while True:
            choice = input("Ban co muon fake typing? (y/n): ").strip().lower()
            if choice in ['y', 'yes']:
                self.fake_typing_enabled = True
                break
            elif choice in ['n', 'no']:
                self.fake_typing_enabled = False
                break
    
    def doc_tin_nhan(self):
        file_tn = "nhay.txt"
        if os.path.exists(file_tn):
            with open(file_tn, 'r', encoding='utf-8') as f:
                self.tin_nhan = [line.strip() for line in f if line.strip()]
        else:
            print("File nhay.txt khong ton tai")
            exit()
    
    def lay_tin_nhan(self):
        with self.lock:
            if not self.tin_nhan:
                return "# Hello"
            
            tin = self.tin_nhan[self.chi_so_tn]
            self.chi_so_tn = (self.chi_so_tn + 1) % len(self.tin_nhan)
            
            if not tin.startswith('#'):
                tin = f"# {tin}"
            
            if self.nguoi_tag:
                tags = " ".join(self.nguoi_tag)
                if random.choice([True, False]):
                    tin = f"{tin} {tags}"
                else:
                    tin = tin.replace("# ", f"# {tags} ", 1)
            
            return tin
    
    def tao_headers(self, token):
        return {
            'Authorization': token,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }
    
    def fake_typing(self, token):
        if not self.fake_typing_enabled:
            return
        headers = self.tao_headers(token)
        try:
            requests.post(f'https://discord.com/api/v9/channels/{self.kenh_id}/typing', 
                         headers=headers, timeout=10)
        except:
            pass
    
    def lay_ten_kenh(self, token, headers):
        try:
            response = requests.get(f'https://discord.com/api/v9/channels/{self.kenh_id}', 
                                  headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json().get('name', 'Unknown')
        except:
            pass
        return 'Unknown'
    
    def gui_tin(self, token):
        token_hien = token[:4] + "..." + token[-4:]
        delay = self.delays[token]
        headers = self.tao_headers(token)
        ten_kenh_cache = None
        
        while True:
            if self.fake_typing_enabled:
                self.fake_typing(token)
            
            time.sleep(delay)
            
            tin = self.lay_tin_nhan()
            data = {'content': tin}
            
            retry_count = 0
            max_retries = 3
            
            while retry_count < max_retries:
                try:
                    response = requests.post(
                        f'https://discord.com/api/v9/channels/{self.kenh_id}/messages',
                        headers=headers,
                        json=data,
                        timeout=15
                    )
                    
                    if response.status_code == 200:
                        if ten_kenh_cache is None:
                            ten_kenh_cache = self.lay_ten_kenh(token, headers)
                        print(f"Token {token_hien} > Success > Kenh: {ten_kenh_cache}")
                        break
                    elif response.status_code == 429:
                        try:
                            retry_after = response.json().get('retry_after', 1)
                            time.sleep(retry_after)
                            retry_count += 1
                            continue
                        except:
                            time.sleep(1)
                            retry_count += 1
                            continue
                    elif response.status_code == 401:
                        print(f"Token {token_hien} > Token invalid")
                        return
                    elif response.status_code == 403:
                        print(f"Token {token_hien} > Khong co quyen")
                        break
                    elif response.status_code == 404:
                        print(f"Token {token_hien} > Kenh khong ton tai")
                        return
                    else:
                        print(f"Token {token_hien} > Loi {response.status_code}")
                        break
                        
                except requests.exceptions.Timeout:
                    print(f"Token {token_hien} > Timeout")
                    retry_count += 1
                except requests.exceptions.ConnectionError:
                    print(f"Token {token_hien} > Loi ket noi")
                    retry_count += 1
                except Exception as e:
                    print(f"Token {token_hien} > Loi: {str(e)[:50]}")
                    break
                
                if retry_count < max_retries:
                    time.sleep(1)
            
            if retry_count >= max_retries:
                print(f"Token {token_hien} > Het lan thu")
    
    def chay(self):
        print("LỒN MÁ HOT NHÂY BẬT TOOL")
        print("-" * 30)
        
        self.doc_token()
        self.nhap_kenh()
        self.nhap_tag()
        self.hoi_fake_typing()
        self.doc_tin_nhan()
        self.nhap_delay()
        
        print("Bat dau gui...")
        
        threads = []
        for token in self.tokens:
            thread = threading.Thread(target=self.gui_tin, args=(token,))
            thread.daemon = True
            thread.start()
            threads.append(thread)
        
        try:
            for thread in threads:
                thread.join()
        except KeyboardInterrupt:
            print("\nDang dung...")

if __name__ == "__main__":
    app = GuiTinNhan()
    app.chay()
