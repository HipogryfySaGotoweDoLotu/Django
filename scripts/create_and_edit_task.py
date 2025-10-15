import requests
s = requests.Session()
# login first
r = s.get('http://127.0.0.1:8000/login/')
csrftoken = s.cookies.get('csrftoken')
headers = {'Referer':'http://127.0.0.1:8000/login/','X-CSRFToken': csrftoken or ''}
post = s.post('http://127.0.0.1:8000/login/', data={'username':'testuser123','password':'TestPassword!234'}, headers=headers, allow_redirects=False)
print('login', post.status_code)
# add task
r = s.get('http://127.0.0.1:8000/tasks/task/add/')
csrftoken = s.cookies.get('csrftoken')
headers = {'Referer':'http://127.0.0.1:8000/tasks/task/add/','X-CSRFToken': csrftoken or ''}
add = s.post('http://127.0.0.1:8000/tasks/task/add/', data={'name':'Moje zadanie','desc':'Opis'}, headers=headers, allow_redirects=False)
print('add', add.status_code, add.headers.get('Location'))
# list tasks and find id
r2 = s.get('http://127.0.0.1:8000/tasks/')
print('tasks page status', r2.status_code)
# assume the edit link has /task/<id>/edit/; find first occurrence
import re
m = re.search(r"/task/(\d+)/edit/", r2.text)
if not m:
    print('no task id found')
else:
    tid = m.group(1)
    print('found task id', tid)
    # edit task
    r3 = s.get(f'http://127.0.0.1:8000/tasks/task/{tid}/edit/')
    csrftoken = s.cookies.get('csrftoken')
    headers = {'Referer':f'http://127.0.0.1:8000/tasks/task/{tid}/edit/','X-CSRFToken': csrftoken or ''}
    edit = s.post(f'http://127.0.0.1:8000/tasks/task/{tid}/edit/', data={'name':'Moje zadanie','desc':'Zmieniony opis'}, headers=headers, allow_redirects=False)
    print('edit', edit.status_code, edit.headers.get('Location'))
    r4 = s.get('http://127.0.0.1:8000/tasks/')
    print('final tasks snippet:', r4.text[:800])
