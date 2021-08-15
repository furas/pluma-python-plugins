
## Existing plugins

Pluma 1.20 uses different code in plugins than older versions. It uses code similar to Gedit 3 plugins - but not identical. Older Pluma used code similar to Gedit 2 plugins.
So new Pluma can't use python plugins for old Pluma, Gedit 2 nor Gedit 3. They need changes.

I found few working plugins in Pluma source code:

[GitHub](https://github.com/) > [Mate-Desktop](https://github.com/mate-desktop/) > [Pluma](https://github.com/mate-desktop/pluma/) > [plugins](https://github.com/mate-desktop/pluma/tree/master/plugins/)

- [ExternalTools](https://github.com/mate-desktop/pluma/tree/master/plugins/externaltools)

- [QuickOpen](https://github.com/mate-desktop/pluma/tree/master/plugins/quickopen)

- [PythonConsole](https://github.com/mate-desktop/pluma/tree/master/plugins/pythonconsole)

- [Snippets](https://github.com/mate-desktop/pluma/tree/master/plugins/snippets)



## Plugin example: Minimal

It is based on ["Minimal plugin"](https://wiki.gnome.org/Apps/Gedit/PythonPluginHowTo#Minimal_plugin)
in ["Python Plugin How To for Gedit 3"](https://wiki.gnome.org/Apps/Gedit/PythonPluginHowTo#Minimal_plugin)
with changes based on [PythonConsole](https://github.com/mate-desktop/pluma/tree/master/plugins/pythonconsole) for Pluma

**example_minimal.plugin**

| diff | Pluma | Gedit 3 |
|-|-------|-------|
| | [Plugin] |  [Plugin]
| | Loader=python | Loader=python |
| | Module=minimal | Module=minimal |
| >> | IAge=**2** | IAge=**3** |
| | Name=Example Plugin | Name=Example Plugin |
| | Description=A Python plugin example | Description=A Python plugin example |
| | Authors=Furas <furas@tlen.pl> | Authors=Furas <furas@tlen.pl> |
| | Copyright=Copyright © 2019 Furas <furas@tlen.pl> | Copyright=Copyright © 2019 Furas <furas@tlen.pl> |
| | Website=https://github.com/furas/pluma-python-plugins | Website=https://github.com/furas/pluma-python-plugins |


**example_minimal.py**

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

Plugins in Pluma source code use `window = self.object` or `self.window = self.object` in all `do_...` methods (like in code below)
but I think it needs `self.window = self.object` only once - in `do_activate()` (like in code above)

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
        #self.window = self.object  # it needs it (or use `self.object` instead of `self.window` in your code)
        window = self.object  # it needs it (or use `self.object` instead of `window` in your code)
        pass

    def do_deactivate(self):
        #self.window = self.object  # it needs it (or use `self.object` instead of `self.window` in your code)
        window = self.object  # it needs it (or use `self.object` instead of `window` in your code)
        pass

    def do_update_state(self):
        #self.window = self.object  # it needs it (or use `self.object` instead of `self.window` in your code)
        window = self.object  # it needs it (or use `self.object` instead of `window` in your code)
        pass
```


Differences in minimal code between Pluma & Gedit 3

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

**example_minimal__debug.plugin / example_minimal__debug.py**

The same code but with many `print()` for tests.



## Plugin example: Add menu

It based on example ["Adding a menu item"](https://wiki.gnome.org/Apps/Gedit/PythonPluginHowTo#Adding_a_menu_item)
in ["Python Plugin How To for Gedit 3"](https://wiki.gnome.org/Apps/Gedit/PythonPluginHowTo)
with changes based on [PythonConsole](https://github.com/mate-desktop/pluma/tree/master/plugins/pythonconsole) for Pluma

**example_add_menu.plugin / example_add_menu.py**

It adds menu "Tools" with function "Clear document".

Changes are the same as in minimal example.

**example_add_menu__debug.plugin / example_add_menu__debug.py**

The same code but with many `print()` for tests.



## Plugin example: Advanced

It based on example ["Advanced plugin"](https://wiki.gnome.org/Apps/Gedit/PythonPluginHowTo#Implementing_an_advanced_plugin)
in ["Python Plugin How To for Gedit 3"](https://wiki.gnome.org/Apps/Gedit/PythonPluginHowTo)
with changes based on [PythonConsole](https://github.com/mate-desktop/pluma/tree/master/plugins/pythonconsole) for Pluma

**example_advanced.plugin / example_advanced.py**

It is not complet. Gedit 3 uses classes `Gedit.WindowActivatable` and `Gedit.ViewActivatable` but Pluma has only `Peas.Activatable`



## Plugin example: Configurable

It based on example ["Configurable plugin"](https://wiki.gnome.org/Apps/Gedit/PythonPluginHowTo#Adding_a_configure_dialog_for_your_plugin)
in ["Python Plugin How To for Gedit 3"](https://wiki.gnome.org/Apps/Gedit/PythonPluginHowTo)
with changes based on [PythonConsole](https://github.com/mate-desktop/pluma/tree/master/plugins/pythonconsole) for Pluma

**example_configurable.plugin / example_configurable.py**

It adds module PeakGtk and method `do_create_configure_widget` to create dialog window. Plugin will use `run()` to execute it.

---

### Similar

- [fszymanski/pluma-plugins](https://github.com/fszymanski/pluma-plugins)

