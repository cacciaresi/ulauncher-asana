from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
from ulauncher.api.shared.action.RenderResultListAction import \
    RenderResultListAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

from asana_extension.asana_api.MyTasks import MyTasks


class ItemEnterEventListener(EventListener):
    def __init__(self, icon_file):
        self.icon_file = icon_file

    def on_event(self, event, extension):
        data = event.get_data()

        if data['action'] == "create":
            MyTasks(extension).create_task(data["task"], data["section_id"])

        if data['action'] == "my_task_search":
            return RenderResultListAction(MyTasks(extension).get_for_name_full_text(data["task"]))

        if data['action'] == "typeahead_task_search":
            return RenderResultListAction(MyTasks(extension).get_for_name_typeahead(data["task"]))

        return self.get_action_to_render(name="Incorrect request", description="todo create my task")

    def get_action_to_render(self, name, description, on_enter=None):
        item = ExtensionResultItem(name=name,
                                   description=description,
                                   icon=self.icon_file,
                                   on_enter=on_enter or DoNothingAction())

        return RenderResultListAction([item])
