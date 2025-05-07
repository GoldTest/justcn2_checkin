import requests
import os
from urllib.parse import quote

# 环境变量获取
url = os.environ.get('URL', 'https://justcn2.top').rstrip('/') + '/'
email = os.environ.get('EMAIL')
passwd = os.environ.get('PASSWD')
SCKEY = os.environ.get('SCKEY')

# 会话设置
session = requests.Session()

# 请求头 - 完全模拟真实请求
headers = {
    'authority': 'justcn2.top',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'dnt': '1',
    'origin': url,
    'priority': 'u=1, i',
    'referer': f'{url}user',
    'sec-ch-ua': '"Chromium";v="136", "Microsoft Edge";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Mobile Safari/537.36 Edg/136.0.0.0',
    'x-requested-with': 'XMLHttpRequest'
}

def login():
    login_url = f'{url}auth/login'
    data = {
        'email': email,
        'passwd': passwd
    }
    response = session.post(login_url, headers=headers, data=data)
    result = response.json()
    if result.get('ret') != 1:
        raise Exception(f"登录失败: {result.get('msg')}")
    return result

def checkin():
    check_url = f'{url}user/checkin'
    response = session.post(check_url, headers=headers)
    result = response.json()
    if result.get('ret') != 1:
        raise Exception(f"签到失败: {result.get('msg')}")
    return result

def push_notification(content):
    if SCKEY:
        push_url = f'https://sctapi.ftqq.com/{SCKEY}.send?title={quote("机场签到")}&desp={quote(content)}'
        requests.post(push_url)

try:
    print('正在登录...')
    login_result = login()
    print(f"登录成功: {login_result.get('msg')}")

    print('正在签到...')
    checkin_result = checkin()
    content = checkin_result.get('msg', '签到成功')
    print(content)
    
    push_notification(content)
    print('推送成功')

except Exception as e:
    error_msg = f"签到失败: {str(e)}"
    print(error_msg)
    push_notification(error_msg)
