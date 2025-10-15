import requests
r = requests.get('http://127.0.0.1:8000/login/')
print('status', r.status_code)
open('scripts/login_debug.html','w',encoding='utf-8').write(r.text)
print('wrote scripts/login_debug.html')
