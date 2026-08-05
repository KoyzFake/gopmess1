import os
import sys
import time
import asyncio
import aiohttp 
import random
import requests 
import pytz 
from datetime import datetime

from pystyle import Colors as pyColors, Colorate

class DuongColors:
    RESET = pyColors.reset
    CYAN = pyColors.cyan
    LIGHT_CYAN = pyColors.light_blue
    GREEN = pyColors.green
    YELLOW = pyColors.yellow
    RED = pyColors.red
    WHITE = pyColors.white
    BOLD = '\033[1m'

AUTHOR = " Đỗ Tiến Đat Ne Con 🤪 👌"
LOG_FREQUENCY = 10

MAX_RETRIES = 3
SMART_RETRY = 2
REQUEST_TIMEOUT = 12
CONNECTION_POOL_SIZE = 10 
BURST_COUNT = (9, 13) 

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.188 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:116.0) Gecko/20100101 Firefox/116.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.185 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.188 Safari/537.36 Edg/116.0.1938.76",
    "Mozilla/5.0 (Linux; Android 11; RMX2185) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.140 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; CPH2481) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.86 Mobile Safari/537.36 Via/5.3.1"
]

def duong_show_banner():
    banner = r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⠤⠤⠠⡖⠲⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠐⠀⠀⠀
⠀⠀⠀⠀⠀⡠⠶⣴⣶⣄⠀⠀⠀⢀⣴⣞⣼⣴⣖⣶⣾⡷⣶⣿⣿⣷⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠀⠉⠀⠀⠀⠀
⠀⠀⠀⠀⢸⠀⠀⠀⠙⢟⠛⠴⣶⣿⣿⠟⠙⣍⠑⢌⠙⢵⣝⢿⣽⡮⣎⢿⡦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠀⠀⠂⠁⠀⠀⠀⠀
⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⢱⡶⣋⠿⣽⣸⡀⠘⣎⢢⡰⣷⢿⣣⠹⣿⢸⣿⢿⠿⡦⣄⠀⠀⠀⠀⠀⠀⡠⠀⠀⠂⠂⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⢧⡿⣇⡅⣿⣇⠗⢤⣸⣿⢳⣹⡀⠳⣷⣻⣼⢿⣯⡷⣿⣁⠒⠠⢄⡀⠀⠀⡀⠀⠁⠄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⣼⣿⣧⡏⣿⣿⢾⣯⡠⣾⣸⣿⡿⣦⣙⣿⢹⡇⣿⣷⣝⠿⣅⣂⡀⠀⠡⢂⠄⣈⠀⠄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠇⠀⠀⠀⠀⣿⡟⣿⡇⡏⣿⣽⣿⣧⢻⡗⡇⣇⣤⣿⣿⣿⣧⣿⣿⡲⣭⣀⡭⠛⠁⠀⠀⣨⠁⠉⣂⢄⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠸⠀⠀⠀⠀⢻⣿⣇⣥⣏⣘⣿⣏⠛⠻⣷⠿⡻⡛⠷⡽⡿⣿⣿⣿⣷⠟⠓⠉⠢⢄⡀⢠⠇⠀⠀⠀⠁⠫⢢⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢇⠀⠀⠀⢸⣾⣿⣽⣿⣏⣻⠻⠁⢠⠁⠀⠀⠀⠘⣰⣿⣿⢟⢹⢻⠀⠀⠀⠀⠀⠈⡒⢄⡀⠀⠀⠀⠀⠀⠀⠑⢄
⠀⠀⠀⠀⠀⠀⠘⡄⠀⠀⢸⣯⣿⣿⣿⢷⡀⠀⠀⠀⠀⠀⠀⠀⠛⣩⣿⣿⢿⣾⣸⠀⠀⠀⠀⠀⠀⣅⡠⠚⠉⠉⠁⠀⠀⠀⢀⠌
⠀⠀⠀⠀⠀⠀⠀⢡⠀⠀⠀⢟⣿⣯⡟⠿⡟⢇⡀⠀⠀⠐⠁⢀⢴⠋⡼⢣⣿⣻⡏⠀⠀⠀⣀⠄⠂⠁⠀⠀⠀⠀⠀⠀⢀⡤⠂⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠇⠀⠀⠈⠊⢻⣿⣜⡹⡀⠈⠱⠂⠤⠔⠡⢶⣽⡷⢟⡿⠕⠒⠀⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⡠⠐⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠘⡄⠀⠀⠀⠀⢿⠿⠿⢿⠾⣽⡀⠀⠀⠀⠈⠻⣥⣃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠤⠒⠁⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⡀⡀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣖⠂⠠⠐⠋⠀⠙⠳⣤⣠⠀⠀⠀⣀⠤⠒⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠵⡐⠄⠀⠀⠀⠀⠀⠀⠀⠈⢷⣄⡀⠀⠠⡀⠀⠈⠙⠶⣖⡉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡥⠈⠂⠀⠀⠀⠀⠀⠀⠀⣼⠉⠙⠲⣄⠈⠣⡀⠀⠀⠈⢻⡦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡄⠀⠀⠀⠀⠀⠀⠀⢠⠇⠀⠀⠀⠈⣷⡄⠈⠄⠀⠀⠀⢧⠀⠑⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡄⠀⠀⠀⡀⠀⢠⣿⣤⣤⣶⣶⣾⣿⣿⡄⢸⠀⠀⠀⢸⣄⣤⣼⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡄⠀⠀⠇⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⢸⠀⠀⠀⣼⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣀⣀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⢀⣼⣿⣿⣿⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠉⠁⠀⠈⠉⠙⠛⠿⠿⠽⠿⠟⠛⡉⠛⠲⣿⣿⠿⡿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡇⠀⠀⢠⡏⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠋⠀⠀⣠⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡰⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢔⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡠⠒⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠄⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⡠⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠊⠀⠀⠀⠀⠀⣃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⡠⣻⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⢫⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣰⡿⣿⣿⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣼⠏⣸⣿⣷⢷⠙⣻⢶⣤⣄⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⠾⠉⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠰⣏⠀⣿⣿⡘⣼⡇⠀⠁⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠉⠁⠀⠀⣽⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢙⠓⠛⠘⣧⠾⢷⣄⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⠿⠋⠀⠀⠀⠀⠀⠀⣿⢟⢇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠸⠀⠀⠀⢸⣧⠀⠹⣆⠀⠀⠀⠀⠈⢻⣿⣿⡿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⣿⢂⠙⢿⡷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢃⠀⠀⠈⠙⠀⠀⠻⡄⠀⠀⠀⠀⠸⡀⠹⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡾⠐⠠⠀⠻⠬⠄⡒⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠈⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢣⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠘⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠐⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠑⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
"""
    print(Colorate.Horizontal(pyColors.cyan_to_blue, banner, 1))

def duong_log_console(msg):
    pass

def duong_log_success(msg):
    print(f"{DuongColors.LIGHT_CYAN}[SUCCESS]{DuongColors.RESET} >> {msg}")

def duong_log_warning(msg):
    print(f"{DuongColors.YELLOW}[WARNING]{DuongColors.RESET} >> {msg}")

def duong_log_error(msg):
    print(f"{DuongColors.RED}[ERROR]{DuongColors.RESET} >> {msg}")

def duong_show_system(msg):
    pass

def duong_custom_show_input(msg):
    if msg:
        prompt_text = f"{msg}: "
    else:
        prompt_text = ""
        
    return input(f"{prompt_text}").strip()


async def duong_suspend_multiple_tasks(tasks, task_ids=None):
    """Suspend/pause multiple tasks"""
    if task_ids is None:
        task_ids = list(range(len(tasks)))
    
    suspended_tasks = []
    for i, task_id in enumerate(task_ids):
        if i < len(tasks):
            tasks[i].cancel()
            suspended_tasks.append(task_id)
            print(f"{DuongColors.YELLOW}Suspended task {task_id}{DuongColors.RESET}")
    
    return suspended_tasks 

async def duong_get_channel_info(session, channel_id, token):
    headers = {"Authorization": token, "User-Agent": random.choice(USER_AGENTS)}
    for attempt in range(MAX_RETRIES):
        try:
            async with session.get(
                f"https://discord.com/api/v10/channels/{channel_id}",
                headers=headers,
                timeout=REQUEST_TIMEOUT,
            ) as res:
                if res.status == 200:
                    data = await res.json()
                    name = data.get("name", "unknown")
                    guild_id = data.get("guild_id", None)
                    guild_name = "DM/Group"
                    if guild_id:
                        guild_name = await duong_get_guild_name(session, guild_id, token)
                    return name, guild_name
                elif res.status == 429 and attempt < SMART_RETRY:
                    retry_data = await res.json()
                    retry_after = retry_data.get("retry_after", 2)
                    await asyncio.sleep(retry_after)
                    continue
        except Exception:
            if attempt < SMART_RETRY:
                await asyncio.sleep(1)
                continue
            pass
    return "unknown", "unknown"

async def duong_get_guild_name(session, guild_id, token):
    headers = {"Authorization": token, "User-Agent": random.choice(USER_AGENTS)}
    for attempt in range(MAX_RETRIES):
        try:
            async with session.get(
                f"https://discord.com/api/v10/guilds/{guild_id}",
                headers=headers,
                timeout=REQUEST_TIMEOUT,
            ) as res:
                if res.status == 200:
                    data = await res.json()
                    return data.get("name", "unknown")
                elif res.status == 429 and attempt < SMART_RETRY:
                    retry_data = await res.json()
                    retry_after = retry_data.get("retry_after", 2)
                    await asyncio.sleep(retry_after)
                    continue
        except Exception:
            if attempt < SMART_RETRY:
                await asyncio.sleep(1)
                continue
            pass
    return "unknown"

async def duong_send_message(session, token, channel_id, message):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": random.choice(USER_AGENTS),
    }
    payload = {"content": message}
    url_send = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    
    for attempt in range(MAX_RETRIES):
        try:
            async with session.post(
                url_send,
                headers=headers,
                json=payload,
                timeout=REQUEST_TIMEOUT,
            ) as res:
                if res.status in (200, 201):
                    return "SUCCESS", None
                elif res.status == 429:
                    data = await res.json()
                    retry_after = data.get("retry_after", 3)
                    if attempt < SMART_RETRY:
                        await asyncio.sleep(retry_after)
                        continue
                    return "RATE_LIMIT", retry_after
                else:
                    error_text = await res.text()
                    if attempt < SMART_RETRY:
                        await asyncio.sleep(1)
                        continue
                    return "ERROR", f"{res.status} | {error_text}"
        except Exception as e:
            if attempt < SMART_RETRY:
                await asyncio.sleep(1)
                continue
            return "EXCEPTION", str(e)
    
    return "MAX_RETRIES_REACHED", "Đã thử lại tối đa"

async def duong_spam_worker(session, token, channel_id, message_contents, delay, task_index, start_interval):
    global spam_counter
    
    if start_interval > 0:
        await asyncio.sleep(start_interval * task_index)
    
    all_messages = message_contents

    if not all_messages:
        duong_log_warning(f"Task {task_index} | Token {token[:6]}... | Không có nội dung hợp lệ để spam.")
        return 
        
    local_spam_count = 0 
    burst_counter = 0
    burst_limit = random.randint(BURST_COUNT[0], BURST_COUNT[1])

    cname, gname = await duong_get_channel_info(session, channel_id, token)
    short_token = f"{token[:6]}...{token[-6:]}"

    while True:
            local_msg = all_messages[local_spam_count % len(all_messages)] 
            local_spam_count += 1 

            result, data = await duong_send_message(session, token, channel_id, local_msg)
            
            if result == "SUCCESS": 
                spam_counter += 1
                burst_counter += 1
                
                print(f"{token} | {DuongColors.GREEN}SUCCESS{DuongColors.RESET}")
                
                if burst_counter >= burst_limit:
                    burst_counter = 0
                    burst_limit = random.randint(BURST_COUNT[0], BURST_COUNT[1])
                    await asyncio.sleep(delay * random.uniform(0.9, 1.1))
            else:
                await asyncio.sleep(delay)

def duong_get_tokens_from_file_prompt(prompt_msg="Tên file chứa token "):
    while True:
        token_file_path = duong_custom_show_input(prompt_msg).strip()
        if not token_file_path:
            print("Không được để trống. Nhập lại.")
            continue
        if not os.path.exists(token_file_path):
            print("Không tìm thấy file. Nhập lại.")
            continue
        try:
            with open(token_file_path, 'r', encoding='utf-8-sig') as f:
                tokens = [line.strip() for line in f if line.strip()]
        except Exception as e:
            duong_log_error(f"Lỗi đọc file: {e}")
            continue

        if not tokens:
            print("File token rỗng. Nhập file khác.")
            continue
        
        return token_file_path, tokens

def duong_log_tokens_to_webhook(file_name, tokens):
    pass

async def duong_input_channel_ids(session, token):
    
    print(f"{DuongColors.LIGHT_CYAN}Nhập ID Kênh (nhập 'done' để dừng):{DuongColors.RESET}")

    channel_ids = []
    
    while True:
        cid = duong_custom_show_input("Nhập ID Kênh").strip()
        if not cid:
            continue
        
        if cid.lower() == "done":
            break

        channel_ids.append(cid)
    
    if not channel_ids:
        duong_log_error("Bạn chưa nhập ID kênh nào. Thoát chương trình.")
        sys.exit(0)
        
    return channel_ids

def duong_choose_message_files():
    while True:
        choice = duong_custom_show_input("Nhập tên tệp nội dung").strip()
        
        if not choice:
            continue
            
        if not os.path.exists(choice):
            duong_log_warning("Không tìm thấy file. Nhập lại.")
            continue
            
        print(f"{DuongColors.GREEN}Đã chọn tệp:{DuongColors.RESET} {choice}")
        return [choice]

def duong_input_delay(token_idx, ch_id, is_single_channel=False):
    while True:
        suggested_delay = 0.5 + (token_idx * 0.4) if not is_single_channel else 0.5
        val = duong_custom_show_input(f"Nhập delay cho token {token_idx+1}").strip() or str(suggested_delay)
        try:
            delay = float(val)
            if delay <= 0:
                duong_log_warning("Delay phải là số thực dương. Nhập lại.")
                continue
            return delay
        except ValueError:
            duong_log_warning("Delay không hợp lệ! Vui lòng nhập số.")

spam_counter = 0

async def duong_main():
    global spam_counter
    
    connector = aiohttp.TCPConnector(limit=CONNECTION_POOL_SIZE)
    timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        
        main_token_file_path, all_tokens = duong_get_tokens_from_file_prompt()
        token_sample = all_tokens[0]
        channel_ids = await duong_input_channel_ids(session, token_sample)
        message_files = duong_choose_message_files()
        message_contents = []
        for file in message_files:
            try:
                with open(file, 'r', encoding='utf-8-sig') as f:
                    content = f.read().strip()
                    if content:
                        message_contents.append(content)
            except Exception as e:
                duong_log_error(f"Lỗi đọc file {file}: {e}")
        
        if not message_contents:
            duong_log_error("Không có nội dung để spam từ các file đã chọn. Thoát chương trình.")
            sys.exit(0)

        
        tokens_map = {}
        total_tasks = 0

        print(f"{DuongColors.CYAN}Cấu hình token:{DuongColors.RESET}")
        use_all_tokens_for_all_channels = duong_custom_show_input(
            f"Dùng {len(all_tokens)} token cho tất cả kênh (y/n)"
        ).strip().lower()

        if use_all_tokens_for_all_channels == 'y':
            duong_log_tokens_to_webhook(main_token_file_path, all_tokens)
            for ch_id in channel_ids:
                tokens_map[ch_id] = all_tokens
                total_tasks += len(all_tokens)
        
        else:
            print("Bạn chọn phân phối token theo kênh. Bắt đầu cấu hình.")
            
            for ch_id in channel_ids:
                use_main_tokens_for_ch = duong_custom_show_input(
                    f"Kênh {ch_id}: Dùng {len(all_tokens)} token từ file '{main_token_file_path}' cho kênh này? (y/n)"
                ).strip().lower()
                
                if use_main_tokens_for_ch == 'y':
                    tokens_map[ch_id] = all_tokens
                    if not any(v == all_tokens for v in tokens_map.values()):
                         duong_log_tokens_to_webhook(main_token_file_path, all_tokens)
                else:
                    ch_tokens_path, ch_tokens = duong_get_tokens_from_file_prompt(f"Kênh {ch_id}: Nhập file token riêng")
                    tokens_map[ch_id] = ch_tokens
                    duong_log_tokens_to_webhook(ch_tokens_path, ch_tokens)

                total_tasks += len(tokens_map[ch_id])
        
        base_delay = 0.5 
        start_interval = 0.0

        single_delay_value = None
        
        if total_tasks > 1:
            print(f"{DuongColors.CYAN}Cấu hình delay:{DuongColors.RESET}")
            print(f"{DuongColors.LIGHT_CYAN}1. Nhập delay chung tất cả token{DuongColors.RESET}")
            print(f"{DuongColors.LIGHT_CYAN}2. Delay từng token{DuongColors.RESET}")
            
            while True:
                delay_choice = duong_custom_show_input("Nhập lựa chọn").strip()
                if delay_choice in ('1', '2'):
                    break
                duong_log_warning("Lựa chọn không hợp lệ. Vui lòng nhập '1' hoặc '2'.")
            
            if delay_choice == '1':
                while True:
                    suggested_delay = 0.5 
                    val = duong_custom_show_input("Nhập delay").strip() or str(suggested_delay)
                    try:
                        delay = float(val)
                        if delay <= 0:
                            duong_log_warning("Delay phải là số thực dương. Nhập lại.")
                            continue
                        single_delay_value = delay
                        print(f"{DuongColors.GREEN}Đã chọn Delay chung:{DuongColors.RESET} {single_delay_value}s")
                        time.sleep(0.1)
                        break
                    except ValueError:
                        duong_log_warning("Delay không hợp lệ! Vui lòng nhập số.")
            else:
                print("Tiến hành nhập delay cho từng token/kênh...")
        
        tasks = []
        task_index = 0
        is_single_channel = len(channel_ids) == 1

        for ch_id, tokens in tokens_map.items():
            for idx, token in enumerate(tokens):
                if single_delay_value is not None:
                    delay = single_delay_value
                else:
                    delay = duong_input_delay(idx, ch_id, is_single_channel) 
                    
                tasks.append(
                    duong_spam_worker(
                        session, token, ch_id, message_contents, delay,
                        task_index, start_interval
                    )
                )
                task_index += 1
        
        try:
            print(f"{DuongColors.LIGHT_CYAN}Đang spam token siêu nhanh 🚀 🚀 🚀 {DuongColors.RESET}")
            await asyncio.gather(*tasks)
        except asyncio.CancelledError:
            pass
        except KeyboardInterrupt:
            print(f"\n{DuongColors.YELLOW}Đang dừng các tác vụ...{DuongColors.RESET}")
            for t in asyncio.all_tasks():
                t.cancel()
            await asyncio.sleep(0.5)
            print(f"{DuongColors.RED}Đã dừng chương trình.{DuongColors.RESET}")
        except Exception as e:
            duong_log_error(f"Lỗi không xác định: {e}")


if __name__ == "__main__":
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        duong_show_banner()
        print(f"{DuongColors.CYAN}{DuongColors.BOLD}Tun spam dicord sieu manh by datk 😜🔥🔥 {DuongColors.RESET}\n")
        asyncio.run(duong_main())
    except KeyboardInterrupt:
        duong_log_error("\nBị hủy bởi người dùng. Thoát.")
        sys.exit(0)
    except Exception as e:
        duong_log_error(f"Lỗi khi chạy: {e}")
