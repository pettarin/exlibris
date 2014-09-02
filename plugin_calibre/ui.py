#!/usr/bin/env python
from __future__ import (unicode_literals, division, absolute_import, print_function)

__license__     = 'GPLv3'
__author__      = 'Alberto Pettarin (alberto AT albertopettarin DOT it)'
__copyright__   = '2012-2014 Alberto Pettarin (alberto AT albertopettarin DOT it)'
__version__     = 'v1.0.19'
__date__        = '2014-09-02'
__description__ = 'exlibris - add a nice ex libris to your EPUB eBook'
__docformat__   = 'restructuredtext en'

# The class that all interface action plugins must inherit from
from calibre.gui2.actions import InterfaceAction
from calibre.gui2 import error_dialog
from calibre_plugins.exlibris_plugin.main import MainDialog

class GUI(InterfaceAction):

    name = 'Ex Libris'

    # Declare the main action associated with this plugin
    # The keyboard shortcut can be None if you dont want to use a keyboard
    # shortcut. Remember that currently calibre has no central management for
    # keyboard shortcuts, so try to use an unusual/unused shortcut.
    action_spec = ('exlibris', None, 'Run exlibris', 'Ctrl+Shift+X')

    def genesis(self):
        # This method is called once per plugin, do initial setup here

        # Set the icon for this interface action
        # The get_icons function is a builtin function defined for all your
        # plugin code. It loads icons from the plugin zip file. It returns
        # QIcon objects, if you want the actual data, use the analogous
        # get_resources builtin function.
        #
        # Note that if you are loading more than one icon, for performance, you
        # should pass a list of names to get_icons. In this case, get_icons
        # will return a dictionary mapping names to QIcons. Names that
        # are not found in the zip file will result in null QIcons.
        icon = get_icons('images/icon.png')

        # The qaction is automatically created from the action_spec defined
        # above
        self.qaction.setIcon(icon)
        self.qaction.triggered.connect(self.show_dialog)


    def show_dialog(self):
        # The base plugin object defined in __init__.py
        base_plugin_object = self.interface_action_base_plugin
        # Show the config dialog
        # The config dialog can also be shown from within
        # Preferences->Plugins, which is why the do_user_config
        # method is defined on the base plugin class
        do_user_config = base_plugin_object.do_user_config

        # self.gui is the main calibre GUI. It acts as the gateway to access
        # all the elements of the calibre user interface, it should also be the
        # parent of the dialog
        d = MainDialog(self.gui, self.qaction.icon(), do_user_config)


    def apply_settings(self):
        from calibre_plugins.exlibris_plugin.config import prefs
        # In an actual non trivial plugin, you would probably need to
        # do something based on the settings in prefs
        prefs

