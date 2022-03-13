import logging

logger = logging.getLogger(__name__)


class FavoritesList(object):
    cached_tags = []

    def __init__(self, extension):
        self.extension = extension

    def get_tags(self):
        if not FavoritesList.cached_tags:
            options = {
                "resource_type": "tag",
                "workspace": self.extension.workspace_gid()
            }
            FavoritesList.cached_tags = [t for t in self.extension.api.users.get_favorites_for_user("me", options)]

        return FavoritesList.cached_tags
