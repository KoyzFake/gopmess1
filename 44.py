import smtplib
import time
import os
import requests
import random
import json
import sys
import webbrowser
from datetime import datetime
from colorama import init, Fore, Back, Style
import itertools
import threading
import re
from urllib.parse import urlparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import hashlib
import uuid

init(autoreset=True)

treo_tabs = {}
treo_history = []

def check_key_system():
    try:
        current_time = datetime.now().timestamp()
        
        print(f"\n{Fore.CYAN}╔{'═' * 50}╗")
        print(f"{Fore.CYAN}║{Fore.YELLOW}{'DATK ĐẸP TRAI VÃI L'.center(50)}{Fore.CYAN}║")
        print(f"{Fore.CYAN}╠{'═' * 50}╣{Fore.RESET}")
        
        input_key = input(f"{Fore.GREEN}🔑 Nhập key vô tool: {Fore.WHITE}").strip()
        
        
      
        valid_keys = {
            # Format: key : [expiry_timestamp]
            "HIGGANG2024": [9999],
            "VIP001": [1],
            "ADMIN999": [2],
            "TEST001": [1]
        }
        
        hidden_keys = {
            "Datkdz": [999999999999999] ,
            "hwducanh": [99999999999999999],
            "condimemaylungu": [99999999999999]
        }
        
        
        if input_key in valid_keys:
            expiry = valid_keys[input_key][0]
            
            
            if current_time > expiry:
                return False, "KEY HẾT HẠN RỒI"
            
            return True, "ZÔ"
        
        elif input_key in hidden_keys:
            expiry = hidden_keys[input_key][0]
            
            if current_time > expiry:
                return False, "Key Hết Hạn Rồi Tk Lồn"
            
            return True, "CON CẶC"
        
        else:
            return False, "Key không hợp lệ"
            
    except Exception as e:
        return False, f"Lỗi hệ thống: {str(e)}"


def get_token(cookie):
    try:
        r = requests.get(f"https://adidaphat.site/facebook/tokentocookie?type=EAAD6V7&cookie={cookie}")
        return r.json().get("token")
    except: return None

def save_config(mode,cfg):
    try:
        data = json.load(open("chnd.txt","r",encoding="utf-8")) if os.path.exists("chnd.txt") else {}
        data[mode]=cfg
        json.dump(data,open("chnd.txt","w",encoding="utf-8"),ensure_ascii=False,indent=2)
    except: pass

def load_config(mode):
    try:
        if os.path.exists("chnd.txt"):
            return json.load(open("chnd.txt","r",encoding="utf-8")).get(mode,{})
        return {}
    except: return {}

def input_with_done(p):
    print(f"{Fore.CYAN}[⚜️] ➜ {p} (gõ 'done' để xong){Fore.RESET}")
    lines=[]
    while True:
        try: line=input("➜ ").strip()
        except: return None
        if line.lower()=="done": break
        if line: lines.append(line)
    return "\n".join(lines) if lines else None

def first_line(m): return next((x.strip() for x in (m or "").splitlines() if x.strip()), None)
def list_from(m): return [x.strip() for x in (m or "").splitlines() if x.strip()]

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def get_fb_dtsg(cookie):
    try:
        headers={'Cookie':cookie,'User-Agent':'Mozilla/5.0'}
        res = requests.get('https://mbasic.facebook.com/profile.php', headers=headers, timeout=10)
        token = re.search(r'name="fb_dtsg" value="(.*?)"', res.text)
        return token.group(1) if token else None
    except:
        return None

def send_messenger(cookie, box_id, content):
    try:
        ts=int(time.time()*1000)
        m = re.search(r"c_user=(\d+)", cookie)
        user_id = m.group(1) if m else "0"
        fb_dtsg=get_fb_dtsg(cookie)
        data = {
            'thread_fbid': box_id,
            'action_type': 'ma-type:user-generated-message',
            'body': content,
            'client': 'mercury',
            'author': f'fbid:{user_id}',
            'timestamp': ts,
            'source': 'source:chat:web',
            'offline_threading_id': str(ts),
            'message_id': str(ts),
            '__user': user_id,
            'fb_dtsg': fb_dtsg
        }
        headers = {'Cookie':cookie,'User-Agent':'Mozilla/5.0'}
        res=requests.post('https://www.facebook.com/messaging/send/', data=data, headers=headers, timeout=10)
        return res.status_code==200, res.text
    except Exception as e:
        return False, str(e)

def send_discord(token, channel_id, content):
    try:
        url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }
        data = {"content": content}
        r = requests.post(url, headers=headers, json=data, timeout=10)
        return r.status_code in (200, 201), r.text
    except Exception as e:
        return False, str(e)

def start_treo_tab(cookie_or_auth, box_id, message, delay, app_name, task_type="Treo", silent=True):
    stop_event = threading.Event()
    def treo_worker():
        ok = 0
        fail = 0
        start_time = datetime.now()
        consecutive_fail = 0
        while not stop_event.is_set():
            try:
                success = False
                if app_name.lower() == "messenger":
                    success, _ = send_messenger(cookie_or_auth, box_id, message)
                elif app_name.lower() == "discord":
                    success, _ = send_discord(cookie_or_auth, box_id, message)
                elif app_name.lower() == "telegram":
                    success, _ = telegram_send(cookie_or_auth, box_id, message)
                else:
                    success = False
                if success:
                    ok += 1
                    consecutive_fail = 0
                    current_time = datetime.now().strftime("%H:%M:%S")
                    print(Fore.GREEN + f"[{current_time}] ✅ {task_type} {app_name} -> {box_id}: OK {ok}")
                else:
                    fail += 1
                    consecutive_fail += 1
                    current_time = datetime.now().strftime("%H:%M:%S")
                    print(Fore.RED + f"[{current_time}] ❌ {task_type} {app_name} -> {box_id}: FAIL {fail}")
                if consecutive_fail >= 5:
                    treo_tabs[threading.current_thread()]['status'] = "🔴 Rớt (fail nhiều)"
                else:
                    treo_tabs[threading.current_thread()]['status'] = "🟢 Đang chạy"
            except Exception as e:
                fail += 1
                consecutive_fail += 1
                current_time = datetime.now().strftime("%H:%M:%S")
                print(Fore.RED + f"[{current_time}] ❌ {task_type} {app_name} -> {box_id}: Lỗi {str(e)[:50]}")
                treo_tabs[threading.current_thread()]['status'] = f"🔴 Lỗi: {str(e)[:50]}"
            uptime_seconds = int((datetime.now() - start_time).total_seconds())
            treo_tabs[threading.current_thread()].update({
                'ok': ok,
                'fail': fail,
                'uptime': uptime_seconds,
                'last_update': datetime.now().strftime("%H:%M:%S %d-%m-%Y")
            })
            for _ in range(max(1, int(delay*10))):
                if stop_event.is_set():
                    break
                time.sleep(0.1)
        info = treo_tabs.get(threading.current_thread(), {}).copy()
        info['stopped_at'] = datetime.now().strftime("%H:%M:%S %d-%m-%Y")
        info['total_runtime'] = int((datetime.now() - start_time).total_seconds())
        treo_history.append(info)
    t = threading.Thread(target=treo_worker, daemon=True)
    treo_tabs[t] = {
        'app': app_name,
        'type': task_type,
        'box_id': box_id,
        'start_time': datetime.now(),
        'ok': 0,
        'fail': 0,
        'uptime': 0,
        'stop_event': stop_event,
        'status': "🟢 Đang khởi động",
        'last_update': datetime.now().strftime("%H:%M:%S %d-%m-%Y")
    }
    t.start()
    if not silent:
        current_time = datetime.now().strftime("%H:%M:%S")
        print(Fore.GREEN + f"[{current_time}] [+] Đã khởi chạy {task_type} {app_name} cho box {box_id}")
    return t

def start_task(app_name, task_type, auth_data, box_id, send_func, messages, delay, silent=True):
    stop_event = threading.Event()
    def worker_wrapper():
        ok = 0
        fail = 0
        start_time = datetime.now()
        consecutive_fail = 0
        message_index = 0
        while not stop_event.is_set():
            try:
                if task_type == "Nhây" or task_type == "Reo" or task_type == "Nhây Tag":
                    if message_index >= len(messages):
                        message_index = 0
                    current_message = messages[message_index]
                    message_index += 1
                    success, _ = send_func(auth_data, box_id, current_message)
                    if success:
                        ok += 1
                        consecutive_fail = 0
                        current_time = datetime.now().strftime("%H:%M:%S")
                        print(Fore.GREEN + f"[{current_time}] ✅ {task_type} {app_name} -> {box_id}: {current_message[:50]}...")
                    else:
                        fail += 1
                        consecutive_fail += 1
                        current_time = datetime.now().strftime("%H:%M:%S")
                        print(Fore.RED + f"[{current_time}] ❌ {task_type} {app_name} -> {box_id}: FAIL {fail}")
                else:
                    success, _ = send_func(auth_data, box_id, messages)
                    if success:
                        ok += 1
                        consecutive_fail = 0
                        current_time = datetime.now().strftime("%H:%M:%S")
                        print(Fore.GREEN + f"[{current_time}] ✅ {task_type} {app_name} -> {box_id}: OK {ok}")
                    else:
                        fail += 1
                        consecutive_fail += 1
                        current_time = datetime.now().strftime("%H:%M:%S")
                        print(Fore.RED + f"[{current_time}] ❌ {task_type} {app_name} -> {box_id}: FAIL {fail}")
                if consecutive_fail >= 5:
                    treo_tabs[threading.current_thread()]['status'] = "🔴 Rớt (fail nhiều)"
                else:
                    treo_tabs[threading.current_thread()]['status'] = "🟢 Đang chạy"
            except Exception as e:
                fail += 1
                consecutive_fail += 1
                current_time = datetime.now().strftime("%H:%M:%S")
                print(Fore.RED + f"[{current_time}] ❌ {task_type} {app_name} -> {box_id}: Lỗi {str(e)[:50]}")
                treo_tabs[threading.current_thread()]['status'] = f"🔴 Lỗi: {str(e)[:50]}"
            uptime_seconds = int((datetime.now() - start_time).total_seconds())
            treo_tabs[threading.current_thread()].update({
                'ok': ok,
                'fail': fail,
                'uptime': uptime_seconds,
                'last_update': datetime.now().strftime("%H:%M:%S %d-%m-%Y")
            })
            for _ in range(max(1, int(delay*10))):
                if stop_event.is_set():
                    break
                time.sleep(0.1)
        info = treo_tabs.get(threading.current_thread(), {}).copy()
        info['stopped_at'] = datetime.now().strftime("%H:%M:%S %d-%m-%Y")
        info['total_runtime'] = int((datetime.now() - start_time).total_seconds())
        treo_history.append(info)
    t = threading.Thread(target=worker_wrapper, daemon=True)
    treo_tabs[t] = {
        'app': app_name,
        'type': task_type,
        'box_id': box_id,
        'start_time': datetime.now(),
        'ok': 0,
        'fail': 0,
        'uptime': 0,
        'stop_event': stop_event,
        'status': "🟢 Đang khởi động",
        'last_update': datetime.now().strftime("%H:%M:%S %d-%m-%Y")
    }
    t.start()
    if not silent:
        current_time = datetime.now().strftime("%H:%M:%S")
        print(Fore.GREEN + f"[{current_time}] [+] Đã khởi chạy {task_type} {app_name} cho box {box_id}")
    return t

def xem_dung_treo():
    while True:
        clear()
        current_time = datetime.now().strftime("%H:%M:%S %d-%m-%Y")
        print(Fore.CYAN + "\n══════════════════════════════════════════════════════════")
        print(Fore.CYAN + f"         DANH SÁCH TASK ĐANG CHẠY - {current_time}")
        print(Fore.CYAN + "══════════════════════════════════════════════════════════")
        if not treo_tabs:
            print(Fore.YELLOW + "[!] Hiện không có task nào đang chạy.")
        else:
            for i, (t, info) in enumerate(list(treo_tabs.items()), 1):
                uptime_s = int(info.get('uptime', 0))
                h, rem = divmod(uptime_s, 3600)
                m, s = divmod(rem, 60)
                uptime_str = f"{h:02}:{m:02}:{s:02}"
                status = info.get('status', '')
                last_update = info.get('last_update', 'Chưa cập nhật')
                print(Fore.CYAN + "─" * 60)
                print(Fore.GREEN + f"[{i}] {info.get('app')} | {info.get('type')} | {status}")
                print(Fore.WHITE + f"    Box ID : {info.get('box_id')}")
                print(Fore.YELLOW + f"    Uptime : {uptime_str}")
                print(Fore.CYAN + f"    OK : {info.get('ok')} | FAIL : {info.get('fail')}")
                print(Fore.MAGENTA + f"    Cập nhật: {last_update}")
            print(Fore.CYAN + "─" * 60)
        print(Fore.MAGENTA + "\nLỰA CHỌN:")
        print(Fore.YELLOW + "• Nhập số STT để dừng task cụ thể")
        print(Fore.YELLOW + "• Nhập '10' để xem lịch sử task đã dừng")
        print(Fore.YELLOW + "• Nhập 'stop all' để dừng tất cả task")
        print(Fore.YELLOW + "• Nhập '0' để quay lại menu chính")
        choice = input(Fore.YELLOW + "\n🎯 Lựa chọn: ").strip()
        if choice == '0':
            clear()
            break
        if choice.lower() == 'stop all':
            current_time = datetime.now().strftime("%H:%M:%S")
            for t in list(treo_tabs.keys()):
                treo_tabs[t]['stop_event'].set()
            print(Fore.GREEN + f"[{current_time}] [✓] Đã gửi lệnh dừng tất cả task.")
            time.sleep(1.0)
            continue
        elif choice == '10':
            clear()
            current_time = datetime.now().strftime("%H:%M:%S %d-%m-%Y")
            print(Fore.CYAN + "\n══════════════════════════════════════════════════════════")
            print(Fore.CYAN + f"        LỊCH SỬ TASK ĐÃ DỪNG - {current_time}")
            print(Fore.CYAN + "══════════════════════════════════════════════════════════")
            if not treo_history:
                print(Fore.YELLOW + "Chưa có task nào được dừng.")
            else:
                for i, h in enumerate(treo_history, 1):
                    uptime_s = int(h.get('total_runtime', h.get('uptime', 0)))
                    h1, rem = divmod(uptime_s, 3600)
                    m1, s1 = divmod(rem, 60)
                    uptime_str = f"{h1:02}:{m1:02}:{s1:02}"
                    print(Fore.CYAN + "─" * 60)
                    print(Fore.GREEN + f"[{i}] {h.get('app')} | {h.get('type')}")
                    print(Fore.WHITE + f"    Box ID : {h.get('box_id')}")
                    print(Fore.YELLOW + f"    Thời gian chạy : {uptime_str}")
                    print(Fore.CYAN + f"    OK : {h.get('ok')} | FAIL : {h.get('fail')}")
                    print(Fore.MAGENTA + f"    Bắt đầu : {h.get('start_time').strftime('%H:%M:%S %d-%m-%Y') if isinstance(h.get('start_time'), datetime) else 'N/A'}")
                    print(Fore.MAGENTA + f"    Dừng lúc : {h.get('stopped_at')}")
                print(Fore.CYAN + "─" * 60)
            input(Fore.YELLOW + "\n📝 Nhấn Enter để quay lại danh sách task hiện tại...")
            continue
        else:
            try:
                idx = int(choice) - 1
                keys = list(treo_tabs.keys())
                if 0 <= idx < len(keys):
                    t = keys[idx]
                    info = treo_tabs[t]
                    info['stop_event'].set()
                    current_time = datetime.now().strftime("%H:%M:%S")
                    print(Fore.GREEN + f"[{current_time}] [✓] Đã gửi lệnh dừng task {info['app']} | {info['type']} (Box: {info['box_id']})")
                    time.sleep(0.3)
                else:
                    print(Fore.RED + "[!] Số thứ tự không hợp lệ.")
            except ValueError:
                print(Fore.RED + "[!] Vui lòng nhập số hợp lệ.")
            time.sleep(1)

def read_messages_from_files(file_list, default_file=None, read_lines=False):
    msgs = []
    files = list(file_list) if file_list else []
    if not files and default_file:
        files = [default_file]
    for fn in files:
        fn = fn.strip()
        if not fn:
            continue
        if not os.path.exists(fn):
            print(Fore.RED + f"[!] File không tồn tại: {fn}")
            continue
        try:
            with open(fn, "r", encoding="utf-8") as f:
                if read_lines:
                    lines = [line.strip() for line in f if line.strip()]
                    msgs.extend(lines)
                else:
                    content = f.read().strip()
                    if content:
                        msgs.append(content)
        except Exception as e:
            print(Fore.RED + f"[!] Lỗi đọc file {fn}: {e}")
    return msgs

def input_int(prompt, default=None):
    while True:
        s = input(Fore.YELLOW + prompt).strip()
        if s == "" and default is not None:
            return default
        try:
            return int(s)
        except:
            print(Fore.RED + "Nhập số hợp lệ!")

def transition_screen(title="DATK"):
    clear()
    spinner = itertools.cycle(['⠋','⠙','⠹','⠸','⠼','⠴','⠦','⠧','⠇','⠏'])
    sys.stdout.write(Fore.CYAN + f"Đang mở {title} ")
    sys.stdout.flush()
    for _ in range(18):
        sys.stdout.write(Fore.YELLOW + next(spinner))
        sys.stdout.flush()
        time.sleep(0.07)
        sys.stdout.write('\b')
    clear()
    big_banner = f"""
{Fore.MAGENTA}
██████╗  █████╗ ████████╗██╗  ██╗
██╔══██╗██╔══██╗╚══██╔══╝██║ ██╔╝
██║  ██║███████║   ██║   █████╔╝ 
██║  ██║██╔══██║   ██║   ██╔═██╗ 
██████╔╝██║  ██║   ██║   ██║  ██╗
╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝
        {Fore.CYAN}{title}
"""
    print(big_banner)
    time.sleep(0.45)

def treo_mess():
    transition_screen("TREO MESSENGER")
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.CYAN + f"[{current_time}] === TREO MESSENGER - GỬI FULL NỘI DUNG ===")
    cookies = []
    while True:
        ck = input("Nhập cookie Messenger (done để xong): ").strip()
        if ck.lower() == "done": break
        if "c_user=" in ck: cookies.append(ck)
    if not cookies:
        print(Fore.RED + "[!] Không có cookie.")
        return
    box_ids = []
    while True:
        b = input("Nhập ID box Messenger (done để xong): ").strip()
        if b.lower() == "done": break
        if b: box_ids.append(b)
    if not box_ids:
        print(Fore.RED + "[!] Không có ID box.")
        return
    files = []
    while True:
        fn = input("Nhập file ngôn treo (done để xong): ").strip()
        if fn.lower() == "done": break
        if fn: files.append(fn)
    messages_list = read_messages_from_files(files, read_lines=False)
    if not messages_list:
        print(Fore.RED + "[!] Không có nội dung để treo.")
        return
    full_message = "\n\n".join(messages_list)
    delay = input_int("Nhập delay (giây): ", 2)
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.GREEN + f"[{current_time}] 🚀 Đang khởi chạy {len(cookies)} cookie × {len(box_ids)} box...")
    for ck in cookies:
        for b in box_ids:
            start_treo_tab(ck, b, full_message, delay, "Messenger", task_type="Treo", silent=False)
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.GREEN + f"[{current_time}] [✓] Đã khởi chạy {len(cookies) * len(box_ids)} task Treo Messenger")
    print(Fore.CYAN + "💡 Mỗi lần gửi sẽ gửi TOÀN BỘ nội dung file")
    time.sleep(1)

def nhay_mess():
    transition_screen("NHÂY MESSENGER")
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.CYAN + f"[{current_time}] === NHÂY MESSENGER - GỬI TỌNG DÒNG ===")
    cookies = []
    while True:
        ck = input("Nhập cookie Messenger (done để xong): ").strip()
        if ck.lower() == "done": break
        if "c_user=" in ck: cookies.append(ck)
    if not cookies:
        print(Fore.RED + "[!] Không có cookie.")
        return
    box_ids = []
    while True:
        b = input("Nhập ID box Messenger (done để xong): ").strip()
        if b.lower() == "done": break
        box_ids.append(b)
    if not box_ids:
        print(Fore.RED + "[!] Không có ID box.")
        return
    messages = read_messages_from_files([], default_file="nhay.txt", read_lines=True)
    if not messages:
        print(Fore.RED + "[!] Không tìm thấy nội dung trong nhay.txt")
        return
    delay = input_int("Nhập delay (giây): ", 2)
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.GREEN + f"[{current_time}] 🚀 Đang khởi chạy {len(cookies)} cookie × {len(box_ids)} box...")
    print(Fore.YELLOW + f"📝 Sẽ gửi {len(messages)} dòng từ nhay.txt")
    for ck in cookies:
        for b in box_ids:
            start_task("Messenger", "Nhây", ck, b, send_messenger, messages, delay, silent=False)
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.GREEN + f"[{current_time}] [✓] Đã khởi chạy {len(cookies) * len(box_ids)} task Nhây Messenger")
    print(Fore.CYAN + "💡 Mỗi lần gửi sẽ gửi 1 DÒNG từ nhay.txt")
    time.sleep(1)

def reo_mess():
    transition_screen("RÉO MESSENGER")
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.CYAN + f"[{current_time}] === RÉO MESSENGER - GỬI TỪNG DÒNG KÈM TÊN ===")
    cookies = []
    while True:
        ck = input("Nhập cookie Messenger (done để xong): ").strip()
        if ck.lower() == "done": break
        if "c_user=" in ck: cookies.append(ck)
    if not cookies:
        print(Fore.RED + "[!] Không có cookie.")
        return
    box_ids = []
    while True:
        b = input("Nhập ID box Messenger (done để xong): ").strip()
        if b.lower() == "done": break
        box_ids.append(b)
    if not box_ids:
        print(Fore.RED + "[!] Không có ID box.")
        return
    names = []
    while True:
        n = input("Nhập tên người réo (done để xong): ").strip()
        if n.lower() == "done": break
        if n: names.append(n)
    if not names:
        print(Fore.RED + "[!] Không có tên để réo.")
        return
    messages = read_messages_from_files([], default_file="nhay.txt", read_lines=True)
    if not messages:
        print(Fore.RED + "[!] Không tìm thấy nội dung trong nhay.txt")
        return
    delay = input_int("Nhập delay (giây): ", 2)
    def make_send_wrapper(name):
        def send_wrapper(cookie, box_id, msg):
            body = f"{msg} {name}"
            return send_messenger(cookie, box_id, body)
        return send_wrapper
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.GREEN + f"[{current_time}] 🚀 Đang khởi chạy {len(cookies)} cookie × {len(box_ids)} box × {len(names)} tên...")
    for ck in cookies:
        for b in box_ids:
            for n in names:
                start_task("Messenger", "Reo", ck, b, make_send_wrapper(n), messages, delay, silent=False)
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.GREEN + f"[{current_time}] [✓] Đã khởi chạy {len(cookies) * len(box_ids) * len(names)} task Réo Messenger")
    print(Fore.CYAN + "💡 Mỗi lần gửi sẽ gửi 1 DÒNG từ nhay.txt + tên người réo")
    time.sleep(1)

def so_mess():
    transition_screen("SỚ MESSENGER")
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.CYAN + f"[{current_time}] === SỚ MESSENGER - GỬI FULL NỘI DUNG SO.TXT ===")
    cookies = []
    while True:
        ck = input("Nhập cookie Messenger (done để xong): ").strip()
        if ck.lower() == "done": break
        if "c_user=" in ck: cookies.append(ck)
    if not cookies:
        print(Fore.RED + "[!] Không có cookie.")
        return
    box_ids = []
    while True:
        b = input("Nhập ID box Messenger (done để xong): ").strip()
        if b.lower() == "done": break
        box_ids.append(b)
    if not box_ids:
        print(Fore.RED + "[!] Không có ID box.")
        return
    messages_list = read_messages_from_files([], default_file="so.txt", read_lines=False)
    if not messages_list:
        print(Fore.RED + "[!] Không tìm thấy nội dung trong so.txt")
        return
    full_message = "\n\n".join(messages_list)
    delay = input_int("Nhập delay (giây): ", 5)
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.GREEN + f"[{current_time}] 🚀 Đang khởi chạy {len(cookies)} cookie × {len(box_ids)} box...")
    for ck in cookies:
        for b in box_ids:
            start_treo_tab(ck, b, full_message, delay, "Messenger", task_type="Sớ", silent=False)
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.GREEN + f"[{current_time}] [✓] Đã khởi chạy {len(cookies) * len(box_ids)} task Sớ Messenger")
    print(Fore.CYAN + "💡 Mỗi lần gửi sẽ gửi TOÀN BỘ nội dung so.txt")
    time.sleep(1)

class Mention:
    thread_id = None
    offset = None
    length = None
    def __init__(self, thread_id, offset, length):
        self.thread_id = thread_id
        self.offset = offset
        self.length = length
    def _to_send_data(self, i):
        return {
            "profile_xmd[{}][id]".format(i): self.thread_id,
            "profile_xmd[{}][offset]".format(i): self.offset,
            "profile_xmd[{}][length]".format(i): self.length,
            "profile_xmd[{}][type]".format(i): "p",
        }

def get_uid_fbdtsg(ck):
    try:
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
            'Connection': 'keep-alive',
            'Cookie': ck,
            'Host': 'www.facebook.com',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }
        response = requests.get('https://www.facebook.com/', headers=headers)
        if response.status_code != 200:
            return None, None, None, None, None
        html_content = response.text
        user_id = None
        fb_dtsg = None
        script_tags = re.findall(r'<script id="__eqmc" type="application/json[^>]*>(.*?)</script>', html_content)
        for script in script_tags:
            try:
                json_data = json.loads(script)
                if 'u' in json_data:
                    user_param = re.search(r'__user=(\d+)', json_data['u'])
                    if user_param:
                        user_id = user_param.group(1)
                        break
            except:
                continue
        fb_dtsg_match = re.search(r'"f":"([^"]+)"', html_content)
        if fb_dtsg_match:
            fb_dtsg = fb_dtsg_match.group(1)
        revision_match = re.search(r'"server_revision":(\d+),"client_revision":(\d+)', html_content)
        rev = revision_match.group(1) if revision_match else ""
        a_match = re.search(r'__a=(\d+)', html_content)
        a = a_match.group(1) if a_match else "1"
        req = "1b"
        return user_id, fb_dtsg, rev, req, a
    except Exception as e:
        return None, None, None, None, None

def get_info(uid: str, cookie: str):
    try:
        user_id, fb_dtsg, rev, req, a = get_uid_fbdtsg(cookie)
        if not all([user_id, fb_dtsg]):
            return {"error": "Không thể lấy thông tin xác thực. Cookie có thể đã hết hạn."}
        form = {
            "ids[0]": uid,
            "fb_dtsg": fb_dtsg,
            "__a": a,
            "__req": req,
            "__rev": rev
        }
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9,vi;q=0.8',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': cookie,
            'Origin': 'https://www.facebook.com',
            'Referer': 'https://www.facebook.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }
        response = requests.post(
            "https://www.facebook.com/chat/user_info/",
            headers=headers,
            data=form
        )
        if response.status_code != 200:
            return {"error": f"Lỗi kết nối: {response.status_code}"}
        try:
            text_response = response.text
            if text_response.startswith("for (;;);"):
                text_response = text_response[9:]
            res_data = json.loads(text_response)
            if "error" in res_data:
                return {"error": res_data.get("error")}
            if "payload" in res_data and "profiles" in res_data["payload"]:
                profiles = res_data["payload"]["profiles"]
                if not profiles:
                    return {"error": "Không Có Data"}
                first_profile_id = next(iter(profiles))
                profile = profiles[first_profile_id]
                return {
                    "id": first_profile_id,
                    "name": profile.get("name", ""),
                    "url": profile.get("url", ""),
                    "thumbSrc": profile.get("thumbSrc", ""),
                    "gender": profile.get("gender", "")
                }
            else:
                return {"error": "Không tìm thấy thông tin người dùng"}
        except json.JSONDecodeError:
            return {"error": "Lỗi khi phân tích dữ liệu JSON"}
    except Exception as e:
        return {"error": str(e)}

def nhay_tag_mess():
    transition_screen("NHÂY TAG MESSENGER")
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.CYAN + f"[{current_time}] === NHÂY TAG MESSENGER ===")
    cookies = []
    while True:
        ck = input("Nhập cookie Facebook (done để xong): ").strip()
        if ck.lower() == "done":
            break
        if ck:
            cookies.append(ck)
    if not cookies:
        print(Fore.RED + "[!] Không có cookie.")
        return
    idboxes = []
    while True:
        idb = input("Nhập ID Box (done để xong): ").strip()
        if idb.lower() == "done":
            break
        if idb:
            idboxes.append(idb)
    if not idboxes:
        print(Fore.RED + "[!] Không có ID box.")
        return
    uid = input("Nhập UID người cần tag: ").strip()
    if not uid:
        print(Fore.RED + "[!] Không có UID.")
        return
    user_data = get_info(uid, cookies[0])
    if "error" in user_data:
        print(Fore.RED + f"[!] Lỗi khi lấy tên người dùng: {user_data['error']}")
        return
    ten = user_data.get("name", "N/A")
    print(Fore.GREEN + f"[+] Tên người được tag: {ten}")
    if not os.path.exists("nhay.txt"):
        print(Fore.RED + "[!] Không tìm thấy file nhay.txt")
        return
    with open("nhay.txt", "r", encoding="utf-8") as f:
        messages = [line.strip() for line in f if line.strip()]
    if not messages:
        print(Fore.RED + "[!] File nhay.txt rỗng")
        return
    delay = input_int("Nhập delay (giây): ", 2)
    def send_wrapper(cookie, box_id, msg):
        user_id, fb_dtsg, rev, req, a = get_uid_fbdtsg(cookie)
        if not user_id or not fb_dtsg:
            return False, "Không lấy được user_id hoặc fb_dtsg"
        if random.choice([True, False]):
            full_message = f"{ten} {msg}"
            offset = 0
            length = len(ten)
        else:
            full_message = f"{msg} {ten}"
            offset = len(msg) + 1
            length = len(ten)
        mention = Mention(thread_id=uid, offset=offset, length=length)
        timestamp = int(datetime.now().timestamp() * 1000)
        if not a:
            a = "1"
        if not req:
            req = "1b"
        payload = {
            "thread_fbid": box_id,
            "action_type": "ma-type:user-generated-message",
            "body": full_message,
            "client": "mercury",
            "author": f"fbid:{user_id}",
            "timestamp": str(timestamp),
            "source": "source:chat:web",
            "source_tags[0]": "source:chat",
            "offline_threading_id": str(timestamp),
            "message_id": str(timestamp),
            "specific_message_type": "non_ad",
            "manual_retry_cnt": 0,
            "specific_to_list[0]": f"fbid:{uid}",
            "specific_to_list[1]": f"fbid:{user_id}",
            "ephemeral_ttl_mode": "0",
            "__user": user_id,
            "__a": a,
            "__req": req,
            "__rev": rev if rev else "1015919737",
            "fb_dtsg": fb_dtsg,
        }
        mention_data = mention._to_send_data(0)
        for key, value in mention_data.items():
            payload[key] = value
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "identity",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": cookie,
            "Host": "www.facebook.com",
            "Origin": "https://www.facebook.com",
            "Referer": f"https://www.facebook.com/messages/t/{box_id}",
            "User-Agent": "python-http/0.27.0",
        }
        try:
            response = requests.post(
                "https://www.facebook.com/messaging/send/",
                headers=headers,
                data=payload,
                timeout=15,
            )
            return response.status_code == 200, response.text
        except Exception as e:
            return False, str(e)
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.GREEN + f"[{current_time}] 🚀 Đang khởi chạy {len(cookies)} cookie × {len(idboxes)} box...")
    for ck in cookies:
        for box_id in idboxes:
            start_task("Messenger", "Nhây Tag", ck, box_id, send_wrapper, messages, delay, silent=False)
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.GREEN + f"[{current_time}] [✓] Đã khởi chạy {len(cookies) * len(idboxes)} task Nhây Tag Messenger")
    print(Fore.CYAN + f"💡 Đang tag: {ten}")
    time.sleep(1)

def treo_discord():
    transition_screen("TREO DISCORD")
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.CYAN + f"[{current_time}] === TREO DISCORD - GỬI FULL NỘI DUNG ===")
    tokens = []
    while True:
        tk = input("Nhập token Discord (done để xong): ").strip()
        if tk.lower() == "done": break
        tokens.append(tk)
    if not tokens:
        print(Fore.RED + "[!] Không có token.")
        return
    channels = []
    while True:
        sv = input("Nhập ID server/channel (done để xong): ").strip()
        if sv.lower() == "done": break
        channels.append(sv)
    if not channels:
        print(Fore.RED + "[!] Không có channel.")
        return
    files = []
    while True:
        fn = input("Nhập file ngôn treo (done để xong): ").strip()
        if fn.lower() == "done": break
        files.append(fn)
    messages_list = read_messages_from_files(files, read_lines=False)
    if not messages_list:
        print(Fore.RED + "[!] Không có nội dung để treo.")
        return
    full_message = "\n\n".join(messages_list)
    delay = input_int("Nhập delay (giây): ", 2)
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.GREEN + f"[{current_time}] 🚀 Đang khởi chạy {len(tokens)} token × {len(channels)} channel...")
    for tk in tokens:
        for ch in channels:
            start_treo_tab(tk, ch, full_message, delay, "Discord", task_type="Treo", silent=False)
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.GREEN + f"[{current_time}] [✓] Đã khởi chạy {len(tokens) * len(channels)} task Treo Discord")
    time.sleep(1)

def nhay_discord():
    transition_screen("NHÂY DISCORD")
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.CYAN + f"[{current_time}] === NHÂY DISCORD - GỬI TỪNG DÒNG ===")
    tokens = []
    while True:
        tk = input("Nhập token Discord (done để xong): ").strip()
        if tk.lower() == "done": break
        tokens.append(tk)
    if not tokens:
        print(Fore.RED + "[!] Không có token.")
        return
    channels = []
    while True:
        sv = input("Nhập ID server/channel (done để xong): ").strip()
        if sv.lower() == "done": break
        channels.append(sv)
    if not channels:
        print(Fore.RED + "[!] Không có channel.")
        return
    messages = read_messages_from_files([], default_file="nhay.txt", read_lines=True)
    if not messages:
        print(Fore.RED + "[!] Không tìm thấy nội dung trong nhay.txt")
        return
    delay = input_int("Nhập delay (giây): ", 2)
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.GREEN + f"[{current_time}] 🚀 Đang khởi chạy {len(tokens)} token × {len(channels)} channel...")
    for tk in tokens:
        for ch in channels:
            start_task("Discord", "Nhây", tk, ch, send_discord, messages, delay, silent=False)
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.GREEN + f"[{current_time}] [✓] Đã khởi chạy {len(tokens) * len(channels)} task Nhây Discord")
    time.sleep(1)

def nhay_discord_tag():
    transition_screen("NHÂY TAG DISCORD")
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.CYAN + f"[{current_time}] === NHÂY TAG DISCORD - GỬI TỪNG DÒNG KÈM TAG ===")
    tokens = []
    while True:
        tk = input("Nhập token Discord (done để xong): ").strip()
        if tk.lower() == "done": break
        tokens.append(tk)
    if not tokens:
        print(Fore.RED + "[!] Không có token.")
        return
    channels = []
    while True:
        sv = input("Nhập ID server/channel (done để xong): ").strip()
        if sv.lower() == "done": break
        channels.append(sv)
    if not channels:
        print(Fore.RED + "[!] Không có channel.")
        return
    target_id = input("Nhập ID user cần tag: ").strip()
    if not target_id:
        print(Fore.RED + "[!] Không có ID user.")
        return
    messages = read_messages_from_files([], default_file="nhay.txt", read_lines=True)
    if not messages:
        print(Fore.RED + "[!] Không tìm thấy nội dung trong nhay.txt")
        return
    delay = input_int("Nhập delay (giây): ", 2)
    def send_discord_tag(token, channel_id, msg):
        content = f"<@{target_id}> {msg}"
        return send_discord(token, channel_id, content)
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.GREEN + f"[{current_time}] 🚀 Đang khởi chạy {len(tokens)} token × {len(channels)} channel...")
    for tk in tokens:
        for ch in channels:
            start_task("Discord", "Nhây Tag", tk, ch, send_discord_tag, messages, delay, silent=False)
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.GREEN + f"[{current_time}] [✓] Đã khởi chạy {len(tokens) * len(channels)} task Nhây Tag Discord")
    time.sleep(1)

def sotagdis():
    transition_screen("SỚ TAG DISCORD")
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.CYAN + f"[{current_time}] === SỚ TAG DISCORD ===")
    tokens = []
    while True:
        tk = input("Nhập token Discord (done để xong): ").strip()
        if tk.lower() == "done": break
        tokens.append(tk)
    if not tokens:
        print(Fore.RED + "[!] Không có token.")
        return
    channels = []
    while True:
        sv = input("Nhập ID server/channel (done để xong): ").strip()
        if sv.lower() == "done": break
        channels.append(sv)
    if not channels:
        print(Fore.RED + "[!] Không có channel.")
        return
    tag_ids = []
    while True:
        uid = input("Nhập ID user cần tag (done để xong): ").strip()
        if uid.lower() == "done": break
        if uid: tag_ids.append(uid)
    tag_str = " ".join([f"<@{uid}>" for uid in tag_ids]) if tag_ids else ""
    delay = input_int("Nhập delay (giây): ", 2)
    filepath = "so.txt"
    if not os.path.exists(filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("Câu hỏi poll 1?\nCâu hỏi poll 2?\n")
        print(f"Đã tạo {filepath}, chỉnh nội dung rồi chạy lại.")
        return
    with open(filepath, "r", encoding="utf-8") as f:
        lines = [x.strip() for x in f if x.strip()]
    if not lines:
        print("so.txt rỗng")
        return
    def make_send_for_sotag(tagstring, bodies):
        def send_sotag(token, ch, _):
            for body in bodies:
                content = f"{tagstring} {body}"
                send_discord(token, ch, content)
                time.sleep(delay)
            return True, "done"
        return send_sotag
    for tk in tokens:
        for ch in channels:
            start_task("Discord", "SoTag", tk, ch, make_send_for_sotag(tag_str, lines), "\n".join(lines), delay, silent=False)
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.GREEN + f"[{current_time}] [✓] Đã khởi chạy {len(tokens) * len(channels)} task Sớ Tag Discord")
    time.sleep(1)

def polldis():
    transition_screen("POLL DISCORD")
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.CYAN + f"[{current_time}] === POLL DISCORD ===")
    REACTIONS = [
        "😭","🤣","💤","💦","😅","🐉","😏","🤯","👁","😪","😤","😓","🤓","😑",
        "👱‍♂️","💔","💙","💓","💘","💤","💥","💌","💢","🕳","💨","💫","☸",
        "🍀","🇻🇳","😰","🌚","🧸","👾","🐻","😱","🤔","😬","🤪","😡","⭐",
        "🙈","💫","🙊","💓","💚","💙","🧡","💜","❤️","💕","🤳","🤝","🙏"
    ]
    TIMEOUT = 5
    def send_message(token, channel_id, content):
        url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "User-Agent": "DiscordSelfBot (polldis)"
        }
        try:
            r = requests.post(url, headers=headers, json={"content": content}, timeout=TIMEOUT)
            if r.status_code in (200, 201):
                return True, r.json().get("id")
            else:
                return False, r.text[:200]
        except Exception as e:
            return False, str(e)
    def add_reaction(token, channel_id, message_id, emoji):
        enc = requests.utils.requote_uri(emoji)
        url = f"https://discord.com/api/v10/channels/{channel_id}/messages/{message_id}/reactions/{enc}/@me"
        headers = {"Authorization": token, "User-Agent": "DiscordSelfBot (polldis)"}
        try:
            r = requests.put(url, headers=headers, timeout=TIMEOUT)
            return r.status_code in (204, 200)
        except:
            return False
    tokens = []
    while True:
        tk = input("Nhập token Discord (done để xong): ").strip()
        if tk.lower() == "done": break
        tokens.append(tk)
    if not tokens:
        print(Fore.RED + "[!] Không có token!")
        return
    channels = []
    while True:
        sv = input("Nhập ID server/channel (done để xong): ").strip()
        if sv.lower() == "done": break
        channels.append(sv)
    if not channels:
        print(Fore.RED + "[!] Không có channel!")
        return
    tag_ids = []
    while True:
        uid = input("Nhập ID user cần tag (done để xong): ").strip()
        if uid.lower() == "done": break
        if uid: tag_ids.append(uid)
    tag_str = " ".join([f"<@{uid}>" for uid in tag_ids]) if tag_ids else ""
    delay = input_int("Nhập delay (giây): ", 3)
    filepath = "nhay.txt"
    if not os.path.exists(filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("Câu hỏi poll 1?\nCâu hỏi poll 2?\n")
        print(f"Đã tạo {filepath}, chỉnh nội dung rồi chạy lại.")
        return
    with open(filepath, "r", encoding="utf-8") as f:
        lines = [x.strip() for x in f if x.strip()]
    if not lines:
        print("nhay.txt rỗng")
        return
    def make_poll_worker(token, channel_id, lines_local):
        def send_poll(tok, ch, _):
            for body in lines_local:
                content = f"{tag_str} 卍ﮩ٨ـﮩﮩ٨ـ♡ﮩ٨ـﮩﮩ٨ـ☯ {body}\n> # > ĐỖ TIẾN ĐẠT KING OF CODE COME TO WAR=))=))=))"
                ok, mid = send_message(token, channel_id, content)
                if ok and mid:
                    def add_reacts(mid_local):
                        for emj in REACTIONS:
                            add_reaction(token, channel_id, mid_local, emj)
                            time.sleep(0.4)
                    threading.Thread(target=add_reacts, args=(mid,), daemon=True).start()
                time.sleep(delay)
            return True, "done"
        return send_poll
    for tk in tokens:
        for ch in channels:
            start_task("Discord", "Poll", tk, ch, make_poll_worker(tk, ch, lines), "\n".join(lines), delay, silent=False)
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.GREEN + f"[{current_time}] [✓] Đã khởi chạy {len(tokens) * len(channels)} task Poll Discord")
    time.sleep(1)

def telegram_send(token, chat_id, content):
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = {"chat_id": chat_id, "text": content}
        r = requests.post(url, data=data, timeout=10)
        return r.status_code == 200, r.text
    except Exception as e:
        return False, str(e)

def treo_telegram():
    transition_screen("TREO TELEGRAM")
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.CYAN + f"[{current_time}] === TREO TELEGRAM - GỬI FULL NỘI DUNG ===")
    tokens = []
    while True:
        tk = input("Nhập token Telegram bot (done để xong): ").strip()
        if tk.lower() == "done": break
        tokens.append(tk)
    if not tokens:
        print(Fore.RED + "[!] Không có token.")
        return
    chats = []
    while True:
        sv = input("Nhập ID chat/group (done để xong): ").strip()
        if sv.lower() == "done": break
        chats.append(sv)
    if not chats:
        print(Fore.RED + "[!] Không có chat.")
        return
    files = []
    while True:
        fn = input("Nhập file ngôn treo (done để xong): ").strip()
        if fn.lower() == "done": break
        files.append(fn)
    messages_list = read_messages_from_files(files, read_lines=False)
    if not messages_list:
        print(Fore.RED + "[!] Không có nội dung để gửi.")
        return
    full_message = "\n\n".join(messages_list)
    delay = input_int("Nhập delay (giây): ", 2)
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.GREEN + f"[{current_time}] 🚀 Đang khởi chạy {len(tokens)} bot × {len(chats)} chat...")
    for bot in tokens:
        for ch in chats:
            start_treo_tab(bot, ch, full_message, delay, "Telegram", task_type="Treo", silent=False)
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.GREEN + f"[{current_time}] [✓] Đã khởi chạy {len(tokens) * len(chats)} task Treo Telegram")
    time.sleep(1)

def nhay_telegram():
    transition_screen("NHÂY TELEGRAM")
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.CYAN + f"[{current_time}] === NHÂY TELEGRAM - GỬI TỪNG DÒNG ===")
    tokens = []
    while True:
        tk = input("Nhập token Telegram bot (done để xong): ").strip()
        if tk.lower() == "done": break
        tokens.append(tk)
    if not tokens:
        print(Fore.RED + "[!] Không có token.")
        return
    chats = []
    while True:
        sv = input("Nhập ID chat/group (done để xong): ").strip()
        if sv.lower() == "done": break
        chats.append(sv)
    if not chats:
        print(Fore.RED + "[!] Không có chat.")
        return
    messages = read_messages_from_files([], default_file="nhay.txt", read_lines=True)
    if not messages:
        print(Fore.RED + "[!] Thiếu nhay.txt")
        return
    delay = input_int("Nhập delay (giây): ", 2)
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.GREEN + f"[{current_time}] 🚀 Đang khởi chạy {len(tokens)} bot × {len(chats)} chat...")
    for bot in tokens:
        for ch in chats:
            start_task("Telegram", "Nhây", bot, ch, telegram_send, messages, delay, silent=False)
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.GREEN + f"[{current_time}] [✓] Đã khởi chạy {len(tokens) * len(chats)} task Nhây Telegram")
    time.sleep(1)

def run_facebook_loop(post, cookies, comments, delays):
    post_id = post.split("/")[-1].split("?")[0] if "facebook.com" in post else post
    tokens=[]
    for c in cookies:
        t=get_token(c)
        if t: tokens.append(t); print(Fore.GREEN + "✅ Token ok")
        else: print(Fore.RED + "❌ Lỗi token")
    if not tokens: print(Fore.RED + "❌ Không có token!"); return
    cnt=0
    while True:
        for i,t in enumerate(tokens):
            try:
                msg=random.choice(comments)
                r=requests.post(f"https://graph.facebook.com/{post_id}/comments",data={"message":msg,"access_token":t})
                if r.status_code==200: cnt+=1; print(Fore.GREEN + f"✅ {cnt}: {msg[:60]}")
                else: print(Fore.RED + f"❌ {r.text}")
                d = delays[i] if i < len(delays) else delays[0]
                for i in range(d, 0, -1):
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Đang chờ {i} giây", end="\r"); time.sleep(1)
                print(" " * 50, end="\r")
            except Exception as e: print(Fore.RED + f"❌ {e}")

def treo_top_facebook(use_old=False):
    transition_screen("TREO TOP FACEBOOK")
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.CYAN + f"[{current_time}] === TREO TOP FACEBOOK ===")
    cfg={}
    if use_old:
        old=load_config("treo_top")
        if old: print(Fore.GREEN + "✅ Tải cấu hình cũ!"); cfg=old
        else: print(Fore.RED + "❌ Không tìm thấy cấu hình!"); use_old=False
    if use_old and 'cookies' in cfg:
        cookies=cfg['cookies']; print(f"{Fore.CYAN}[⚜️] ➜ {Fore.RESET}Cookie: {cookies[0][:40]}... (cũ)")
    else:
        ck=input_with_done("Nhập Cookie")
        if not ck: return
        cookies=list_from(ck); cfg['cookies']=cookies
    if use_old and 'post_url' in cfg:
        post=cfg['post_url']; print(f"{Fore.CYAN}[⚜️] ➜ {Fore.RESET}Link: {post} (cũ)")
    else:
        p=input_with_done("Nhập Link Bài Viết")
        if not p: return
        post=first_line(p); cfg['post_url']=post
    comments=[]
    if use_old and 'files' in cfg:
        for f in cfg['files']:
            if os.path.exists(f):
                comments.append(open(f,'r',encoding='utf-8').read().strip()); print(Fore.GREEN + f"✅ {f}")
    else:
        fls=input_with_done("Nhập tên file ngôn (mỗi file 1 dòng)")
        if not fls: return
        files=list_from(fls); cfg['files']=files
        for f in files:
            if os.path.exists(f):
                comments.append(open(f,'r',encoding='utf-8').read().strip()); print(Fore.GREEN + f"✅ {f}")
            else: print(Fore.RED + f"❌ {f}")
    if not comments: print(Fore.RED + "❌ Không có nội dung!"); return
    if use_old and 'delays' in cfg:
        delays=cfg['delays']
    else:
        d=input_with_done("Delay riêng cho từng acc? (gõ 'y' hoặc 'n', rồi gõ done)")
        if d is None: return
        ans=first_line(d) or "n"
        if ans.lower()=="y":
            delays=[]
            for i in range(len(cookies)):
                dm=input_with_done(f"Delay cho acc {i+1} (giây)")
                if dm is None: return
                v=first_line(dm); delays.append(int(v) if v and v.isdigit() else 60)
        else:
            dm=input_with_done("Delay chung (giây)")
            if dm is None: return
            v=first_line(dm); common=int(v) if v and v.isdigit() else 60
            delays=[common]*len(cookies)
        cfg['delays']=delays
    if not use_old: save_config("treo_top",cfg)
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.GREEN + f"[{current_time}] 🚀 Bắt đầu treo top Facebook...")
    run_facebook_loop(post, cookies, comments, cfg['delays'])

def nhay_top_facebook(use_old=False):
    transition_screen("NHÂY TOP FACEBOOK")
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.CYAN + f"[{current_time}] === NHÂY TOP FACEBOOK ===")
    cfg={}
    if use_old:
        old=load_config("nhay_top")
        if old: print(Fore.GREEN + "✅ Tải cấu hình cũ!"); cfg=old
        else: print(Fore.RED + "❌ Không tìm thấy cấu hình!"); use_old=False
    if use_old and 'cookies' in cfg:
        cookies=cfg['cookies']; print(f"{Fore.CYAN}[⚜️] ➜ {Fore.RESET}Cookie: {cookies[0][:40]}... (cũ)")
    else:
        ck=input_with_done("Nhập Cookie")
        if not ck: return
        cookies=list_from(ck); cfg['cookies']=cookies
    if use_old and 'post_url' in cfg:
        post=cfg['post_url']; print(f"{Fore.CYAN}[⚜️] ➜ {Fore.RESET}Link: {post} (cũ)")
    else:
        p=input_with_done("Nhập Link Bài Viết")
        if not p: return
        post=first_line(p); cfg['post_url']=post
    comments=[]
    if os.path.exists("nhay.txt"):
        try:
            comments=[line.strip() for line in open("nhay.txt",'r',encoding='utf-8') if line.strip()]
        except: comments=[]
    if use_old and 'files' in cfg and cfg['files']:
        for f in cfg['files']:
            if os.path.exists(f): comments += [line.strip() for line in open(f,'r',encoding='utf-8') if line.strip()]
    else:
        fls=input_with_done("Nhập tên file ngôn (hoặc bỏ qua bằng cách gõ done nếu đã có nhay.txt)")
        if fls:
            files=list_from(fls); cfg['files']=files
            for f in files:
                if os.path.exists(f): comments += [line.strip() for line in open(f,'r',encoding='utf-8') if line.strip()]; print(Fore.GREEN + f"✅ {f}")
                else: print(Fore.RED + f"❌ {f}")
    comments=[c for c in comments if c]
    if not comments: print(Fore.RED + "❌ Không có nội dung (tạo nhay.txt hoặc nhập file)!"); return
    if use_old and 'delays' in cfg:
        delays=cfg['delays']
    else:
        dm=input_with_done("Delay chung (giây)")
        if dm is None: return
        v=first_line(dm); common=int(v) if v and v.isdigit() else 30
        delays=[common]*len(cookies); cfg['delays']=delays
    if not use_old: save_config("nhay_top",cfg)
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.GREEN + f"[{current_time}] 🚀 Bắt đầu nhây top Facebook...")
    run_facebook_loop(post, cookies, comments, delays)

def so_top_facebook(use_old=False):
    transition_screen("SỚ TOP FACEBOOK")
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.CYAN + f"[{current_time}] === SỚ TOP FACEBOOK ===")
    cfg={}
    if use_old:
        old=load_config("so_top")
        if old: print(Fore.GREEN + "✅ Tải cấu hình cũ!"); cfg=old
        else: print(Fore.RED + "❌ Không tìm thấy cấu hình!"); use_old=False
    if use_old and 'cookies' in cfg:
        cookies=cfg['cookies']; print(f"{Fore.CYAN}[⚜️] ➜ {Fore.RESET}Cookie: {cookies[0][:40]}... (cũ)")
    else:
        ck=input_with_done("Nhập Cookie")
        if not ck: return
        cookies=list_from(ck); cfg['cookies']=cookies
    if use_old and 'post_url' in cfg:
        post=cfg['post_url']; print(f"{Fore.CYAN}[⚜️] ➜ {Fore.RESET}Link: {post} (cũ)")
    else:
        p=input_with_done("Nhập Link Bài Viết")
        if not p: return
        post=first_line(p); cfg['post_url']=post
    comments=[]
    if os.path.exists("so.txt"):
        try:
            comments=[line.strip() for line in open("so.txt",'r',encoding='utf-8') if line.strip()]
        except: comments=[]
    if use_old and 'files' in cfg and cfg['files']:
        for f in cfg['files']:
            if os.path.exists(f): comments += [line.strip() for line in open(f,'r',encoding='utf-8') if line.strip()]
    else:
        fls=input_with_done("Nhập tên file số (hoặc bỏ qua nếu có so.txt)")
        if fls:
            files=list_from(fls); cfg['files']=files
            for f in files:
                if os.path.exists(f): comments += [line.strip() for line in open(f,'r',encoding='utf-8') if line.strip()]; print(Fore.GREEN + f"✅ {f}")
                else: print(Fore.RED + f"❌ {f}")
    comments=[c for c in comments if c]
    if not comments: print(Fore.RED + "❌ Không có nội dung (tạo so.txt hoặc nhập file)!"); return
    if use_old and 'delays' in cfg:
        delays=cfg['delays']
    else:
        dm=input_with_done("Delay chung (giây)")
        if dm is None: return
        v=first_line(dm); common=int(v) if v and v.isdigit() else 45
        delays=[common]*len(cookies); cfg['delays']=delays
    if not use_old: save_config("so_top",cfg)
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.GREEN + f"[{current_time}] 🚀 Bắt đầu sớ top Facebook...")
    run_facebook_loop(post, cookies, comments, delays)

def send_gmail(email, password, to_email, subject, message):
    try:
        msg = MIMEMultipart()
        msg['From'] = email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, to_email, msg.as_string())
        server.quit()
        return True, "Gửi thành công"
    except Exception as e:
        return False, str(e)

def treo_gmail():
    transition_screen("TREO GMAIL")
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.CYAN + f"[{current_time}] === TREO GMAIL - GỬI MAIL LIÊN TỤC ===")
    sender_emails_input = input_with_done("Nhập email gửi (cách nhau bởi dấu ,)")
    if not sender_emails_input:
        return
    sender_emails = [email.strip() for email in sender_emails_input.split(",") if email.strip()]
    if not sender_emails:
        print(Fore.RED + "❌ Không có email gửi!")
        return
    passwords_input = input_with_done("Nhập mật khẩu (cách nhau bởi dấu ,)")
    if not passwords_input:
        return
    passwords = [pwd.strip() for pwd in passwords_input.split(",") if pwd.strip()]
    if len(passwords) != len(sender_emails):
        print(Fore.RED + "❌ Số lượng mật khẩu phải bằng số lượng email!")
        return
    receiver_emails_input = input_with_done("Nhập email nhận (cách nhau bởi dấu ,)")
    if not receiver_emails_input:
        return
    receiver_emails = [email.strip() for email in receiver_emails_input.split(",") if email.strip()]
    if not receiver_emails:
        print(Fore.RED + "❌ Không có email nhận!")
        return
    files = []
    while True:
        fn = input(Fore.YELLOW + "Nhập file ngôn treo (Enter để kết thúc): ").strip()
        if not fn:
            break
        files.append(fn)
    messages = read_messages_from_files(files, read_lines=False)
    if not messages:
        print(Fore.RED + "❌ Không có nội dung!")
        return
    full_message = "\n".join(messages)
    subject = input(Fore.YELLOW + "Nhập tiêu đề mail: ").strip()
    if not subject:
        subject = "Thư tự động từ TOOL"
    delay = input_int("Nhập delay (giây): ", 2)
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.GREEN + f"[{current_time}] === BẮT ĐẦU TREO GMAIL ===")
    def gmail_worker(email, password, receivers, subj, msg, delay_sec, stop_event):
        ok = 0
        fail = 0
        start = datetime.now()
        consecutive_fail = 0
        while not stop_event.is_set():
            try:
                for receiver in receivers:
                    if stop_event.is_set():
                        break
                    success, result = send_gmail(email, password, receiver, subj, msg)
                    if success:
                        ok += 1
                        consecutive_fail = 0
                        treo_tabs[threading.current_thread()]['status'] = "🟢 Đang gửi"
                        current_time = datetime.now().strftime("%H:%M:%S")
                        print(Fore.GREEN + f"[{current_time}] [{ok}] ✅ Gửi thành công từ {email} đến {receiver}")
                    else:
                        fail += 1
                        consecutive_fail += 1
                        if consecutive_fail >= 3:
                            treo_tabs[threading.current_thread()]['status'] = "🔴 Lỗi xác thực"
                        else:
                            treo_tabs[threading.current_thread()]['status'] = "🟡 Lỗi tạm thời"
                        current_time = datetime.now().strftime("%H:%M:%S")
                        print(Fore.RED + f"[{current_time}] [{fail}] ❌ Gửi thất bại từ {email} đến {receiver}: {result}")
                    treo_tabs[threading.current_thread()].update({
                        'ok': ok,
                        'fail': fail,
                        'uptime': (datetime.now() - start).total_seconds()
                    })
                    for i in range(delay_sec, 0, -1):
                        if stop_event.is_set():
                            break
                        sys.stdout.write(f"\r{Fore.YELLOW}⏳ Chờ {i}s để gửi tiếp... {Fore.RESET}")
                        sys.stdout.flush()
                        time.sleep(1)
                    print("\r" + " " * 50 + "\r", end="")
            except Exception as e:
                fail += 1
                consecutive_fail += 1
                treo_tabs[threading.current_thread()]['status'] = f"🔴 Lỗi: {str(e)[:50]}"
                time.sleep(delay_sec)
    for i, (email, password) in enumerate(zip(sender_emails, passwords)):
        stop_event = threading.Event()
        t = threading.Thread(target=gmail_worker, args=(email, password, receiver_emails, subject, full_message, delay, stop_event), daemon=True)
        treo_tabs[t] = {
            'app': "Gmail",
            'type': "Treo",
            'box_id': f"From: {email}",
            'start_time': datetime.now(),
            'ok': 0,
            'fail': 0,
            'uptime': 0,
            'stop_event': stop_event,
            'status': "🟢 Đang gửi"
        }
        t.start()
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.GREEN + f"[{current_time}] [✓] Đã khởi chạy {len(sender_emails)} task Treo Gmail")
    print(Fore.CYAN + "🎯 Chạy ẩn ngoài menu - Dùng 'Xem / Dừng Tab Treo' để quản lý")
    time.sleep(2)

def nhay_gmail():
    transition_screen("NHÂY GMAIL")
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.CYAN + f"[{current_time}] === NHÂY GMAIL - GỬI MAIL TỪ NHÂY.TXT ===")
    sender_emails_input = input_with_done("Nhập email gửi (cách nhau bởi dấu ,)")
    if not sender_emails_input:
        return
    sender_emails = [email.strip() for email in sender_emails_input.split(",") if email.strip()]
    if not sender_emails:
        print(Fore.RED + "❌ Không có email gửi!")
        return
    passwords_input = input_with_done("Nhập mật khẩu (cách nhau bởi dấu ,)")
    if not passwords_input:
        return
    passwords = [pwd.strip() for pwd in passwords_input.split(",") if pwd.strip()]
    if len(passwords) != len(sender_emails):
        print(Fore.RED + "❌ Số lượng mật khẩu phải bằng số lượng email!")
        return
    receiver_emails_input = input_with_done("Nhập email nhận (cách nhau bởi dấu ,)")
    if not receiver_emails_input:
        return
    receiver_emails = [email.strip() for email in receiver_emails_input.split(",") if email.strip()]
    if not receiver_emails:
        print(Fore.RED + "❌ Không có email nhận!")
        return
    messages = read_messages_from_files([], default_file="nhay.txt", read_lines=True)
    if not messages:
        print(Fore.RED + "❌ Không tìm thấy nội dung trong nhay.txt!")
        return
    subject = input(Fore.YELLOW + "Nhập tiêu đề mail: ").strip()
    if not subject:
        subject = "Thư tự động từ TOOL"
    delay = input_int("Nhập delay (giây): ", 2)
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.GREEN + f"[{current_time}] === BẮT ĐẦU NHÂY GMAIL ===")
    print(Fore.YELLOW + f"📝 Sử dụng {len(messages)} dòng từ nhay.txt")
    def nhay_gmail_worker(email, password, receivers, subj, msgs_list, delay_sec, stop_event):
        ok = 0
        fail = 0
        start = datetime.now()
        consecutive_fail = 0
        msg_index = 0
        while not stop_event.is_set():
            try:
                for receiver in receivers:
                    if stop_event.is_set():
                        break
                    if msg_index >= len(msgs_list):
                        msg_index = 0
                    message = msgs_list[msg_index]
                    msg_index += 1
                    success, result = send_gmail(email, password, receiver, subj, message)
                    if success:
                        ok += 1
                        consecutive_fail = 0
                        treo_tabs[threading.current_thread()]['status'] = "🟢 Đang nhây"
                        current_time = datetime.now().strftime("%H:%M:%S")
                        print(Fore.GREEN + f"[{current_time}] [{ok}] ✅ Nhây thành công từ {email} đến {receiver}: {message[:50]}...")
                    else:
                        fail += 1
                        consecutive_fail += 1
                        if consecutive_fail >= 3:
                            treo_tabs[threading.current_thread()]['status'] = "🔴 Lỗi xác thực"
                        else:
                            treo_tabs[threading.current_thread()]['status'] = "🟡 Lỗi tạm thời"
                        current_time = datetime.now().strftime("%H:%M:%S")
                        print(Fore.RED + f"[{current_time}] [{fail}] ❌ Nhây thất bại từ {email}: {result}")
                    treo_tabs[threading.current_thread()].update({
                        'ok': ok,
                        'fail': fail,
                        'uptime': (datetime.now() - start).total_seconds()
                    })
                    for i in range(delay_sec, 0, -1):
                        if stop_event.is_set():
                            break
                        sys.stdout.write(f"\r{Fore.YELLOW}⏳ Chờ {i}s để nhây tiếp... {Fore.RESET}")
                        sys.stdout.flush()
                        time.sleep(1)
                    print("\r" + " " * 50 + "\r", end="")
            except Exception as e:
                fail += 1
                consecutive_fail += 1
                treo_tabs[threading.current_thread()]['status'] = f"🔴 Lỗi: {str(e)[:50]}"
                time.sleep(delay_sec)
    for i, (email, password) in enumerate(zip(sender_emails, passwords)):
        stop_event = threading.Event()
        t = threading.Thread(target=nhay_gmail_worker, args=(email, password, receiver_emails, subject, messages, delay, stop_event), daemon=True)
        treo_tabs[t] = {
            'app': "Gmail",
            'type': "Nhây",
            'box_id': f"From: {email}",
            'start_time': datetime.now(),
            'ok': 0,
            'fail': 0,
            'uptime': 0,
            'stop_event': stop_event,
            'status': "🟢 Đang nhây"
        }
        t.start()
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.GREEN + f"[{current_time}] [✓] Đã khởi chạy {len(sender_emails)} task Nhây Gmail")
    print(Fore.CYAN + "🎯 Chạy ẩn ngoài menu - Dùng 'Xem / Dừng Tab Treo' để quản lý")
    time.sleep(2)

try:
    import cloudscraper
    from fake_useragent import UserAgent
except:
    os.system("pip install cloudscraper fake-useragent")
    import cloudscraper
    from fake_useragent import UserAgent

def golike_instagram():
    transition_screen("GOLIKE INSTAGRAM")
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.CYAN + f"[{current_time}] === GOLIKE INSTAGRAM ===")
    ua_golike = UserAgent()
    def delay_golike(sec):
        for i in range(sec, -1, -1):
            sys.stdout.write(f"\r{Fore.YELLOW}[⏳️] ➜ Đang chờ {i}s.. ")
            sys.stdout.flush()
            time.sleep(1)
        print()
    def select_parse_golike(inp):
        return [int(i) for i in re.split(r"[+, ]+", inp.strip()) if i.isdigit()]
    def require_input_golike(prompt, allow_empty=False):
        while True:
            value = input(prompt).strip()
            if not allow_empty and not value:
                print(Fore.RED + "[❌] ➜ Trường này không được để trống!")
            else:
                return value
    os.system("cls" if os.name == "nt" else "clear")
    print(Fore.CYAN + "════════════════════════════════════════════════")
    print(Fore.MAGENTA + " ⚜️ TOOL GOLIKE INSTAGRAM - NEWBIE VIẾT CODE ⚜️")
    print(Fore.CYAN + "════════════════════════════════════════════════")
    auth = require_input_golike(Fore.WHITE + "[🐷] ➜ Nhập Authorization: ")
    t = require_input_golike(Fore.WHITE + "[🐷] ➜ Nhập T: ")
    scraper = cloudscraper.create_scraper()
    headers = {"Authorization": auth, "T": t, "Content-Type": "application/json;charset=utf-8"}
    try:
        r = scraper.get("https://gateway.golike.net/api/users/me", headers=headers, timeout=20).json()
    except:
        print(Fore.RED + "[❌] ➜ Đăng nhập thất bại!")
        return
    if r.get("status") != 200:
        print(Fore.RED + "[❌] ➜ Đăng nhập thất bại!")
        return
    print(Fore.GREEN + "[✅] ➜ Đăng nhập thành công!")
    user = r["data"]
    print(Fore.CYAN + f"[🔍] ➜ Tài khoản: {user['username']} | Số dư: {user['coin']}")
    accs = scraper.get("https://gateway.golike.net/api/instagram-account", headers=headers, timeout=20).json()
    if accs.get("status") != 200 or not accs.get("data"):
        print(Fore.RED + "[❌] ➜ Không tìm thấy tài khoản Instagram nào.")
        return
    data = accs["data"]
    print(Fore.MAGENTA + "[👀] ➜ Danh sách tài khoản Instagram hiện có:")
    for i, a in enumerate(data, 1):
        print(Fore.BLUE + f"[⚜️] ➜ {i}. {a['instagram_username']}")
    while True:
        sel = select_parse_golike(require_input_golike(Fore.WHITE + "[🐷] ➜ Vui lòng chọn tài khoản chạy (1 hoặc 1+2+3): "))
        if sel:
            break
        else:
            print(Fore.RED + "[❌] ➜ Vui lòng chọn ít nhất một tài khoản hợp lệ!")
    cookies = []
    for i in sel:
        name = data[i - 1]['instagram_username']
        cookie = require_input_golike(Fore.YELLOW + f"[🐷] ➜ Nhập cookie của tài khoản {name}: ")
        cookies.append(cookie)
    def get_int_input_golike(prompt, default):
        value = input(prompt).strip()
        return int(value) if value.isdigit() else default
    num_task = get_int_input_golike(Fore.YELLOW + "[🐷] ➜ Nhập số nhiệm vụ muốn làm (mặc định 50): ", 50)
    delay_sec = get_int_input_golike(Fore.YELLOW + "[🐷] ➜ Nhập delay giữa mỗi nhiệm vụ (mặc định 30s): ", 30)
    rest_after = get_int_input_golike(Fore.YELLOW + "[🐷] ➜ Nghỉ ngơi sau bao nhiêu nhiệm vụ (0 = bỏ qua): ", 0)
    rest_time = get_int_input_golike(Fore.YELLOW + "[🐷] ➜ Nghỉ ngơi bao nhiêu giây (0 = bỏ qua): ", 0)
    change_after = get_int_input_golike(Fore.YELLOW + "[🐷] ➜ Đổi tài khoản sau bao nhiêu nhiệm vụ (0 = bỏ qua): ", 0)
    auto_change = require_input_golike(Fore.YELLOW + "[🐷] ➜ Tự đổi tài khoản khi hết nhiệm vụ không (y/n): ").lower() == "y"
    total_done = 0
    for n, i in enumerate(sel):
        acc = data[i - 1]
        cookie = cookies[n]
        name = acc['instagram_username']
        id_acc = acc['id']
        print(Fore.CYAN + f"[⚙️] ➜ Đang chạy tài khoản {name}")
        suc = fai = earned = 0
        for task_count in range(1, num_task + 1):
            try:
                job = scraper.get(f"https://gateway.golike.net/api/advertising/publishers/instagram/jobs?instagram_account_id={id_acc}&data=null", headers=headers, timeout=20).json()
                if job.get("status") != 200 or not job.get("data"):
                    if auto_change:
                        print(Fore.MAGENTA + f"[⏭️] ➜ Đang chuyển sang tài khoản tiếp theo..")
                        break
                    else:
                        print(Fore.YELLOW + f"[❌] ➜ Hết nhiệm vụ, dừng tài khoản {name}")
                        return
                j = job["data"]
                jid, oid, jtype = j["id"], j["object_id"], j["type"].lower()
                csrf_token = ""
                if "csrftoken=" in cookie:
                    csrf_token = cookie.split("csrftoken=")[1].split(";")[0]
                insta_headers = {
                    'accept': '*/*',
                    'accept-language': 'vi,en-US;q=0.9,en;q=0.8',
                    'content-type': 'application/x-www-form-urlencoded',
                    'cookie': cookie,
                    'origin': 'https://www.instagram.com',
                    'priority': 'u=1, i',
                    'referer': 'https://www.instagram.com/',
                    'sec-ch-prefers-color-scheme': 'dark',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': ua_golike.random,
                    'x-asbd-id': '129477',
                    'x-csrftoken': csrf_token,
                    'x-ig-app-id': '936619743392459',
                    'x-ig-www-claim': '0',
                    'x-instagram-ajax': '1014868636',
                    'x-requested-with': 'XMLHttpRequest'
                }
                ok = False
                if jtype == "follow":
                    r = requests.post(f"https://www.instagram.com/api/v1/friendships/create/{oid}/", headers=insta_headers)
                    ok = r.status_code == 200
                elif jtype == "like":
                    r = requests.post(f"https://www.instagram.com/api/v1/web/likes/{oid}/like/", headers=insta_headers)
                    ok = r.status_code == 200
                time.sleep(1)
                if ok:
                    done = scraper.post("https://gateway.golike.net/api/advertising/publishers/instagram/complete-jobs",
                                        headers=headers,
                                        json={"instagram_account_id": id_acc,
                                              "instagram_users_advertising_id": jid,
                                              "async": True,
                                              "data": "null"}).json()
                    if done.get("success"):
                        money = done["data"]["prices"]
                        suc += 1
                        earned += money
                        print(Fore.GREEN + f"[⚜️] ➜ [{task_count}] Thành công | {jtype.capitalize()} | ID: {oid} | +{money} | Tổng: {earned}")
                    else:
                        fai += 1
                        print(Fore.RED + f"[⚜️] ➜ [{task_count}] Thất bại | {jtype.capitalize()} | ID: {oid} | Tổng: {earned}")
                else:
                    fai += 1
                    print(Fore.RED + f"[⚜️] ➜ [{task_count}] Thất bại | {jtype.capitalize()} | ID: {oid} | Tổng: {earned}")
                total_done += 1
                delay_golike(delay_sec)
                if rest_after > 0 and total_done % rest_after == 0:
                    delay_golike(rest_time)
                if change_after > 0 and total_done % change_after == 0:
                    print(Fore.MAGENTA + f"[⏭️] ➜ Đang chuyển sang tài khoản tiếp theo..")
                    break
            except:
                fai += 1
                delay_golike(3)
                continue
        print(Fore.GREEN + f"[🎉] ➜ Hoàn thành | Nhiệm vụ: {suc + fai} | Thành công: {suc} | Thất bại: {fai} | Kiếm được: {earned} | Tổng: {earned}")

def get_joined_groups_share(token: str):
    url = "https://graph.facebook.com/v15.0/me/groups"
    params = {"access_token": token, "limit": "1000"}
    try:
        res = requests.get(url, params=params, timeout=10)
        data = res.json()
        groups = []
        if "data" in data:
            for g in data["data"]:
                groups.append(g.get("id"))
        return groups
    except:
        return []

def share_post_to_group_share(token: str, post_id: str, group_id: str):
    url = f"https://graph.facebook.com/{group_id}/feed"
    params = {
        "access_token": token,
        "link": f"https://www.facebook.com/{post_id}"
    }
    try:
        res = requests.post(url, data=params, timeout=10)
        return res.json()
    except:
        return {"error": "Thất bại!"}

def share_facebook_worker(cookie, post_id, group_ids, delay, stop_event):
    token = get_token(cookie)
    if not token:
        return
    ok = 0
    fail = 0
    start = datetime.now()
    consecutive_fail = 0
    while not stop_event.is_set():
        random.shuffle(group_ids)
        for gid in group_ids:
            if stop_event.is_set():
                break
            result = share_post_to_group_share(token, post_id, gid)
            group_link = f"https://facebook.com/groups/{gid}"
            if "id" in result:
                ok += 1
                consecutive_fail = 0
                treo_tabs[threading.current_thread()]['status'] = "🟢 Đang share"
                current_time = datetime.now().strftime("%H:%M:%S")
                print(Fore.GREEN + f"[{current_time}] [{ok}] ✅ Share thành công | Link: {group_link}")
            else:
                fail += 1
                consecutive_fail += 1
                if consecutive_fail >= 5:
                    treo_tabs[threading.current_thread()]['status'] = "🔴 Rớt (fail nhiều)"
                else:
                    treo_tabs[threading.current_thread()]['status'] = "🟡 Lỗi tạm thời"
                current_time = datetime.now().strftime("%H:%M:%S")
                print(Fore.RED + f"[{current_time}] [{fail}] ❌ Share thất bại | Link: {group_link} | Lỗi: {result.get('error', 'Không xác định')}")
            treo_tabs[threading.current_thread()].update({
                'ok': ok,
                'fail': fail,
                'uptime': (datetime.now() - start).total_seconds()
            })
            for i in range(delay, 0, -1):
                if stop_event.is_set():
                    break
                sys.stdout.write(f"\r{Fore.YELLOW}⏳ Chờ {i}s để share tiếp... {Fore.RESET}")
                sys.stdout.flush()
                time.sleep(1)
            print("\r" + " " * 50 + "\r", end="")

def start_share_facebook(cookie, post_id, group_ids, delay):
    stop_event = threading.Event()
    t = threading.Thread(target=share_facebook_worker, args=(cookie, post_id, group_ids, delay, stop_event), daemon=True)
    treo_tabs[t] = {
        'app': "Facebook",
        'type': "Share",
        'box_id': f"Post: {post_id}",
        'start_time': datetime.now(),
        'ok': 0,
        'fail': 0,
        'uptime': 0,
        'stop_event': stop_event,
        'status': "🟢 Đang share"
    }
    t.start()
    return t

def share_facebook():
    transition_screen("SHARE FACEBOOK")
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.CYAN + f"[{current_time}] === TOOL SHARE FACEBOOK ===")
    cookie_input = input_with_done("Nhập Cookie Facebook")
    if not cookie_input:
        return
    cookies = list_from(cookie_input)
    if not cookies:
        print(Fore.RED + "❌ Không có cookie!")
        return
    token = get_token(cookies[0])
    if not token:
        print(Fore.RED + "❌ Không lấy được token, vui lòng thử lại!")
        return
    print(Fore.CYAN + "\nVui Lòng Lựa Chọn:")
    print(Fore.YELLOW + "1. Nhập ID Nhóm Thủ Công")
    print(Fore.YELLOW + "2. Tự Động Lấy Tất Cả ID Nhóm Đã Tham Gia")
    choice = input(Fore.WHITE + "Nhập Lựa Chọn (1/2): ").strip()
    group_ids = []
    if choice == "1":
        group_input = input_with_done("Nhập ID Nhóm")
        if group_input:
            group_ids = list_from(group_input)
    elif choice == "2":
        print(Fore.CYAN + "Đang lấy danh sách nhóm...")
        group_ids = get_joined_groups_share(token)
        print(Fore.GREEN + f"✅ Đã lấy được {len(group_ids)} nhóm")
    else:
        print(Fore.RED + "❌ Lựa chọn không hợp lệ!")
        return
    if not group_ids:
        print(Fore.RED + "❌ Không có nhóm nào để share!")
        return
    post_input = input_with_done("Nhập ID Bài Viết Cần Share")
    if not post_input:
        return
    post_id = first_line(post_input)
    delay_input = input_with_done("Nhập Delay Share (giây)")
    delay = int(first_line(delay_input)) if delay_input and first_line(delay_input).isdigit() else 5
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.GREEN + f"[{current_time}] === BẮT ĐẦU SHARE ===")
    print(Fore.YELLOW + "📊 Task sẽ chạy ẩn ngoài menu với uptime tracking")
    print(Fore.YELLOW + "🔗 Link group sẽ được hiển thị khi share")
    print(Fore.YELLOW + "🔍 Dùng chức năng 'Xem / Dừng Tab Treo' để quản lý")
    for cookie in cookies:
        start_share_facebook(cookie, post_id, group_ids, delay)
    current_time = datetime.now().strftime("%H:%M:%S")
    print(Fore.GREEN + f"[{current_time}] [✓] Đã khởi chạy {len(cookies)} task Share Facebook")
    print(Fore.CYAN + "🎯 Chạy ẩn ngoài menu - Dùng 'Xem / Dừng Tab Treo' để quản lý")
    time.sleep(2)

def rainbow_text(text):
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    result = ""
    for i, char in enumerate(text):
        result += colors[i % len(colors)] + char
    return result

def animated_banner():
    clear()
    banner_lines = [
        "╔════════════════════════════════════════════╗",
        "║                                            ║",
        "║  ██████╗  █████╗ ████████╗██╗  ██╗         ║",
        "║  ██╔══██╗██╔══██╗╚══██╔══╝██║ ██╔╝         ║",
        "║  ██║  ██║███████║   ██║   █████╔╝          ║",
        "║  ██║  ██║██╔══██║   ██║   ██╔═██╗          ║",
        "║  ██████╔╝██║  ██║   ██║   ██║  ██╗         ║",
        "║                                            ║",
        "║           Chak Là DATK x DATK             ║",
        "║                                            ║",
        "╚════════════════════════════════════════════╝"
    ]
    
    for line in banner_lines:
        print(rainbow_text(line))
        time.sleep(0.05)

def main_menu():
    def clear():
        os.system("cls" if os.name == "nt" else "clear")
    
    def rainbow_text(text):
        colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
        result = ""
        for i, char in enumerate(text):
            result += colors[i % len(colors)] + char
        return result

    while True:
        clear()
        
        colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
        bright_colors = [Fore.LIGHTRED_EX, Fore.LIGHTYELLOW_EX, Fore.LIGHTGREEN_EX, 
                        Fore.LIGHTCYAN_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX]
        
        # Header chắc chắn
        print(f"\n{Fore.WHITE}▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓")
        print(f"{bright_colors[0]}▓ {bright_colors[1]}T O O L   D A T K   -   W A R   x Tiện Ích{bright_colors[5]}")
        print(f"{bright_colors[2]}▓ {bright_colors[3]}5 A P P - 1 W E B{bright_colors[4]}")
        print(f"{Fore.WHITE}▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓")
        
        # Phần MESSENGER
        print(f"{bright_colors[0]}▓◄►►►►►►►►►►► {bright_colors[1]}M E S S E N G E R {bright_colors[0]}◄►►►►►►►►►►►▓")
        print(f"{bright_colors[0]}▓ {bright_colors[1]}1. {bright_colors[2]}Treo ngôn mess{' ' * 35}{bright_colors[0]}")
        print(f"{bright_colors[0]}▓ {bright_colors[1]}2. {bright_colors[2]}Nhây mess{' ' * 40}{bright_colors[0]}")
        print(f"{bright_colors[0]}▓ {bright_colors[1]}3. {bright_colors[2]}Réo Mess{' ' * 41}{bright_colors[0]}")
        print(f"{bright_colors[0]}▓ {bright_colors[1]}4. {bright_colors[2]}Sớ Mess{' ' * 43}{bright_colors[0]}")
        print(f"{bright_colors[0]}▓ {bright_colors[1]}5. {bright_colors[2]}Nhây tag mess{' ' * 37}{bright_colors[0]}")
        
        # Phần DISCORD
        print(f"{bright_colors[1]}▓◄►►►►►►►►►►►►► {bright_colors[2]}D I S C O R D {bright_colors[1]}◄►►►►►►►►►►►►▓")
        print(f"{bright_colors[1]}▓ {bright_colors[2]}6. {bright_colors[3]}Treo Discord{' ' * 37}{bright_colors[1]}")
        print(f"{bright_colors[1]}▓ {bright_colors[2]}7. {bright_colors[3]}Nhây Discord{' ' * 38}{bright_colors[1]}")
        print(f"{bright_colors[1]}▓ {bright_colors[2]}8. {bright_colors[3]}Nhây Tag Discord{' ' * 34}{bright_colors[1]}")
        print(f"{bright_colors[1]}▓ {bright_colors[2]}9. {bright_colors[3]}Sớ Tag Discord{' ' * 35}{bright_colors[1]}")
        print(f"{bright_colors[1]}▓ {bright_colors[2]}10.{bright_colors[3]} Poll Discord{' ' * 37}{bright_colors[1]}")
        
        # Phần TELEGRAM
        print(f"{bright_colors[2]}▓◄►►►►►►►►►►► {bright_colors[3]}T E L E G R A M {bright_colors[2]}◄►►►►►►►►►►►▓")
        print(f"{bright_colors[2]}▓ {bright_colors[3]}11.{bright_colors[4]} Treo Telegram{' ' * 35}{bright_colors[2]}")
        print(f"{bright_colors[2]}▓ {bright_colors[3]}12.{bright_colors[4]} Nhây Telegram{' ' * 36}{bright_colors[2]}")
        
        # Phần FACEBOOK
        print(f"{bright_colors[3]}▓◄►►►►►►►►►►► {bright_colors[4]}F A C E B O O K {bright_colors[3]}◄►►►►►►►►►►►▓")
        print(f"{bright_colors[3]}▓ {bright_colors[4]}13.{bright_colors[5]} Treo Top Facebook{' ' * 32}{bright_colors[3]}")
        print(f"{bright_colors[3]}▓ {bright_colors[4]}14.{bright_colors[5]} Nhây Top Facebook{' ' * 33}{bright_colors[3]}")
        print(f"{bright_colors[3]}▓ {bright_colors[4]}15.{bright_colors[5]} Sớ Top Facebook{' ' * 34}{bright_colors[3]}")
        print(f"{bright_colors[3]}▓ {bright_colors[4]}16.{bright_colors[5]} Share Facebook{' ' * 35}{bright_colors[3]}")
        
        # Phần GMAIL
        print(f"{bright_colors[4]}▓◄►►►►►►►►►►►►► {bright_colors[5]}G M A I L {bright_colors[4]}◄►►►►►►►►►►►►►▓")
        print(f"{bright_colors[4]}▓ {bright_colors[5]}17.{bright_colors[0]} Treo Gmail{' ' * 39}{bright_colors[4]}")
        print(f"{bright_colors[4]}▓ {bright_colors[5]}18.{bright_colors[0]} Nhây Gmail{' ' * 40}{bright_colors[4]}")
        
        # Phần chức năng khác
        print(f"{bright_colors[5]}▓◄►►►►►►►►►► {bright_colors[0]}C H Ứ C  N Ă N G  K H Á C {bright_colors[5]}◄►►►►►►►►▓")
        print(f"{bright_colors[5]}▓ {bright_colors[0]}19.{bright_colors[1]} Golike Instagram{' ' * 33}{bright_colors[5]}")
        print(f"{bright_colors[5]}▓ {bright_colors[0]}00.{bright_colors[2]} Xem / Dung Tab Treo{' ' * 29}{bright_colors[5]}")
        print(f"{bright_colors[5]}▓ {bright_colors[0]}99.{bright_colors[3]} Datk Facebook{' ' * 35}{bright_colors[5]}")
        print(f"{bright_colors[5]}▓ {bright_colors[0]} 0.{bright_colors[4]} Thoat{' ' * 43}{bright_colors[5]}")
        
        # Footer
        print(f"{Fore.WHITE}▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓")
        print(f"{bright_colors[1]}▓ {bright_colors[2]}LƯU Ý: {bright_colors[3]}Tool Đéo Chống Die Acc {bright_colors[4]}• {bright_colors[5]} Datk(◍⁠•⁠ᴗ⁠•⁠◍⁠)⁠❤{bright_colors[0]} ")
        print(f"{Fore.WHITE}▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓")
        
        choice = input(f"\n{bright_colors[3]}➤ Chọn chức năng: {bright_colors[5]}").strip()
        
        if choice == "1": 
            treo_mess()
        elif choice == "2": 
            nhay_mess()
        elif choice == "3": 
            reo_mess()
        elif choice == "4": 
            so_mess()
        elif choice == "5": 
            nhay_tag_mess()
        elif choice == "6": 
            treo_discord()
        elif choice == "7": 
            nhay_discord()
        elif choice == "8": 
            nhay_discord_tag()
        elif choice == "9": 
            sotagdis()
        elif choice == "10": 
            polldis()
        elif choice == "11": 
            treo_telegram()
        elif choice == "12": 
            nhay_telegram()
        elif choice == "13": 
            treo_top_facebook()
        elif choice == "14": 
            nhay_top_facebook()
        elif choice == "15": 
            so_top_facebook()
        elif choice == "16": 
            share_facebook()
        elif choice == "17": 
            treo_gmail()
        elif choice == "18": 
            nhay_gmail()
        elif choice == "19": 
            golike_instagram()
        elif choice == "00": 
            xem_dung_treo()
        elif choice == "99":
            webbrowser.open("https://www.facebook.com/DvierAlex/")
        elif choice == "0":
            print(f"\n{bright_colors[2]}👋 OK BYE")
            break
        else:
            print(f"{bright_colors[0]}❌ CHỌN SAI RỒI")
            time.sleep(1)
def main():
    try:
        key_valid, message = check_key_system()
        if not key_valid:
            print(f"\n{Fore.RED}❌ {message}")
            input(f"{Fore.YELLOW}Nhan Enter de thoat...")
            return
            
        print(f"\n{Fore.GREEN}✅ {message}")
        time.sleep(1)
        
        colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
        
        print(f"\n{Fore.CYAN}╔{'═' * 58}╗")
        print(f"║{Fore.YELLOW}{'Tool gộp By DATK'.center(58)}{Fore.CYAN}║")
        print(f"╚{'═' * 58}╝")
        
        kael_art = [
        "  ██████   █████   ██████  ██   ██ ",
        "  ██   ██ ██   ██ ██    ██ ██  ██  ",
        "  ██   ██ ███████ ██    ██ █████   ",
        "  ██   ██ ██   ██ ██    ██ ██  ██  ",
        "  ██████  ██   ██  ██████  ██   ██ ",
    ]
        
        for i, line in enumerate(kael_art):
            color = colors[i % len(colors)]
            print(f"{color}{line}")
            time.sleep(0.15)
        
        print(f"\n{Fore.CYAN}{'─' * 58}")
        
        spinner_frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        for i in range(25):
            color = colors[i % len(colors)]
            percent = (i + 1) * 4
            bar = "█" * (i + 1) + "░" * (25 - i - 1)
            sys.stdout.write(f"\r{color}{spinner_frames[i % 10]} Đang tải: [{bar}] {percent}%")
            sys.stdout.flush()
            time.sleep(0.08)
        
        print(f"\r{Fore.GREEN}✅ Khởi động thành công!{' ' * 30}")
        
        time.sleep(1)
        main_menu()
        
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}DỪNG RỒI")
    except Exception as e:
        print(f"\n{Fore.RED}LỖI NÈ: {e}")
        input(f"{Fore.YELLOW}Nhan Enter de thoat")

if __name__ == "__main__":
    main()
