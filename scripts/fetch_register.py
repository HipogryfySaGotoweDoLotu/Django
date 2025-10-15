import requests
r = requests.get('http://127.0.0.1:8000/register/')
print(r.status_code)
print(r.url)
print(r.text[:800])
