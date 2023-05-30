from requests import get
from random import shuffle

class Playlist():
  shuffleOrder = []
  filenames = []
  currentTrackIndex = 0
  def __init__(self, source, sourceType = "localFile") -> None:
    """Source = path or url, sourcetype = localFile, remoteFile"""
    self.source = source
    self.sourceType = sourceType
    self.fetch()

  def asList(self):
    return self.filenames
  
  def getLength(self):
    return len(self.asList())
  

  def fetch(self):
    if self.sourceType == "localFile":
      playlistFile = open(self.source,"r")
      playlistPlainText = playlistFile.read()
      playlistFile.close()
    else:
      playlistFile = get(self.source).text

    if playlistPlainText.split("\n")[0] == "#EXTM3U":
      # convert m3u to fpl
      raise NotImplementedError("Use m3u as playlist")
      pass
    else:
      self.filenames = playlistPlainText.split("\n")
      # remove empty string that sometimes appear in server response
    self.filenames = list(filter(None,self.filenames))

  def shuffle(self):
    self.shuffleOrder = list(range(0,len(self.filenames)))

    # remove currentlyPlayingTrackIndex from the order
    self.shuffleOrder.pop(self.shuffleOrder.index(self.currentTrackIndex))

    #  put current track index to the start of order 
    shuffle(self.shuffleOrder)

  def asShuffledList(self):
    return [self.filenames[i] for i in self.shuffleOrder]
  
  def getTrackByIndex(self,index,shuffle = False,willPlay=False):
    if willPlay: self.currentTrackIndex = index
    if shuffle:
      return self.asShuffledList[min(index,len(self.shuffleOrder)-1)]
    else:
      return self.filenames[index]
