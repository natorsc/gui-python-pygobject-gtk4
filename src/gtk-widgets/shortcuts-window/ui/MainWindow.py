# -*- coding: utf-8 -*-
"""Python e GTK: PyGObject Gtk.ShortcutsWindow() ui file."""

import sys
from pathlib import Path



import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk

Adw.init()

BASE_DIR = Path(__file__).resolve().parent
APPLICATION_WINDOW = str(BASE_DIR.joinpath('MainWindow.ui'))
SHORTCUTS_WINDOW = str(BASE_DIR.joinpath('ShortcutsWindow.ui'))

_MODULES = BASE_DIR.parent.parent.parent.joinpath('_modules')
sys.path.append(str(_MODULES))
import _tools

_tools.compile_blueprint_ui(ui_dir=BASE_DIR)


@Gtk.Template(filename=SHORTCUTS_WINDOW)
class ShortcutsWindow(Gtk.ShortcutsWindow):
    __gtype_name__ = 'ShortcutsWindow'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@Gtk.Template(filename=APPLICATION_WINDOW)
class ExampleWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'ExampleWindow'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ExampleApplication(Gtk.Application):

    def __init__(self):
        super().__init__(application_id='br.com.justcode.PyGObject',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

        self.create_action('quit', self.exit_app, ['<primary>q'])
        self.create_action('preferences', self.on_preferences_action)
        self.create_action(
            'shortcuts-window',
            self.on_shortcuts_window_action, ['<primary>1'],
        )

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
        print('Action `app.preferences` was active.')

    def on_shortcuts_window_action(self, action, param):
        shortcuts_window = ShortcutsWindow(
            transient_for=self.get_active_window())
        shortcuts_window.present()

    def exit_app(self, action, param):
        self.quit()

    def create_action(self, name: str, callback: Callable[[str, str], None],
                      shortcuts: str | None = None):
        action = Gio.SimpleAction.new(name=name, parameter_type=None)
        action.connect('activate', callback)
        self.add_action(action=action)
        if shortcuts:
            self.set_accels_for_action(
                detailed_action_name=f'app.{name}',
                accels=shortcuts,
            )


if __name__ == '__main__':
    import sys

    app = ExampleApplication()
    app.run(sys.argv)
