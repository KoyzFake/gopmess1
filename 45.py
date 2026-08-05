import requests
import os
import re
import json
import random
from time import sleep
from datetime import datetime

do = "\033[1;31m"
luc = "\033[1;32m"
vang = "\033[1;33m"
trang = "\033[1;37m"
xanh = "\033[1;36m"
thanh = f'{do}[{trang}</>{do}] {trang}=> '

def thanhngang(so):
    for i in range(so):
        print(trang+'-', end='')
    print('')

def banner():
    os.system('cls' if os.name=='nt' else 'clear')
    print("Tool Thêm Bạn Bè Facebook")
    print("DoTienDat-Tool")
    thanhngang(50)

def Delay(value):
    while not(value <= 1):
        value -= 0.123
        print(f'[{xanh}DELAY{trang}] [{xanh}{str(value)[0:5]}{trang}]', ' ', end = '\r')
        sleep(0.02)
    print('')

def generate_vietnamese_names():
    ho = [
        "Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Vũ", "Đặng", "Bùi", "Đỗ", "Hồ",
        "Ngô", "Dương", "Lý", "Võ", "Đinh", "Tô", "Lâm", "Phan", "Trương", "Huỳnh",
        "Cao", "Đoàn", "Lưu", "Mai", "Tăng", "Hà", "Trịnh", "Đào", "Bành", "Lục",
        "La", "Quách", "Tạ", "Thái", "Đàm", "Bế", "Châu", "Hứa", "Kiều", "Ninh",
        "Vương", "Triệu", "Hán", "Tôn", "Lã", "Lương", "Khương", "Tần", "Hình", "Từ"
    ]
    
    ten_dem = [
        "Văn", "Thị", "Ngọc", "Minh", "Hồng", "Anh", "Hải", "Bích", "Đức", "Lan",
        "Phong", "Mai", "Hương", "Tuấn", "Quỳnh", "Hòa", "Linh", "Khoa", "Như", "Phúc",
        "Thanh", "Tâm", "Duy", "Hạnh", "Hằng", "Khánh", "Bảo", "Trung", "Nga", "Nhật",
        "Thùy", "Yến", "Xuân", "Sơn", "Tùng", "Phương", "Diệu", "Kiên", "Trí", "Vinh",
        "Huyền", "Thảo", "Đạt", "Cường", "Hòa", "Khôi", "Long", "Nam", "Quân", "Việt"
    ]
    
    ten = [
        "An", "Bình", "Cường", "Duy", "Hà", "Hùng", "Hương", "Khang", "Lan", "Linh",
        "Mai", "Minh", "Nam", "Ngọc", "Phúc", "Phong", "Quân", "Quỳnh", "Sơn", "Thảo",
        "Tâm", "Thanh", "Thịnh", "Trang", "Trí", "Tuấn", "Tùng", "Vân", "Việt", "Vy",
        "Xuân", "Yến", "Ân", "Bảo", "Châu", "Đạt", "Đông", "Hải", "Hòa", "Khoa",
        "Hân", "Hiếu", "Hiệp", "Huy", "Khải", "Long", "Nhi", "Phương", "Quý", "Thắng"
    ]
    
    vietnamese_names = []
    
    for i in range(5000):
        ho_random = random.choice(ho)
        structure = random.choice([2, 3, 4])
        
        if structure == 2:
            ten_random = random.choice(ten)
            name = f"{ho_random} {ten_random}"
        elif structure == 3:
            ten_dem_random = random.choice(ten_dem)
            ten_random = random.choice(ten)
            name = f"{ho_random} {ten_dem_random} {ten_random}"
        else:
            ten_dem_random1 = random.choice(ten_dem)
            ten_dem_random2 = random.choice(ten_dem)
            ten_random = random.choice(ten)
            name = f"{ho_random} {ten_dem_random1} {ten_dem_random2} {ten_random}"
        
        vietnamese_names.append(name)
    
    return vietnamese_names

class Facebook:
    def __init__(self, cookie: str):
        try:
            self.fb_dtsg = ''
            self.jazoest = ''
            self.cookie = cookie
            self.session = requests.Session()
            self.id = self.cookie.split('c_user=')[1].split(';')[0]
            self.headers = {
                'authority': 'www.facebook.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-language': 'vi',
                'sec-ch-prefers-color-scheme': 'light',
                'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
                'viewport-width': '1366',
                'Cookie': self.cookie
            }
            url = self.session.get(f'https://www.facebook.com/{self.id}', headers=self.headers).url
            response = self.session.get(url, headers=self.headers).text
            matches = re.findall(r'\["DTSGInitialData",\[\],\{"token":"(.*?)"\}', response)
            if len(matches) > 0:
                self.fb_dtsg += matches[0]
                self.jazoest += re.findall(r'jazoest=(.*?)\"', response)[0]
        except:
            pass

    def info(self):
        try:
            get = self.session.get('https://www.facebook.com/me', headers=self.headers).url
            url = 'https://www.facebook.com/' + get.split('%2F')[-2] + '/' if 'next=' in get else get
            response = self.session.get(url, headers=self.headers, params={"locale": "vi_VN"})
            data_split = response.text.split('"CurrentUserInitialData",[],{')
            json_data = '{' + data_split[1].split('},')[0] + '}'
            parsed_data = json.loads(json_data)
            id = parsed_data.get('USER_ID', '0')
            name = parsed_data.get('NAME', '')
            if id == '0' and name == '':
                return 'cookieout'
            elif '828281030927956' in response.text:
                return '956'
            elif '1501092823525282' in response.text:
                return '282'
            elif '601051028565049' in response.text:
                return 'spam'
            else:
                id, name = parsed_data.get('USER_ID'), parsed_data.get('NAME')
                return {'success': 200, 'id': id, 'name': name}
        except:
            pass

    def timban(self, text):
        try:
            data = {
                'av': self.id,
                'fb_dtsg': self.fb_dtsg,
                'jazoest': self.jazoest,
                'fb_api_caller_class': 'RelayModern',
                'fb_api_req_friendly_name': 'SearchCometResultsInitialResultsQuery',
                'variables': '{"count":5,"allow_streaming":false,"args":{"callsite":"COMET_GLOBAL_SEARCH","config":{"exact_match":false,"high_confidence_config":null,"intercept_config":null,"sts_disambiguation":null,"watch_config":null},"context":{"bsid":"23bd9138-cec6-4e71-aaeb-225fc8964e5b","tsid":"0.10477759801522946"},"experience":{"client_defined_experiences":["ADS_PARALLEL_FETCH"],"encoded_server_defined_params":null,"fbid":null,"type":"GLOBAL_SEARCH"},"filters":[],"text":"'+text+'"},"cursor":null,"feedbackSource":23,"fetch_filters":true,"renderLocation":"search_results_page","scale":1,"stream_initial_count":0,"useDefaultActor":false,"__relay_internal__pv__GHLShouldChangeAdIdFieldNamerelayprovider":true,"__relay_internal__pv__GHLShouldChangeSponsoredDataFieldNamerelayprovider":true,"__relay_internal__pv__IsWorkUserrelayprovider":false,"__relay_internal__pv__FBReels_deprecate_short_form_video_context_gkrelayprovider":true,"__relay_internal__pv__CometFeedStoryDynamicResolutionPhotoAttachmentRenderer_experimentWidthrelayprovider":500,"__relay_internal__pv__CometImmersivePhotoCanUserDisable3DMotionrelayprovider":false,"__relay_internal__pv__WorkCometIsEmployeeGKProviderrelayprovider":false,"__relay_internal__pv__IsMergQAPollsrelayprovider":false,"__relay_internal__pv__FBReelsMediaFooter_comet_enable_reels_ads_gkrelayprovider":true,"__relay_internal__pv__CometUFIReactionsEnableShortNamerelayprovider":false,"__relay_internal__pv__CometUFIShareActionMigrationrelayprovider":true,"__relay_internal__pv__CometUFI_dedicated_comment_routable_dialog_gkrelayprovider":false,"__relay_internal__pv__StoriesArmadilloReplyEnabledrelayprovider":true,"__relay_internal__pv__FBReelsIFUTileContent_reelsIFUPlayOnHoverrelayprovider":false}',
                'server_timestamps': 'true',
                'doc_id': '9545374252239656'
            }
            response = self.session.post('https://www.facebook.com/api/graphql/', headers=self.headers, data=data).json()
            profile = response["data"]["serpResponse"]["results"]["edges"][0]['rendering_strategy']['result_rendering_strategies'][0]['view_model']['profile']
            name = profile.get('name')
            uid = profile.get('id')
            return {'status': 'success', 'id': uid, 'name': name}
        except:
            return {'status': 'error', 'trangthai': 'thatbai'}

    def ketban(self, idkb):
        try:
            data = {
                'av': self.id,
                'fb_dtsg': self.fb_dtsg,
                'jazoest': self.jazoest,
                'fb_api_caller_class': 'RelayModern',
                'fb_api_req_friendly_name': 'FriendingCometFriendRequestSendMutation',
                'variables': '{"input":{"attribution_id_v2":"ProfileCometTimelineListViewRoot.react,comet.profile.timeline.list,unexpected,1748257667487,475021,190055527696468,,;SearchCometGlobalSearchDefaultTabRoot.react,comet.search_results.default_tab,tap_search_bar,1748257603766,498383,391724414624676,,","click_proof_validation_result":null,"friend_requestee_ids":["'+idkb+'"],"friending_channel":"PROFILE_BUTTON","warn_ack_for_ids":[],"actor_id":"'+self.id+'","client_mutation_id":"6"},"scale":1}',
                'server_timestamps': 'true',
                'doc_id': '8805328442902902'
            }
            response = self.session.post('https://www.facebook.com/api/graphql/', headers=self.headers, data=data).json()
            trangthai = response["data"]["friend_request_send"]["friend_requestees"]
            if trangthai and trangthai[0].get('friendship_status') == 'OUTGOING_REQUEST':
                return {'status': 'success', 'trangthai': 'thanhcong'}
            else:
                return {'status': 'error', 'trangthai': 'thatbai'}
        except:
            return {'status': 'error', 'trangthai': 'thatbai'}

def addcookie():
    cookie = input(f'{thanh}{luc}Nhập Cookie Facebook: {vang}')
    fb = Facebook(cookie)
    info = fb.info()
    if 'success' in info:
        name = info['name']
        print(f'{thanh}{luc}Tên Facebook: {vang}{name}')
        thanhngang(50)
        return cookie
    else:
        print(f'{do}Cookie Facebook Die! Vui Lòng Nhập Lại!')
        return None

def main():
    banner()
    
    cookie = addcookie()
    if not cookie:
        return
    
    banner()
    
    print(f'{luc}=== CẤU HÌNH TOOL ===')
    
    while True:
        try:
            delay = int(input(f'{thanh}{luc}Nhập Delay Giữa Các Lần Tìm Bạn: {vang}'))
            if delay > 0:
                break
            else:
                print(f'{do}Vui Lòng Nhập Số Lớn Hơn 0')
        except:
            print(f'{do}Vui Lòng Nhập Số')
    
    while True:
        try:
            JobbBlock = int(input(f'{thanh}{luc}Sau Bao Nhiêu Lần Tìm Bạn Chống Block: {vang}'))
            if JobbBlock > 1:
                break
            else:
                print(f'{do}Vui Lòng Nhập Lớn Hơn 1')
        except:
            print(f'{do}Vui Lòng Nhập Số')
    
    while True:
        try:
            DelayBlock = int(input(f'{thanh}{luc}Sau {vang}{JobbBlock} {luc}Lần Tìm Bạn Nghỉ Bao Nhiêu Giây: {vang}'))
            if DelayBlock > 0:
                break
            else:
                print(f'{do}Vui Lòng Nhập Số Lớn Hơn 0')
        except:
            print(f'{do}Vui Lòng Nhập Số')
    
    while True:
        runidfb = input(f'{thanh}{luc}Bạn Có Muốn Ẩn Id Facebook Không? (y/n): {vang}').lower().strip()
        if runidfb in ['y', 'n', 'yes', 'no']:
            break
        else:
            print(f'{do}Vui Lòng Nhập y hoặc n')
    
    thanhngang(50)
    
    stt = 0
    fb = Facebook(cookie)
    vietnamese_names = generate_vietnamese_names()
    
    print(f'{luc}=== Do Tien Dat - Thêm Bạn Bè ===')
    thanhngang(50)
    
    while True:
        try:
            info = fb.info()
            if 'success' not in info:
                print(f'{do}Cookie Facebook Die! Vui Lòng Nhập Lại!')
                break
            
            namefb = info['name']
            idfb = str(info['id'])
            idrun = idfb[0]+idfb[1]+idfb[2]+"#"*(int(len(idfb)-3)) if runidfb.upper() =='Y' else idfb
            
            print(f'{luc}Id Facebook: {vang}{idrun}{do} | {luc}Tên Tài Khoản: {vang}{namefb}')
            
            ten = random.choice(vietnamese_names)
            
            timbb = fb.timban(ten)
            if timbb.get('trangthai') == 'thatbai':
                print(f'{trang}[{do}ERROR{trang}] {trang}Không Tìm Thấy Id Nào')
            else:
                id, name = timbb['id'], timbb['name']
                
                ketban = fb.ketban(id)
                if ketban.get('trangthai') == 'thanhcong':
                    timejob = datetime.now().strftime('%H:%M:%S')
                    stt += 1
                    print(f'{do}| {vang}{stt}{do} | {xanh}{timejob}{do} | {vang}THÊM BẠN{do} | {trang}{id}{do} | {luc}{name}{do}')
                else:
                    print(f'{trang}[{do}ERROR{trang}] {trang}Không Có Nút Kết Bạn')
            
            if stt % 20 == 0 and stt > 0:
                check = fb.info()
                if 'spam' in check:
                    print(f'{do}Tài Khoản {vang}{namefb} {do} bị spam')
                elif '282' in check:
                    print(f'{do}Tài Khoản {vang}{namefb} {do} bị chặn 282')
                    break
                elif '956' in check:
                    print(f'{do}Tài Khoản {vang}{namefb} {do} bị chặn 956')
                    break
                else:
                    print(f'{do}Tài Khoản {vang}{namefb} {do} cookie die')
                    break
            
            if stt % int(JobbBlock) == 0 and stt > 0:
                print(f'{luc}Nghỉ {vang}{DelayBlock} {luc} giây để hạn chế block...')
                Delay(DelayBlock)
            else:
                Delay(delay)
                
        except Exception as e:
            print(f'{do}Lỗi: {e}')
            sleep(2)

if __name__ == "__main__":
    main()
