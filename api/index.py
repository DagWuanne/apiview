from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import requests
import json

# Thông số Auth Leofame của bạn
TOKEN = '110b97200d34e0a6f57c7ba021e92af6'
CI_SESSION = '880d1be104850ad44146c920746399ef12eeeff4'
CF_CLEARANCE = 'awN0Rgkw2l.Jv_q9T_aUmCtCe3U7XAC.TEokkjY3mTI-1776609999-1.2.1.1-b9UT8V5FkRWvhaT79wTuhlxpCI4fklGgWeYNNyArN2MdZ0mNWsOJpblaG2IvHXTapNMVdGZce1O9QBQpHGUxx41flMD3Jp4y1To9lyH8K2otmsoj6lL368.ODozd2o9ofAUfRcxQnKeU2IwKU4gUwSl3suM1gf37txFNjMR.KNlTiKADpett7P3XTIB__8hMt0np_vLs2zjRHgrbAjwiYz6DG3lb5nfiqIp5r0MWK6GxvXxp2ONb79.sv1c0zHyw7d.jNLKwayYpHabFPlyQqDW_bj_kWVCQomth.wOt2CVNvi7ZCN.DYWmctT3ENTFBK.u7GrS_b3aBm3jvrGiMug'

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        tiktok_link = query_params.get('link', [None])[0]

        # Kiểm tra nếu thiếu link đầu vào
        if not tiktok_link:
            err_response = {
                "status": "error",
                "developer": {
                    "name": "Đăng Quân",
                    "Group": "t.me/tienichchanel",
                    "Facebook": "fb.me/bdquan"
                },
                "message": "Thiếu tham số link. Ví dụ: ?link=https://vt.tiktok.com/..."
            }
            self.wfile.write(json.dumps(err_response, ensure_ascii=False).encode('utf-8'))
            return

        session = requests.Session()
        session.cookies.update({
            'token': TOKEN,
            'ci_session': CI_SESSION,
            'cf_clearance': CF_CLEARANCE
        })

        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Referer': 'https://leofame.com/free-instagram-followers'
        })

        # Khởi tạo form JSON phản hồi mẫu theo ý bạn
        final_response = {
            "status": "error",
            "developer": {
                "name": "Đăng Quân",
                "Group": "t.me/tienichchanel",
                "Facebook": "fb.me/bdquan"
            },
            "request_info": {
                "target_link": tiktok_link
            },
            "api_source": {
                "status_code": 0
            },
            "data": {}
        }

        try:
            # Bypass bước đệm lấy session
            session.get('https://leofame.com/free-tiktok-views', timeout=10)
            session.get('https://leofame.com/client/is_mobile/false', timeout=10)

            # Gửi yêu cầu buff views
            post_data = {
                'token': TOKEN,
                'timezone_offset': 'Asia/Bangkok',
                'timezone_offset_2': 'abcd',
                'free_link': tiktok_link
            }

            headers_post = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Origin': 'https://leofame.com',
                'Referer': 'https://leofame.com/free-tiktok-views'
            }

            resp = session.post(
                'https://leofame.com/free-tiktok-views?api=1', 
                data=post_data, 
                headers=headers_post, 
                timeout=15
            )

            # Ghi nhận trạng thái kết nối từ API gốc
            final_response["api_source"]["status_code"] = resp.status_code

            if resp.status_code == 200:
                try:
                    leofame_data = resp.json()
                    
                    # Kiểm tra xem là báo cooldown hay thành công
                    if "error" in leofame_data:
                        final_response["status"] = "success"  # Vẫn gọi API thành công nhưng dính cooldown
                        final_response["data"] = {
                            "success": "Failed",
                            "estimated_views": "+0 view",
                            "cooldown_status": leofame_data["error"]
                        }
                    else:
                        final_response["status"] = "success"
                        final_response["data"] = {
                            "success": leofame_data.get("success", "Success"),
                            "estimated_views": "+200 ~ +600 view",
                            "cooldown_status": "Ready"
                        }
                except ValueError:
                    # Trường hợp trả về text/html thay vì JSON
                    final_response["status"] = "success"
                    final_response["data"] = {
                        "success": "Unknown",
                        "estimated_views": "Kiểm tra lại tài khoản Leofame",
                        "raw_response": resp.text[:100]
                    }
            else:
                final_response["message"] = f"Leofame từ chối yêu cầu (HTTP {resp.status_code})"

        except Exception as e:
            final_response["message"] = f"Lỗi hệ thống Serverless: {str(e)}"

        # Trả JSON ra ngoài
        self.wfile.write(json.dumps(final_response, ensure_ascii=False).encode('utf-8'))
        return
      w
