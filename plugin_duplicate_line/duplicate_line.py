from gettext import gettext as _
from gi.repository import GObject, Gtk, Gio, Pluma, Peas

#
# based on: https://github.com/hannenz/duplicate for Gedit >3.14
# and "example with menu" from Gedit 3.x PythonPluginHowTo https://wiki.gnome.org/Apps/Gedit/PythonPluginHowTo
#
# it use `Ctrl+Shift=D` instead of `Ctrl+D` because it can't replace it
#

# Menu item example, insert a new item in the Tools menu
ui_str = """<ui>
  <menubar name="MenuBar">
    <menu name="ToolsMenu" action="Tools">
      <placeholder name="ToolsOps_2">
        <menuitem name="DuplicateLinePlugin" action="DuplicateLinePlugin"/>
      </placeholder>
    </menu>
  </menubar>
</ui>
"""

class DuplicateLineWindowActivatable(GObject.Object, Peas.Activatable):
    __gtype_name__ = "DuplicateLinePlugin"

    object = GObject.property(type=GObject.Object)


#    def __init__(self):
#        GObject.Object.__init__(self)


    def do_activate(self):
        self.window = self.object

        # Insert menu items
        self._insert_menu()


    def do_deactivate(self):
        self.window = self.object

        # Remove any installed menu items
        self._remove_menu()


    def _insert_menu(self):
        # Get the Gtk.UIManager
        manager = self.window.get_ui_manager()

        # Create a new action group
        self._action_group = Gtk.ActionGroup("DuplicateLinePluginActions")
        self._action_group.add_actions([("DuplicateLinePlugin", None, _("Duplicate Line"), "<Ctrl><Shift>D", _("Duplicate line"), self.on_duplicate_line)])

        #accel = Gtk.AccelGroup()
        #accel.connect(Gdk.keyval_from_name('O'), Gdk.ModifierType.CONTROL_MASK, 0, self.on_accel_pressed)
        #key, mod = Gtk.accelerator_parse("<Control><Shift>D")
        #accel.connect(key, mod, Gtk.AccelFlags.VISIBLE, self.on_duplicate_line)
        #self.window.add_accel_group(accel)

        # Insert the action group
        manager.insert_action_group(self._action_group, -1)

        # Merge the UI
        self._ui_id = manager.add_ui_from_string(ui_str)


    def _remove_menu(self):
        # Get the Gtk.UIManager
        manager = self.window.get_ui_manager()

        # Remove the ui
        manager.remove_ui(self._ui_id)

        # Remove the action group
        manager.remove_action_group(self._action_group)

        # Make sure the manager updates
        manager.ensure_update()

        self._action_group = None


    def do_update_state(self):
        self.window = self.object
#        for action, config in ACTIONS.items():
#            self.window.lookup_action(action).set_enabled(self.window.get_active_document() is not None)


    def on_duplicate_line(self, action=None):
        self.window = self.object

        doc = self.window.get_active_document()
        if not doc:
            return

        if doc.get_has_selection():
            # User has text selected, get bounds.
            s, e = doc.get_selection_bounds()
            l1 = s.get_line()
            l2 = e.get_line()

            if l1 != l2:
                # Multi-lines selected. Grab the text, insert.
                s.set_line_offset(0)
                e.set_line_offset(e.get_chars_in_line())

                text = doc.get_text(s, e, False)
                if text[-1:] != '\n':
                    # Text doesn't have a new line at the end. Add one for the beginning of the next.
                    text = "\n" + text

                doc.insert(e, text)
            else:
                # Same line selected. Grab the text, insert on same line after selection.
                text = doc.get_text(s, e, False)
                doc.move_mark_by_name("selection_bound", s)
                doc.insert(e, text)
        else:
            # No selection made. Grab the current line the cursor is on, insert on new line.
            s = doc.get_iter_at_mark(doc.get_insert())
            e = doc.get_iter_at_mark(doc.get_insert())
            s.set_line_offset(0)

            if not e.ends_line():
                e.forward_to_line_end()

            text = "\n" + doc.get_text(s, e, False)

            doc.insert(e, text)

