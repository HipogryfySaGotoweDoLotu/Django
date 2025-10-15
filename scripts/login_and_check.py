import requests
s = requests.Session()
r = s.get('http://127.0.0.1:8000/login/')
print('GET /login', r.status_code)
csrftoken = s.cookies.get('csrftoken')
print('csrf:', csrftoken)
payload = {'username':'testuser123','password':'TestPassword!234'}
headers = {'Referer':'http://127.0.0.1:8000/login/','X-CSRFToken': csrftoken or ''}
post = s.post('http://127.0.0.1:8000/login/', data=payload, headers=headers, allow_redirects=False)
print('POST /login', post.status_code, 'Location:', post.headers.get('Location'))
r2 = s.get('http://127.0.0.1:8000/tasks/')
print('/tasks/ status', r2.status_code)
print('contains tasks header?', '<h1>Twoje zadania</h1>' in r2.text)
