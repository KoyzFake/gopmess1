import time
import os
import gc
import threading
import random
import requests
import json
import socket
import platform
import ctypes
import sys
from datetime import datetime
from collections import deque

SESSION_POOL_SIZE  = 5
KEEPALIVE_INTERVAL = 20
GC_INTERVAL        = 45
BACKOFF_BASE       = 2
BACKOFF_MAX        = 60
RETRY_LIMIT        = 5
HEARTBEAT_TIMEOUT  = 8
DNS_CACHE          = {}
_dns_lock          = threading.Lock()

treo_tabs    = {}
treo_history = deque(maxlen=50)
_tab_lock    = threading.Lock()


def dotiendat_don_ram():
    gc.collect(0)
    gc.collect(1)
    gc.collect(2)
    with _tab_lock:
        dead = [k for k in list(treo_tabs)
                if treo_tabs[k].get("stop_event") and treo_tabs[k]["stop_event"].is_set()]
        for k in dead:
            treo_tabs.pop(k, None)

def dotiendat_don_disk(folder=".", exts=(".log", ".tmp"), max_mb=5):
    try:
        for fn in os.listdir(folder):
            if any(fn.endswith(e) for e in exts):
                fp = os.path.join(folder, fn)
                if os.path.getsize(fp) > max_mb * 1024 * 1024:
                    os.remove(fp)
    except Exception:
        pass

def dotiendat_don_lich_su():
    while len(treo_history) > 30:
        treo_history.popleft()

def dotiendat_don_dns_cache():
    with _dns_lock:
        DNS_CACHE.clear()

def dotiendat_don_thread_chet():
    alive = [t for t in threading.enumerate() if t.is_alive()]
    return len(alive)

def dotiendat_giam_priority():
    try:
        if platform.system() == "Windows":
            p = ctypes.windll.kernel32.GetCurrentProcess()
            ctypes.windll.kernel32.SetPriorityClass(p, 0x00004000)
        else:
            os.nice(10)
    except Exception:
        pass

def dotiendat_don_toan_bo():
    dotiendat_don_ram()
    dotiendat_don_disk()
    dotiendat_don_lich_su()
    dotiendat_don_dns_cache()
    dotiendat_don_thread_chet()

def dotiendat_auto_gc(stop_event):
    dotiendat_giam_priority()
    while not stop_event.is_set():
        dotiendat_don_toan_bo()
        stop_event.wait(GC_INTERVAL)


def dotiendat_kiem_tra_mang():
    for host in ("8.8.8.8", "1.1.1.1", "208.67.222.222"):
        try:
            socket.setdefaulttimeout(3)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, 53))
            s.close()
            return True
        except Exception:
            continue
    return False

def dotiendat_cho_co_mang(stop_event, interval=5):
    warned = False
    while not stop_event.is_set():
        if dotiendat_kiem_tra_mang():
            if warned:
                dotiendat_log("MẠNG", "Kết nối lại thành công")
            return True
        if not warned:
            dotiendat_log("MẠNG", "Mất kết nối, đang chờ...")
            warned = True
        stop_event.wait(interval)
    return False

def dotiendat_kiem_tra_dns(host="discord.com"):
    with _dns_lock:
        if host in DNS_CACHE:
            return DNS_CACHE[host]
    try:
        ip = socket.gethostbyname(host)
        with _dns_lock:
            DNS_CACHE[host] = ip
        return ip
    except Exception:
        return None

def dotiendat_ping_discord():
    try:
        start = time.time()
        r = requests.get("https://discord.com/api/v10/gateway", timeout=5)
        ms = int((time.time() - start) * 1000)
        return r.status_code == 200, ms
    except Exception:
        return False, -1


_UA_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Edg/120.0.0.0",
]

_XSUPER_LIST = [
    "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIn0=",
    "eyJvcyI6Ik1hY09TIiwiYnJvd3NlciI6IlNhZmFyaSIsImRldmljZSI6IiJ9",
    "eyJvcyI6IkxpbnV4IiwiYnJvd3NlciI6IkZpcmVmb3giLCJkZXZpY2UiOiIifQ==",
]

def dotiendat_xoay_user_agent():
    return random.choice(_UA_LIST)

def dotiendat_tao_session():
    s = requests.Session()
    s.headers.update({
        "User-Agent": dotiendat_xoay_user_agent(),
        "Accept-Language": random.choice(["en-US,en;q=0.9", "vi-VN,vi;q=0.9,en;q=0.8"]),
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip, deflate, br",
    })
    adapter = requests.adapters.HTTPAdapter(
        pool_connections=2,
        pool_maxsize=SESSION_POOL_SIZE,
        max_retries=0,
        pool_block=False,
    )
    s.mount("https://", adapter)
    s.mount("http://",  adapter)
    return s

class dotiendat_SessionPool:
    def __init__(self, size=SESSION_POOL_SIZE):
        self._pool = [dotiendat_tao_session() for _ in range(size)]
        self._idx  = 0
        self._lock = threading.Lock()

    def get(self):
        with self._lock:
            s = self._pool[self._idx % len(self._pool)]
            self._idx += 1
            return s

    def rebuild(self, idx=None):
        with self._lock:
            i = (idx if idx is not None else self._idx) % len(self._pool)
            try: self._pool[i].close()
            except: pass
            self._pool[i] = dotiendat_tao_session()

    def rebuild_tat_ca(self):
        with self._lock:
            for i in range(len(self._pool)):
                try: self._pool[i].close()
                except: pass
                self._pool[i] = dotiendat_tao_session()

_pool = dotiendat_SessionPool()


def dotiendat_keepalive(token, stop_event):
    url = "https://discord.com/api/v10/users/@me"
    fail = 0
    while not stop_event.is_set():
        try:
            hdr = {"Authorization": token, "User-Agent": dotiendat_xoay_user_agent()}
            r = _pool.get().get(url, headers=hdr, timeout=HEARTBEAT_TIMEOUT)
            if r.status_code == 200:
                fail = 0
            elif r.status_code == 401:
                dotiendat_log("TOKEN", f"Token hết hạn: {token[:20]}...")
                break
            elif r.status_code == 429:
                dotiendat_doi_ratelimit(r.headers)
        except Exception:
            fail += 1
            if fail >= 3:
                dotiendat_cho_co_mang(stop_event)
                fail = 0
        interval = KEEPALIVE_INTERVAL + random.uniform(-3, 5)
        stop_event.wait(interval)

def dotiendat_kiem_tra_token(token):
    try:
        url = "https://discord.com/api/v10/users/@me"
        hdr = {"Authorization": token, "User-Agent": dotiendat_xoay_user_agent()}
        r = _pool.get().get(url, headers=hdr, timeout=HEARTBEAT_TIMEOUT)
        return r.status_code == 200
    except Exception:
        return False

def dotiendat_loc_token_hop_le(tokens):
    hop_le = []
    for t in tokens:
        if dotiendat_kiem_tra_token(t):
            hop_le.append(t)
        else:
            dotiendat_log("TOKEN", f"Không hợp lệ, bỏ qua: {t[:20]}...")
    return hop_le

def dotiendat_xoay_token(tokens):
    t = tokens[:]
    random.shuffle(t)
    return t


def dotiendat_tinh_backoff(fail_count):
    wait = min(BACKOFF_BASE ** fail_count, BACKOFF_MAX)
    return wait + random.uniform(0.1, 2.0)

def dotiendat_doi_ratelimit(headers):
    try:
        ra = float(headers.get("Retry-After", 0))
        if ra > 0:
            dotiendat_log("GIỚI HẠN", f"Rate-limit, chờ {ra:.1f}s")
            time.sleep(ra + random.uniform(0.2, 0.8))
    except Exception:
        pass

def dotiendat_delay_ngau_nhien(base):
    return max(0.5, base + random.uniform(-0.1, 0.9))


def dotiendat_tao_headers(token):
    return {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": dotiendat_xoay_user_agent(),
        "X-Super-Properties": random.choice(_XSUPER_LIST),
        "Accept-Language": random.choice(["en-US,en;q=0.9", "vi-VN,vi;q=0.9"]),
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "X-Discord-Locale": random.choice(["en-US", "vi"]),
    }

def dotiendat_nghi_ngau_nhien(stop_event, min_s=30, max_s=90):
    wait = random.uniform(min_s, max_s)
    dotiendat_log("NGHỈ", f"Nghỉ {wait:.0f}s tránh detect")
    stop_event.wait(wait)

def dotiendat_gia_lap_typing(token, channel_id):
    try:
        url = f"https://discord.com/api/v10/channels/{channel_id}/typing"
        hdr = {"Authorization": token, "User-Agent": dotiendat_xoay_user_agent()}
        _pool.get().post(url, headers=hdr, timeout=5)
    except Exception:
        pass

def dotiendat_them_noise_tin(content):
    noise = ["​", "\u200b", "\u2060", "\ufeff"]
    if random.random() < 0.3:
        pos = random.randint(0, len(content))
        ch  = random.choice(noise)
        return content[:pos] + ch + content[pos:]
    return content


_log_lock = threading.Lock()

def dotiendat_log(tag, msg):
    with _log_lock:
        print(f"[{datetime.now().strftime('%H:%M:%S')}][{tag}] {msg}")

def dotiendat_log_file(tag, msg, path="tool.log"):
    try:
        with _log_lock:
            with open(path, "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now().strftime('%H:%M:%S %d-%m-%Y')}][{tag}] {msg}\n")
        if os.path.getsize(path) > 2 * 1024 * 1024:
            os.remove(path)
    except Exception:
        pass


def dotiendat_gui_discord(token, channel_id, content, session=None, typing=False, allow_everyone=False):
    if typing and random.random() < 0.4:
        dotiendat_gia_lap_typing(token, channel_id)
        time.sleep(random.uniform(0.3, 1.2))

    content = dotiendat_them_noise_tin(content)
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    hdr = dotiendat_tao_headers(token)
    s   = session or _pool.get()

    payload = {"content": content}
    if allow_everyone:
        payload["allowed_mentions"] = {"parse": ["everyone", "roles", "users"]}

    for attempt in range(3):
        try:
            r = s.post(url, headers=hdr, json=payload, timeout=HEARTBEAT_TIMEOUT)
            if r.status_code in (200, 201):
                dotiendat_log_file("OK", f"ch={channel_id} | {content[:40]}")
                return True, r.text
            if r.status_code == 429:
                dotiendat_doi_ratelimit(r.headers)
                continue
            if r.status_code in (401, 403):
                return False, f"Token lỗi {r.status_code}"
            if r.status_code >= 500:
                time.sleep(2 + attempt)
                continue
            return False, f"HTTP {r.status_code}"
        except requests.exceptions.ConnectionError:
            _pool.rebuild()
            dotiendat_cho_co_mang(threading.Event(), interval=3)
            time.sleep(1 + attempt)
        except requests.exceptions.Timeout:
            dotiendat_log("TIMEOUT", f"Lần {attempt+1}")
            time.sleep(2)
        except Exception as e:
            return False, str(e)
    return False, "Hết retry"

def dotiendat_gui_tag_all(token, channel_id, content, session=None, typing=False):
    """Gửi @everyone — header tối giản, không X-Super-Properties để tránh Discord reject."""
    if typing and random.random() < 0.4:
        dotiendat_gia_lap_typing(token, channel_id)
        time.sleep(random.uniform(0.3, 1.2))

    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    text = dotiendat_them_noise_tin(content)[:1990]
    body = json.dumps({
        "content": f"@everyone {text}",
        "allowed_mentions": {"parse": ["everyone"]},
    })
    hdr = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }
    for attempt in range(3):
        try:
            r = requests.post(url, headers=hdr, data=body.encode("utf-8"), timeout=HEARTBEAT_TIMEOUT)
            if r.status_code in (200, 201):
                dotiendat_log_file("OK", f"ch={channel_id} | @everyone")
                return True, r.text
            if r.status_code == 429:
                dotiendat_doi_ratelimit(r.headers)
                continue
            if r.status_code in (401, 403):
                return False, f"Token lỗi {r.status_code}"
            if r.status_code >= 500:
                time.sleep(2 + attempt); continue
            return False, f"HTTP {r.status_code} {r.text[:200]}"
        except requests.exceptions.ConnectionError:
            dotiendat_cho_co_mang(threading.Event(), interval=3)
            time.sleep(1 + attempt)
        except requests.exceptions.Timeout:
            dotiendat_log("TIMEOUT", f"Lần {attempt+1}")
            time.sleep(2)
        except Exception as e:
            return False, str(e)
    return False, "Hết retry"


    """Gửi tin nhắn kèm ảnh/video qua embed — chỉ hiện nội dung + ảnh, không hiện link."""
    if typing and random.random() < 0.4:
        dotiendat_gia_lap_typing(token, channel_id)
        time.sleep(random.uniform(0.3, 1.2))

    text_content = dotiendat_them_noise_tin(content)
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    hdr = dotiendat_tao_headers(token)
    s   = session or _pool.get()

    # Dùng embed image/video — Discord hiện ảnh, không hiện link trong chat
    ext = cdn_url.split("?")[0].lower()
    if any(ext.endswith(e) for e in (".mp4", ".webm", ".mov", ".mkv")):
        # Video: dùng link trong content với flags suppress_embeds=False
        # Discord tự embed video CDN khi link đứng riêng
        payload = {
            "content": f"{text_content}\n{cdn_url}",
            "flags": 0,
        }
    else:
        # Ảnh: dùng embed image để ẩn link hoàn toàn
        payload = {
            "content": text_content,
            "embeds": [{"image": {"url": cdn_url}}],
        }

    for attempt in range(3):
        try:
            r = s.post(url, headers=hdr, json=payload, timeout=HEARTBEAT_TIMEOUT)
            if r.status_code in (200, 201):
                dotiendat_log_file("OK", f"ch={channel_id} | {text_content[:60]}")
                return True, r.text
            if r.status_code == 429:
                dotiendat_doi_ratelimit(r.headers)
                continue
            if r.status_code in (401, 403):
                return False, f"Token lỗi {r.status_code}"
            if r.status_code >= 500:
                time.sleep(2 + attempt)
                continue
            return False, f"HTTP {r.status_code}"
        except requests.exceptions.ConnectionError:
            _pool.rebuild()
            dotiendat_cho_co_mang(threading.Event(), interval=3)
            time.sleep(1 + attempt)
        except requests.exceptions.Timeout:
            dotiendat_log("TIMEOUT", f"Lần {attempt+1}")
            time.sleep(2)
        except Exception as e:
            return False, str(e)
    return False, "Hết retry"

def dotiendat_them_reaction(token, channel_id, message_id, emoji):
    enc = requests.utils.requote_uri(emoji)
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages/{message_id}/reactions/{enc}/@me"
    hdr = {"Authorization": token, "User-Agent": dotiendat_xoay_user_agent()}
    try:
        r = _pool.get().put(url, headers=hdr, timeout=HEARTBEAT_TIMEOUT)
        if r.status_code == 429:
            dotiendat_doi_ratelimit(r.headers)
        return r.status_code in (200, 204)
    except Exception:
        return False


def dotiendat_worker(token, channel_id, get_message_fn, delay, task_type, stop_event, tab_key, allow_everyone=False):
    ok = fail = consec_fail = msg_count = 0
    start = datetime.now()
    s = dotiendat_tao_session()
    ka_stop = threading.Event()
    threading.Thread(target=dotiendat_keepalive, args=(token, ka_stop), daemon=True).start()
    gc_counter = 0

    while not stop_event.is_set():
        if not dotiendat_kiem_tra_mang():
            dotiendat_cho_co_mang(stop_event)
            _pool.rebuild_tat_ca()
            try: s.close()
            except: pass
            s = dotiendat_tao_session()
            continue

        msg = get_message_fn()
        if allow_everyone:
            success, resp = dotiendat_gui_tag_all(token, channel_id, msg, session=s, typing=True)
        else:
            success, resp = dotiendat_gui_discord(token, channel_id, msg, session=s, typing=True)

        if success:
            ok += 1
            msg_count += 1
            consec_fail = 0
            status = "Đang chạy"
            dotiendat_log("OK", f"#{ok} -> {channel_id} | {msg[:40]}")
        else:
            fail += 1
            consec_fail += 1
            status = "Rớt (fail x5)" if consec_fail >= RETRY_LIMIT else "Đang chạy"
            dotiendat_log("LỖI", f"#{fail} -> {channel_id} | {resp[:200]}")
            if consec_fail >= RETRY_LIMIT:
                sleep_t = dotiendat_tinh_backoff(consec_fail)
                dotiendat_log("BACKOFF", f"Chờ {sleep_t:.1f}s")
                stop_event.wait(sleep_t)
                try: s.close()
                except: pass
                s = dotiendat_tao_session()
                continue

        uptime = int((datetime.now() - start).total_seconds())
        with _tab_lock:
            if tab_key in treo_tabs:
                treo_tabs[tab_key].update({
                    "ok": ok, "fail": fail, "uptime": uptime,
                    "status": status,
                    "last_update": datetime.now().strftime("%H:%M:%S"),
                })

        gc_counter += 1
        if gc_counter >= 100:
            dotiendat_don_ram()
            gc_counter = 0

        if msg_count > 0 and msg_count % 200 == 0:
            dotiendat_nghi_ngau_nhien(stop_event, 30, 90)

        actual_delay = dotiendat_delay_ngau_nhien(delay)
        for _ in range(max(1, int(actual_delay * 10))):
            if stop_event.is_set():
                break
            time.sleep(0.1)

    ka_stop.set()
    try: s.close()
    except: pass
    with _tab_lock:
        info = treo_tabs.pop(tab_key, {}).copy()
    info["dừng_lúc"]       = datetime.now().strftime("%H:%M:%S %d-%m-%Y")
    info["tổng_thời_gian"] = int((datetime.now() - start).total_seconds())
    treo_history.append(info)

def dotiendat_gui_file(token, channel_id, content, file_path, session=None, typing=False):
    """Upload file ảnh/video thật lên Discord — không có link trong chat."""
    if typing and random.random() < 0.4:
        dotiendat_gia_lap_typing(token, channel_id)
        time.sleep(random.uniform(0.3, 1.2))

    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    hdr = {
        "Authorization": token,
        "User-Agent": dotiendat_xoay_user_agent(),
        "X-Super-Properties": random.choice(_XSUPER_LIST),
    }
    s = session or _pool.get()
    text = dotiendat_them_noise_tin(content)

    for attempt in range(3):
        try:
            with open(file_path, "rb") as f:
                files = {"file": (os.path.basename(file_path), f)}
                data  = {"content": text}
                r = s.post(url, headers=hdr, data=data, files=files, timeout=30)
            if r.status_code in (200, 201):
                dotiendat_log_file("OK", f"ch={channel_id} | file={os.path.basename(file_path)}")
                return True, r.text
            if r.status_code == 429:
                dotiendat_doi_ratelimit(r.headers)
                continue
            if r.status_code in (401, 403):
                return False, f"Token lỗi {r.status_code}"
            if r.status_code >= 500:
                time.sleep(2 + attempt); continue
            return False, f"HTTP {r.status_code} {r.text[:80]}"
        except requests.exceptions.ConnectionError:
            _pool.rebuild()
            dotiendat_cho_co_mang(threading.Event(), interval=3)
            time.sleep(1 + attempt)
        except requests.exceptions.Timeout:
            dotiendat_log("TIMEOUT", f"Lần {attempt+1}")
            time.sleep(2)
        except Exception as e:
            return False, str(e)
    return False, "Hết retry"

def dotiendat_worker_file(token, channel_id, get_message_fn, file_list, delay, task_type, stop_event, tab_key):
    """Worker upload file ảnh/video thật — xoay vòng các file trong thư mục."""
    ok = fail = consec_fail = msg_count = 0
    start = datetime.now()
    s = dotiendat_tao_session()
    ka_stop = threading.Event()
    threading.Thread(target=dotiendat_keepalive, args=(token, ka_stop), daemon=True).start()
    gc_counter = 0
    file_idx = 0

    while not stop_event.is_set():
        if not dotiendat_kiem_tra_mang():
            dotiendat_cho_co_mang(stop_event)
            _pool.rebuild_tat_ca()
            try: s.close()
            except: pass
            s = dotiendat_tao_session()
            continue

        msg       = get_message_fn()
        fp        = file_list[file_idx % len(file_list)]
        file_idx += 1
        success, resp = dotiendat_gui_file(token, channel_id, msg, fp, session=s, typing=True)

        if success:
            ok += 1; msg_count += 1; consec_fail = 0; status = "Đang chạy"
            dotiendat_log("OK", f"#{ok} -> {channel_id} | {os.path.basename(fp)}")
        else:
            fail += 1; consec_fail += 1
            status = "Rớt (fail x5)" if consec_fail >= RETRY_LIMIT else "Đang chạy"
            dotiendat_log("LỖI", f"#{fail} -> {os.path.basename(fp)} | {resp[:60]}")
            if consec_fail >= RETRY_LIMIT:
                sleep_t = dotiendat_tinh_backoff(consec_fail)
                dotiendat_log("BACKOFF", f"Chờ {sleep_t:.1f}s")
                stop_event.wait(sleep_t)
                try: s.close()
                except: pass
                s = dotiendat_tao_session()
                continue

        uptime = int((datetime.now() - start).total_seconds())
        with _tab_lock:
            if tab_key in treo_tabs:
                treo_tabs[tab_key].update({
                    "ok": ok, "fail": fail, "uptime": uptime,
                    "status": status, "last_update": datetime.now().strftime("%H:%M:%S"),
                })

        gc_counter += 1
        if gc_counter >= 100: dotiendat_don_ram(); gc_counter = 0
        if msg_count > 0 and msg_count % 200 == 0:
            dotiendat_nghi_ngau_nhien(stop_event, 30, 90)

        actual_delay = dotiendat_delay_ngau_nhien(delay)
        for _ in range(max(1, int(actual_delay * 10))):
            if stop_event.is_set(): break
            time.sleep(0.1)

    ka_stop.set()
    try: s.close()
    except: pass
    with _tab_lock:
        info = treo_tabs.pop(tab_key, {}).copy()
    info["dừng_lúc"]       = datetime.now().strftime("%H:%M:%S %d-%m-%Y")
    info["tổng_thời_gian"] = int((datetime.now() - start).total_seconds())
    treo_history.append(info)

def dotiendat_bat_task_file(token, channel_id, get_msg_fn, file_list, delay, task_type):
    stop_event = threading.Event()
    key = f"{task_type}_{channel_id}_{int(time.time()*1000)}"
    with _tab_lock:
        treo_tabs[key] = {
            "type": task_type, "channel": channel_id, "token": token[:20] + "...",
            "ok": 0, "fail": 0, "uptime": 0,
            "status": "Khởi động", "last_update": "---",
            "stop_event": stop_event,
        }
    threading.Thread(
        target=dotiendat_worker_file,
        args=(token, channel_id, get_msg_fn, file_list, delay, task_type, stop_event, key),
        daemon=True,
    ).start()
    dotiendat_log("KHỞI CHẠY", f"[{task_type}] channel={channel_id} | {len(file_list)} file")
    return key


    """Worker dùng cho Treo Ảnh và Treo Video — gửi nội dung kèm link CDN."""
    ok = fail = consec_fail = msg_count = 0
    start = datetime.now()
    s = dotiendat_tao_session()
    ka_stop = threading.Event()
    threading.Thread(target=dotiendat_keepalive, args=(token, ka_stop), daemon=True).start()
    gc_counter = 0

    while not stop_event.is_set():
        if not dotiendat_kiem_tra_mang():
            dotiendat_cho_co_mang(stop_event)
            _pool.rebuild_tat_ca()
            try: s.close()
            except: pass
            s = dotiendat_tao_session()
            continue

        msg = get_message_fn()
        success, resp = dotiendat_gui_discord_embed(token, channel_id, msg, cdn_url, session=s, typing=True)

        if success:
            ok += 1; msg_count += 1; consec_fail = 0; status = "Đang chạy"
            dotiendat_log("OK", f"#{ok} -> {channel_id} | {msg[:40]}")
        else:
            fail += 1; consec_fail += 1
            status = "Rớt (fail x5)" if consec_fail >= RETRY_LIMIT else "Đang chạy"
            dotiendat_log("LỖI", f"#{fail} -> {channel_id} | {resp[:60]}")
            if consec_fail >= RETRY_LIMIT:
                sleep_t = dotiendat_tinh_backoff(consec_fail)
                dotiendat_log("BACKOFF", f"Chờ {sleep_t:.1f}s")
                stop_event.wait(sleep_t)
                try: s.close()
                except: pass
                s = dotiendat_tao_session()
                continue

        uptime = int((datetime.now() - start).total_seconds())
        with _tab_lock:
            if tab_key in treo_tabs:
                treo_tabs[tab_key].update({
                    "ok": ok, "fail": fail, "uptime": uptime,
                    "status": status, "last_update": datetime.now().strftime("%H:%M:%S"),
                })

        gc_counter += 1
        if gc_counter >= 100:
            dotiendat_don_ram(); gc_counter = 0
        if msg_count > 0 and msg_count % 200 == 0:
            dotiendat_nghi_ngau_nhien(stop_event, 30, 90)

        actual_delay = dotiendat_delay_ngau_nhien(delay)
        for _ in range(max(1, int(actual_delay * 10))):
            if stop_event.is_set(): break
            time.sleep(0.1)

    ka_stop.set()
    try: s.close()
    except: pass
    with _tab_lock:
        info = treo_tabs.pop(tab_key, {}).copy()
    info["dừng_lúc"]       = datetime.now().strftime("%H:%M:%S %d-%m-%Y")
    info["tổng_thời_gian"] = int((datetime.now() - start).total_seconds())
    treo_history.append(info)

def dotiendat_bat_task_embed(token, channel_id, get_msg_fn, cdn_url, delay, task_type):
    """Khởi động task embed (ảnh/video)."""
    stop_event = threading.Event()
    key = f"{task_type}_{channel_id}_{int(time.time()*1000)}"
    with _tab_lock:
        treo_tabs[key] = {
            "type": task_type, "channel": channel_id, "token": token[:20] + "...",
            "ok": 0, "fail": 0, "uptime": 0,
            "status": "Khởi động", "last_update": "---",
            "stop_event": stop_event,
        }
    threading.Thread(
        target=dotiendat_worker_embed,
        args=(token, channel_id, get_msg_fn, cdn_url, delay, task_type, stop_event, key),
        daemon=True,
    ).start()
    dotiendat_log("KHỞI CHẠY", f"[{task_type}] channel={channel_id}")
    return key

def dotiendat_bat_task(token, channel_id, get_msg_fn, delay, task_type, allow_everyone=False):
    stop_event = threading.Event()
    key = f"{task_type}_{channel_id}_{int(time.time()*1000)}"
    with _tab_lock:
        treo_tabs[key] = {
            "type": task_type, "channel": channel_id, "token": token[:20] + "...",
            "ok": 0, "fail": 0, "uptime": 0,
            "status": "Khởi động", "last_update": "---",
            "stop_event": stop_event,
        }
    threading.Thread(
        target=dotiendat_worker,
        args=(token, channel_id, get_msg_fn, delay, task_type, stop_event, key),
        kwargs={"allow_everyone": allow_everyone},
        daemon=True,
    ).start()
    dotiendat_log("KHỞI CHẠY", f"[{task_type}] channel={channel_id}")
    return key


def dotiendat_doc_file(path, tung_dong=False):
    if not os.path.exists(path):
        dotiendat_log("LỖI", f"Không tìm thấy file: {path}")
        return []
    with open(path, "r", encoding="utf-8") as f:
        if tung_dong:
            return [l.strip() for l in f if l.strip()]
        content = f.read().strip()
        return [content] if content else []

def dotiendat_nhap_so(prompt, default=2):
    while True:
        s = input(prompt).strip()
        if not s:
            return default
        try:
            return int(s)
        except:
            print("Nhập số nguyên hợp lệ!")

def dotiendat_nhap_nhieu(prompt):
    items = []
    while True:
        v = input(f"  {prompt} (gõ done để xong): ").strip()
        if v.lower() == "done":
            break
        if v:
            items.append(v)
    return items

def dotiendat_thong_tin_he_thong():
    ok, ms = dotiendat_ping_discord()
    alive  = dotiendat_don_thread_chet()
    print(f"\n  Hệ điều hành   : {platform.system()} {platform.release()}")
    print(f"  Python         : {sys.version.split()[0]}")
    print(f"  Discord ping   : {'OK' if ok else 'FAIL'} ({ms}ms)")
    print(f"  Kết nối mạng  : {'Có' if dotiendat_kiem_tra_mang() else 'Không'}")
    print(f"  Thread sống   : {alive}")
    print(f"  Task đang chạy: {len(treo_tabs)}")
    print(f"  Lịch sử task  : {len(treo_history)}")
    input("\n  Nhấn Enter để quay lại...")


def dotiendat_xem_dung():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(f"\n=== TASK ĐANG CHẠY [{datetime.now().strftime('%H:%M:%S')}] ===")
        with _tab_lock:
            keys = list(treo_tabs.keys())
            snap = {k: dict(treo_tabs[k]) for k in keys}
        if not keys:
            print("  (Không có task nào)")
        for i, k in enumerate(keys, 1):
            info = snap[k]
            u = int(info.get("uptime", 0))
            h, r = divmod(u, 3600); m, s2 = divmod(r, 60)
            print(f"  [{i}] {info['type']} | ch={info['channel']} | {info['status']}")
            print(f"       OK={info['ok']} FAIL={info['fail']} UP={h:02}:{m:02}:{s2:02} | {info['last_update']}")
        print("\n  0 = quay lại | stop all = dừng hết | số = dừng task đó")
        c = input("  > ").strip().lower()
        if c == "0":
            break
        elif c == "stop all":
            with _tab_lock:
                for k in keys:
                    if k in treo_tabs:
                        treo_tabs[k]["stop_event"].set()
            dotiendat_log("HỆ THỐNG", "Đã dừng tất cả task")
            time.sleep(1)
        else:
            try:
                idx = int(c) - 1
                if 0 <= idx < len(keys):
                    k = keys[idx]
                    with _tab_lock:
                        if k in treo_tabs:
                            treo_tabs[k]["stop_event"].set()
                    dotiendat_log("HỆ THỐNG", f"Đã dừng task {k}")
                else:
                    print("  STT không hợp lệ")
            except ValueError:
                print("  Nhập số hoặc 'stop all'")
            time.sleep(0.8)


def dotiendat_treo():
    print("\n=== TREO DISCORD ===")
    tokens   = dotiendat_nhap_nhieu("Token Discord")
    channels = dotiendat_nhap_nhieu("ID Channel")
    files    = dotiendat_nhap_nhieu("File ngôn treo (.txt)")
    if not tokens or not channels or not files:
        print("[!] Thiếu thông tin."); return
    msgs = []
    for f in files:
        msgs += dotiendat_doc_file(f, tung_dong=False)
    if not msgs:
        print("[!] File rỗng."); return
    full_msg = "\n\n".join(msgs)
    delay  = dotiendat_nhap_so("  Delay (giây, mặc định 2): ", 2)
    tokens = dotiendat_loc_token_hop_le(tokens)
    if not tokens:
        print("[!] Không có token hợp lệ."); return
    tokens = dotiendat_xoay_token(tokens)
    for tk in tokens:
        for ch in channels:
            dotiendat_bat_task(tk, ch, lambda: full_msg, delay, "Treo")

def dotiendat_nhay():
    print("\n=== NHAY DISCORD ===")
    tokens   = dotiendat_nhap_nhieu("Token Discord")
    channels = dotiendat_nhap_nhieu("ID Channel")
    if not tokens or not channels:
        print("[!] Thiếu thông tin."); return
    msgs = dotiendat_doc_file("nhay.txt", tung_dong=True)
    if not msgs:
        print("[!] nhay.txt rỗng hoặc không tồn tại."); return
    delay  = dotiendat_nhap_so("  Delay (giây, mặc định 2): ", 2)
    tokens = dotiendat_loc_token_hop_le(tokens)
    if not tokens:
        print("[!] Không có token hợp lệ."); return
    tokens = dotiendat_xoay_token(tokens)
    for tk in tokens:
        for ch in channels:
            def make_fn(m_list):
                lk = threading.Lock(); c2 = [0]
                def fn():
                    with lk:
                        v = m_list[c2[0] % len(m_list)]; c2[0] += 1; return v
                return fn
            dotiendat_bat_task(tk, ch, make_fn(msgs), delay, "Nhay")

def dotiendat_nhay_tag():
    print("\n=== NHAY TAG DISCORD ===")
    tokens   = dotiendat_nhap_nhieu("Token Discord")
    channels = dotiendat_nhap_nhieu("ID Channel")
    target   = input("  ID user cần tag: ").strip()
    if not tokens or not channels or not target:
        print("[!] Thiếu thông tin."); return
    msgs = dotiendat_doc_file("nhay.txt", tung_dong=True)
    if not msgs:
        print("[!] nhay.txt rỗng."); return
    delay  = dotiendat_nhap_so("  Delay (giây, mặc định 2): ", 2)
    tokens = dotiendat_loc_token_hop_le(tokens)
    if not tokens:
        print("[!] Không có token hợp lệ."); return
    tokens = dotiendat_xoay_token(tokens)
    for tk in tokens:
        for ch in channels:
            def make_fn(m_list):
                lk = threading.Lock(); c2 = [0]
                def fn():
                    with lk:
                        v = m_list[c2[0] % len(m_list)]; c2[0] += 1
                        return f"<@{target}> {v}"
                return fn
            dotiendat_bat_task(tk, ch, make_fn(msgs), delay, "Nhay Tag")

def dotiendat_so_tag():
    print("\n=== SỚ TAG DISCORD ===")
    tokens   = dotiendat_nhap_nhieu("Token Discord")
    channels = dotiendat_nhap_nhieu("ID Channel")
    tag_ids  = dotiendat_nhap_nhieu("ID user cần tag")
    if not tokens or not channels or not tag_ids:
        print("[!] Thiếu thông tin."); return
    tag_str = " ".join(f"<@{u}>" for u in tag_ids)
    msgs = dotiendat_doc_file("so.txt", tung_dong=True)
    if not msgs:
        print("[!] so.txt rỗng."); return
    delay  = dotiendat_nhap_so("  Delay (giây, mặc định 2): ", 2)
    tokens = dotiendat_loc_token_hop_le(tokens)
    if not tokens:
        print("[!] Không có token hợp lệ."); return
    tokens = dotiendat_xoay_token(tokens)
    for tk in tokens:
        for ch in channels:
            def make_fn(m_list, ts):
                lk = threading.Lock(); c2 = [0]
                def fn():
                    with lk:
                        v = m_list[c2[0] % len(m_list)]; c2[0] += 1
                        return f"{ts} {v}"
                return fn
            dotiendat_bat_task(tk, ch, make_fn(msgs, tag_str), delay, "Sớ Tag")

def dotiendat_poll():
    print("\n=== POLL DISCORD ===")
    REACTIONS = ["😭","🤣","💤","💦","😅","🐉","😏","🤯","👁","😪",
                 "😤","😓","🤓","😑","💔","💙","💓","💘","💥","💌",
                 "💢","💨","💫","🍀","😰","🌚","🧸","👾","🐻","😱",
                 "🤔","😬","🤪","😡","⭐","🙈","🙊","💚","💜","❤️"]
    tokens   = dotiendat_nhap_nhieu("Token Discord")
    channels = dotiendat_nhap_nhieu("ID Channel")
    tag_ids  = dotiendat_nhap_nhieu("ID user cần tag (bỏ trống thì done luôn)")
    tag_str  = " ".join(f"<@{u}>" for u in tag_ids) if tag_ids else ""
    if not tokens or not channels:
        print("[!] Thiếu thông tin."); return
    msgs = dotiendat_doc_file("nhay.txt", tung_dong=True)
    if not msgs:
        with open("nhay.txt", "w", encoding="utf-8") as f:
            f.write("Câu hỏi 1?\nCâu hỏi 2?\n")
        print("[!] Đã tạo nhay.txt mẫu, sửa nội dung rồi chạy lại."); return
    delay  = dotiendat_nhap_so("  Delay (giây, mặc định 3): ", 3)
    tokens = dotiendat_loc_token_hop_le(tokens)
    if not tokens:
        print("[!] Không có token hợp lệ."); return
    tokens = dotiendat_xoay_token(tokens)

    def poll_worker(token, channel_id, stop_event, key):
        s = dotiendat_tao_session()
        ka_stop = threading.Event()
        threading.Thread(target=dotiendat_keepalive, args=(token, ka_stop), daemon=True).start()
        ok = fail = 0
        start = datetime.now()
        while not stop_event.is_set():
            if not dotiendat_kiem_tra_mang():
                dotiendat_cho_co_mang(stop_event)
                continue
            for body in msgs:
                if stop_event.is_set():
                    break
                content = f"{tag_str} {body}".strip()
                ok_s, resp = dotiendat_gui_discord(token, channel_id, content, session=s, typing=True)
                if ok_s:
                    ok += 1
                    mid = None
                    try: mid = json.loads(resp).get("id")
                    except: pass
                    if mid:
                        def add_all(m):
                            for emj in REACTIONS:
                                dotiendat_them_reaction(token, channel_id, m, emj)
                                time.sleep(0.35)
                        threading.Thread(target=add_all, args=(mid,), daemon=True).start()
                else:
                    fail += 1
                uptime = int((datetime.now() - start).total_seconds())
                with _tab_lock:
                    if key in treo_tabs:
                        treo_tabs[key].update({
                            "ok": ok, "fail": fail, "uptime": uptime,
                            "status": "Đang chạy",
                            "last_update": datetime.now().strftime("%H:%M:%S")
                        })
                stop_event.wait(dotiendat_delay_ngau_nhien(delay))
        ka_stop.set()
        try: s.close()
        except: pass
        with _tab_lock:
            info = treo_tabs.pop(key, {}).copy()
        info["dừng_lúc"] = datetime.now().strftime("%H:%M:%S %d-%m-%Y")
        treo_history.append(info)

    for tk in tokens:
        for ch in channels:
            stop_event = threading.Event()
            key = f"Poll_{ch}_{int(time.time()*1000)}"
            with _tab_lock:
                treo_tabs[key] = {
                    "type": "Poll", "channel": ch, "token": tk[:20]+"...",
                    "ok": 0, "fail": 0, "uptime": 0,
                    "status": "Khởi động", "last_update": "---",
                    "stop_event": stop_event,
                }
            threading.Thread(target=poll_worker, args=(tk, ch, stop_event, key), daemon=True).start()


                                                               
                         
                                                               
def dotiendat_treo_anh():
    print("\n=== TREO ẢNH DISCORD ===")
    tokens   = dotiendat_nhap_nhieu("Token Discord")
    channels = dotiendat_nhap_nhieu("ID Channel")
    files    = dotiendat_nhap_nhieu("File ngôn treo (.txt)")
    if not tokens or not channels or not files:
        print("[!] Thiếu thông tin."); return
    msgs = []
    for f in files:
        msgs += dotiendat_doc_file(f, tung_dong=False)
    if not msgs:
        print("[!] File rỗng."); return
    full_msg = "\n\n".join(msgs)

    thu_muc = input("  Tên thư mục chứa ảnh (vd: anh/): ").strip().rstrip("/\\")
    anh_exts = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp")
    if not os.path.isdir(thu_muc):
        print(f"[!] Không tìm thấy thư mục: {thu_muc}"); return
    file_list = sorted([
        os.path.join(thu_muc, fn) for fn in os.listdir(thu_muc)
        if fn.lower().endswith(anh_exts)
    ])
    if not file_list:
        print(f"[!] Không có file ảnh nào trong thư mục {thu_muc}"); return
    print(f"  Tìm thấy {len(file_list)} ảnh.")

    delay  = dotiendat_nhap_so("  Delay (giây, mặc định 2): ", 2)
    tokens = dotiendat_loc_token_hop_le(tokens)
    if not tokens:
        print("[!] Không có token hợp lệ."); return
    tokens = dotiendat_xoay_token(tokens)
    for tk in tokens:
        for ch in channels:
            dotiendat_bat_task_file(tk, ch, lambda: full_msg, file_list, delay, "Treo Ảnh")

                                                               
                           
                                                               
def dotiendat_treo_video():
    print("\n=== TREO VIDEO DISCORD ===")
    tokens   = dotiendat_nhap_nhieu("Token Discord")
    channels = dotiendat_nhap_nhieu("ID Channel")
    files    = dotiendat_nhap_nhieu("File ngôn treo (.txt)")
    if not tokens or not channels or not files:
        print("[!] Thiếu thông tin."); return
    msgs = []
    for f in files:
        msgs += dotiendat_doc_file(f, tung_dong=False)
    if not msgs:
        print("[!] File rỗng."); return
    full_msg = "\n\n".join(msgs)

    thu_muc = input("  Tên thư mục chứa video (vd: video/): ").strip().rstrip("/\\")
    vid_exts = (".mp4", ".webm", ".mov", ".mkv", ".avi")
    if not os.path.isdir(thu_muc):
        print(f"[!] Không tìm thấy thư mục: {thu_muc}"); return
    file_list = sorted([
        os.path.join(thu_muc, fn) for fn in os.listdir(thu_muc)
        if fn.lower().endswith(vid_exts)
    ])
    if not file_list:
        print(f"[!] Không có file video nào trong thư mục {thu_muc}"); return
    print(f"  Tìm thấy {len(file_list)} video.")

    delay  = dotiendat_nhap_so("  Delay (giây, mặc định 2): ", 2)
    tokens = dotiendat_loc_token_hop_le(tokens)
    if not tokens:
        print("[!] Không có token hợp lệ."); return
    tokens = dotiendat_xoay_token(tokens)
    for tk in tokens:
        for ch in channels:
            dotiendat_bat_task_file(tk, ch, lambda: full_msg, file_list, delay, "Treo Video")

                                                               
                                         
                                                               
def dotiendat_treo_tag_all():
    print("\n=== NHAY TAG ALL DISCORD ===")
    tokens   = dotiendat_nhap_nhieu("Token Discord")
    channels = dotiendat_nhap_nhieu("ID Channel")
    files    = dotiendat_nhap_nhieu("File nội dung (.txt)")
    if not tokens or not channels or not files:
        print("[!] Thiếu thông tin."); return
    msgs = []
    for f in files:
        msgs += dotiendat_doc_file(f, tung_dong=True)
    if not msgs:
        print("[!] File rỗng."); return
    delay  = dotiendat_nhap_so("  Delay (giây, mặc định 2): ", 2)
    tokens = dotiendat_loc_token_hop_le(tokens)
    if not tokens:
        print("[!] Không có token hợp lệ."); return
    tokens = dotiendat_xoay_token(tokens)
    for tk in tokens:
        for ch in channels:
            def make_fn(m_list):
                lk = threading.Lock(); c2 = [0]
                def fn():
                    with lk:
                        v = m_list[c2[0] % len(m_list)]; c2[0] += 1; return v
                return fn
            dotiendat_bat_task(tk, ch, make_fn(msgs), delay, "Nhay Tag All", allow_everyone=True)

                                                               
                                            
                                                               
def dotiendat_nhay_tag_phong_to():
    print("\n=== NHAY TAG PHÓNG TO DISCORD ===")
    tokens   = dotiendat_nhap_nhieu("Token Discord")
    channels = dotiendat_nhap_nhieu("ID Channel")
    raw_ids  = input("  ID user cần tag (nhiều UID cách nhau dấu ,): ").strip()
    if not tokens or not channels or not raw_ids:
        print("[!] Thiếu thông tin."); return
    # Tách nhiều UID bằng dấu phẩy, loại bỏ khoảng trắng
    uid_list = [u.strip() for u in raw_ids.replace(",", " ").split() if u.strip()]
    tag_str  = " ".join(f"<@{u}>" for u in uid_list)
    msgs = dotiendat_doc_file("nhay.txt", tung_dong=True)
    if not msgs:
        print("[!] nhay.txt rỗng."); return
    delay  = dotiendat_nhap_so("  Delay (giây, mặc định 2): ", 2)
    tokens = dotiendat_loc_token_hop_le(tokens)
    if not tokens:
        print("[!] Không có token hợp lệ."); return
    tokens = dotiendat_xoay_token(tokens)
    for tk in tokens:
        for ch in channels:
            def make_fn(m_list, ts):
                lk = threading.Lock(); c2 = [0]
                def fn():
                    with lk:
                        v = m_list[c2[0] % len(m_list)]; c2[0] += 1
                        return f"# {ts} {v}"
                return fn
            dotiendat_bat_task(tk, ch, make_fn(msgs, tag_str), delay, "Nhay Tag Phóng To")

                                                               
                                                    
                                                               
def dotiendat_nhay_phong_to():
    print("\n=== NHAY PHÓNG TO DISCORD ===")
    tokens   = dotiendat_nhap_nhieu("Token Discord")
    channels = dotiendat_nhap_nhieu("ID Channel")
    if not tokens or not channels:
        print("[!] Thiếu thông tin."); return
    msgs = dotiendat_doc_file("nhay.txt", tung_dong=True)
    if not msgs:
        print("[!] nhay.txt rỗng hoặc không tồn tại."); return
    delay  = dotiendat_nhap_so("  Delay (giây, mặc định 2): ", 2)
    tokens = dotiendat_loc_token_hop_le(tokens)
    if not tokens:
        print("[!] Không có token hợp lệ."); return
    tokens = dotiendat_xoay_token(tokens)
    for tk in tokens:
        for ch in channels:
            def make_fn(m_list):
                lk = threading.Lock(); c2 = [0]
                def fn():
                    with lk:
                        v = m_list[c2[0] % len(m_list)]; c2[0] += 1
                        return f"# {v}"
                return fn
            dotiendat_bat_task(tk, ch, make_fn(msgs), delay, "Nhay Phóng To")


def dotiendat_menu():
    _gc_stop = threading.Event()
    threading.Thread(target=dotiendat_auto_gc, args=(_gc_stop,), daemon=True).start()
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("=" * 42)
        print("        TOOL TREO DISCORD")
        print("=" * 42)
        print("  1. Treo Discord")
        print("  2. Nhay Discord")
        print("  3. Nhay Tag Discord")
        print("  4. Sớ Tag Discord")
        print("  5. Poll Discord")
        print("  ──────────────────────────────────────")
        print("  6. Treo Ảnh")
        print("  7. Treo Video")
        print("  8. Treo Tag All (@everyone)")
        print("  9. Nhay Tag Phóng To")
        print("  10. Nhay Phóng To")
        print("  ──────────────────────────────────────")
        print("  0. Xem / Dừng Task")
        print("  i. Thông tin hệ thống")
        print("  q. Thoát")
        print("=" * 42)
        c = input("\n  Chọn: ").strip().lower()
        if   c == "1":  dotiendat_treo()
        elif c == "2":  dotiendat_nhay()
        elif c == "3":  dotiendat_nhay_tag()
        elif c == "4":  dotiendat_so_tag()
        elif c == "5":  dotiendat_poll()
        elif c == "6":  dotiendat_treo_anh()
        elif c == "7":  dotiendat_treo_video()
        elif c == "8":  dotiendat_treo_tag_all()
        elif c == "9":  dotiendat_nhay_tag_phong_to()
        elif c == "10": dotiendat_nhay_phong_to()
        elif c == "0":  dotiendat_xem_dung()
        elif c == "i":  dotiendat_thong_tin_he_thong()
        elif c == "q":
            _gc_stop.set()
            dotiendat_log("HỆ THỐNG", "Thoát.")
            break
        else:
            print("  Chọn sai rồi!")
            time.sleep(0.8)

if __name__ == "__main__":
    try:
        dotiendat_menu()
    except KeyboardInterrupt:
        dotiendat_log("HỆ THỐNG", "Dừng.")
    except Exception as e:
        dotiendat_log("LỖI", str(e))
        input("Nhấn Enter để thoát")
