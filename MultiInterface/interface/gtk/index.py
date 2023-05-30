from launch import player
from lib.UserInterface import UserInterface
import gi,time
gi.require_version("Gtk", "3.0")
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk
from lib.macros import clamp


# @Gtk.Template(filename="./interface/gtk/gui2.ui")
class MainWindow(Gtk.ApplicationWindow, UserInterface):
  __gtype_name__ = "MainWindow"
  # PlayerPlayButton = Gtk.Template.Child()
  # PlayerNextButton = Gtk.Template.Child()
  # PlayerPreviousButton = Gtk.Template.Child()
  # PlayerSeekerSlider = Gtk.Template.Child()
  # PlayerCurrentTrackNameLabel = Gtk.Template.Child()

  # DebugCommandLine = Gtk.Template.Child()

  def __init__(self,**kwargs):
    super().__init__(**kwargs)
    self.name = "GTK3"
    self.builder = Gtk.Builder()
    self.builder.add_from_file("./interface/gtk/gui2.ui")
    self.builder.connect_signals(self)

    self.PlayerPlayButton            = self.builder.get_object("PlayerPlayButton")
    self.PlayerNextButton            = self.builder.get_object("PlayerNextButton")
    self.PlayerPreviousButton        = self.builder.get_object("PlayerPreviousButton")
    self.PlayerSeekerSlider          = self.builder.get_object("PlayerSeekerSlider")
    self.PlayerCurrentTrackNameLabel = self.builder.get_object("PlayerCurrentTrackNameLabel")
    self.DebugCommandLine = self.builder.get_object("DebugCommandLine")

    # self.PlayerPlayButton.connect('clicked', self.onPlayButtonClick)
    # self.PlayerNextButton.connect('clicked', self.onNextButtonClick)
    # self.PlayerPreviousButton.connect('clicked', self.onPreviousButtonClick)
    # self.PlayerSeekerSlider.connect('change-value',self.onSeekerValueChange)
    # self.DebugCommandLine.connect('activate',self.debugCLI)

    self.connect("destroy", Gtk.main_quit)

    self.screen = Gdk.Screen.get_default()
    self.provider = Gtk.CssProvider()
    self.provider.load_from_path("./interface/gtk/ui.css")
    Gtk.StyleContext.add_provider_for_screen(self.screen, self.provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
    
    self.GtkPlay = self.builder.get_object("GtkPlay")
    self.GtkPause = self.builder.get_object("GtkPause")
    self.updatePlayButtonIcon()


  def debugCLI(self,*args):
    try:
      exec(self.DebugCommandLine.get_text())
    finally:
      self.DebugCommandLine.set_text("")

  def onPlayButtonClick(self,*args):
    player.togglePlay()


  def onNextButtonClick(self,*args):
    player.next()
    print("clicked next button")

  def onPreviousButtonClick(self,*args):
    player.prev()
    print("clicked previous button")

  def onSeekerValueChange(self,*args):
    player.setPosition(self.PlayerSeekerSlider.get_value()/100)
    print(self.PlayerSeekerSlider.get_value())

  def updateSeekerPosition(self,position):
    self.PlayerSeekerSlider.set_value(position)

  def onTrackFinished(self):
    self.updateSeekerPosition(0)
    """Function that called when trackfinished"""

  def updatePlayButtonIcon(self):
    if player.isPlaying():
      self.PlayerPlayButton.set_image(self.GtkPause)
    else:
      self.PlayerPlayButton.set_image(self.GtkPlay)

  def onTick(self):
    self.updateSeekerPosition(clamp(player.getPosition()*100,0,100))
    txt = player.getCurrentTrackFilename(format="clean")
    self.PlayerCurrentTrackNameLabel.set_text(txt)

  def run(self):
    window = self.builder.get_object("MainWindow")
    window.show()
    Gtk.main()


