import unicodedata

from ulauncher.api.shared.action.OpenUrlAction import OpenUrlAction
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem


class BaseAsanaAPIModel(object):
    def __init__(self, extension):
        self.extension = extension
        self.api = self.extension.api
        self.me = self.extension.me

    @staticmethod
    def base_url():
        return "https://app.asana.com/0/"

    def open_asana_model_url_result(self, item):
        action = OpenUrlAction(f"{self.base_url()}{self.me['gid']}/{item['gid']}/f")
        icon = f'images/{"completed" if item["completed"] else "incomplete"}_task.svg'
        name = item["name"]

        return ExtensionResultItem(icon=icon, name=name, on_enter=action)

    @staticmethod
    def strip_accents(s):
        return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
