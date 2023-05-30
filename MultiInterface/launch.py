import json
from lib.Player import Player
from lib.Client import Client
from lib.macros import style


# get config
settings = json.loads(open("config.json","r").read())

username = settings['username']
password = settings['password']
accountServiceUrl = settings['accountServiceUrl']
remoteMusicStorageUrl = settings['remoteMusicStorageUrl']
localMusicStoragePath = settings['localMusicStoragePath']
userdataPath = settings['userdataPath']
cookiesPath = settings['cookiesPath']
onlineMode = settings['onlineMode']
interface = settings['interface']

# setup client and storage
global client
client = Client(
  userdataPath=userdataPath,
  cookiesPath=cookiesPath,
  localMusicStorage=localMusicStoragePath,
  remoteMusicRepositories=[remoteMusicStorageUrl],
  accountServiceUrl=accountServiceUrl,
  credentials=[username,password],
  onlineMode=onlineMode
  )

global player

player = Player()
player.setClient(client=client)

# Preparing 
print("Starting client")
print(style.INFO,"Is online? ",end="")
print(style.OK,onlineMode)

if onlineMode:
  # authenticate on server and get cookies
  print(style.INFO,"Trying to authenticate on service: ",end="")
  if client.tryLogin():
    print(style.OK,"Success")
  else:
    print(style.ERROR,"Failed, fallback to offline")
    client.onlineMode = False    

  # sync with server
  print(style.INFO,"Trying to fetch data from server: ",end="")
  if client.downloadUserData():
    print(style.OK,"success")
  else:
    print(style.ERROR,"Failed")


# Track generator
def getRadio():
  return client.getNextTrack(True)


match interface:
  case "gtk":
    from interface.gtk.index import MainWindow
    UI = MainWindow()
    player.connect(player.ONPLAY,UI.updatePlayButtonIcon)
    player.connect(player.ONPAUSE,UI.updatePlayButtonIcon)
  case "cli":
    from interface.cli.index import CLI
    from interface.cli.Commands import Commands
    UI = CLI()
    
