from lib.Client import Client
from launch import *
import json
from lib.macros import style


class Commands():

  def showPlaylists(*args):
    print(args)
    print(client.getPlaylists(True))

  def help(*args):
    with open("./interface/cli/help.json") as file:
      dickt = json.load(file)
      for help in dickt:
        print(style.INFO,help["command"])
        print("  ",style.GREEN,help["description"],style.RESET)

  def syncUp(*args):
    playlists = client.getPlaylists(False)
    for file in playlists:
      client.uploadFile(f"{userdataPath}/{file}")
      print(f"uploaded {file}")

  def play(*args):
    player.play()

  def pause(*args):
    player.pause()

  def seekto(*args):
    print(args)
    player.setPosition(float(args[0][0]))

  def getCurrentTrack(*args):
    print(player.getCurrentTrackFilename(format="clean"))

  def downloadCurrent(*args):
    client.downloadTrack(player.getCurrentTrackFilename())