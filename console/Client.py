from io import BufferedReader
import json, requests, glob, os

class Client():

  def __init__(self,userdataPath = "./userdata/",cookiesPath="./cookies/",accountServiceUrl=None,credentials=None,onlineMode=False):
    self.userdataPath      = userdataPath
    self.cookiesPath       = cookiesPath
    self.accountServiceUrl = accountServiceUrl
    self.credentials = {"login-username":credentials[0],"login-password":credentials[1]}
    self.authenticateUrl = f"{accountServiceUrl}/login/index.php?client"


  def tryLogin(self):
    credentials = self.credentials
    try:
      open(f"{self.cookiesPath}/credentialsCookie.json","x")
    except FileExistsError:
      pass # workaround

    try:
      credentialsCookieFile = open(f"{self.cookiesPath}/credentialsCookie.json","r")
      cookies = json.loads(credentialsCookieFile.read()) # inline file.json to dict
      credentialsCookieFile.close()
    except Exception:
      cookies = {}

    session = requests.Session()
    response = session.post(self.authenticateUrl,data=credentials,cookies=cookies)
    if response.text == "ok" :
      if response.cookies.get_dict()!={}:
        credentialsCookieFile = open(f"{self.cookiesPath}/credentialsCookie.json","w")
        credentialsCookieFile.write(json.dumps(response.cookies.get_dict())) # write cookies back
        session.close()
      return True
    return False
  
  def getCredentialsCookies(self):
    try:
      credentialsCookieFile = open(f"{self.cookiesPath}/credentialsCookie.json","r")
      cookies = json.loads(credentialsCookieFile.read())
      credentialsCookieFile.close()
      return cookies
    except Exception:
      return {}

  def getPlaylists(self,onRemote = None) -> list:
    if onRemote == None:
      onRemote = self.onlineMode
    if onRemote:
      # search playlists list on remote host
      response = requests.get(f"{self.accountServiceUrl}/api/getMyPlaylists.php",cookies=self.getCredentialsCookies())
      playlists = response.text.split("\n")
      return playlists
    else:
      # search playlists locally
      return glob.glob("*.fpl",root_dir=self.userdataPath)
    
  def isTrackInFavourite(self,trackFileName,onRemote = None) -> bool:
    if onRemote == None:
      onRemote = self.onlineMode
    if onRemote:
      response = requests.get(f"{self.accountServiceUrl}/api/isInFavourite.php?track={trackFileName}",cookies=self.getCredentialsCookies())
      return response.text.lower() == "true"
    else:
      try:
        favouritePlaylist = open(self.userdataPath+"/favourite.fpl","r")
      except FileNotFoundError:
        return False
      trackInList = trackFileName in favouritePlaylist.read()
      favouritePlaylist.close()
      return trackInList
    
  def searchTracks(self, query: str,limit: int = 100,type: str = "query",onRemote : bool = False) -> list:
    """type= query|artist|genre|album"""
    if onRemote:
      response = requests.get(f"{self.accountServiceUrl}/api/searchTrack.php?query={query}&type={type}&limit={limit}")
      jsonList = json.loads(response.text)
      return jsonList
    
  def getUsername(self):
    return self.getCredentialsCookies()["who"]

  def getRemoteDirectory(self):
    return f"{self.accountServiceUrl}/userdata/{self.getUsername()}/"

  def downloadUserData(self):
    settingsFiles = ["artists.fbl","genres.fbl"]
    userFiles = self.getPlaylists(True)
    downloadList = settingsFiles + userFiles
    out = False
    for file in downloadList:
      response = requests.get(f"{self.getRemoteDirectory()}/{file}")
      if response.status_code == 200:
        localFile = open(f"{self.userdataPath}/{file}","wb")
        localFile.write(response.content)
        localFile.close()
      out=True
    return out

  # method overload for string and file
  def uploadFile(self,filePath:str):
    with open(filePath,'rb') as f:
      url = f"{self.accountServiceUrl}/api/uploadFile.php"
      payload = {'file':(f.name,f.read())}
      cookies = self.getCredentialsCookies()
      return requests.post(url,files=payload,cookies=cookies).status_code

  def uploadFile(self,file:BufferedReader):
    with file as f:
      url = f"{self.accountServiceUrl}/api/uploadFile.php"
      payload = {'file':(f.name,f.read())}
      cookies = self.getCredentialsCookies()
      return requests.post(url,files=payload,cookies=cookies).status_code

  def deleteFile(self,filename,onRemote = None):
    if onRemote == None:
      onRemote = self.onlineMode
    if onRemote:
      requests.get(f"{self.accountServiceUrl}/api/deleteFile.php?file={filename}")
    else:
      if os.path.exists(f"{self.userdataPath}/{filename}"):
        os.remove(f"{self.userdataPath}/{filename}")

  def getNextTrack(self,onRemote: bool = False,generatorSettings: list = []):
    if onRemote == None:
      onRemote = self.onlineMode
    if onRemote:
      if generatorSettings == []:
        url = f"{self.accountServiceUrl}/api/getNextTrack.php"
      else:
        # TODO use parameters as required in docs
        url = f"{self.accountServiceUrl}/api/getNextTrack?"
      response = requests.get(url,cookies=self.getCredentialsCookies())
      return response.text