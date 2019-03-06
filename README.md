
### Existing plugins ###

Pluma 1.20 plugin uses different code than older versions. It uses code similar to Gedit 3 plugins - but not identical - and older Pluma used code similar to Gedit 2 plugins.
So new Pluma can't use python plugins for old Pluma, Gedit 2 nor Gedit 3.

I found only one python plugin which works with Pluma 1.20.

It is _PythonConsole_ in new Pluma source code:

[GitHub](https://github.com/) > [Mate-Desktop](https://github.com/mate-desktop/) > [Pluma](https://github.com/mate-desktop/pluma/) > [plugins](https://github.com/mate-desktop/pluma/tree/master/plugins/) > [PythonConsole](https://github.com/mate-desktop/pluma/tree/master/plugins/pythonconsole) (folder) > [PythonConsole](https://github.com/mate-desktop/pluma/tree/master/plugins/pythonconsole/pythonconsole) (module)


### Example: Minimal ###

It is "minimal example" from [Gedit Plugin Official Tutorial](https://wiki.gnome.org/Apps/Gedit/PythonPluginHowTo) with changes based on `PythonConsole`

**example.plugin**

| diff | Pluma | Gedit |
|-|-------|-------|
| | [Plugin] |  [Plugin]
| | Loader=python | Loader=python |
| | Module=example | Module=example |
| >> | IAge=**2** | IAge=**3** |
| | Name=Example Plugin | Name=Example Plugin |
| | Description=A Python plugin example | Description=A Python plugin example |
| | Authors=Furas <furas@tlen.pl> | Authors=Furas <furas@tlen.pl> |
| | Copyright=Copyright © 2019 Furas <furas@tlen.pl> | Copyright=Copyright © 2019 Furas <furas@tlen.pl> |
| | Website=https://github.com/furas/pluma-python-plugins | Website=https://github.com/furas/pluma-python-plugins |


**example.py**

```python
# Pluma

from gi.repository import GObject, Gtk, Pluma, Peas

class ExampleMinimalPlugin(GObject.Object, Peas.Activatable):
    __gtype_name__ = "ExampleMinimalPlugin"

    object = GObject.Property(type=GObject.Object)  # it needs `self.window = self.object` in `do_activate()`
                                                    # or use `self.object` instead of `self.window` in your code

    def __init__(self):
        GObject.Object.__init__(self)

    def do_activate(self):
        self.window = self.object  # it needs it (or use `self.object` instead of `self.window` in your code)
        pass

    def do_deactivate(self):
        pass

    def do_update_state(self):
        pass
```

Differences between Pluma & Gedit

```python
# differences between Pluma & Gedit 3

#from gi.repository import GObject, Gtk, Gedit       # <-- Gedit
from gi.repository import GObject, Gtk, Pluma, Peas  # <-- Pluma

#class ExampleMinimalPlugin(GObject.Object, Gedit.WindowActivatable):  # <-- Gedit
class ExampleMinimalPlugin(GObject.Object, Peas.Activatable):          # <-- Pluma
    __gtype_name__ = "ExampleMinimalPlugin"

    #window = GObject.property(type=Gedit.Window)    # <-- Gedit: it doesn't need `self.window = self.object` in `do_activate()`
    #window = GObject.Property(type=Pluma.Window)    # <-- Pluma: ERROR - doesn't works, `Pluma.Window` is incorrect property
    #object = GObject.Property(type=Pluma.Window)    # <-- Pluma: ERROR - doesn't works, `Pluma.Window` is incorrect property
    #window = GObject.Property(type=GObject.Object)  # <-- Pluma: ERROR - doesn't works, `self.window` will be `None`
    object = GObject.Property(type=GObject.Object)   # <-- Pluma: OK - but it needs `self.window = self.object` in `do_activate()`

    def __init__(self):
        GObject.Object.__init__(self)
        #self.window = self.object  # <-- Pluma: ERROR - `self.object` doesn't exist

    def do_activate(self):
        self.window = self.object   # <-- Pluma: it needs it (or use `self.object` instead of `self.window`)
        pass

    def do_deactivate(self):
        pass

    def do_update_state(self):
        pass
```

### Example: Add menu ###

It is "example with menu" from [Gedit Plugin Official Tutorial](https://wiki.gnome.org/Apps/Gedit/PythonPluginHowTo) with changes based on `PythonConsole`
