import gi

gi.require_version('Gdk', '3.0')
from asana_extension.AsanaExtension import AsanaExtension

if __name__ == '__main__':
    AsanaExtension().run()
