import logging
import unicodedata

from gi.repository import Notify
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

logger = logging.getLogger(__name__)

ASANA_BASE_URL = "https://app.asana.com/0/"


class MyTasks(object):
    def __init__(self, extension):
        self.extension = extension
        self.api = self.extension.api
        self.me = self.extension.me

    def get_for_name_typeahead(self, task_name=None):
        tasks = []

        options = {
            'query': task_name,
            'resource_type': 'task'
        }

        result = self.api.typeahead.typeahead_for_workspace(
            self.extension.workspace_gid(),
            options,
            opt_fields=['completed', 'name']
        )

        for item in result:
            if item["completed"]:
                continue

            tasks.append(self.open_task_url_result(item))

        return tasks

    @staticmethod
    def strip_accents(s):
        return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

    def get_for_name_full_text(self, task_name=None):
        tasks = []
        options = {
            'text': task_name,
            'assignee.any': [self.me['gid']]
        }

        result = self.api.tasks.search_tasks_for_workspace(
            self.extension.workspace_gid(),
            options,
            opt_fields=['completed', 'name']
        )

        for item in result:
            name_ = item["name"]

            if self.strip_accents(task_name.lower()) in self.strip_accents(name_.lower()):
                tasks.append(self.open_task_url_result(item))

        return tasks

    def get_for_tag(self, tag, include_completed=False):
        tasks = []
        params = {}

        if not include_completed:
            params["completed_since"] = "now"

        result = self.api.tasks.get_tasks_for_tag(tag["gid"], params=params, opt_fields=['completed', 'name'])

        for item in result:
            tasks.append(self.open_task_url_result(item))

        return tasks

    def get_for_section(self, section, include_completed=False):
        tasks = []
        params = {}

        if not include_completed:
            params["completed_since"] = "now"

        result = self.api.tasks.get_tasks_for_section(section["gid"], params=params,
                                                      opt_fields=['completed', 'name'])

        for item in result:
            tasks.append(self.open_task_url_result(item))

        return tasks

    def create_task(self, task, section_id=None):
        options = {
            'name': task,
            'assignee': self.me['gid'],
            'workspace': self.extension.workspace_gid(),
        }

        if section_id:
            options['assignee_section'] = section_id

        self.api.tasks.create_task(options)

        Notify.init("AsanaExtension")
        Notify.Notification.new("Created Asana Task", "", "").show()

    def open_task_url_result(self, item):
        action = OpenUrlAction(f"{ASANA_BASE_URL}{self.me['gid']}/{item['gid']}")
        icon = f'images/{"completed" if item["completed"] else "incomplete"}_task.svg'
        name = item["name"]

        return ExtensionResultItem(icon=icon, name=name, on_enter=action)
