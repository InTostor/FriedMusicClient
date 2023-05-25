from Playlist import Playlist
import vlc

class Player():
  """Wrapper for vlc player that implements essential audio features. If you need more power, use vlc methods on `Player.vlcPlayer` and `Player.vlcInstance`"""
  currentTrackFilename = ""
  vlcInstance = None
  vlcPlayer = None

  def __init__(self,currentTrack=0,repeat=None,shuffle=False,volume=50):
    self.currentTrack = currentTrack
    self.repeat = repeat
    self.shuffle = shuffle
    self.volume = volume
    self.vlcInstance = vlc.Instance()
    self.vlcPlayer = self.vlcInstance.media_player_new()

  # source preparing
  def insertPlaylist(self,plalyist: Playlist) -> None:
    self.currentPlaylist = plalyist
    self.sourceMode = "playlist"

  def insertDynamicSource(self,filenameGetter) -> None:
    self.dynamicSource = filenameGetter()
    self.sourceMode = "dynamic"

  def getCurrentTrackFilename(self) -> str:
    return self.currentTrackFilename
  
  def getLoadedPlaylist(self)->Playlist:
    return self.currentPlaylist
  
  def loadNewTrackFromDynamic(self):
    self.currentTrackFilename = self.dynamicSource()

  # wrappers on the vlc player
  def forceLoadUrl(self,url: str):
    self.vlcPlayer.set_mrl(url)

  def play(self):
    return self.vlcPlayer.play()
  
  def pause(self):
    return self.vlcPlayer.pause()
  
  def stop(self):
    return self.vlcPlayer.stop()
  
  def mute(self):
    return self.vlcPlayer.audio_set_mute(True)
  
  def unmute(self):
    return self.vlcPlayer.audio_set_mute(False)
  
  def toggleMute(self):
    return self.vlcPlayer.audio_toggle_mute()
  
  def setVolume(self,percent,logarithmic=False):
    # Use logarithmic for non vlc player (because it is already)
    self.volume = percent
    if logarithmic:
      percent = (percent**0.5)*10
    return self.vlcPlayer.audio_set_volume(percent)
  
  def getVolume(self):
    return self.vlcPlayer.audio_get_volume()
  
  def isPlaying(self):
    return self.vlcPlayer.isPlaying()

  def getTime(self):
    """played time in ms"""
    return self.vlcPlayer.get_time()
  
  def setTime(self,timing):
    """played time in ms"""
    return self.vlcPlayer.set_time(timing)
  
  def getLength(self):
    return self.vlcPlayer.get_length()
  
  def getPosition(self):
    return self.vlcPlayer.get_position()
  
  def setPosition(self,pos):
    return self.vlcPlayer.set_position(pos)