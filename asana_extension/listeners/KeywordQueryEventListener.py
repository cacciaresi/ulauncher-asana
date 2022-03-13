import re

from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction

from asana_extension.Utils import filter_task_action, create_task_with_section, \
    create_task_without_section, filter_task_menu_action, create_task_menu_action, show_tags, show_sections, \
    filter_tasks_by_name
from asana_extension.asana_api.FavoritesList import FavoritesList
from asana_extension.asana_api.MyTasks import MyTasks
from asana_extension.asana_api.MyTasksSections import MyTasksSections


class KeywordQueryEventListener(EventListener):
    previous_tag = None
    previous_tag_search = []

    previous_section = None
    previous_section_search = []

    def on_event(self, event, extension):
        query = event.get_argument() or ""

        if not query:
            return extension.show_menu()

        if query == "create":
            return create_task_menu_action()

        if query == "tasks":
            return filter_task_menu_action()

        if query == "tags":
            return show_tags(extension)

        if query == "sections":
            return show_sections(extension)

        tasks_filter = re.findall(r"^tasks\s(.*)?$", query, re.IGNORECASE)

        # Filtering by "tasks {task_name} #"
        if tasks_filter:
            task = tasks_filter[0]
            return filter_task_action(task)

        # Filtering by "create {task_name} #"
        task_with_section = re.findall(r"^create\s(.*)?\s#(\S*)?$", query, re.IGNORECASE)
        if task_with_section:
            return create_task_with_section(extension, task_with_section)

        # Filtering by "create {task_name}"
        task_without_section = re.findall(r"^create\s(.*)?$", query, re.IGNORECASE)
        if task_without_section:
            return create_task_without_section(task_without_section)

        # Filtering by "tags [tag_name] {task_name}"
        filter_tasks_for_tag = re.findall(r"^tags\s\[(.*?)\](.*)?$", query, re.IGNORECASE)
        if filter_tasks_for_tag:
            return filter_tasks_with_tag(extension, filter_tasks_for_tag)

        # Filtering by "sections [section_name] {task_name}"
        filter_tasks_for_section = re.findall(r"^sections\s\[(.*?)\](.*)?$", query, re.IGNORECASE)
        if filter_tasks_for_section:
            return filter_tasks_with_section(extension, filter_tasks_for_section)


def filter_tasks_with_tag(extension, filter_tasks_for_tag):
    current_tag = filter_tasks_for_tag[0][0]
    selected_filter = filter_tasks_for_tag[0][1]
    tag = None

    for _tag in FavoritesList(extension).get_tags():
        if current_tag in _tag["name"]:
            tag = _tag

    if KeywordQueryEventListener.previous_tag != current_tag:
        KeywordQueryEventListener.previous_tag = current_tag
        all_tasks_for_tag = MyTasks(extension).get_for_tag(tag, include_completed=False)
        KeywordQueryEventListener.previous_tag_search = all_tasks_for_tag
        return RenderResultListAction(all_tasks_for_tag)
    else:
        return filter_tasks_by_name(KeywordQueryEventListener.previous_tag_search, selected_filter)


def filter_tasks_with_section(extension, filter_tasks_for_section):
    current_section = filter_tasks_for_section[0][0]
    selected_filter_section = filter_tasks_for_section[0][1]
    sections = MyTasksSections(extension).get_list()
    section = None

    for _section in sections:
        if current_section in _section["name"]:
            section = _section

    if KeywordQueryEventListener.previous_section != current_section:
        KeywordQueryEventListener.previous_section = current_section
        all_tasks_for_section = MyTasks(extension).get_for_section(section, include_completed=False)
        KeywordQueryEventListener.previous_section_search = all_tasks_for_section
        return RenderResultListAction(all_tasks_for_section)
    else:
        return filter_tasks_by_name(KeywordQueryEventListener.previous_section_search, selected_filter_section)
