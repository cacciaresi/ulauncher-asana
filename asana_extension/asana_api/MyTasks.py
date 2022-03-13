import logging
import unicodedata

import asana
from gi.repository import Notify
from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

logger = logging.getLogger(__name__)

ASANA_BASE_URL = "https://app.asana.com/0/"


class MyTasks(object):
    me = None
    api = None

    def __init__(self, extension):
        self.extension = extension
        self.initialize_asana_api_client()

    def initialize_asana_api_client(self):
        if not MyTasks.me:
            api = asana.Client.access_token(self.extension.api_token)
            MyTasks.me = api.users.me()
            MyTasks.api = api

    def get_for_name_typeahead(self, task_name=None):
        workspace_gid = MyTasks.me['workspaces'][0]['gid']
        tasks = []
        options = {
            'query': task_name,
            'resource_type': 'task'
        }

        result = MyTasks.api.typeahead.typeahead_for_workspace(workspace_gid, options,
                                                               opt_fields=['completed', 'name'])

        for item in result:
            if item["completed"]:
                continue

            svg = "images/incomplete_task.svg"
            name_ = "%s" % (str(item["name"]))
            tasks.append(self.open_task_url_result(item['gid'], name_, svg))

        return tasks

    def open_task_url_result(self, task_gid, name, icon):
        action = OpenUrlAction(f"{ASANA_BASE_URL}{MyTasks.me['gid']}/{task_gid}")
        return ExtensionResultItem(icon=icon, name=name, on_enter=action)

    @staticmethod
    def strip_accents(s):
        return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

    def get_for_name_full_text(self, task_name=None):
        workspace_gid = MyTasks.me['workspaces'][0]['gid']
        tasks = []
        options = {
            'text': task_name,
            'assignee.any': [MyTasks.me['gid']]
        }

        result = MyTasks.api.tasks.search_tasks_for_workspace(workspace_gid, options,
                                                              opt_fields=['completed', 'name'])

        for item in result:
            name_ = item["name"]

            if self.strip_accents(task_name.lower()) in self.strip_accents(name_.lower()):
                icon = f'images/task_{"completed" if item["completed"] else "incompleted"}.svg'
                tasks.append(self.open_task_url_result(item['gid'], name_, icon))

        return tasks

    def get_for_tag(self, tag, include_completed=False):
        tasks = []
        params = {}

        if not include_completed:
            params["completed_since"] = "now"

        result = MyTasks.api.tasks.get_tasks_for_tag(tag["gid"], params=params, opt_fields=['completed', 'name'])

        for item in result:
            icon = f'images/task_{"completed" if item["completed"] else "incompleted"}.svg'
            tasks.append(self.open_task_url_result(item['gid'], item["name"], icon))

        return tasks

    def get_for_section(self, section, include_completed=False):
        tasks = []
        params = {}

        if not include_completed:
            params["completed_since"] = "now"

        result = MyTasks.api.tasks.get_tasks_for_section(section["gid"], params=params,
                                                         opt_fields=['completed', 'name'])

        for item in result:
            icon = f'images/task_{"completed" if item["completed"] else "incompleted"}.svg'
            tasks.append(self.open_task_url_result(item['gid'], item["name"], icon))

        return tasks

    def create_task(self, task, section_id=None):
        workspace_id = MyTasks.me['workspaces'][0]['gid']
        options = {
            'name': task,
            'assignee': MyTasks.me['gid'],
            'workspace': workspace_id,
        }

        if section_id:
            options['assignee_section'] = section_id

        MyTasks.api.tasks.create_task(options)

        Notify.init("AsanaExtension")
        Notify.Notification.new("Created Asana Task", "", "").show()
