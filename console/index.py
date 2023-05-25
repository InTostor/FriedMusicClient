import requests, json, glob, os, vlc
from Player import Player
from Client import Client

settings = json.loads(open("config.json","r").read())

username = settings['username']
password = settings['password']
accountServiceUrl = settings['accountServiceUrl']
remoteMusicStorageUrl = settings['remoteMusicStorageUrl']
userdataPath = settings['userdataPath']
cookiesPath = settings['cookiesPath']
onlineMode = settings['onlineMode']





client = Client(userdataPath,cookiesPath,accountServiceUrl,[username,password],)



print("starting client")
print("Is online? ",onlineMode)

if onlineMode:
  # authenticate on server and get cookies
  if client.tryLogin():
    print("successfully logged to account service")
  else:
    print("Login failed, return")
    exit()

  # sync with server
  print("Trying to fetch data from server")
  if client.downloadUserData():
    print("Fetched userdata from account server")
  else:
    print("failed to sync userdata")