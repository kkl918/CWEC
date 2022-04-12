import requests

def auto_check(text): 
    url     = "https://notify-api.line.me/api/notify"
    token   = "FGKqZNLaKj5Wjr9cpvHHkgs98Yi5c5wYlqtNEnQYiyj"
    headers = {"Authorization" : "Bearer "+ token}

    message = "\n{}".format(text)

    payload = {"message" : message}
    r = requests.post(url,headers=headers,params=payload)
    print('LineBot msg.')
    
def kk_check(text): 
    url     = "https://notify-api.line.me/api/notify"
    token   = "0tbPvcFP35JiroJGPeZakDDc5fNhVKn1IEGQCoiWAaz"
    headers = {"Authorization" : "Bearer "+ token}

    message = "\n{}".format(text)

    payload = {"message" : message}
    r = requests.post(url,headers=headers,params=payload)
    print('LineBot msg.')