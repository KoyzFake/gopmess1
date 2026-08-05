import os
import sys
import time
import json
import random
import multiprocessing
from datetime import datetime
import requests
from colorama import Fore, Style, init
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from zlapi import ZaloAPI
from zlapi.models import Message, ThreadType
import pyfiglet
import traceback

DEBUG_FILE = "debug.log"

def save_debug(title, data):
    with open(DEBUG_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n===== {title} =====\n{data}\n")

init(autoreset=True)
console = Console()


def get_rainbow_color(index, total):
    colors = [
        "bright_red", "red", "bright_yellow", "yellow", 
        "bright_green", "green", "bright_cyan", "cyan",
        "bright_blue", "blue", "bright_magenta", "magenta"
    ]
    return colors[index % len(colors)]


def create_banner():
    banner = pyfiglet.figlet_format('GIA BAO', font="slant")
    
    # Rainbow gradient cho banner
    lines = banner.split('\n')
    colored_banner = ""
    colors = ['bright_red', 'bright_yellow', 'bright_green', 'bright_cyan', 'bright_blue', 'bright_magenta']
    
    for i, line in enumerate(lines):
        color = colors[i % len(colors)]
        colored_banner += f"[{color}]{line}[/]\n"
    
    return f"""
[cyan]{'═'*70}[/]
{colored_banner}
[cyan]{'═'*70}[/]
[yellow]⏰ {time.strftime('%I:%M %p, %d/%m/%Y')}[/]
[bright_green]✅  Tool - địt mẹ m [/]
[bright_magenta]📧 By: Đỗ Tiến Đạt[/]
[cyan]{'═'*70}[/]
    """


def parse_cookie_string(cookie_input):
    cookie_dict = {}
    
    if cookie_input.strip().startswith('{'):
        try:
            cookie_dict = eval(cookie_input)
            if isinstance(cookie_dict, dict):
                return cookie_dict
        except:
            pass
    
    if ';' in cookie_input or '=' in cookie_input:
        try:
            pairs = cookie_input.split(';')
            for pair in pairs:
                if '=' in pair:
                    key, value = pair.strip().split('=', 1)
                    cookie_dict[key.strip()] = value.strip()
            if cookie_dict:
                return cookie_dict
        except:
            pass
    
    try:
        cookie_dict = json.loads(cookie_input)
        if isinstance(cookie_dict, dict):
            return cookie_dict
    except:
        pass
    
    return None


class ZaloBotFixed(ZaloAPI):
    
    def __init__(self, api_key, secret_key, imei, session_cookies, delay=3):
        if isinstance(session_cookies, str):
            session_cookies = parse_cookie_string(session_cookies)
            if not session_cookies:
                raise ValueError("Cookie không hợp lệ!")
        
        super().__init__(api_key, secret_key, imei, session_cookies)
        self.delay = delay
        self.user_info = None
        self.stats = {'success': 0, 'failed': 0, 'total': 0}
    
    def check_account_debug(self):
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[yellow]Đang kiểm tra tài khoản..."),
                console=console
            ) as progress:
                progress.add_task("check", total=None)
                
                profile = self.fetchAccountInfo()
                save_debug("fetchAccountInfo() Response", {
                    'type': str(type(profile)),
                    'data': str(profile)
                })
                
                if profile:
                    if hasattr(profile, 'profile'):
                        user_data = profile.profile
                    elif hasattr(profile, 'data'):
                        user_data = profile.data
                    elif isinstance(profile, dict):
                        user_data = profile
                    else:
                        console.print("[red]❌ Không đọc được thông tin profile[/]")
                        return False
                    
                    self.user_info = {
                        'name': (getattr(user_data, 'displayName', None) or 
                                getattr(user_data, 'zalo_name', None) or
                                user_data.get('displayName') if isinstance(user_data, dict) else None or
                                user_data.get('zalo_name') if isinstance(user_data, dict) else None or
                                'Unknown'),
                        'phone': (getattr(user_data, 'phoneNumber', None) or
                                 user_data.get('phoneNumber') if isinstance(user_data, dict) else None or
                                 'N/A'),
                        'uid': (getattr(user_data, 'userId', None) or
                               user_data.get('userId') if isinstance(user_data, dict) else None or
                               'N/A')
                    }
                    
                    save_debug("User Info", self.user_info)
                    
                    console.print()
                    console.print(Panel.fit(
                        f"[bold green]✅ TÀI KHOẢN HOẠT ĐỘNG[/]\n\n"
                        f"[cyan]👤 Tên:[/] [white bold]{self.user_info['name']}[/]\n"
                        f"[cyan]📱 SĐT:[/] [white]{self.user_info['phone']}[/]\n"
                        f"[cyan]🆔 UID:[/] [white]{self.user_info['uid']}[/]",
                        border_style="bold green",
                        title="[bold white]THÔNG TIN[/]"
                    ))
                    console.print()
                    
                    return True
                else:
                    console.print("[red]❌ Profile trống![/]")
                    return False
                    
        except Exception as e:
            console.print(f"[red]❌ Lỗi kiểm tra: {str(e)}[/]")
            save_debug("check_account_debug Exception", {
                'error': str(e),
                'traceback': __import__('traceback').format_exc()
            })
            return False
    
    def get_friends_debug(self):
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[yellow]Đang tải danh sách bạn bè..."),
                console=console
            ) as progress:
                progress.add_task("friends", total=None)
                
                friends_data = self.fetchAllFriends()
                save_debug("fetchAllFriends() Response", {
                    'type': str(type(friends_data)),
                    'length': len(friends_data) if friends_data else 0,
                })
                
                if not friends_data:
                    console.print("[red]❌ Không có dữ liệu bạn bè![/]")
                    return None
                
                friends_list = []
                
                if isinstance(friends_data, list):
                    for user_obj in friends_data:
                        try:
                            uid = getattr(user_obj, 'userId', None) or getattr(user_obj, 'uid', None)
                            name = (getattr(user_obj, 'displayName', None) or 
                                   getattr(user_obj, 'zaloName', None) or 
                                   getattr(user_obj, 'username', None) or 
                                   'Unknown')
                            
                            if uid:
                                friends_list.append({
                                    'uid': uid,
                                    'name': name
                                })
                        except:
                            continue
                
                elif isinstance(friends_data, dict):
                    if hasattr(friends_data, 'data'):
                        data = friends_data.data
                        if isinstance(data, dict):
                            for uid, info in data.items():
                                if isinstance(info, dict):
                                    friends_list.append({
                                        'uid': uid,
                                        'name': info.get('dName', 'Unknown')
                                    })
                    else:
                        for uid, info in friends_data.items():
                            if isinstance(info, dict):
                                friends_list.append({
                                    'uid': uid,
                                    'name': info.get('dName', 'Unknown')
                                })
                
                if friends_list:
                    console.print(f"[green]✅ Tìm thấy {len(friends_list)} bạn bè![/]")
                    save_debug("Parsed friends", {'count': len(friends_list)})
                    return friends_list
                else:
                    console.print("[yellow]⚠️ Không parse được bạn bè![/]")
                    return None
                    
        except Exception as e:
            console.print(f"[red]❌ Lỗi lấy bạn bè: {str(e)}[/]")
            save_debug("get_friends_debug Exception", __import__('traceback').format_exc())
            return None
    
    def send_to_friend(self, uid, message):
        try:
            self.send(
                Message(text=message),
                thread_id=uid,
                thread_type=ThreadType.USER
            )
            return True
        except Exception as e:
            save_debug(f"send_to_friend({uid}) error", str(e))
            return False
    
    def spam_friends(self, friends, messages):
        """Vòng lặp spam với rainbow effect"""
        msg_idx = 0
        try:
            console.print(f"\n[bold green]{'═'*70}[/]")
            console.print(f"[bold yellow]🚀đang địt mẹ  - {len(friends)} BẠN BÈ[/]")
            console.print(f"[bold green]{'═'*70}[/]\n")
            
            while True:
                for idx, f in enumerate(friends):
                    try:
                        msg = messages[msg_idx % len(messages)]
                        ok = self.send_to_friend(f['uid'], msg)
                        
                        self.stats['total'] += 1
                        
                        color = get_rainbow_color(idx, len(friends))
                        
                        if ok:
                            self.stats['success'] += 1
                            console.print(f"[green]✅[/] [{color}]{f['name'][:30]:<30}[/] [dim]| {msg[:35]}...[/]")
                        else:
                            self.stats['failed'] += 1
                            console.print(f"[red]❌[/] [{color}]{f['name'][:30]:<30}[/] [dim]| Lỗi gửi[/]")
                        
                        msg_idx += 1
                        time.sleep(max(1, self.delay + random.uniform(-0.3, 0.3)))
                    except KeyboardInterrupt:
                        raise
                    except Exception as e:
                        console.print(f"[yellow]⚠️ {str(e)[:50]}[/]")
                        time.sleep(2)
        except KeyboardInterrupt:
            console.print("\n[yellow]⏹️ địt mẹ m đã tha cn chó chết![/]")
        
        self.show_stats()
    
    def show_stats(self):

        console.print()
        console.print(Panel.fit(
            f"[bold cyan]📊 THỐNG KÊ địt mẹ m [/]\n\n"
            f"[bright_green]✅ số lần Thành công địt mẹ nó:[/] [white bold]{self.stats['success']}[/]\n"
            f"[bright_red]❌ số lầnThất bại địt mẹ nó:[/] [white]{self.stats['failed']}[/]\n"
            f"[bright_yellow]📨 Tổng số lần địt mẹ nó :[/] [white]{self.stats['total']}[/]\n"
            f"[bright_magenta]📈 Tỉ lệ địt mẹ nó :[/] [white bold]{(self.stats['success']/max(1,self.stats['total'])*100):.1f}%[/]",
            border_style="cyan",
            title="[bold white]KẾT QUẢ[/]"
        ))


def parse_selection(s, max_idx):
    try:
        nums = []
        for part in s.split(','):
            part = part.strip()
            if '-' in part:
                start, end = map(int, part.split('-'))
                nums.extend(range(start, end + 1))
            else:
                nums.append(int(part))
        return [n for n in nums if 1 <= n <= max_idx]
    except:
        return []


def read_msgs(filename):

    try:
        console.print(f"\n[yellow]⏳ Đang đọc tẩn mẹ nó '{filename}'...[/]")
        with open(filename, 'r', encoding='utf-8') as f:
            msgs = [line.strip() for line in f if line.strip()]
        if msgs:
            console.print(f"[green]✅ Đã tải {len(msgs)} tin nhắn tẩn chết mẹ nó![/]")
            return msgs
        return None
    except:
        console.print("[red]❌ Không tìm thấy file![/]")
        return None


def spam_process(api_key, secret_key, imei, cookies, delay, friends, msgs):
    try:
        bot = ZaloBotFixed(api_key, secret_key, imei, cookies, delay)
        bot.spam_friends(friends, msgs)
    except Exception as e:
        console.print(f"[red]❌ {e}[/]")


def display_friends_rainbow(friends):
    console.print()
    console.print(f"[bold cyan]{'═'*70}[/]")
    console.print(f"[bold yellow]DANH SÁCH {len(friends)} BẠN BÈ - địt mẹ m  ✨[/]")
    console.print(f"[bold cyan]{'═'*70}[/]\n")
    
    for idx, f in enumerate(friends, 1):
        color = get_rainbow_color(idx, len(friends))
        
        text = Text()
        text.append(f"STT {idx:>3} ", style="bold white")
        text.append("(", style="dim")
        text.append(f"{f['name']}", style=f"bold {color}")
        text.append(")", style="dim")
        
        console.print(text)
        
        time.sleep(0.02)
    
    console.print(f"\n[bold cyan]{'═'*70}[/]\n")


def main():
    console.clear()
    
    try:
        num = int(Prompt.ask("💠 Số tài khoản", default="1"))
    except:
        console.print("[red]❌ Số không hợp lệ![/]")
        return
    
    procs = []
    
    for i in range(num):
        console.print(f"\n{Fore.CYAN}{'═'*70}")
        console.print(f"{Fore.YELLOW}🔹 TÀI KHOẢN {i+1}/{num} 🔹")
        console.print(f"{Fore.CYAN}{'═'*70}\n")
        
        imei = Prompt.ask("[cyan]📱 nhập ime đi thk ngu [/]", default="auto").strip()
        if imei == "auto" or not imei:
            imei = ''.join([str(random.randint(0,9)) for _ in range(15)])
            console.print(f"[dim]Auto IMEI: {imei}[/]")
        
        console.print("\n[dim]💡 Format: zpw_sek=xxx; zpw_enk=yyy[/]")
        cookie = Prompt.ask("[cyan]🍪 nhập cookie đi thk ngu[/]").strip()
        
        if not cookie:
            console.print("[red]❌ nhập cookie lẹ đéo cho trống ma![/]")
            continue
        
        cookie_dict = parse_cookie_string(cookie)
        if not cookie_dict:
            console.print("[red]❌ Cookie m die r cn chó ngu ![/]")
            continue
        
        console.print(f"[green]✅ Parsed: {', '.join(cookie_dict.keys())}[/]")
        save_debug("Cookie Input", cookie_dict)
        
        try:
            delay = int(Prompt.ask("[cyan]⏳ số delay dập lồn mẹ nó (giây)[/]", default="3"))
        except:
            delay = 3
        
        try:
            bot = ZaloBotFixed('api_key', 'secret_key', imei, cookie_dict, delay)
        except Exception as e:
            console.print(f"[red]❌ Lỗi tạo bot: {e}[/]")
            continue
        
        if not bot.check_account_debug():
            console.print("[red]❌ Bỏ qua tài khoản này![/]")
            console.print(f"[dim]📄 Xem {DEBUG_FILE} để biết chi tiết[/]")
            time.sleep(2)
            continue
        
        friends = bot.get_friends_debug()
        
        if not friends:
            console.print("[red]❌ Không có bạn bè![/]")
            console.print(f"[dim]📄 Xem {DEBUG_FILE}[/]")
            continue
        
        display_friends_rainbow(friends)
        
        sel = Prompt.ask("[cyan]👉 Chọn (1,3,5 hoặc 'all')[/]", default="all").strip().lower()
        
        if sel == "all":
            selected = friends
        else:
            indices = parse_selection(sel, len(friends))
            if not indices:
                console.print("[red]❌ Lựa chọn không hợp lệ![/]")
                continue
            selected = [friends[i-1] for i in indices]
        
        console.print(f"[green]✅ Đã chọn {len(selected)} bạn![/]")
        
        filename = Prompt.ask("[cyan]📄 File tin nhắn[/]", default="nhaychet.txt").strip()
        msgs = read_msgs(filename)
        
        if not msgs:
            continue
        
        p = multiprocessing.Process(
            target=spam_process,
            args=('api_key', 'secret_key', imei, cookie_dict, delay, selected, msgs)
        )
        procs.append(p)
        p.start()
        
        console.print(f"\n[green]✅ Bot {i+1} đã khởi động![/]")
        time.sleep(1)
    
    if not procs:
        console.print("\n[red]❌ Không có bot nào chạy![/]")
        console.print(f"[dim]📄 Xem {DEBUG_FILE}[/]")
        return
    
    console.print(f"\n{Fore.GREEN}{'═'*70}")
    console.print(Panel.fit(
        f"[bold green]🚀 tất cả acc đang địt mẹ nó![/]\n\n"
        f"[cyan]✅ Đang chạy:[/] [white bold]{len(procs)} bots[/]\n"
        f"[yellow]📄 Debug:[/] [white]{DEBUG_FILE}[/]\n"
        f"[red]⏹️ Nhấn Ctrl+C để dừng[/]",
        border_style="bold green",
        title="[bold white]TRẠNG THÁI[/]"
    ))
    console.print(f"{Fore.GREEN}{'═'*70}\n")
    
    try:
        for p in procs:
            p.join()
    except KeyboardInterrupt:
        console.print("\n[yellow]⏹️ Đang dừng tất cả acc tẩn mẹ nó...[/]")
        for p in procs:
            p.terminate()
            p.join(timeout=3)
        console.print("[green]✅ Đã dừng hết acc tẩn mẹ nó![/]")


if __name__ == "__main__":
    main()
