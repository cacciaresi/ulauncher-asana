import logging

import asana

logger = logging.getLogger(__name__)


class FavoritesList(object):
    cached_tags = []

    def __init__(self, extension):
        self.extension = extension

    def get_tags(self):
        if not FavoritesList.cached_tags:
            api = asana.Client.access_token(self.extension.api_token)
            me = api.users.me()
            options = {
                "resource_type": "tag",
                "workspace": me['workspaces'][0]['gid']
            }
            FavoritesList.cached_tags = [t for t in api.users.get_favorites_for_user("me", options)]

        return FavoritesList.cached_tags
