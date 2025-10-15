import requests

def run():
    s = requests.Session()
    resp = s.get('http://127.0.0.1:8000/register/')
    print('GET /register status', resp.status_code)
    csrftoken = s.cookies.get('csrftoken')
    print('csrftoken cookie:', csrftoken)
    # prepare post data
    payload = {
        'username': 'testuser123',
        'password1': 'TestPassword!234',
        'password2': 'TestPassword!234',
    }
    headers = {
        'Referer': 'http://127.0.0.1:8000/register/',
        'X-CSRFToken': csrftoken or ''
    }
    post = s.post('http://127.0.0.1:8000/register/', data=payload, headers=headers, allow_redirects=False)
    print('POST /register status', post.status_code)
    print('Location header:', post.headers.get('Location'))
    print('Response snippet:', post.text[:800])

if __name__ == '__main__':
    run()
