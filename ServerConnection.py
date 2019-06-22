import requests
r = requests.get('https://www.youtube.com/watch?v=Q-BpqyOT3a8', auth=('user', 'pass'))
r.status_code

print(r.content)