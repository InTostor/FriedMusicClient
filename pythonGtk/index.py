	

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


@Gtk.Template(filename="pythonGtk/gui.ui")
class MainWindow(Gtk.ApplicationWindow):
  __gtype_name__ = "MainWindow"
  PlayerPlayButton = Gtk.Template.Child()
  def __init__(self,**kwargs):
    super().__init__(**kwargs)
    self.PlayerPlayButton.connect('clicked', onClick)


def onClick(**kwargs):
  print("clicked")


window = MainWindow()
window.show()

Gtk.main()