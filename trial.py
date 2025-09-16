import requests
from bs4 import BeautifulSoup

url = "https://myinternship.id/index.php?page=student_login"
r = requests.get(url)
requests.session()

soup = BeautifulSoup(r.text, 'html.parser')

# cari input yang punya nama umum csrf
token_input = soup.find('meta', attrs={'name': 'csrf-token'})
if token_input:
    token = token_input.get('content')
    print("CSRF token:", token)
else:
    print("Token tidak ditemukan di input[name='csrf_token']")
