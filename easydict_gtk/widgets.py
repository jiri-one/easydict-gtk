"""
Widgets for EasyDict-GTK
"""
import asyncio
from abc import abstractmethod
from settings import images

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio, GLib, Gdk, GdkPixbuf

# internal imports
from backends.sqlite_backend import search_async


class ListViewBase(Gtk.ListView):
    """ListView base class, it setup the basic factory, selection model & data model
    handlers must be overloaded & implemented in a sub class
    """

    def __init__(self, model_cls):
        super().__init__()
        # Use the signal Factory, so we can connect our own methods to setup
        self.factory = Gtk.SignalListItemFactory()
        # connect to Gtk.SignalListItemFactory signals
        # check https://docs.gtk.org/gtk4/class.SignalListItemFactory.html for details
        self.factory.connect("setup", self.on_factory_setup)
        self.factory.connect("bind", self.on_factory_bind)
        self.factory.connect("unbind", self.on_factory_unbind)
        self.factory.connect("teardown", self.on_factory_teardown)
        # Create data model, use our own class as elements
        self.set_factory(self.factory)
        self.store = self.setup_store(model_cls)
        # create a selection model containing our data model
        self.model = self.setup_model(self.store)
        self.model.connect("selection-changed", self.on_selection_changed)
        # set the selection model to the view
        self.set_model(self.model)

    def setup_model(self, store: Gio.ListModel) -> Gtk.SelectionModel:
        """Setup the selection model to use in Gtk.ListView
        Can be overloaded in subclass to use another Gtk.SelectModel model
        """
        return Gtk.SingleSelection.new(store)

    @abstractmethod
    def setup_store(self, model_cls) -> Gio.ListModel:
        """Setup the data model
        must be overloaded in subclass to use another Gio.ListModel
        """
        raise NotImplemented

    def add(self, elem):
        """add element to the data model"""
        self.store.append(elem)

    # Gtk.SignalListItemFactory signal callbacks
    # transfer to some some callback stubs, there can be overloaded in
    # a subclass.

    def on_factory_setup(self, widget, item: Gtk.ListItem):
        """GtkSignalListItemFactory::setup signal callback

        Setup the widgets to go into the ListView"""

        self.factory_setup(widget, item)

    def on_factory_bind(self, widget: Gtk.ListView, item: Gtk.ListItem):
        """GtkSignalListItemFactory::bind signal callback

        apply data from model to widgets set in setup"""
        self.factory_bind(widget, item)

    def on_factory_unbind(self, widget, item: Gtk.ListItem):
        """GtkSignalListItemFactory::unbind signal callback

        Undo the the binding done in ::bind if needed
        """
        self.factory_unbind(widget, item)

    def on_factory_teardown(self, widget, item: Gtk.ListItem):
        """GtkSignalListItemFactory::setup signal callback

        Undo the creation done in ::setup if needed
        """
        self.factory_teardown(widget, item)

    def on_selection_changed(self, widget, position, n_items):
        # get the current selection (GtkBitset)
        selection = widget.get_selection()
        # the the first value in the GtkBitset, that contain the index of the selection in the data model
        # as we use Gtk.SingleSelection, there can only be one ;-)
        ndx = selection.get_nth(0)
        self.selection_changed(widget, ndx)

    # --------------------> abstract callback methods <--------------------------------
    # Implement these methods in your subclass

    @abstractmethod
    def factory_setup(self, widget: Gtk.ListView, item: Gtk.ListItem):
        """Setup the widgets to go into the ListView (Overload in subclass)"""
        pass

    @abstractmethod
    def factory_bind(self, widget: Gtk.ListView, item: Gtk.ListItem):
        """apply data from model to widgets set in setup (Overload in subclass)"""
        pass

    @abstractmethod
    def factory_unbind(self, widget: Gtk.ListView, item: Gtk.ListItem):
        pass

    @abstractmethod
    def factory_teardown(self, widget: Gtk.ListView, item: Gtk.ListItem):
        pass

    @abstractmethod
    def selection_changed(self, widget, ndx):
        """trigged when selecting in listview is changed
        ndx: is the index in the data store model that is selected
        """
        pass


class ListViewStrings(ListViewBase):
    """Add ListView with only strings"""

    def __init__(self):
        super(ListViewStrings, self).__init__(Gtk.StringObject)

    def setup_store(self, model_cls) -> Gio.ListModel:
        """Setup the data model
        Can be overloaded in subclass to use another Gio.ListModel
        """
        return Gtk.StringList()


class SearchBar(Gtk.SearchBar):
    """Wrapper for Gtk.Searchbar Gtk.SearchEntry"""

    def __init__(self, loop, win: Gtk.ApplicationWindow = None):
        super(SearchBar, self).__init__()
        self._loop = loop
        self.task = None
        self.search_type = "first_chars"
        self.win = win
        search_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        search_box.add_css_class("ui/search_box.css")
        first_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        second_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        # Add SearchEntry
        self.entry = Gtk.SearchEntry()
        self.entry.set_hexpand(True)
        self.entry.connect("changed", self.on_search)
        first_hbox.append(self.entry)
        # add Search button
        self.button = Gtk.Button(label="Search")
        # Add DropDown menu
        self.dropdown = Gtk.DropDown.new_from_strings(["ENG", "CZE"])
        self.button.connect("clicked", self.on_search)
        # first_hbox.append(self.button)
        first_hbox.append(self.dropdown)

        # second line with toggle buttons
        self.toggle_first = Gtk.ToggleButton(label="First chars")
        self.toggle_first.set_active(True)
        self.toggle_whole_word = Gtk.ToggleButton(label="Whole word")
        self.toggle_whole_word.set_active(False)
        self.toggle_whole_word.set_group(self.toggle_first)
        self.toggle_fulltext = Gtk.ToggleButton(label="Fulltext")
        self.toggle_fulltext.set_active(False)
        self.toggle_fulltext.set_group(self.toggle_first)

        self.toggle_first.props.hexpand = True
        self.toggle_whole_word.props.hexpand = True
        self.toggle_fulltext.props.hexpand = True
        self.toggle_first.connect("clicked", self.on_toggle)
        self.toggle_whole_word.connect("clicked", self.on_toggle)
        self.toggle_fulltext.connect("clicked", self.on_toggle)

        second_hbox.append(self.toggle_first)
        second_hbox.append(self.toggle_whole_word)
        second_hbox.append(self.toggle_fulltext)

        search_box.append(first_hbox)
        search_box.append(second_hbox)
        self.set_child(search_box)
        # connect search entry to seach bar
        self.connect_entry(self.entry)
        if win:
            # set key capture from main window, it will show searchbar, when you start typing
            self.set_key_capture_widget(win)
        # show close button in search bar
        self.set_show_close_button(False)
        # Turn ON search mode
        self.set_search_mode(True)

    async def search_task(self, word, lng, search_type):
        # default language for results
        lng1 = lng
        # and second language for translation results
        lng2 = [lang for lang in ["cze", "eng"] if lang != lng1][0]

        result_strings = list()
        async with asyncio.TaskGroup() as tg:
            self.task = tg.create_task(search_async(word, lng, search_type))
            results = await self.task
            if results:
                for item in results.items:
                    if item.notes:
                        notes = " | " + item.notes
                    else:
                        notes = ""
                    if item.special:
                        special = " | " + item.special
                    else:
                        special = ""
                    whole_string = f"""<b>{getattr(item, lng1)}</b>\n {getattr(item, lng2)}{notes}{special}"""
                    result_strings.append(whole_string)
        # and with results we need to update the ListViewString store - it is StringList
        store = self.win.listview_str.store
        # remove all search results from current store and add all results together
        GLib.idle_add(store.splice, 0, len(store), result_strings)
        # https://lazka.github.io/pgi-docs/Gtk-4.0/classes/StringList.html#Gtk.StringList.splice
        # https://lazka.github.io/pgi-docs/#GLib-2.0/functions.html#GLib.idle_add
        # https://pygobject.readthedocs.io/en/latest/guide/threading.html

    async def search_in_db(self, word, lng, search_type):
        create_new_task = False
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                print(f"canceled: {self.task.cancelled()} or done: {self.task.done()}")

            if self.task.cancelled() or self.task.done():
                create_new_task = True
        else:
            create_new_task = True
        # if we initiate new search task and search word is not empty
        if create_new_task and word != "":
            await self.search_task(word, lng, search_type)

        # NOTE: this part down is now not unnecessary, because we delete content of store in on_search method
        # elif the word is empty, so we will empty the listview
        elif create_new_task and word == "":
            # need to update the ListViewString store - it is StringList
            store = self.win.listview_str.store
            # remove all search results from current store
            GLib.idle_add(store.splice, 0, len(store))

    def on_search(self, caller_obj):
        # get text from search entry
        word = self.entry.props.text
        # if we have word (searched text), then we need show the stack with results
        if word:
            if self.win.front_page in self.win.main_box:
                self.win.main_box.remove(self.win.front_page)
            if self.win.stack not in self.win.main_box:
                self.win.main_box.append(self.win.stack)
        else:  # if entry is empty, we will shof front page
            if self.win.stack in self.win.main_box:
                self.win.main_box.remove(self.win.stack)
            if self.win.front_page not in self.win.main_box:
                self.win.main_box.append(self.win.front_page)
            # store = self.win.listview_str.store
            # and remove all search results from current store
            # store.splice(0, len(store))
            # return None
        # get current language settings
        lng = self.dropdown.get_selected_item().props.string.lower()
        # get current search type
        search_type = self.search_type
        asyncio.run_coroutine_threadsafe(
            self.search_in_db(word, lng, search_type), self._loop
        )
        return None

    def on_toggle(self, button):
        # firsly we will get info about toggle button and set correct search type
        if button.props.label == "Fulltext":
            self.search_type = "fulltext"
        elif button.props.label == "Whole word":
            self.search_type = "whole_word"
        elif button.props.label == "First chars":
            self.search_type = "first_chars"
        else:
            raise ValueError(
                "Use only known toggles: 'Fulltext' or 'Whole word' or 'First chars'"
            )
        # and then we run search in db to sync toggle button state with results
        self.on_search(button)


class FrontPage(Gtk.Box):
    """Fron page of EasyDict-GTK in one Box"""

    def __init__(self):
        super().__init__()
        self.set_orientation(Gtk.Orientation.VERTICAL)
        welcome = self.welcome_label()
        self.append(welcome)
        logo = self.logo_image()
        self.append(logo)
        slogan = self.slogan_label()
        self.append(slogan)

    def welcome_label(self):
        label = Gtk.Label.new()
        # markup = GLib.markup_escape_text()
        label.set_justify(Gtk.Justification.CENTER)
        label.set_wrap(True)
        label.set_markup(
            '\n<b><span size="x-large">Welcome to EasyDict</span></b>\n\nJust start typing to see results!\n'
        )
        return label

    def logo_image(self):
        logo_pixbuf = GdkPixbuf.Pixbuf.new_from_file(images["ed_icon.png"])
        print(images.get("ed_icon.png", None))
        image = Gtk.Image.new_from_pixbuf(logo_pixbuf)
        image.set_size_request(500, 500)
        image.set_halign(Gtk.Align.CENTER)
        return image

    def slogan_label(self):
        label = Gtk.Label.new()
        # markup = GLib.markup_escape_text()
        label.set_justify(Gtk.Justification.CENTER)
        label.set_wrap(True)
        label.set_markup(
            "\n<big>The first translator which is completely open with dictionary data too.</big>"
        )
        return label


class MenuButton(Gtk.MenuButton):
    """
    Wrapper class for at Gtk.Menubutton with a menu defined
    in a Gtk.Builder xml string
    """

    def __init__(self, xml, name, icon_name="open-menu-symbolic"):
        super(MenuButton, self).__init__()
        builder = Gtk.Builder()
        builder.add_from_string(xml)
        menu = builder.get_object(name)
        self.set_menu_model(menu)
        self.set_icon_name(icon_name)


class MyListViewStrings(ListViewStrings):
    """Custom ListView"""

    def __init__(self, win: Gtk.ApplicationWindow):
        # Init ListView with store model class.
        super(MyListViewStrings, self).__init__()
        self.win = win
        self.set_vexpand(True)
        # put some data into the model
        # results = db_search("eng", "live", fulltext=False)
        # for row in results:
        #     self.add(f"""<b>{row["eng"]}</b>\n {row["cze"]}""")

    def factory_setup(self, widget: Gtk.ListView, item: Gtk.ListItem):
        """Gtk.SignalListItemFactory::setup signal callback (overloaded from parent class)

        Handles the creation widgets to put in the ListView
        """
        label = Gtk.Label()
        label.set_halign(Gtk.Align.START)
        label.set_hexpand(True)
        label.set_wrap(True)
        label.set_margin_start(10)
        item.set_child(label)

    def factory_bind(self, widget: Gtk.ListView, item: Gtk.ListItem):
        """Gtk.SignalListItemFactory::bind signal callback (overloaded from parent class)

        Handles adding data for the model to the widgets created in setup
        """
        # get the Gtk.Label
        label = item.get_child()
        # get the model item, connected to current ListItem
        data = item.get_item()
        # Update Gtk.Label with data from model item
        label.set_markup(data.get_string())
        # Update Gtk.Switch with data from model item
        item.set_child(label)

    def selection_changed(self, widget, ndx: int):
        """trigged when selecting in listview is changed"""
        # print("ZDEEEEEEEEEEE", self.win, widget, ndx)
        # markup = self.win._get_text_markup(
        #     f"Row {ndx} was selected ( {self.store[ndx].get_string()} )"
        # )
        # self.win.page4_label.set_markup(markup)
