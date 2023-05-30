from lib.Playlist import Playlist
from lib.Client import Client


from vlc import MediaPlayer
from urllib.parse import unquote, urlparse
import os

class Player():
  """Wrapper for vlc player that implements essential audio features. If you need more power, use vlc methods on `Player.vlcPlayer` and `Player.vlcInstance`"""
  currentTrackFilename:str
  REPEATNONE = 0
  REPEATTRACK = 1
  REPEATPLAYLIST = 2
  STATICSOURCE = 0
  DYNAMICSOURCE = 1

  ONPLAY = 0
  ONPAUSE = 1
  ONMUTE = 2
  ONUNMUTE = 3
  ONSETVOLUME = 4
  ONSTOP = 5
  ONTRACKLOAD = 6
  callbacks = [None]*7

  def __init__(self,currentTrack=0,repeat=None,shuffle=False,volume=50):
    """
    `repeat` = `"REPEATRACK" | "REPEATPLAYLIST" | REPEATNONE`
    """
    self.currentTrack = currentTrack
    self.repeat = repeat
    self.shuffle = shuffle
    self.volume = volume
    self.vlcPlayer = MediaPlayer()
    self.setVolume(volume)

  def setClient(self,client:Client):
    """Pass client object to player, so it can be used to get track path"""
    self.client = client

  def connect(self,event,func):
    self.callbacks[event] = func


  # source preparing
  def insertPlaylist(self,plalyist: Playlist) -> None:
    """Insert playlist as source for player"""
    self.currentPlaylist = plalyist
    self.sourceMode = self.STATICSOURCE
    self.loadTrackFromPlaylist()

  def insertDynamicSource(self,filenameGetter) -> None:
    """
    Insert source that will give next track (dynamic infinite playlist, a.k.a. Gachiradio.fm)
    Function should return absolute local path or full url or filename only:\n
    /home/user/Music/example.mp3\n
    http://example.com/Music/example.mp3\n
    example.mp3
    """
    self.dynamicSource = filenameGetter
    self.sourceMode = self.DYNAMICSOURCE
    self.forceLoadUrl(self.getPathForSelf(self.dynamicSource()))

  def next(self):
    """Select next track"""
    playing = self.isPlaying()
    if self.sourceMode == self.STATICSOURCE:
      self.currentTrack+=1      
      if self.repeat == self.REPEATPLAYLIST and self.currentTrack>=self.currentPlaylist.getLength():
        self.currentTrack = 0      
      self.loadTrackFromPlaylist()
    else:
      self.forceLoadUrl(self.getPathForSelf(self.dynamicSource()))
      
    # continue playing after track change
    if playing:
      self.play()

  def prev(self):
    """Select previous track from playlist"""
    playing = self.isPlaying()
    # prevent player to going into void
    if self.sourceMode == self.DYNAMICSOURCE:
      return
    
    if self.currentTrack>0:
      self.currentTrack-=1
    elif self.currentTrack<=0 and self.repeat == self.REPEATPLAYLIST:
      self.currentTrack = self.currentPlaylist.getLength()-1
    else:
      return # prevent going to void (trackN < 0)
    self.loadTrackFromPlaylist()
    if playing:
      self.play()

  def trackFinished(self):
    """Perform actions on trackFinish event (ideally should be called by vlc)"""
    self.next()
    if self.repeat == self.REPEATTRACK:
      self.prev()
    self.play()


  def loadTrackFromPlaylist(self):
    """Load track into vlc from playlist"""
    r = self.getPathForSelf(
      self.currentPlaylist.getTrackByIndex(self.currentTrack,willPlay=True,shuffle=self.shuffle)
    )
    self.currentTrackFilename = r
    
    self.forceLoadUrl(r)

  def getPathForSelf(self,trackFileName:str):
    """Find track in repos, get and normalize absolute path for vlc"""
    return self.client.findTrackInRepos(trackFileName=trackFileName)

  def getCurrentTrackFilename(self,format=None) -> str:
    """
    returns absolute path of currently playing track\n
    format = None | "unquote" | "clean"
    """
    match format:
      case None:
        return self.currentTrackFilename
      case "unquote":
        return unquote(self.currentTrackFilename)
      case "clean":
        return os.path.basename(urlparse(unquote(self.currentTrackFilename)).path)
  
  def getLoadedPlaylist(self)->Playlist:
    """Returns currently loaded playlist"""
    return self.currentPlaylist
  
  def loadNewTrackFromDynamic(self):
    """Same as Player.loadTrackFromPlaylist but for dynamic playlists"""
    self.currentTrackFilename = self.dynamicSource()

  # wrappers on the vlc player
  def forceLoadUrl(self,url: str):
    """Insert Media Resource Locator into vlc"""
    self.currentTrackFilename = url
    self.vlcPlayer.set_mrl(url)
    try:
      self.callbacks[self.ONTRACKLOAD]()
    except TypeError:
      print("not registered")

  def getPlayerState(self):
    return self.vlcPlayer.get_state()
  
  def isEnded(self):
    # magic number are from https://www.olivieraubert.net/vlc/python-ctypes/doc/ State enum
    return self.getPlayerState == 6

  def play(self):
    """Play current track"""
    self.vlcPlayer.play()
    try:
      self.callbacks[self.ONPLAY]()
    except TypeError:
      print("not registered")
  
  def pause(self):
    """Pause player"""
    self.vlcPlayer.pause()
  
  def togglePlay(self):
    if self.isPlaying():
      self.pause()
    else:
      self.play()

  def stop(self):
    """Stop player. Resets position to zero, keeping source"""
    return self.vlcPlayer.stop()
  
  def mute(self):
    """Mute player"""
    return self.vlcPlayer.audio_set_mute(True)
  
  def unmute(self):
    """Unmute player"""
    return self.vlcPlayer.audio_set_mute(False)
  
  def toggleMute(self):
    """Toggle mute player"""
    self.vlcPlayer.audio_toggle_mute()
  
  def setVolume(self,percent:int):
    """Sets volume of player in [0,100]"""
    self.vlcPlayer.audio_set_volume(percent)
  
  def getVolume(self):
    """Returns current player volume in [0;100]"""
    return self.vlcPlayer.audio_get_volume()
  
  def isPlaying(self):
    return bool(self.vlcPlayer.is_playing())

  def getTime(self):
    """returns played time in ms"""
    return int(self.vlcPlayer.get_time())
  
  def setTime(self,timing:int):
    """seeks to time in ms"""
    self.vlcPlayer.set_time(timing)
  
  def getLength(self):
    """Returns length of track in ms"""
    return self.vlcPlayer.get_length()
  
  def getPosition(self) -> float:
    """Current position of player in [0;1]"""
    return self.vlcPlayer.get_position()
  
  def setPosition(self,pos:float):
    self.vlcPlayer.set_position(pos)
