import requests, json, re, os

session = requests.session()
# 机场的地址
url = os.environ.get('URL')
# 配置用户名（一般是邮箱）
email = os.environ.get('EMAIL')
# 配置用户名对应的密码 和上面的email对应上
passwd = os.environ.get('PASSWD')
# server酱
SCKEY = os.environ.get('SCKEY')

login_url = f'{url}/auth/login'
check_url = f'{url}/user/checkin'

headers = {
    'origin': url,
    'referer': f'{url}/user',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}

data = {
    'email': email,
    'passwd': passwd
}

try:
    print('进行登录...')
    login_response = session.post(url=login_url, headers=headers, data=data)
    login_result = login_response.json()
    print(login_result['msg'])
    
    # 更新headers，添加可能需要的token
    checkin_headers = headers.copy()
    # 如果需要，可以从登录响应中获取token
    # token = login_result.get('data', {}).get('token', '')
    # if token:
    #     checkin_headers['Authorization'] = f'Bearer {token}'
    
    print('进行签到...')
    # 有些站点需要POST空数据而不是GET
    checkin_response = session.post(url=check_url, headers=checkin_headers, data={})
    checkin_result = checkin_response.json()
    print(checkin_result['msg'])
    content = checkin_result['msg']
    
    # 进行推送
    if SCKEY:
        push_url = f'https://sctapi.ftqq.com/{SCKEY}.send?title=机场签到&desp={content}'
        requests.post(url=push_url)
        print('推送成功')
except Exception as e:
    content = f'签到失败: {str(e)}'
    print(content)
    if SCKEY:
        push_url = f'https://sctapi.ftqq.com/{SCKEY}.send?title=机场签到&desp={content}'
        requests.post(url=push_url)
