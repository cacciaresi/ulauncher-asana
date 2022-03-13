class MyTasksSections(object):
    cached_sections = []

    def __init__(self, extension):
        self.extension = extension

    def get_list(self):
        if not MyTasksSections.cached_sections:
            api = self.extension.api

            user_task_lists = api.user_task_lists.get_user_task_list_for_user(
                self.extension.me['gid'],
                {
                    'workspace': self.extension.workspace_gid()
                }
            )

            MyTasksSections.cached_sections = [s for s in api.sections.get_sections_for_project(user_task_lists['gid'])]

        return MyTasksSections.cached_sections
