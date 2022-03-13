from ulauncher.api.client.EventListener import EventListener


class PreferencesEventListener(EventListener):
    def on_event(self, event, extension):
        extension.keyword = event.preferences["asana_kw"]
        extension.api_token = event.preferences["asana_api_token"]


class PreferencesUpdateEventListener(EventListener):
    def on_event(self, event, extension):
        if event.id == "asana_kw":
            extension.keyword = event.new_value
        elif event.id == "asana_api_token":
            extension.api_token = event.new_value
