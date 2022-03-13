import os

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')

from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.RenderResultListAction import \
    RenderResultListAction
from ulauncher.api.shared.action.SetUserQueryAction import SetUserQueryAction
from ulauncher.api.shared.event import (ItemEnterEvent, KeywordQueryEvent,
                                        PreferencesEvent,
                                        PreferencesUpdateEvent)
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

from asana_extension.listeners.ItemEnterEventListener import ItemEnterEventListener
from asana_extension.listeners.KeywordQueryEventListener import KeywordQueryEventListener
from asana_extension.listeners.PreferencesEventListener import (PreferencesEventListener,
                                                                PreferencesUpdateEventListener)


class AsanaExtension(Extension):
    ICON_FILE = 'images/icon.png'

    keyword = None
    api_token = None

    def __init__(self):
        super(AsanaExtension, self).__init__()
        self.icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), self.ICON_FILE)
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener(self.ICON_FILE))
        self.subscribe(PreferencesEvent, PreferencesEventListener())
        self.subscribe(PreferencesUpdateEvent, PreferencesUpdateEventListener())

    def get_icon(self):
        return self.ICON_FILE

    def show_menu(self):
        keyword = self.keyword

        items = [ExtensionResultItem(name="Create a Task",
                                     description="Add a new task in My Tasks List",
                                     icon="images/create.svg",
                                     on_enter=SetUserQueryAction("%s create " % keyword)),

                 ExtensionResultItem(name="Search My Tasks",
                                     description="Exact or Typeahead search in My Tasks List",
                                     icon="images/search.svg",
                                     on_enter=SetUserQueryAction("%s tasks " % keyword)),

                 ExtensionResultItem(name="Filter by Tags",
                                     description="Find tasks by Tags",
                                     icon="images/tags.svg",
                                     on_enter=SetUserQueryAction("%s tags " % keyword)),

                 ExtensionResultItem(name="Filter by Sections",
                                     description="Find tasks by Sections",
                                     icon="images/sections.svg",
                                     on_enter=SetUserQueryAction("%s sections " % keyword))]

        return RenderResultListAction(items)
