import asana


class MyTasksSections(object):
    cached_sections = []

    def __init__(self, extension):
        self.extension = extension

    def get_list(self):
        if not MyTasksSections.cached_sections:
            api = asana.Client.access_token(self.extension.api_token)
            me = api.users.me()
            workspace_id = me['workspaces'][0]['gid']
            user_task_lists = api.user_task_lists.get_user_task_list_for_user(me['gid'], {'workspace': workspace_id})

            MyTasksSections.cached_sections = [s for s in api.sections.get_sections_for_project(user_task_lists['gid'])]

        return MyTasksSections.cached_sections
