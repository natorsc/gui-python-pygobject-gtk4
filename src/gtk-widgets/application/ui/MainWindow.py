# -*- coding: utf-8 -*-
"""Python and GTK: PyGObject Gtk.Application."""

import pathlib
import sys

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk

Adw.init()

BASE_DIR = pathlib.Path(__file__).resolve().parent


@Gtk.Template(filename=str(BASE_DIR.joinpath('MainWindow.ui')))
class ExampleWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'ExampleWindow'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Your code here:
        # ...


# This class can be placed in a separate file (e.g. main.py).
class ExampleApplication(Gtk.Application):

    def __init__(self):
        super().__init__(application_id='br.com.justcode.PyGObject',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

        # Menu actions.
        # `<primary>q` = `Ctrl + q`.
        self.create_action('quit', self.exit_app, ['<primary>q'])
        self.create_action('preferences', self.on_preferences_action)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = ExampleWindow(application=self)
        win.present()

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_shutdown(self):
        Gtk.Application.do_shutdown(self)

    def on_preferences_action(self, action, param):
        """Callback for the `app.preferences` action of the interface file."""
        print('Action `app.preferences` was active.')

    def exit_app(self, action, param):
        """Callback is executed when the shortcut keys `Ctrl + q` are pressed."""
        self.quit()

    def create_action(self, name, callback, shortcuts=None):
        """Adds an action to the application.

        Args:
            name (str): Name of the action.
            callback (def): Function that will be called when the action is active.
            shortcuts (list[str]): List of shortcuts that trigger the action.
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect('activate', callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f'app.{name}', shortcuts)


if __name__ == '__main__':
    app = ExampleApplication()
    app.run(sys.argv)
