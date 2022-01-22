import requests
import json

f = open('client_info.json')
clientInfo = json.load(f)

clientID = clientInfo['id']
clientSecret = clientInfo['secret']
print(clientID)
print(clientSecret)
