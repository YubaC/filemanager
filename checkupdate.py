import sys
from urllib import response
import requests

url = 'https://api.github.com/repos/yubac/filemanager/releases/latest'

response = requests.get(url)

with open ('version.txt','r') as f:
    version = f.read()
    f.close()

if version != response.json()["tag_name"]:
    print(response.json()["tag_name"])

sys.exit(0)