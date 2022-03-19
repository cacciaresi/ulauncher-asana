from asana_extension.asana_api.BaseAsanaAPIModel import BaseAsanaAPIModel


class UserFavorites(BaseAsanaAPIModel):
    def get_tags(self):
        options = {
            "resource_type": "tag",
            "workspace": self.extension.workspace_gid()
        }

        return [tag for tag in self.extension.api.users.get_favorites_for_user("me", options)]

    def get_projects(self):
        options = {
            "resource_type": "project",
            "workspace": self.extension.workspace_gid()
        }

        projects_with_stats = []

        for project in self.api.users.get_favorites_for_user("me", options):
            task_counts_for_project = self.api.projects.get_task_counts_for_project(
                project["gid"],
                opt_fields=['num_tasks', 'num_incomplete_tasks']
            )

            project["stats"] = task_counts_for_project
            projects_with_stats.append(project)

        return projects_with_stats
