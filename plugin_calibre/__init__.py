#!/usr/bin/env python
from __future__ import (unicode_literals, division, absolute_import, print_function)

__license__     = 'GPLv3'
__author__      = 'Alberto Pettarin (alberto AT albertopettarin DOT it)'
__copyright__   = '2012-2014 Alberto Pettarin (alberto AT albertopettarin DOT it)'
__version__     = 'v1.0.19'
__date__        = '2014-09-02'
__description__ = 'exlibris - add a nice ex libris to your EPUB eBook'
__docformat__   = 'restructuredtext en'

# The class that all Interface Action plugin wrappers must inherit from
from calibre.customize import InterfaceActionBase

class GUIStarter(InterfaceActionBase):
    name                    = 'Ex Libris'
    description             = 'Add a nice ex libris to your EPUB eBook'
    supported_platforms     = ['windows', 'osx', 'linux']
    author                  = 'Alberto Pettarin'
    version                 = (1, 0, 19)
    minimum_calibre_version = (0, 8, 51)
    can_be_disabled         = True

    #: This field defines the GUI plugin class that contains all the code
    #: that actually does something. Its format is module_path:class_name
    #: The specified class must be defined in the specified module.
    actual_plugin           = 'calibre_plugins.exlibris_plugin.ui:GUI'

    def is_customizable(self):
        return True

    def config_widget(self):
        from calibre_plugins.exlibris_plugin.config import ConfigWidget
        return ConfigWidget()

    def save_settings(self, config_widget):
        config_widget.save_settings()

        # Apply the changes
        ac = self.actual_plugin_
        if ac is not None:
            ac.apply_settings()


