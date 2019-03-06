
### Existing plugins ###

Pluma 1.20 uses different plugin code than older versions. It looks like plugin uses code similar to Gedit 3 plugin but not identical. Older Pluma used code similar to Gedit 2 plugin.
So old plugins for Pluma don't work with new Pluma. The same plugins for Gedit2 don't work with new Pluma. Plugins for Gedit 3 also don't works with new Pluma.

I found only one python plugin which works with Pluma 1.20.

It is _PythonConsole_ in Pluma source code:

[GitHub](https://github.com/) > [Mate-Desktop](https://github.com/mate-desktop/) > [Pluma](https://github.com/mate-desktop/pluma/) > [plugins](https://github.com/mate-desktop/pluma/tree/master/plugins/) > [PythonConsole](https://github.com/mate-desktop/pluma/tree/master/plugins/pythonconsole) (folder) > [PythonConsole](https://github.com/mate-desktop/pluma/tree/master/plugins/pythonconsole/pythonconsole) (module)


### Example: Minimal ###

It is "minimal example" from [Gedit Plugin Official Tutorial](https://wiki.gnome.org/Apps/Gedit/PythonPluginHowTo) with changes based on `PythonConsole`

**example.plugin**

| diff | Pluma | Gedit |
|-|-------|-------|
| | [Plugin] |  [Plugin]
| | Loader=python | Loader=python |
| | Module=examplepy | Module=examplepy |
| >> | IAge=*2* | IAge=*3* |
| | Name=Example py | Name=Example py |
| | Description=A Python plugin example | Description=A Python plugin example |
| | Authors=Jesse van den Kieboom <jesse@icecrew.nl> | Authors=Jesse van den Kieboom <jesse@icecrew.nl> |
| | Copyright=Copyright © 2006 Jesse van den Kieboom <jesse@icecrew.nl> | Copyright=Copyright © 2006 Jesse van den Kieboom <jesse@icecrew.nl> |
| | Website=http://www.gedit.org | Website=http://www.gedit.org |


**example.py**

```python
# Pluma

from gi.repository import GObject, Gtk, Pluma, Peas

class ExamplePyPlugin(GObject.Object, Peas.Activatable):
    __gtype_name__ = "ExamplePyPlugin"

    object = GObject.Property(type=GObject.Object)   # <-- needs `self.window = self.object` in methods

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        self.window = self.object
        pass

    def do_deactivate(self):
        self.window = self.object
        pass

    def do_update_state(self):
        self.window = self.object
        pass
```

Differences between Pluma & Gedit

```python
# differences between Pluma & Gedit

#from gi.repository import GObject, Gtk, Gedit  # <-- Gedit
from gi.repository import GObject, Gtk, Pluma, Peas  # <-- Pluma

#class ExamplePyPlugin(GObject.Object, Gedit.WindowActivatable):  # <-- Gedit
class ExamplePyPlugin(GObject.Object, Peas.Activatable):  # <-- Pluma
    __gtype_name__ = "ExamplePyPlugin"

    #window = GObject.property(type=Gedit.Window)    # <-- Gedit - it doesn't need `self.window = self.object` in methods
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
```

### Example: Add menu ###

It is "example with menu" from [Gedit Plugin Official Tutorial](https://wiki.gnome.org/Apps/Gedit/PythonPluginHowTo) with changes based on `PythonConsole`
