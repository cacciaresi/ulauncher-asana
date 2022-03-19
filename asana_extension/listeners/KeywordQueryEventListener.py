import re

from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction

from asana_extension.Utils import filter_task_action, create_task_with_section, \
    create_task_without_section, show_tags, show_sections, \
    filter_tasks_by_name, show_projects, create_task, filter_tasks
from asana_extension.asana_api.MyTasks import MyTasks
from asana_extension.asana_api.MyTasksSections import MyTasksSections
from asana_extension.asana_api.UserFavorites import UserFavorites


class KeywordQueryEventListener(EventListener):
    previous_tag = None
    previous_tag_search = []

    previous_section = None
    previous_section_search = []

    previous_selected_project_gid = None
    previous_project_sections_search = []

    def on_event(self, event, extension):
        query = event.get_argument() or ""

        if not query:
            return extension.show_menu()

        if query == "create":
            return create_task()

        if query == "tasks":
            return filter_tasks()

        if query == "tags":
            return show_tags(extension)

        if query == "sections":
            return show_sections(extension)

        if query == "projects":
            return show_projects(extension)

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
        filter_tasks_for_tag = re.findall(r"^tags\s\[(.*?)](.*)?$", query, re.IGNORECASE)
        if filter_tasks_for_tag:
            return filter_tasks_with_tag(extension, filter_tasks_for_tag)

        # Filtering by "projects [project_name] [section_name] {task_name}"
        filter_for_section_from_project = re.findall(r"^projects\s\[(.*?)]\s\[(.*?)](.*)?$", query,
                                                     re.IGNORECASE)
        if filter_for_section_from_project:
            return self.filter_tasks_for_section_from_project(filter_for_section_from_project)

        # Select project [project_name] section"
        select_project_section = re.findall(r"^projects\s\[(.*?)]$", query, re.IGNORECASE)
        if select_project_section:
            return self.select_project_section(extension, select_project_section)

        # Filtering by "sections [section_name] {task_name}"
        filter_tasks_for_section = re.findall(r"^sections\s\[(.*?)](.*)?$", query, re.IGNORECASE)
        if filter_tasks_for_section:
            return filter_tasks_with_section(extension, filter_tasks_for_section)

    def select_project_section(self, extension, filter_tasks_per_project_gid):
        project_gid = filter_tasks_per_project_gid[0]

        if KeywordQueryEventListener.previous_selected_project_gid != project_gid:
            KeywordQueryEventListener.previous_selected_project_gid = project_gid
            all_tasks_by_section_for_project = MyTasksSections(extension).get_sections_for_project({"gid": project_gid})
            KeywordQueryEventListener.previous_project_sections_search = all_tasks_by_section_for_project

        project_sections = []

        for (section, tasks) in KeywordQueryEventListener.previous_project_sections_search:
            project_sections.append(section)

        return RenderResultListAction(project_sections)

    def filter_tasks_for_section_from_project(self, filter_tasks_per_project_gid):
        section_name = filter_tasks_per_project_gid[0][1]
        filter_task_name = filter_tasks_per_project_gid[0][2]

        for section, tasks in KeywordQueryEventListener.previous_project_sections_search:
            if section.get_name() == section_name:
                return filter_tasks_by_name(tasks, filter_task_name)


def filter_tasks_with_tag(extension, filter_tasks_for_tag):
    current_tag = filter_tasks_for_tag[0][0]
    selected_filter = filter_tasks_for_tag[0][1]
    tag = None

    for _tag in UserFavorites(extension).get_tags():
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
