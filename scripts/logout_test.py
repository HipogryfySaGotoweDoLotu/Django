import requests
s = requests.Session()
# login
r = s.get('http://127.0.0.1:8000/login/')
csrftoken = s.cookies.get('csrftoken')
headers = {'Referer':'http://127.0.0.1:8000/login/','X-CSRFToken': csrftoken or ''}
post = s.post('http://127.0.0.1:8000/login/', data={'username':'testuser123','password':'TestPassword!234'}, headers=headers, allow_redirects=False)
print('login', post.status_code, 'Location:', post.headers.get('Location'))
# logout
r2 = s.get('http://127.0.0.1:8000/logout/', allow_redirects=False)
print('GET /logout status', r2.status_code, 'Location:', r2.headers.get('Location'))
open('scripts/logout_debug.html','w',encoding='utf-8').write(r2.text)
print('wrote scripts/logout_debug.html')
