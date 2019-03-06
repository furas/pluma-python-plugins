import sys
print('[DEBUG]', sys.version) # Python 2.7

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Pluma', '1.0')
gi.require_version('Peas', '1.0')
#from gi.repository import GObject, Gtk, Gedit  # <-- Gedit
from gi.repository import GObject, Gtk, Pluma, Peas  # <-- Pluma

#class ExamplePyPlugin(GObject.Object, Gedit.WindowActivatable):  # <-- Gedit
class ExamplePyPlugin(GObject.Object, Peas.Activatable):  # <-- Pluma
    __gtype_name__ = "ExamplePyPlugin"

    #window = GObject.property(type=Gedit.Window)  # <-- Gedit
    window = GObject.Property(type=GObject.Object)   # <-- Pluma: ERROR - doesn't works, `self.window` will be `None`
    object = GObject.Property(type=GObject.Object)   # <-- Pluma: OK - but needs `self.window = self.object` in methods

    def __init__(self):
        GObject.Object.__init__(self)
        #self.window = GObject.Property(type=GObject.Object)  # ERROR
        print('[DEBUG] __init__: window:', self.window)  # <-- Pluma: None - it makes problem
        print('[DEBUG] __init__: object:', self.object)  # <-- Pluma: None - it makes problem

    def do_activate(self):
        print('[DEBUG] do_activate: window:', self.window)  # <-- Pluma: None - it makes problem
        print('[DEBUG] do_activate: object:', self.object)  # <-- Pluma: OK
        #self.window = self.object # <-- Pluma: OK
        pass

    def do_deactivate(self):
        print('[DEBUG] do_deactivate: window:', self.window)  # <-- Pluma: OK
        print('[DEBUG] do_deactivate: object:', self.object)  # <-- Pluma: OK
        #self.window = self.object # <-- Pluma: OK
        pass

    def do_update_state(self):
        print('[DEBUG] do_update_state: window:', self.window)  # <-- Pluma: OK
        print('[DEBUG] do_update_state: object:', self.object)  # <-- Pluma: OK
        #self.window = self.object # <-- Pluma: OK
        pass

if __name__ == '__main__':
    print('[DEBUG]: main')
    plugin = ExamplePyPlugin()
    plugin.do_activate()
