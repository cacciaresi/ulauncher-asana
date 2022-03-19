import itertools

from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from ulauncher.api.shared.action.SetUserQueryAction import SetUserQueryAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

from asana_extension.asana_api.BaseAsanaAPIModel import BaseAsanaAPIModel


class AsanaExtensionResultItem(ExtensionResultItem):
    def __init__(self, tasks=None, *args, **kw):
        super().__init__(*args, **kw)
        self.tasks = tasks

    def get_tasks(self):
        return self.tasks


class MyTasksSections(BaseAsanaAPIModel):
    def get_list(self):
        api = self.extension.api

        user_task_lists = api.user_task_lists.get_user_task_list_for_user(
            self.extension.me['gid'],
            {
                'workspace': self.extension.workspace_gid()
            }
        )

        return [section for section in api.sections.get_sections_for_project(user_task_lists['gid'])]

    def open_project_section_result_item(self, section, project_gid):
        on_enter = SetUserQueryAction(f'{self.extension.keyword} projects [{project_gid}] [{section}] ')

        icon = f'images/section.svg'
        name = section

        return ExtensionResultItem(icon=icon,
                                   name=name,
                                   on_enter=on_enter,
                                   description="Search tasks for section")

    def get_sections_for_project(self, project):
        api = self.extension.api

        tasks_with_sections = api.tasks.get_tasks_for_project(
            project['gid'],
            params={"completed_since": "now"},
            opt_fields=['name', 'completed', 'memberships.section.name']
        )

        def key_func(x):
            return x['memberships'][0]['section']['name']

        results = []

        for section, tasks in itertools.groupby(tasks_with_sections, key_func):
            section_result_item = self.open_project_section_result_item(section, project["gid"])
            tasks_result_items = []

            for task in tasks:
                tasks_result_items.append(self.open_asana_model_url_result(task))

            results.append((section_result_item, tasks_result_items))

        return results

    def open_asana_model_url_result(self, item):
        action = OpenUrlAction(f"{self.base_url()}{self.me['gid']}/{item['gid']}/f")
        icon = f'images/{"completed" if item["completed"] else "incomplete"}_task.svg'
        name = item["name"]

        return ExtensionResultItem(icon=icon, name=name, on_enter=action)
