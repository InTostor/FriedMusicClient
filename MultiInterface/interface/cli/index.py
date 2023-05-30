from lib.UserInterface import UserInterface
from launch import *
from interface.cli.Commands import Commands

class CLI(UserInterface, Commands):
  def __init__(self):
    super().__init__()
    self.name = "CLI"

  def run(self):
    while True:
      inp = input(":")
      if inp[0] == "/":
        try:
          args = inp[1:].split(" ")
          getattr(Commands, args[0])(args[1:])
        except AttributeError:
          print(style.ERROR,f"command {args[0]} not found",style.RESET)
        except Exception as e:
          print(e)
      else:
        try:
          exec(inp)
        except Exception as e:
          print("error running cli command")
          print(e)