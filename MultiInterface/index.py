import time

from launch import *
from lib.UserInterface import UserInterface

from interface.cli.Commands import Commands


def mainLoop():
  UI.startUI()
  sentToHistory = False
  
  while True:
    time.sleep(0.2) # decreasing cpu usage by little delay
    UI.onTick()  

    if player.getPosition()>=0.08 and not sentToHistory:
      client.addTrackToHistory(player.getCurrentTrackFilename(format="clean"))
      sentToHistory = True

    if player.getPosition()>=0.995:
      player.trackFinished()
      UI.onTrackFinished()
      sentToHistory = False
    


    



player.insertDynamicSource(getRadio)

try:
  mainLoop()
finally:
  UI.onExit()
