import requests

url = 'http://localhost:3000/recommend'

r = requests.post(url)
print(r.json())