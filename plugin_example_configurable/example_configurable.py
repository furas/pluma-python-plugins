
from gi.repository import GObject, Gtk, Pluma, Peas
from gi.repository import PeasGtk  # <-- need for configuration


class ExampleConfigurablePlugin(GObject.Object, Peas.Activatable, PeasGtk.Configurable):
    __gtype_name__ = "ExampleConfigurablePlugin"

    object = GObject.Property(type=GObject.Object)

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        self.window = self.object  # OK
        pass

    def do_deactivate(self):
        pass

    def do_update_state(self):
        pass

    def do_create_configure_widget(self):
        widget = Gtk.Label("A configuration widget goes here.")
        return widget
