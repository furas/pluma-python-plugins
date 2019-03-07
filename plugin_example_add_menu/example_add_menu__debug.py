import sys
print(sys.version)

from gettext import gettext as _

#from gi.repository import GObject, Gtk, Gedit  # <-- Gedit
from gi.repository import GObject, Gtk, Pluma, Peas  # <-- Pluma

# Menu item example, insert a new item in the Tools menu
ui_str = """<ui>
  <menubar name="MenuBar">
    <menu name="ToolsMenu" action="Tools">
      <placeholder name="ToolsOps_2">
        <menuitem name="ExamplePy" action="ExamplePy"/>
      </placeholder>
    </menu>
  </menubar>
</ui>
"""


#class ExamplePyWindowActivatable(GObject.Object, Gedit.WindowActivatable):  # <-- Gedit
class ExamplePyWindowActivatable__Debug(GObject.Object, Peas.Activatable):  # <-- Pluma
    __gtype_name__ = "ExamplePyWindowActivatable__Debug"

    #window = GObject.property(type=Gedit.Window)    # <-- Gedit
    window = GObject.Property(type=GObject.Object)   # <-- Pluma: ERROR
    object = GObject.Property(type=GObject.Object)   # <-- Pluma: OK (but needs `self.window = self.object` in methods)
    print('[DEBUG] window:', window)
    print('[DEBUG] object:', object)

    def __init__(self):
        print('[DEBUG] __init__ before: window:', self.window)
        print('[DEBUG] __init__ before: object:', self.object)
        GObject.Object.__init__(self)
        print('[DEBUG] __init__ after: window:', self.window)
        print('[DEBUG] __init__ after: object:', self.object)
        self.window = self.object # <-- Pluma: ERROR: None

    def do_activate(self):
        print('[DEBUG] do_activate: window:', self.window) # <-- Pluma: ERROR: None
        print('[DEBUG] do_activate: object:', self.object) # <-- Pluma: OK
        # Insert menu items
        self._insert_menu()

    def do_deactivate(self):
        print('[DEBUG] do_deactivate: window:', self.window) # <-- Pluma: OK
        print('[DEBUG] do_deactivate: object:', self.object) # <-- Pluma: OK
        # Remove any installed menu items
        self._remove_menu()

        self._action_group = None

    def _insert_menu(self):
        print('[DEBUG] _insert_menu: window:', self.window) # <-- Pluma: ERROR: None
        print('[DEBUG] _insert_menu: object:', self.object) # <-- Pluma: OK
        self.window = self.object  # <-- Pluma: OK

        # Get the Gtk.UIManager
        manager = self.window.get_ui_manager()

        # Create a new action group
        self._action_group = Gtk.ActionGroup("ExamplePyPluginActions")
        self._action_group.add_actions([("ExamplePy", None, _("Clear document"),
                                         None, _("Clear the document"),
                                         self.on_clear_document_activate)])

        # Insert the action group
        manager.insert_action_group(self._action_group, -1)

        # Merge the UI
        self._ui_id = manager.add_ui_from_string(ui_str)

    def _remove_menu(self):
        print('[DEBUG] _remove_menu: window:', self.window) # <-- Pluma: OK
        print('[DEBUG] _remove_menu: object:', self.object) # <-- Pluma: OK
        self.window = self.object  # <-- Pluma: OK

        # Get the Gtk.UIManager
        manager = self.window.get_ui_manager()

        # Remove the ui
        manager.remove_ui(self._ui_id)

        # Remove the action group
        manager.remove_action_group(self._action_group)

        # Make sure the manager updates
        manager.ensure_update()

    def do_update_state(self):
        print('[DEBUG] do_update_state: window:', self.window) # <-- Pluma: OK
        print('[DEBUG] do_update_state: object:', self.object) # <-- Pluma: OK
        self.window = self.object  # <-- Pluma: OK

        self._action_group.set_sensitive(self.window.get_active_document() != None)

    # Menu activate handlers
    def on_clear_document_activate(self, action):
        print('[DEBUG] on_clear_document_activate: window:', self.window) # <-- Pluma: OK
        print('[DEBUG] on_clear_document_activate: object:', self.object) # <-- Pluma: OK
        self.window = self.object  # <-- Pluma: OK

        doc = self.window.get_active_document()
        if not doc:
            return

        doc.set_text('')
