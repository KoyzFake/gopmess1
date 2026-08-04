import os
import re
import time
import requests
import pyfiglet
import threading
import random
import json
from termcolor import colored

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    text = """
  _    _  ____ _______  __          __     _____  
 | |  | |/ __ \__   __| \ \        / /\   |  __ \ 
 | |__| | |  | | | |     \ \  /\  / /  \  | |__) |
 |  __  | |  | | | |      \ \/  \/ / /\ \ |  _  / 
 | |  | | |__| | | |       \  /\  / ____ \| | \ \ 
 |_|  |_|\____/  |_|        \/  \/_/    \_\_|  \_\                                                                                                                                                                                     
    © BẢN QUYỀN DATK! SOURCE CODE PYTHON !!!              
--------------------------------------------------------"""

    start_rgb = (255, 105, 180)  
    end_rgb   = (30, 144, 255)   

    def rgb_to_ansi(r, g, b):
        return f"\033[38;2;{r};{g};{b}m"

    reset = "\033[0m"
    length = sum(1 for ch in text if ch.strip() != "")  
    out, i = "", 0

    for ch in text:
        if ch.strip() != "":
            ratio = i / length
            r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
            g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
            b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)
            out += rgb_to_ansi(r, g, b) + ch + reset
            i += 1
        else:
            out += ch
    print(out)

def pastel(r, g, b, text):
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

def get_uid(cookie):
    try:
        return re.search(r'c_user=(\d+)', cookie).group(1)
    except:
        return '0'

def get_fb_dtsg_jazoest(cookie, target_id):
    try:
        response = requests.get(
            f'https://mbasic.facebook.com/privacy/touch/block/confirm/?bid={target_id}',
            headers={ 'cookie': cookie, 'user-agent': 'Mozilla/5.0' }
        ).text
        fb_dtsg = re.search('name="fb_dtsg" value="([^"]+)"', response).group(1)
        jazoest = re.search('name="jazoest" value="([^"]+)"', response).group(1)
        return fb_dtsg, jazoest
    except:
        try:
            response = requests.get(
                'https://mbasic.facebook.com/home.php',
                headers={ 'cookie': cookie, 'user-agent': 'Mozilla/5.0' }
            ).text
            fb_dtsg = re.search('name="fb_dtsg" value="([^"]+)"', response)
            jazoest = re.search('name="jazoest" value="([^"]+)"', response)
            
            if fb_dtsg and jazoest:
                return fb_dtsg.group(1), jazoest.group(1)
            return None, None
        except:
            return None, None

def get_eaag_token(cookie):
    try:
        res = requests.get(
            'https://business.facebook.com/business_locations',
            headers={ 'cookie': cookie, 'user-agent': 'Mozilla/5.0' }
        )
        return re.search(r'EAAG\w+', res.text).group()
    except:
        return None

class Mention:
    def __init__(self, thread_id, offset, length):
        self.thread_id = thread_id
        self.offset = offset
        self.length = length

    def _to_send_data(self, i):
        return {
            f"profile_xmd[{i}][id]": self.thread_id,
            f"profile_xmd[{i}][offset]": self.offset,
            f"profile_xmd[{i}][length]": self.length,
            f"profile_xmd[{i}][type]": "p",
        }

def send_message_with_tags(idbox, fb_dtsg, jazoest, cookie, message_body, tag_ids, tag_names):
    try:
        uid = get_uid(cookie)
        timestamp = int(time.time() * 1000)
        
        tag_parts = []
        mentions = []
        offset = len(message_body) + 1 if message_body else 0
        
        for i in range(len(tag_ids)):
            name = tag_names[i] if i < len(tag_names) else f"User_{tag_ids[i][:4]}"
            tag_text = f"@{name}"
            tag_parts.append(tag_text)
            mention = Mention(thread_id=tag_ids[i], offset=offset, length=len(tag_text))
            mentions.append(mention)
            offset += len(tag_text) + 1
        
        full_message = f"{message_body} {' '.join(tag_parts)}".strip()
        
        data = {
            'thread_fbid': idbox,
            'action_type': 'ma-type:user-generated-message',
            'body': full_message,
            'client': 'mercury',
            'author': f'fbid:{uid}',
            'timestamp': timestamp,
            'offline_threading_id': str(timestamp),
            'message_id': str(timestamp),
            'source': 'source:chat:web',
            '__user': uid,
            '__a': '1',
            '__req': '1b',
            '__rev': '1015919737',
            'fb_dtsg': fb_dtsg,
            'jazoest': jazoest,
            'source_tags[0]': 'source:chat'
        }
        
        for idx, mention in enumerate(mentions):
            data.update(mention._to_send_data(idx))
        
        headers = {
            'Cookie': cookie,
            'User-Agent': 'Mozilla/5.0',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        response = requests.post('https://www.facebook.com/messaging/send/', data=data, headers=headers)
        return response.status_code == 200
    except Exception as e:
        print(f'Lỗi gửi tin nhắn với tag tới ID {idbox}: {e}')
        return False

def load_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        if not lines:
            raise Exception(f"File {file_path} trống!")
        return lines
    except Exception as e:
        raise Exception(f"Lỗi đọc file {file_path}: {str(e)}")

def check_live(cookie):
    try:
        if 'c_user=' not in cookie:
            return {"status": "failed", "msg": "Cookie không chứa user_id"}
        
        user_id = cookie.split('c_user=')[1].split(';')[0]
        headers = {
            'authority': 'm.facebook.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'vi-VN,vi;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': cookie,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        }
        profile_response = requests.get(f'https://m.facebook.com/profile.php?id={user_id}', headers=headers, timeout=30)
        name = profile_response.text.split('<title>')[1].split('<')[0].strip()
        return {
            "status": "success",
            "name": name,
            "user_id": user_id,
            "msg": "successful"
        }
    except Exception as e:
        return {"status": "failed", "msg": f"Lỗi xảy ra: {str(e)}"}

def auto_worker(cookie_data, id_list, message_list, base_delay, tag_ids, tag_names):
    cookie = cookie_data['cookie']
    account_name = cookie_data['name']
    index = 0
    while True:
        try:
            fb_dtsg, jazoest = get_fb_dtsg_jazoest(cookie, id_list[0])
            if not fb_dtsg or not jazoest:
                print(f"[{account_name}] Không lấy được fb_dtsg/jazoest")
                time.sleep(60)
                continue

            for idbox in id_list:
                message_body = message_list[index]
                if "{name}" in message_body and replace_text:
                    message_body = message_body.replace("{name}", replace_text)
                
                success = False
                if tag_ids:
                    success = send_message_with_tags(idbox, fb_dtsg, jazoest, cookie, message_body, tag_ids, tag_names)
                else:
                    try:
                        uid = get_uid(cookie)
                        timestamp = int(time.time() * 1000)
                        data = {
                            'thread_fbid': idbox,
                            'action_type': 'ma-type:user-generated-message',
                            'body': message_body,
                            'client': 'mercury',
                            'author': f'fbid:{uid}',
                            'timestamp': timestamp,
                            'offline_threading_id': str(timestamp),
                            'message_id': str(timestamp),
                            'source': 'source:chat:web',
                            '__user': uid,
                            '__a': '1',
                            '__req': '1b',
                            '__rev': '1015919737',
                            'fb_dtsg': fb_dtsg,
                            'jazoest': jazoest
                        }
                        headers = {
                            'Cookie': cookie,
                            'User-Agent': 'Mozilla/5.0',
                            'Content-Type': 'application/x-www-form-urlencoded'
                        }
                        response = requests.post('https://www.facebook.com/messaging/send/', data=data, headers=headers)
                        success = response.status_code == 200
                    except Exception as e:
                        print(f'[{account_name}] Lỗi gửi tới ID {idbox}: {e}')
                        success = False
                
                if success:
                    tag_info = f" với {len(tag_ids)} tag" if tag_ids else ""
                    print(f"[{account_name}] ✓ Gửi tin nhắn thành công tới: {idbox}{tag_info}")
                else:
                    print(f"[{account_name}] ✗ Gửi tin nhắn thất bại tới: {idbox}")
                
                index = (index + 1) % len(message_list)
                delay = base_delay + random.uniform(-0.5, 0.5)
                if delay < 0:
                    delay = 0
                time.sleep(delay)
        except Exception as err:
            print(f"[{account_name}] Lỗi không xác định: {err}")
            time.sleep(60)

def nhay_mess():
    clear()
    banner()
    
    # Nhập danh sách cookie
    cookie_list = []
    print(colored("\n=== NHẬP DANH SÁCH COOKIE ===", 'yellow', attrs=['bold']))
    while True:
        ck = input(colored("=> Nhập cookie (Hoặc ấn 'enter' để dừng): ", 'cyan', attrs=['bold'])).strip()
        if ck == "":
            break
        if 'c_user=' in ck and 'xs=' in ck:
            check = check_live(ck)
            if check["status"] == "success":
                print(colored(f"  ✓ {check['name']} (ID: {check['user_id']}) - Cookie sống!", 'green'))
                cookie_list.append(ck)
            else:
                print(colored(f"  ✗ Cookie không hợp lệ: {check['msg']}", 'red'))
        else:
            print(colored("  ✗ Cookie không đúng định dạng!", 'red'))
    
    if not cookie_list:
        print(colored("Không có cookie hợp lệ để chạy!", 'red'))
        return
    
    # Nhập danh sách ID Box
    id_list = []
    print(colored("\n=== NHẬP DANH SÁCH ID BOX ===", 'yellow', attrs=['bold']))
    while True:
        idbox = input(colored("=> Nhập ID Box (Hoặc ấn 'enter' để dừng): ", 'cyan', attrs=['bold'])).strip()
        if idbox == "":
            break
        if idbox.isdigit():
            id_list.append(idbox)
            print(colored(f"  Đã thêm ID: {idbox}", 'green'))
        else:
            print(colored("  ✗ ID phải là số!", 'red'))
    
    if not id_list:
        print(colored("Không có ID Box nào được nhập!", 'red'))
        return
    
    # NHẬP DANH SÁCH ID CẦN TAG (ĐƠN GIẢN)
    tag_ids = []
    tag_names = []
    print(colored("\n=== NHẬP DANH SÁCH ID CẦN TAG ===", 'yellow', attrs=['bold']))
    print(colored("Nhập ID cần tag (giống như nhập ID Box)", 'magenta'))
    print(colored("Enter để bỏ qua không tag", 'magenta'))
    while True:
        tag_id = input(colored("=> Nhập ID cần tag (Hoặc ấn 'enter' để dừng): ", 'cyan', attrs=['bold'])).strip()
        if tag_id == "":
            break
        if tag_id.isdigit():
            tag_ids.append(tag_id)
            print(colored(f"  Đã thêm ID tag: {tag_id}", 'green'))
        else:
            print(colored("  ✗ ID phải là số!", 'red'))
    
    # NHẬP TÊN TƯƠNG ỨNG CHO TAG
    if tag_ids:
        print(colored("\n=== NHẬP TÊN TƯƠNG ỨNG CHO TAG ===", 'yellow', attrs=['bold']))
        print(colored(f"Có {len(tag_ids)} ID cần tag.", 'magenta'))
        print(colored("Nhập tên tương ứng (cách nhau bằng dấu phẩy), hoặc Enter để dùng tên mặc định:", 'magenta'))
        
        names_input = input(colored("=> Nhập tên: ", 'cyan', attrs=['bold'])).strip()
        if names_input:
            names = [name.strip() for name in names_input.split(',')]
            if len(names) == len(tag_ids):
                tag_names = names
            elif len(names) < len(tag_ids):
                tag_names = names + [f"User_{tag_ids[i][:4]}" for i in range(len(names), len(tag_ids))]
            else:
                tag_names = names[:len(tag_ids)]
            print(colored(f"  Đã thiết lập {len(tag_names)} tên tag", 'green'))
        else:
            tag_names = [f"User_{tag_id[:4]}" for tag_id in tag_ids]
            print(colored(f"  Đã dùng tên mặc định cho {len(tag_ids)} tag", 'green'))

    print(colored("\n=== NHẬP FILE NỘI DUNG ===", 'yellow', attrs=['bold']))
    while True:
        name_file = input(colored("=> Nhập file ngôn [ví dụ file.txt]: ", 'cyan', attrs=['bold'])).strip()
        if name_file:
            try:
                with open(name_file, 'r', encoding='utf-8') as file:
                    message_list = [line.strip() for line in file if line.strip()]
                if not message_list:
                    print(colored(f"  ✗ File {name_file} trống!", 'red'))
                else:
                    print(colored(f"  ✓ Đã tải {len(message_list)} dòng từ {name_file}", 'green'))
                    break
            except Exception as e:
                print(colored(f"  ✗ Lỗi đọc file: {e}", 'red'))
        else:
            print(colored("  ✗ Vui lòng nhập tên file!", 'red'))

    print(colored("\n=== CÀI ĐẶT DELAY ===", 'yellow', attrs=['bold']))
    while True:
        try:
            base_delay = int(input(colored('=> Nhập delay (giây): ', 'cyan', attrs=['bold'])))
            if base_delay < 1:
                print(colored("  ✗ Delay phải lớn hơn 0!", 'red'))
            else:
                break
        except ValueError:
            print(colored("  ✗ Vui lòng nhập số!", 'red'))
    
    user_data_list = []
    print(colored("\n=== ĐANG LẤY THÔNG TIN TÀI KHOẢN ===", 'yellow', attrs=['bold']))
    for index, ck in enumerate(cookie_list, 1):
        try:
            uid = get_uid(ck)
            token = get_eaag_token(ck)

            if token:
                try:
                    res = requests.get(
                        f'https://graph.facebook.com/{uid}?fields=name&access_token={token}',
                        headers={'cookie': ck, 'user-agent': 'Mozilla/5.0'},
                        timeout=10
                    ).json()
                    name = res.get('name', f'User_{index}')
                except:
                    name = f'User_{index}'
            else:
                name = f'User_{index}'

            user_data_list.append({'name': name, 'id': uid, 'cookie': ck})
            print(colored(f"  [{index}] {name} (ID: {uid})", 'green'))
        except Exception as e:
            print(colored(f"  [{index}] Lỗi lấy thông tin: {e}", 'red'))
            user_data_list.append({'name': f'User_{index}', 'id': '0', 'cookie': ck})
    
    if not user_data_list:
        print(colored("Không có cookie hợp lệ để chạy", 'red'))
        return
    
    print(colored("\n=== THÔNG TIN CẤU HÌNH ===", 'yellow', attrs=['bold']))
    print(colored(f"Số tài khoản: {len(user_data_list)}", 'cyan'))
    print(colored(f"Số ID Box: {len(id_list)}", 'cyan'))
    print(colored(f"Số tin nhắn: {len(message_list)}", 'cyan'))
    if tag_ids:
        print(colored(f"Số tag: {len(tag_ids)}", 'cyan'))

    print(colored(f"Delay: {base_delay} giây", 'cyan'))
    
    print(colored("\n=== KHỞI ĐỘNG TOOL ===", 'yellow', attrs=['bold']))
    for data in user_data_list:
        thread = threading.Thread(
            target=auto_worker, 
            args=(data, id_list, message_list, base_delay, tag_ids, tag_names), 
            daemon=True
        )
        thread.start()
        print(colored(f"  Đã khởi động bot cho: {data['name']}", 'green'))
        time.sleep(0.5)
    
    print(pastel(173, 216, 230, "\n☘️ 𝘊𝘵𝘦𝘝𝘤𝘭 𝘍𝘰𝘳𝘦𝘷𝘦𝘳"))
    print(colored("=== 🚀 BẮT ĐẦU TRIỂN KHAI SPAM ===", 'green', attrs=['bold']))
    if tag_ids:
        print(colored(f"⚡ Chế độ: SPAM với TAG ({len(tag_ids)} người được tag)", 'yellow', attrs=['bold']))
    else:
        print(colored("⚡ Chế độ: SPAM thông thường", 'yellow', attrs=['bold']))
    print(colored("Nhấn Ctrl+C để dừng chương trình", 'red', attrs=['bold']))
    
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print(pastel(255, 182, 193, "\n👋 Goodbye! Đang dừng tất cả bot..."))
        os._exit(0)

if __name__ == '__main__':
    nhay_mess()
