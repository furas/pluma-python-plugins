
# Based on
# Mike Doty's Gedit 2 plugin
#     http://www.psyguygames.com/SplitView2.tar.gz
# and maciejzgadzaj port to (old) Pluma.
#     https://github.com/maciejzgadzaj/split-view-pluma-plugin
#

from gi.repository import GObject, Gtk, Pluma, Peas
import os

ui_string = """<ui>
  <menubar name="MenuBar">
    <menu name="ViewMenu" action="View">
      <placeholder name="ViewOps_2">
        <menuitem name="ExamplePy" action="ExamplePy"/>
      </placeholder>
    </menu>
  </menubar>
</ui>
"""

class PluginHelper:
    def __init__(self, plugin, window):
        self.window = window
        self.plugin = plugin

        self.ui_id = None

        # Add a "toggle split view" item to the View menu
        self.insert_menu_item(window)

        # We're going to keep track of each tab's split view
        # and, if used, ALT view -- the view of a separate
        # document -- with a couple of dictionaries.  We'll
        # index each dictionary via the tab objects.
        self.split_views = {}
        self.alt_views = {}

        # This keeps track of whether the user is viewing an ALT document.
        self.same_document = {}

        # I hardly even know how this works, but it gets our encoding.
        try: self.encoding = Pluma.encoding_get_current()
        except: self.encoding = Pluma.Pluma_encoding_get_current()

    def deactivate(self):
        self.remove_menu_item()

        self.window = None
        self.plugin = None

    def update_ui(self):
        return

    def toggle_split_view(self, unused):
        # Get the current tab...
        current_tab = self.window.get_active_tab()

        # Don't allow splitview of an unsaved document...
        if (self.window.get_active_document().is_untitled()):
            self.show_error_dialog()
            return # Can't split view on an unsaved document

        # If we already have a split view defined for this tab,
        # then clearly the user wants to end the split view.
        if (current_tab in self.split_views):
            self.end_split_view(None)

        # Otherwise, let's start a split view!
        else:
            self.split_view(None)

    # This function creates the split view.
    def split_view(self, whatever, direction="vertical"):

        # Get the tab / document
        current_tab = self.window.get_active_tab()
        current_document = self.window.get_active_document()

        old_other_view = None
        if (current_tab in self.split_views):
            old_other_view = self.split_views[current_tab].get_child2()

        # Create a new HPaned or VPaned object for the splitview.
        if (direction == "vertical"):
            self.split_views[current_tab] = Gtk.HPaned()

        else:
            self.split_views[current_tab] = Gtk.VPaned()

        old_view = None

        if (not (current_tab in self.same_document)):
            self.same_document[current_tab] = True

        # Here we just kind of loop through the child object of the tab
        # and get rid of all of the existing GUI objects.
        for each in current_tab.get_children():

            # The child of the child has the View object for the active document.
            for any in each.get_children():

                old_view = any
                each.remove(any)

            # Create a scrolled window for the left / top side.
            sw1 = Gtk.ScrolledWindow()
            sw1.add(old_view)

            # Set up a new View object
            new_view = None
            # If we are viewing a separate file, then just get that document
            if (current_tab in self.alt_views):
                #new_view = Pluma.View(self.alt_views[current_tab])#.get_children()[0]
                new_view = Pluma.View.new_with_buffer(self.alt_views[current_tab])#.get_children()[0]

            # Otherwise, just share the same document as the active View.
            # This makes sure changes to either side reflect in the other side.
            else:
                new_view = Pluma.View.new_with_buffer(current_document)

            # Second scrolled window.
            sw2 = Gtk.ScrolledWindow()
            sw2.add(new_view)

            # Add the two scrolled windows to our Paned object.
            self.split_views[current_tab].add1(sw1)
            self.split_views[current_tab].add2(sw2)

            # The next few lines of code just create some buttons.
            hbox = Gtk.HBox()

            self.btn_cancel = Gtk.Button("End Splitview")
            self.btn_cancel.connect("clicked", self.end_split_view)

            self.btn_flip = Gtk.Button("Vertical Splitview")
            self.btn_flip.connect("clicked", self.flip_split_view)

            self.btn_view_other_file = Gtk.Button("View other file...")
            self.btn_view_other_file.connect("clicked", self.view_other_file)

            self.btn_save_alt_file = Gtk.Button("Save Alt Document")
            self.btn_save_alt_file.connect("clicked", self.save_other_file)

            self.label_other_document = Gtk.Label(os.path.basename(current_document.get_uri()))
            self.label_other_document.set_alignment(1.0, self.label_other_document.get_alignment()[1])

            hbox.pack_start(self.btn_cancel, False, False, 0)
            hbox.pack_start(self.btn_flip, False, False, 0)
            hbox.pack_start(self.btn_view_other_file, False, False, 0)
            hbox.pack_start(self.btn_save_alt_file, False, False, 0)
            hbox.pack_start(self.label_other_document, True, True, 0)

            vbox = Gtk.VBox()

            vbox.pack_start(hbox, False, False, 0)
            vbox.pack_start(self.split_views[current_tab], True, True, 0)

            each.add_with_viewport(vbox)

            # The trick of this whole thing is that you have to wait a second for the
            # Paned object to figure out how much room it can take up.  So, we're just
            # going to set a timer that'll check every 500 milliseconds until it
            # decides it can trust the width that the Paned object returns.
            GObject.timeout_add(500, self.debug)

        current_tab.show_all()

        # If we're just using the same document twice, then we don't need to worry
        # about "saving" the "other" document.
        if (self.same_document[current_tab] == True):
            self.btn_save_alt_file.hide()

    # Oh, what does this do... oh yeah, this makes it so that if you're in the
    # "other" document and it's not the active document (you're viewing an alternate
    # file), you get the line / column information in the status bar at the bottom.
    def update_line_column_data(self, buffer, location, mark, user_data=None):
        if (mark != None and location != None):
            if ( not (mark.get_name() in (None, "None") ) ):

                (line, column) = (location.get_line(), location.get_line_offset())

                # I put this in a try / except just in case something strange happens.
                # GEdit just seems to throw the status bar in an element and add 5
                # children or something like that into it, so I just loop through
                # until I find a Gtk.Label that starts with "  Ln".  Seems hacky?
                # Yeah.  Go make your own splitview if ya don't like it.  :P
                try:
                    for each in self.window.get_statusbar().get_children():
                        if (type(each) == Gtk.Statusbar):
                            frame = each.get_children()[0]

                            frame_child = frame.get_children()[0]

                            if (type(frame_child) == Gtk.Label):
                                if (frame_child.get_label().lstrip().startswith("Ln ")):
                                    frame_child.set_label("  Ln %d, Col %d [2]" % (line, column))

                except:
                    pass

    # This of course ends the split view... though I call this when switching
    # from left / right to top / bottom or vice versa.  If I'm doing that then
    # changing will be True I believe.
    def end_split_view(self, unused, changing=False):
        current_tab = self.window.get_active_tab()
        current_document = current_tab.get_document()

        if (not changing):
            if ( (current_tab in self.alt_views) ):
                # For some reason it always claims you have modified the document.  Oh well.
                if (self.alt_views[current_tab].is_untouched() == False):
                    # See if they are sure about closing this alternate document
                    if (not (self.show_save2_dialog(None)) ):
                        return # Don't close the split view after all...

        original_view = self.split_views[current_tab].get_child1().get_children()[0]

        for each in current_tab.get_children():

            for any in each.get_children():
                each.remove(any)

            original_view.reparent(each)

        current_tab.show_all()

        self.split_views.pop(current_tab)

        if (not changing):
            self.same_document.pop(current_tab)

            if (current_tab in self.alt_views):
                self.alt_views.pop(current_tab)

    # Basically recreate the split view.
    def flip_split_view(self, button):
        if (self.btn_flip.get_label() == "Vertical Splitview"):
            self.end_split_view(None, changing = True)
            self.split_view(None, "horizontal")

            self.btn_flip.set_label("Horizontal Splitview")

        else:
            self.end_split_view(None, changing = True)
            self.split_view(None, "vertical")

            self.btn_flip.set_label("Vertical Splitview")

        current_tab = self.window.get_active_tab()
        self.label_other_document.set_label(os.path.basename(self.alt_views[current_tab].get_uri().replace("%20", " ")))

    # Create a dialog that lets the user select a different document to view...
    def view_other_file(self, button):
        dialog = Gtk.FileChooserDialog("Open...", None,
                                       Gtk.FILE_CHOOSER_ACTION_OPEN,
                                       (Gtk.STOCK_CANCEL, Gtk.RESPONSE_CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.RESPONSE_OK))

        filter_list = [
            {"label": "All Files", "patterns": ["*"], "mime-types": []},
            {"label": "Text Files", "patterns": [], "mime-types": ["text/html", "text/plain"]}
        ]

        for dict in filter_list:
            filter = Gtk.FileFilter()
            filter.set_name(dict["label"])
            for each in dict["patterns"]:
                filter.add_pattern(each)

            for each in dict["mime-types"]:
                filter.add_mime_type(each)

            dialog.add_filter(filter)

        response = dialog.run()

        if (response == Gtk.RESPONSE_OK):
            self.load_other_file(dialog.get_filename())

        else:
            pass

        dialog.destroy()

    # Load a separate file into the alternate view.
    def load_other_file(self, source):
        current_tab = self.window.get_active_tab()

        self.same_document[current_tab] = False

        self.split_views[current_tab].remove(self.split_views[current_tab].get_children()[1])

        new_document = Pluma.Document()#.Pluma_document_new()
        new_document.load("file://" + source.replace(" ", "%20"), self.encoding, 1, True)
        new_view = Pluma.View.new_with_buffer(new_document)#.Pluma_view_new(new_document)

        new_document.connect("mark-set", self.update_line_column_data)

        new_document.save(0)

        self.alt_views[current_tab] = new_document

        sw = Gtk.ScrolledWindow()
        sw.add(new_view)

        self.split_views[current_tab].add2(sw)

        self.label_other_document.set_label(os.path.basename(source).replace("%20", " "))

        self.window.get_active_tab().show_all()

    def save_other_file(self, button):
        current_tab = self.window.get_active_tab()

        self.alt_views[current_tab].save(0)

        self.show_confirm_save_dialog(None)

    def show_save2_dialog(self, button):
        current_tab = self.window.get_active_tab()

        dialog = Gtk.Dialog(title = "Help me help you!",
                            parent = None,
                            flags = Gtk.DIALOG_MODAL,
                            buttons = (Gtk.STOCK_CANCEL, Gtk.RESPONSE_CANCEL,
                                       Gtk.STOCK_NO, Gtk.RESPONSE_NO,
                                       Gtk.STOCK_YES, Gtk.RESPONSE_YES)
                           )

        hbox = Gtk.HBox()
        hbox.pack_start(Gtk.Label("Save changes to '%s'?" % os.path.basename(self.alt_views[current_tab].get_uri().replace("%20", " "))), True, True, 0)

        dialog.vbox.pack_start(hbox, True, True, 0)

        dialog.vbox.show_all()

        response = dialog.run()

        if (response == Gtk.RESPONSE_OK):
            self.alt_views[current_tab].save(0)

        elif (response == Gtk.RESPONSE_CANCEL):
            dialog.destroy()
            return False

        else:
            pass

        dialog.destroy()

        return True

    def show_confirm_save_dialog(self, button):
        current_tab = self.window.get_active_tab()

        dialog = Gtk.Dialog(title = "Document saved!",
                            parent = None,
                            flags = Gtk.DIALOG_MODAL,
                            buttons = (Gtk.STOCK_OK, Gtk.RESPONSE_OK,
                                       Gtk.STOCK_YES, Gtk.RESPONSE_YES)
                           )

        hbox = Gtk.HBox()
        hbox.pack_start(Gtk.Label("You have successfully saved"), True, True, 0)

        dialog.vbox.pack_start(hbox, True, True, 0)

        hbox = Gtk.HBox()
        hbox.pack_start(Gtk.Label("'%s'!" % os.path.basename(self.alt_views[current_tab].get_uri().replace("%20", " "))), True, True, 0)

        dialog.vbox.pack_start(hbox, True, True, 0)

        dialog.vbox.show_all()

        response = dialog.run()

        if (response == Gtk.RESPONSE_OK):
            pass

        else:
            pass

        dialog.destroy()

    def show_error_dialog(self):
        dialog = Gtk.Dialog(title = "Error",
                            parent = None,
                            flags = Gtk.DIALOG_MODAL,
                            buttons = (Gtk.STOCK_OK, Gtk.RESPONSE_OK)
                           )

        hbox = Gtk.HBox()
        hbox.pack_start(Gtk.Label("You can't splitview"), True, True, 0)

        dialog.vbox.pack_start(hbox, True, True, 0)

        hbox = Gtk.HBox()
        hbox.pack_start(Gtk.Label("an empty document."), True, True, 0)

        dialog.vbox.pack_start(hbox, True, True, 0)

        dialog.vbox.show_all()

        response = dialog.run()

        dialog.destroy()

    # This function eventually sets the divider of the splitview at 50%.
    # It waits until the gui object returns a reasonable width.
    def debug(self):
        current_tab = self.window.get_active_tab()

        x = self.split_views[current_tab].get_property("max-position")

        # At first it just says 0 or 1 ... I just picked 50 at random.  If you're using GEdit
        # and you have a viewable editing window of < 50 pixels, then, uh, sorry!
        if (x > 50):
            self.split_views[current_tab].set_position(x / 2)

            return False

        return True

    def insert_menu_item(self, window):
        manager = self.window.get_ui_manager()

        self.action_group = Gtk.ActionGroup("PluginActions")

        # Create an action for the "Run in python" menu option
        # and set it to call the "run_document_in_python" function.
        self.split_view_action = Gtk.Action(name="ExamplePy", label="Toggle Split View", tooltip="Create a split view of the current document", stock_id=Gtk.STOCK_REFRESH)
        self.split_view_action.connect("activate", self.toggle_split_view)

        # Add the action with Ctrl + F5 as its keyboard shortcut.
        self.action_group.add_action_with_accel(self.split_view_action, "<Ctrl><Shift>T")

        # Add the action group.
        manager.insert_action_group(self.action_group, -1)

        # Add the item to the "Views" menu.
        self.ui_id = manager.add_ui_from_string(ui_string)

    def remove_menu_item(self):
        panel = self.window.get_side_panel()

        panel.remove_item(self.results_view)


class SplitViewPlugin(GObject.Object, Peas.Activatable):
    __gtype_name__ = "SplitViewPlugin"

    object = GObject.Property(type=GObject.Object)  # it needs `self.window = self.object` in `do_activate()`
                                                    # or use `self.object` instead of `self.window` in your code

    def __init__(self):
        GObject.Object.__init__(self)
        self.instances = {}

    def do_activate(self):
        window = self.object
        self.instances[window] = PluginHelper(self, window)

    def do_deactivate(self):
        window = self.object
        self.instances[window].deactivate()

    def do_update_state(self):
        window = self.object
        self.instances[window].update_ui()
