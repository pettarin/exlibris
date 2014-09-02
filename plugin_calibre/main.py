#!/usr/bin/env python
#from __future__ import (unicode_literals, division, absolute_import, print_function)

__license__     = 'GPLv3'
__author__      = 'Alberto Pettarin (alberto AT albertopettarin DOT it)'
__copyright__   = '2012-2014 Alberto Pettarin (alberto AT albertopettarin DOT it)'
__version__     = 'v1.0.19'
__date__        = '2014-09-02'
__description__ = 'exlibris - add a nice ex libris to your EPUB eBook'
__docformat__   = 'restructuredtext en'

try:
    from PyQt5.Qt import QDialog, QGridLayout, QPushButton, QMessageBox, QLabel, QListWidget, QTextEdit, QLineEdit
except ImportError as e:
    from PyQt4.Qt import QDialog, QGridLayout, QPushButton, QMessageBox, QLabel, QListWidget, QTextEdit, QLineEdit
#    import PyQt4.Qt as QtCore

import types
import datetime

from calibre.gui2 import error_dialog, question_dialog
from calibre.ptempfile import PersistentTemporaryFile, PersistentTemporaryDirectory

from exlibris import exlibris

from calibre_plugins.exlibris_plugin.config import prefs

class MainDialog(QDialog):

    def __init__(self, gui, icon, do_user_config):
        QDialog.__init__(self, gui)
        self.gui = gui
        self.do_user_config = do_user_config
        self.db = gui.current_db

        row = 0
        self.l = QGridLayout()
        self.setLayout(self.l)
        self.setWindowTitle('exlibris')
        self.setWindowIcon(icon)
        
        # This label will contain the 'title'
        self.label_selected_files = QLabel('')
        self.l.addWidget(self.label_selected_files, row, 0, 1, 6)
        row += 1
        
        # Separator
        self.l.addWidget(QLabel(''), row, 1)
        row += 1
        
        self.selectedEPUBFiles = []
        
        #print(prefs)
        
        rows = self.gui.library_view.selectionModel().selectedRows()
        ids = list(map(self.gui.library_view.model().id, rows))
        for book_id in ids:
            # Get the current book_id from the db
            fmts = self.db.formats(book_id, index_is_id=True)
            if ('EPUB' in fmts) or ('epub' in fmts):
                self.selectedEPUBFiles += [ book_id ]
                
        if (len(self.selectedEPUBFiles) < 1):
            # No valid EPUB selected
            error_dialog(self.gui, 'Cannot apply ex libris', 'You must select at least an eBook in EPUB format.', show_copy_button=False, show=True)
            self.close()
            return

        if (len(self.selectedEPUBFiles) == 1):
            # Only one EPUB file selected
            book_id = self.selectedEPUBFiles[0]
            mi = self.db.get_metadata(book_id, index_is_id=True)
            self.label_selected_files.setText('Selected EPUB file: "%s"' % mi.title)
            self.spine = QListWidget(self)
            ffile = self.db.format(book_id, 'epub', index_is_id=True, as_path=True)
            self.populateSpineList(ffile)
            self.spine.currentRowChanged.connect(self.updateSpine)
            self.toc = QListWidget(self)
            self.populateTOCList(ffile)
            self.toc.currentRowChanged.connect(self.updateTOC)
            self.l.addWidget(self.spine, row, 0, 1, 3)
            self.l.addWidget(self.toc, row, 3, 1, 3)
            row += 1
        else:
            # Multiple EPUB files selected
            self.label_selected_files.setText('Multiple EPUB files selected')
		
        # Set up the GUI
        self.label_include_spine = QLabel('Include in spine at index:')
        self.l.addWidget(self.label_include_spine, row, 0, 1, 3)        
        self.label_include_toc = QLabel('Include in TOC at index:')
        self.l.addWidget(self.label_include_toc, row, 3, 1, 3)
        row += 1
        
        self.include_spine = QLineEdit(self)
        self.include_spine.setText(prefs['include_spine'])
        self.l.addWidget(self.include_spine, row, 0)
        
        self.button_include_spine_first = QPushButton('first', self)
        self.button_include_spine_first.clicked.connect(self.include_spine_first)
        self.l.addWidget(self.button_include_spine_first, row, 1)
        
        self.button_include_spine_last = QPushButton('last', self)
        self.button_include_spine_last.clicked.connect(self.include_spine_last)
        self.l.addWidget(self.button_include_spine_last, row, 2)
        
        self.include_toc = QLineEdit(self)
        self.include_toc.setText(prefs['include_toc'])
        self.l.addWidget(self.include_toc, row, 3)
        
        self.button_include_toc_first = QPushButton('first', self)
        self.button_include_toc_first.clicked.connect(self.include_toc_first)
        self.l.addWidget(self.button_include_toc_first, row, 4)
        
        self.button_include_toc_last = QPushButton('last', self)
        self.button_include_toc_last.clicked.connect(self.include_toc_last)
        self.l.addWidget(self.button_include_toc_last, row, 5)
        row += 1
        
        self.l.addWidget(QLabel(''), row, 1)
        row += 1
                
        self.button_apply_replace = QPushButton('Add ex libris and replace', self)
        self.button_apply_replace.clicked.connect(self.apply_replace)
        self.l.addWidget(self.button_apply_replace, row, 0, 1, 3)
        
        self.button_apply_copy = QPushButton('Add ex libris and copy', self)
        self.button_apply_copy.clicked.connect(self.apply_copy)
        self.l.addWidget(self.button_apply_copy, row, 3, 1, 3)
        row += 1
        
        
        
        
        self.l.addWidget(QLabel(''), row, 1)
        row += 1
                
        self.button_remove_replace = QPushButton('Remove ex libris and replace', self)
        self.button_remove_replace.clicked.connect(self.remove_replace)
        self.l.addWidget(self.button_remove_replace, row, 0, 1, 3)
        
        self.button_remove_copy = QPushButton('Remove ex libris and copy', self)
        self.button_remove_copy.clicked.connect(self.remove_copy)
        self.l.addWidget(self.button_remove_copy, row, 3, 1, 3)
        row += 1
        
        
        
        
        self.l.addWidget(QLabel(''), row, 1)
        row += 1
        
        self.button_config = QPushButton('Configure', self)
        self.button_config.clicked.connect(self.config)
        self.l.addWidget(self.button_config, row, 0, 1, 2)
        
        self.button_help = QPushButton('Help', self)
        self.button_help.clicked.connect(self.help)
        self.l.addWidget(self.button_help, row, 2, 1, 1)
        
        self.button_about = QPushButton('About', self)
        self.button_about.clicked.connect(self.about)
        self.l.addWidget(self.button_about, row, 3, 1, 1)
 
        self.button_close = QPushButton('Close', self)
        self.button_close.clicked.connect(self.close)
        self.l.addWidget(self.button_close, row, 4, 1, 2)
        row += 1
		

        self.include_spine.setText(prefs['include_spine'])
        self.include_toc.setText(prefs['include_toc'])
        
        self.resize(self.sizeHint())
        self.show()


    def updateSpine(self, newRow):
		self.include_spine.setText(str(newRow + 1))


    def updateTOC(self, newRow):
		self.include_toc.setText(str(newRow + 1))


    def about(self):
        text = get_resources('about.txt')
        QMessageBox.about(self, 'About exlibris', text.decode('utf-8'))

    def help(self):
        text = get_resources('help.txt')
        QMessageBox.about(self, 'Help exlibris', text.decode('utf-8'))

    def include_spine_first(self):
        self.include_spine.setText('first')


    def include_spine_last(self):
        self.include_spine.setText('last')


    def include_toc_first(self):
        self.include_toc.setText('first')


    def include_toc_last(self):
        self.include_toc.setText('last')
        

    def config(self):
        self.do_user_config(parent=self)

    def metadatumToStr(self, metadatum, floatToInt=False):
        toReturn = ""
        if (isinstance(metadatum, types.StringTypes)):
            return str(metadatum)
        if (isinstance(metadatum, types.IntType) or isinstance(metadatum, types.LongType)):
            return str(metadatum)
        if (isinstance(metadatum, types.FloatType)):
            if (floatToInt):
                return str(int(metadatum))
            else:
                return str(metadatum)
        if (isinstance(metadatum, types.ListType)):
            if (len(metadatum) == 1):
                return str(metadatum[0])
            for x in metadatum:
                toReturn += str(x) + ", "
            return toReturn
        if (isinstance(metadatum, types.TupleType)):
            for x in metadatum:
                toReturn += str(x) + ", "
            return toReturn
        if (isinstance(metadatum, types.DictType)):
            if (len(metadatum.keys()) == 1):
                key = metadatum.keys()[0]
                return str(key) + ":" + str(metadatum[key])
            for key in metadatum.keys():
                toReturn += str(key) + ":" + str(metadatum[key]) + ", "
            return toReturn
        if (isinstance(metadatum, datetime.datetime)):
            return str(metadatum)
        return toReturn
        
    def apply_replace(self):
        self.applyExlibris(True, False)


    def apply_copy(self):
        self.applyExlibris(False, False)
        
    def remove_replace(self):
        self.applyExlibris(True, True)

    def remove_copy(self):
        self.applyExlibris(False, True)

        
    def applyExlibris(self, replace, remove):
        if (len(self.selectedEPUBFiles) == 1):
            admissible_spine_values = map(lambda x: str(x), range(1, self.spine_max_index + 1)) + ['first', 'last']
            admissible_toc_values = map(lambda x: str(x), range(1, self.toc_max_index + 1)) + ['first', 'last']
        else:
            admissible_spine_values = ['first', 'last', '1']
            admissible_toc_values = ['first', 'last', '1']
        insertion_point_spine = str(self.include_spine.text()).strip().lower()
        insertion_point_toc = str(self.include_toc.text()).strip().lower()
        counter = 0
        total = len(self.selectedEPUBFiles)
        
        # Check if the provided insertion points are valid
        if (total == 1):
            if (not ((insertion_point_spine in admissible_spine_values) and (insertion_point_toc in admissible_toc_values))):
                error_dialog(self.gui, 'Cannot apply ex libris', 'The specified insertion point(s) are invalid.', show_copy_button=False, show=True)
                return
        else:
            if ((prefs['checkbox_disable_first_last_only'] == 'False') and not ((insertion_point_spine in admissible_spine_values) and (insertion_point_toc in admissible_toc_values))):
                error_dialog(self.gui, 'Cannot apply ex libris', 'The specified insertion point(s) are invalid.', show_copy_button=False, show=True)
                return
        
        # Ask confirmation before replacing books in library    
        if ((replace) and (prefs['checkbox_ask_replace'] == 'True')):
            proceed = question_dialog(self.gui, 'Are you sure?', 'Do you really want to replace the selected eBook(s) with the new one(s) containing your ex libris?', show_copy_button=False, default_yes=False)
            if (not proceed):
                self.gui.status_bar.show_message("Aborted", 60000)
                return
        
        # Add ex libris to the selected EPUB files
        for book_id in self.selectedEPUBFiles:
            inputEPUB = self.db.format(book_id, 'epub', index_is_id=True, as_path=True)
            tmpEPUB = PersistentTemporaryDirectory() + '/tmp.epub'
            outputEPUB = PersistentTemporaryDirectory() + '/tmp2.epub'
            
            inputXHTML = prefs['xhtml_filename']
            insertionPointSpine = insertion_point_spine
            insertionPointTOC = insertion_point_toc
            inputDirectory = None
            if (prefs['checkbox_include_dir']):
                inputDirectory = prefs['include_dir']
            workingDirectory = PersistentTemporaryDirectory()
            userReplacementStrings = self.parseUserReplacementStrings(prefs['replace_strings'].strip().replace('\n',';'))
            # Add calibre- prefixed metadata from Calibre
            mi = self.db.get_metadata(book_id, index_is_id=True)
            
            if (mi.title != None):
                userReplacementStrings['calibre-title'] = self.metadatumToStr(mi.title)
                
            if (mi.authors != None):
                userReplacementStrings['calibre-author'] = self.metadatumToStr(mi.authors)
                userReplacementStrings['calibre-authors'] = self.metadatumToStr(mi.authors)
                
            if (mi.timestamp != None):
                userReplacementStrings['calibre-date'] = self.metadatumToStr(mi.timestamp)
                userReplacementStrings['calibre-timestamp'] = self.metadatumToStr(mi.timestamp)
                
            if (mi.size != None):
                userReplacementStrings['calibre-size'] = self.metadatumToStr(mi.size)
            if (mi.rating != None):
                userReplacementStrings['calibre-rating'] = self.metadatumToStr(mi.rating)
            if (mi.tags != None):
                userReplacementStrings['calibre-tags'] = self.metadatumToStr(mi.tags)
            if (mi.series != None):
                userReplacementStrings['calibre-series'] = self.metadatumToStr(mi.series)
                userReplacementStrings['calibre-series-index'] = self.metadatumToStr(mi.series_index, True)
            else:
                userReplacementStrings['calibre-series'] = self.metadatumToStr("")
                userReplacementStrings['calibre-series-index'] = self.metadatumToStr("")
            if (mi.publisher != None):
                userReplacementStrings['calibre-publisher'] = self.metadatumToStr(mi.publisher)
            if (mi.pubdate != None):
                userReplacementStrings['calibre-published'] = self.metadatumToStr(mi.pubdate)
            if (mi.pubdate != None):
                userReplacementStrings['calibre-pubdate'] = self.metadatumToStr(mi.pubdate)
            if (mi.languages != None):
                userReplacementStrings['calibre-languages'] = self.metadatumToStr(mi.languages)
            if (mi.identifiers != None):
                userReplacementStrings['calibre-identifiers'] = self.metadatumToStr(mi.identifiers)
            if (mi.comments != None):
                userReplacementStrings['calibre-comments'] = self.metadatumToStr(mi.comments)
            if (mi.rights != None):
                userReplacementStrings['calibre-rights'] = self.metadatumToStr(mi.rights)

            exlibrisGuideString = ''
            if (prefs['checkbox_include_guide_text']):
                exlibrisGuideString = prefs['include_guide_text']
            exlibrisTOCString = ''
            if (prefs['checkbox_include_toc_text']):
                exlibrisTOCString = prefs['include_toc_text']
            includeInGuide = prefs['checkbox_include_guide_text']
            
            #print(inputEPUB)
            #print(outputEPUB)
            #print(inputXHTML)
            #print(insertionPointSpine)
            #print(insertionPointTOC)
            #print(inputDirectory)
            #print(workingDirectory)
            #print(userReplacementStrings)
            #print(exlibrisGuideString)
            #print(exlibrisTOCString)
            #print(includeInGuide)
            
            try:
                counter += 1
                self.gui.status_bar.show_message("Adding ex libris to book %s/%s" % (counter, total), 60000)
                
                producer = exlibris(calibre=True)
                producer.initialize(inputEPUB, tmpEPUB, inputXHTML, insertionPointSpine, insertionPointTOC, inputDirectory, workingDirectory, userReplacementStrings, exlibrisGuideString, exlibrisTOCString, includeInGuide)
                producer.removeExLibris()
                producer.createNewEPUB()
                producer.clean()
                
                if (not remove):
                    producer = exlibris(calibre=True)
                    producer.initialize(tmpEPUB, outputEPUB, inputXHTML, insertionPointSpine, insertionPointTOC, inputDirectory, workingDirectory, userReplacementStrings, exlibrisGuideString, exlibrisTOCString, includeInGuide)
                    producer.insertExLibris()
                    producer.createNewEPUB()
                    producer.clean()
                else:
                    outputEPUB = tmpEPUB
                
                if (replace):
                    # Replace the original EPUB file with the new one with the ex libris
                    self.db.add_format_with_hooks(book_id, 'EPUB', outputEPUB, index_is_id=True)
                else:
                    # Keep the original EPUB file and create a new one with the ex libris
                    mi = self.db.get_metadata(book_id, index_is_id=True)
                    new_book_id = self.db.create_book_entry(mi, add_duplicates=True)
                    self.db.add_format_with_hooks(new_book_id, 'EPUB', outputEPUB, index_is_id=True)
                    cover = self.db.cover(book_id, index_is_id=True)
                    self.db.set_cover(new_book_id, cover)
                
                # TODO  aggiungere qui un test sul remove/add
                self.gui.status_bar.show_message("Done adding ex libris to book %s/%s." % (counter, total), 60000)
                
            except Exception as msg:
                print(str(msg.args[0]))
                self.gui.status_bar.show_message(str(msg.args[0]))
                
            self.gui.library_view.model().refresh()
            self.close()



    def parseUserReplacementStrings(self, string):
        toReturn = dict()
        pairs = string.split(';')
        for pair in pairs:
            sep = pair.split('=')
            if (len(sep) == 2):
                key = sep[0].strip()
                value = sep[1]
                toReturn[key] = value
        return toReturn


    def populateSpineList(self, fileName):
        try:
            # create exlibris instance
            inputEPUB = fileName
            workingDirectory = PersistentTemporaryDirectory()
            
            producer = exlibris(calibre=True)
            producer.initialize(inputEPUB, inputEPUB, inputEPUB, '1', '1', None, workingDirectory, None, None, None, None)
            
            # get spine list
            spineList = producer.getSpineList()
            pageDictionary = producer.getPageDictionary()
            
            # add spine list to listbox
            maxIndex = int(spineList[-1][0])
            nod = len(str(maxIndex))
            maxLen = 0
            for l in spineList:
                maxLen = max(maxLen, len(l[1]))

            for l in spineList:
                index = str(l[0]).zfill(nod)
                idref = l[1]
                pageFileName = pageDictionary.get(idref, 'UNKNOWN')
                string = "%s  %s (%s)" % (index, idref, pageFileName)
                self.spine.addItem(string.decode('utf-8'))
            self.spine.addItem("=== Insert as last element ===")

            # remove tmp dir
            producer.clean()
            
            # update self.spine_max_index
            self.spine_max_index = len(spineList) + 1

        except Exception as msg:
            self.gui.status_bar.show_message(str(msg.args[0]))


    def populateTOCList(self, fileName):
        try:
            # create exlibris instance
            inputEPUB = fileName
            workingDirectory = PersistentTemporaryDirectory()
            producer = exlibris(calibre=True)
            producer.initialize(inputEPUB, inputEPUB, inputEPUB, '1', '1', None, workingDirectory, None, None, None, None)
            
            # get spine list
            tocList = producer.getTOCList()
            pageDictionary = producer.getPageDictionary()
            
            # add TOC list to listbox
            maxIndex = int(tocList[-1][0])
            nod = len(str(maxIndex))
            maxLen = 0
            for l in tocList:
                maxLen = max(maxLen, len(l[1]))

            for l in tocList:
                index = str(l[0]).zfill(nod)
                text = l[1]
                spaces = " " + ("-" * (l[2] * 3)) + " "
                string = "%s%s%s" % (index, spaces, text.ljust(maxLen))
                self.toc.addItem(string.decode('utf-8'))
            self.toc.addItem("=== Insert as last element ===")

            # remove tmp dir
            producer.clean()
            
            # update self.toc_max_index
            self.toc_max_index = len(tocList) + 1

        except Exception as msg:
            self.gui.status_bar.show_message(str(msg.args[0]))
