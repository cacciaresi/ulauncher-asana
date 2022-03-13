from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.SetUserQueryAction import SetUserQueryAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

from asana_extension.asana_api.FavoritesList import FavoritesList
from asana_extension.asana_api.MyTasks import MyTasks
from asana_extension.asana_api.MyTasksSections import MyTasksSections


def filter_task_action(task):
    on_enter = ExtensionCustomAction({"action": "my_task_search", "task": task}, keep_app_open=True)
    on_alt_enter = ExtensionCustomAction({"action": "typeahead_task_search", "task": task}, keep_app_open=True)

    return RenderResultListAction([
        ExtensionResultItem(
            icon="images/keyboard.svg",
            name=f"Find task: {task}",
            description="Enter: exact search. Alt-Enter: typeahead",
            highlightable=False,
            on_enter=on_enter,
            on_alt_enter=on_alt_enter
        )
    ])


def create_task_with_section(extension, task_with_section):
    task = task_with_section[0][0]
    sections = [ExtensionResultItem(
        icon="images/section.svg",
        name=section["name"],
        description="Add the new task to this section?",
        highlightable=False,
        on_enter=ExtensionCustomAction(
            {"action": "create", "task": task, "section_id": section["gid"]}, keep_app_open=False))
        for section in MyTasksSections(extension).get_list()]

    return RenderResultListAction(sections)


def create_task_without_section(task_without_section):
    on_enter = ExtensionCustomAction({
        "action": "create",
        "task": (task_without_section[0]),
        "section_id": None},
        keep_app_open=False
    )

    item = ExtensionResultItem(icon="images/create.svg",
                               name=f"Create task: {task_without_section[0]}",
                               description="Use <space># at the end to choose a Section.",
                               highlightable=False,
                               on_enter=on_enter)

    return RenderResultListAction([item])


def filter_task_menu_action():
    return RenderResultListAction([
        ExtensionResultItem(
            icon="images/keyboard.svg",
            name="Filter tasks",
            highlightable=False,
            description="Start typing to search for a Task.",
        )
    ])


def create_task_menu_action():
    return RenderResultListAction([
        ExtensionResultItem(
            icon="images/create.svg",
            name="Enter the task name",
            highlightable=False,
            description="Use <space># at the end to choose a Section.",
        )
    ])


def show_tags(extension=None):
    tags = FavoritesList(extension).get_tags()
    results = []

    for tag in tags:
        on_enter = SetUserQueryAction(f'{extension.keyword} tags [{tag["name"]}] ')
        r = ExtensionResultItem(
            icon="images/tag.svg",
            name=tag["name"],
            description="Search tasks for tag",
            highlightable=False,
            on_enter=on_enter
        )

        results.append(r)

    return RenderResultListAction(results)


def show_sections(extension=None):
    results = []

    for section in MyTasksSections(extension).get_list():
        on_enter = SetUserQueryAction(f'{extension.keyword} sections [{section["name"]}] ')

        results.append(ExtensionResultItem(
            icon="images/section.svg",
            name=section["name"],
            description="Search tasks for tag",
            highlightable=False,
            on_enter=on_enter
        ))

    return RenderResultListAction(results)


def filter_tasks_by_name(tasks, selected_filter_section):
    tasks_matching_search = []

    for task in tasks:
        accents = MyTasks.strip_accents(selected_filter_section.lower().strip())
        strip_accents = MyTasks.strip_accents(task.get_name().lower())

        if accents in strip_accents:
            tasks_matching_search.append(task)

    return RenderResultListAction(tasks_matching_search)
