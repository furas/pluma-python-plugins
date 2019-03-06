#from gi.repository import GObject, Gtk, Gedit  # <-- Gedit
from gi.repository import GObject, Gtk, Pluma, Peas  # <-- Pluma

#class ExamplePyPlugin(GObject.Object, Gedit.WindowActivatable):  # <-- Gedit
class ExamplePyPlugin(GObject.Object, Peas.Activatable):  # <-- Pluma
    __gtype_name__ = "ExamplePyPlugin"

    #window = GObject.property(type=Gedit.Window)    # <-- Gedit
    #window = GObject.Property(type=GObject.Object)  # <-- Pluma: ERROR - doesn't works, `self.window` will be `None`
    object = GObject.Property(type=GObject.Object)   # <-- Pluma: OK - but needs `self.window = self.object` in methods

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        self.window = self.object # <-- Pluma: OK
        pass

    def do_deactivate(self):
        self.window = self.object # <-- Pluma: OK
        pass

    def do_update_state(self):
        self.window = self.object # <-- Pluma: OK
        pass
