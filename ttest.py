import os, requests


url   = 'http://cwec.twport.com.tw/index.php'


r    = requests.head(url)
code = r.status_code
if code == 200:   
    res   = requests.get(url)
    
print(code, res)