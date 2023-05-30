import threading

class UserInterface():
  """Wrapper and parent of UI classes"""

  def __init__(self,name=None):
    self.name = name
    pass

  def onTick(self):
    pass

  def onTrackFinished(self):
    pass

  def onTrackStarted(self):
    pass

  def onStart(self):
    pass

  def onExit(self):
    pass

  def run(self):
    pass

  def startUI(self):
    self.Thread = threading.Thread(target=self.run)
    self.Thread.start()
