#!/usr/bin/env python
from __future__ import (unicode_literals, division, absolute_import, print_function)

__license__     = 'GPLv3'
__author__      = 'Alberto Pettarin (alberto AT albertopettarin DOT it)'
__copyright__   = '2012-2014 Alberto Pettarin (alberto AT albertopettarin DOT it)'
__version__     = 'v1.0.19'
__date__        = '2014-09-02'
__description__ = 'exlibris - add a nice ex libris to your EPUB eBook'
__docformat__   = 'restructuredtext en'

try:
    from PyQt5.Qt import QCheckBox, QFileDialog, QGridLayout, QLabel, QLineEdit, QListWidget, QPushButton, QTextEdit, QWidget
except ImportError as e:
    from PyQt4.Qt import QCheckBox, QFileDialog, QGridLayout, QLabel, QLineEdit, QListWidget, QPushButton, QTextEdit, QWidget

import os
from calibre.utils.config import JSONConfig

from calibre_plugins.exlibris_plugin.exlibris import exlibris

# This is where all preferences for this plugin will be stored
# Remember that this name (i.e. plugins/interface_demo) is also
# in a global namespace, so make it as unique as possible.
# You should always prefix your config file name with plugins/,
# so as to ensure you dont accidentally clobber a calibre config file
prefs = JSONConfig('plugins/exlibris_plugin')

# Set defaults
prefs.defaults['xhtml_filename'] = u''
prefs.defaults['include_dir'] = u''
prefs.defaults['include_guide_text'] = u'Ex libris'
prefs.defaults['include_toc_text'] = u'Ex libris'
prefs.defaults['replace_strings'] = u'key1=string1;\nkey2=string2;\nkey3=string3;'
prefs.defaults['include_spine'] = u'1'
prefs.defaults['include_toc'] = u'1'
prefs.defaults['checkbox_include_dir'] = u'True'
prefs.defaults['checkbox_include_guide_text'] = u'True'
prefs.defaults['checkbox_include_toc_text'] = u'True'
prefs.defaults['checkbox_ask_replace'] = u'True'
prefs.defaults['checkbox_disable_first_last_only'] = u'False'


class ConfigWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        
        self.setWindowTitle('exlibris preferences')
        
        row = 0
        self.l = QGridLayout()
        self.setLayout(self.l)
        
        self.label_xhtml_filename = QLabel('Ex libris XHTML filename:')
        self.xhtml_filename = QLineEdit(self)
        self.xhtml_filename.setText(prefs['xhtml_filename'])
        self.button_xhtml_filename = QPushButton('Change', self)
        self.button_xhtml_filename.clicked.connect(self.button_xhtml_filename_handler)
        
        self.l.addWidget(self.label_xhtml_filename, row, 1)
        row += 1
        self.l.addWidget(self.xhtml_filename, row, 1)
        self.l.addWidget(self.button_xhtml_filename, row, 2)
        row += 1
        
        self.l.addWidget(QLabel(''), row, 1)
        row += 1

        self.label_include_dir = QLabel('Include additional files from directory:')
        self.checkbox_include_dir = QCheckBox('', self)
        self.checkbox_include_dir.setChecked(prefs['checkbox_include_dir'] == 'True')
        self.include_dir = QLineEdit(self)
        self.include_dir.setText(prefs['include_dir'])
        self.button_include_dir = QPushButton('Change', self)
        self.button_include_dir.clicked.connect(self.button_include_dir_handler)
        
        self.l.addWidget(self.checkbox_include_dir, row, 0)
        self.l.addWidget(self.label_include_dir, row, 1)
        row += 1
        self.l.addWidget(self.include_dir, row, 1)
        self.l.addWidget(self.button_include_dir, row, 2)
        row += 1
        
        self.l.addWidget(QLabel(''), row, 1)
        row += 1
        
        self.label_include_guide_text = QLabel('Include in guide with string:')
        self.checkbox_include_guide_text = QCheckBox('', self)
        self.checkbox_include_guide_text.setChecked(prefs['checkbox_include_guide_text'] == 'True')
        self.include_guide_text = QLineEdit(self)
        self.include_guide_text.setText(prefs['include_guide_text'])
        
        self.l.addWidget(self.checkbox_include_guide_text, row, 0)
        self.l.addWidget(self.label_include_guide_text, row, 1)
        row += 1
        self.l.addWidget(self.include_guide_text, row, 1)
        row += 1
        
        self.l.addWidget(QLabel(''), row, 1)
        row += 1
        
        self.label_include_toc_text = QLabel('Include in TOC with string:')
        self.checkbox_include_toc_text = QCheckBox('', self)
        self.checkbox_include_toc_text.setChecked(prefs['checkbox_include_toc_text'] == 'True')
        self.include_toc_text = QLineEdit(self)
        self.include_toc_text.setText(prefs['include_toc_text'])
        
        self.l.addWidget(self.checkbox_include_toc_text, row, 0)
        self.l.addWidget(self.label_include_toc_text, row, 1)
        row += 1
        self.l.addWidget(self.include_toc_text, row, 1)
        row += 1
        
        self.l.addWidget(QLabel(''), row, 1)
        row += 1
        
        self.label_ask_replace = QLabel('Ask before replacing book in library')
        self.checkbox_ask_replace = QCheckBox('', self)
        self.checkbox_ask_replace.setChecked(prefs['checkbox_ask_replace'] == 'True')
        self.l.addWidget(self.checkbox_ask_replace, row, 0)
        self.l.addWidget(self.label_ask_replace, row, 1)
        row += 1
        
        self.label_disable_first_last_only = QLabel('When multiple EPUB files are selected, allow insertion points other than "1", "first", and "last"')
        self.checkbox_disable_first_last_only = QCheckBox('', self)
        self.checkbox_disable_first_last_only.setChecked(prefs['checkbox_disable_first_last_only'] == 'True')
        self.l.addWidget(self.checkbox_disable_first_last_only, row, 0)
        self.l.addWidget(self.label_disable_first_last_only, row, 1)
        row += 1
        
        self.l.addWidget(QLabel(''), row, 1)
        row += 1
        
        self.label_replace_strings = QLabel('Replace strings:')
        self.replace_strings = QTextEdit(self)
        self.replace_strings.setText(prefs['replace_strings'])
        self.label_supportedMetadata = QLabel('Supported metadata:')
        self.supportedMetadata = QListWidget(self)
        #QtCore.QObject.connect(self.supportedMetadata, QtCore.SIGNAL("doubleClicked()"), self.add_replace_string)
        self.supportedMetadata.doubleClicked.connect(self.add_replace_string)
        
        producer = exlibris()
        tags = producer.getSupportedMetadataList()
        for tag in tags:
            self.supportedMetadata.addItem(tag.decode('utf-8'))
        
        self.l.addWidget(self.label_replace_strings, row, 1)
        self.l.addWidget(self.label_supportedMetadata, row, 2)
        row += 1
        self.l.addWidget(self.replace_strings, row, 1)
        self.l.addWidget(self.supportedMetadata, row, 2)
        row += 1
                
        self.resize(self.sizeHint())


    def add_replace_string(self):
        currentText = str(self.replace_strings.toPlainText()).strip()
        currentItem = self.supportedMetadata.currentItem().text()
        self.replace_strings.setText("%s\n%s=your_value_goes_here;" % (currentText, currentItem))


    def button_xhtml_filename_handler(self):
        initial_dir = os.path.dirname(str(self.xhtml_filename.text()))
        new_file = QFileDialog.getOpenFileName(self, "Select ex libris XHTML file", initial_dir, "XHTML Files (*.xhtml)")
        if new_file:
            new_file = new_file[0] if isinstance(new_file, tuple) else new_file
            if new_file and os.path.exists(new_file):
                self.xhtml_filename.setText(new_file)

    def button_include_dir_handler(self):
        initial_dir = os.path.dirname(str(self.include_dir.text()))
        dirDialog = QFileDialog()
        dirDialog.setFileMode(QFileDialog.Directory)
        new_dir = dirDialog.getExistingDirectory(self, "Select directory", initial_dir)
        if (len(new_dir) > 0):
            self.include_dir.setText(new_dir)

    def save_settings(self):
        prefs['xhtml_filename'] = unicode(self.xhtml_filename.text())
        prefs['include_dir'] = unicode(self.include_dir.text())
        prefs['include_guide_text'] = unicode(self.include_guide_text.text())
        prefs['include_toc_text'] = unicode(self.include_toc_text.text())
        prefs['replace_strings'] = unicode(self.replace_strings.toPlainText())
        prefs['checkbox_include_dir'] = unicode(self.checkbox_include_dir.isChecked())
        prefs['checkbox_include_guide_text'] = unicode(self.checkbox_include_guide_text.isChecked())
        prefs['checkbox_include_toc_text'] = unicode(self.checkbox_include_toc_text.isChecked())
        prefs['checkbox_ask_replace'] = unicode(self.checkbox_ask_replace.isChecked())
        prefs['checkbox_disable_first_last_only'] = unicode(self.checkbox_disable_first_last_only.isChecked())
        # TODO: save value from main.py (?)
        prefs['include_spine'] = u'1'
        prefs['include_toc'] = u'1'
