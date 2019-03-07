
from gi.repository import GObject, Gtk, Pluma, Peas

class ExampleMinimalPlugin(GObject.Object, Peas.Activatable):
    __gtype_name__ = "ExampleMinimalPlugin"

    object = GObject.Property(type=GObject.Object)  # it needs `self.window = self.object` in `do_activate()`

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        self.window = self.object  # it needs it (or use `self.object` instead of `self.window` in your code`do_activate()`
        pass

    def do_deactivate(self):
        pass

    def do_update_state(self):
        pass
