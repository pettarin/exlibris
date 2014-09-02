#!/usr/bin/env python
# -*- coding: utf-8 -*-

__license__     = 'GPLv3'
__author__      = 'Alberto Pettarin (alberto AT albertopettarin DOT it)'
__copyright__   = '2012-2014 Alberto Pettarin (alberto AT albertopettarin DOT it)'
__version__     = 'v1.0.19'
__date__        = '2014-09-02'
__description__ = 'exlibris-gui - GUI frontend to exlibris'


from Tkinter import *
import tkMessageBox, tkFileDialog

import os
from exlibris import exlibris



### STATUS BAR ###
class StatusBar(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.label = Label(self, bd=1, relief=SUNKEN, anchor=W)
        self.label.pack(fill=X)

    def setText(self, args):
        self.label.config(text=args)
        self.label.update_idletasks()

    def clearText(self):
        self.label.config(text="")
        self.label.update_idletasks()
### STATUS BAR ###


### APPLICATION CLASS ###
class Application():


    def setLanguage(self, language):
        language = language.lower()
        
        if (language == 'en'):
            self.labelMenuExit = 'Exit'
            self.labelMenuAbout = 'About'
            self.labelButtonExit = 'Exit'
            self.labelButtonAbout = 'About'
            self.labelAboutDialogTitle = 'exlibris'
            self.labelAboutDialogMessage = "exlibris-gui (v1.0.19)\nCopyright (c) 2012-2014 Alberto Pettarin.\nLicense GNU GPL version 3 <http://gnu.org/licenses/gpl.html>.\nThis is free software: you are free to change and redistribute it.\nThere is NO WARRANTY, to the extent permitted by law."
            self.labelLblOriginalEPUB = 'Original EPUB filename:'
            self.labelLblNewEPUB = 'New EPUB filename:'
            self.labelLblExLibris = 'Ex Libris XHTML filename:'
            self.labelLblDirectory = 'Ex Libris additional files directory:'
            self.labelButtonOriginalEPUB = '...'
            self.labelButtonNewEPUB = '...'
            self.labelButtonExLibris = '...'
            self.labelButtonDirectory = '...'
            self.labelCheckbuttonIncludeDirectory = 'Include additional files from directory:'
            self.labelButtonAddExLibris = 'Add ex libris'
            self.labelButtonRemoveExLibris = 'Remove ex libris'
            self.labelFileDialogEPUBFilter = 'IDPF EPUB eBook'
            self.labelFileDialogOpenOriginalEPUB = 'Please select your original EPUB eBook'
            self.labelFileDialogSaveNewEPUB = 'Please select the filename of your new EPUB eBook'
            self.labelFileDialogExLibrisFilter = 'XHTML page'
            self.labelFileDialogOpenExLibris = 'Please select your XHTML ex libris'
            self.labelFileDialogOpenOriginalDir = 'Please select the directory of your ex libris resources'
            self.labelLblSpine = 'Include in the spine at index:'
            self.labelIndexSpine = '1'
            self.labelLblTOC = 'Include in the TOC at index:'
            self.labelIndexTOC = '1'
            self.labelAddAsLast = 'ADD AS LAST ELEMENT'
            self.labelCheckbuttonKeepTMP = 'Keep TMP dir'
            self.labelCheckbuttonIncludeGuide = 'Include in guide with string: '
            self.labelStringGuide = 'EX LIBRIS'
            self.labelCheckbuttonIncludeTOC = 'Include in TOC with string: '
            self.labelStringTOC = 'EX LIBRIS'
            self.labelReplacementStrings = 'key1=value1;\nkey2=value3;\nkey3=value3;'
            self.labelLblReplacementStrings = 'Replace\nStrings: '
            self.labelStatusbarReady = 'Ready'
            self.labelStatusbarReadingSpine = 'Reading spine from '
            self.labelStatusbarReadingTOC = 'Reading TOC from '
            self.labelStatusbarMessageInsertingDone = 'Congratulations! Your eBook has a nice ex libris now.'
            self.labelStatusbarInsertingExLibris = 'Inserting the ex libris...'
            self.labelStatusbarMessageRemovingDone = 'The ex libris has been removed from your eBook.'
            self.labelStatusbarRemovingExLibris = 'Removing the ex libris...'
            self.labelMasterTitle = 'exlibris-gui v1.0.19'

        if (language == 'it'):
            self.labelMenuExit = 'Esci'
            self.labelMenuAbout = '?'
            self.labelButtonExit = 'Esci'
            self.labelButtonAbout = '?'
            self.labelAboutDialogTitle = 'exlibris'
            self.labelAboutDialogMessage = "exlibris-gui (v1.0.19)\nCopyright (c) 2012-2014 Alberto Pettarin.\nLicenza GNU GPL version 3 <http://gnu.org/licenses/gpl.html>.\nQuesto e' software libero: sei libero di modificarlo e redistribuirlo.\nL'autore declina ogni responsabilita'."
            self.labelLblOriginalEPUB = 'File EPUB originale:'
            self.labelLblNewEPUB = 'Nuovo file EPUB:'
            self.labelLblExLibris = 'Pagina XHTML dell\'ex Libris:'
            self.labelLblDirectory = 'Aggiungi ulteriori files dalla directory:'
            self.labelButtonOriginalEPUB = '...'
            self.labelButtonNewEPUB = '...'
            self.labelButtonExLibris = '...'
            self.labelButtonDirectory = '...'
            self.labelCheckbuttonIncludeDirectory = 'Includi ulteriori files dalla directory:'
            self.labelButtonAddExLibris = 'Inserisci ex libris'
            self.labelButtonRemoveExLibris = 'Rimuovi ex libris'
            self.labelFileDialogEPUBFilter = 'IDPF EPUB eBook'
            self.labelFileDialogOpenOriginalEPUB = 'Seleziona il file EPUB originale'
            self.labelFileDialogSaveNewEPUB = 'Seleziona il nome del nuovo file EPUB'
            self.labelFileDialogExLibrisFilter = 'Pagina XHTML'
            self.labelFileDialogOpenExLibris = 'Seleziona la pagina XHTML dell\'ex libris'
            self.labelFileDialogOpenOriginalDir = 'Seleziona la directory contenente le risorse per l\'ex libris'
            self.labelLblSpine = 'Includi nella spine come numero:'
            self.labelIndexSpine = '1'
            self.labelLblTOC = 'Includi nella TOC come numero:'
            self.labelIndexTOC = '1'
            self.labelAddAsLast = 'AGGIUNGI COME ULTIMO'
            self.labelCheckbuttonKeepTMP = 'Non cancellare la directory TMP'
            self.labelCheckbuttonIncludeGuide = 'Includi nella guide come:'
            self.labelStringGuide = 'EX LIBRIS'
            self.labelCheckbuttonIncludeTOC = 'Includi nella TOC come:'
            self.labelStringTOC = 'EX LIBRIS'
            self.labelReplacementStrings = 'chiave1=valore1;\nchiave2=valore3;\nchiave3=valore3;'
            self.labelLblReplacementStrings = 'Sostituisci\nStringhe: '
            self.labelStatusbarReady = 'Pronto'
            self.labelStatusbarReadingSpine = 'Leggendo la spine da '
            self.labelStatusbarReadingTOC = 'Leggendo la TOC da '
            self.labelStatusbarMessageInsertingDone = 'Congratulazioni! Il tuo eBook ora ha un simpatico ex libris.'
            self.labelStatusbarInsertingExLibris = 'Inserendo l\'ex libris...'
            self.labelStatusbarMessageRemovingDone = 'L\'ex libris e\' stato rimosso correttamente dal tuo eBook.'
            self.labelStatusbarRemovingExLibris = 'Rimuovendo l\'ex libris...'
            self.labelMasterTitle = 'exlibris-gui v1.0.19'




    def about(self):
        tkMessageBox.showinfo(self.labelAboutDialogTitle, self.labelAboutDialogMessage)

    def selectOriginalEPUB(self):
        fileName = tkFileDialog.askopenfilename(parent=self.master, filetypes=[(self.labelFileDialogEPUBFilter, "*.epub")], initialdir="./", title=self.labelFileDialogOpenOriginalEPUB)
        if (len(fileName) > 0):
            self.txtOriginalEPUB.config(state=NORMAL)
            self.txtOriginalEPUB.delete(1.0, END)
            self.txtOriginalEPUB.insert(END, fileName)
            self.txtOriginalEPUB.config(state=DISABLED)
            
            self.txtNewEPUB.delete(1.0, END)
            self.txtNewEPUB.insert(END, self.generateNewName(fileName))

            self.statusbar.setText(self.labelStatusbarReadingSpine + fileName)
            self.populateSpineList(fileName)
            self.statusbar.setText(self.labelStatusbarReadingTOC + fileName)
            self.populateTOCList(fileName)
            self.statusbar.setText(self.labelStatusbarReady)


    def selectNewEPUB(self):
        fileName = tkFileDialog.asksaveasfilename(parent=self.master, filetypes=[(self.labelFileDialogEPUBFilter, "*.epub")], initialdir="./", title=self.labelFileDialogSaveNewEPUB)
        if (fileName != None):
            self.txtNewEPUB.delete(1.0, END)
            self.txtNewEPUB.insert(END, fileName)

    def selectExLibris(self):
        fileName = tkFileDialog.askopenfilename(parent=self.master, filetypes=[(self.labelFileDialogExLibrisFilter, "*.xhtml")], initialdir="./", title=self.labelFileDialogOpenExLibris)
        if (fileName != None):
            self.txtExLibris.config(state=NORMAL)
            self.txtExLibris.delete(1.0, END)
            self.txtExLibris.insert(END, fileName)
            self.txtExLibris.config(state=DISABLED)
    
    def selectDirectory(self):
        directoryName = tkFileDialog.askdirectory(parent=self.master, initialdir="./", title=self.labelFileDialogOpenOriginalDir)
        if (directoryName != None):
            self.txtDirectory.config(state=NORMAL)
            self.txtDirectory.delete(1.0, END)
            self.txtDirectory.insert(END, directoryName)
            self.txtDirectory.config(state=DISABLED)

    def changeStateIncludeDirectory(self):
        if (self.includeDirectory.get() == 0):
            self.buttonDirectory.configure(state=DISABLED)
        else:
            self.buttonDirectory.configure(state=NORMAL)

    def updateListSpine(self, event):
        item = int(self.listSpine.curselection()[0]) + 1
        self.txtIndexSpine.delete(1.0, END)
        self.txtIndexSpine.insert(END, str(item))

    def updateListTOC(self, event):
        item = int(self.listTOC.curselection()[0]) + 1
        self.txtIndexTOC.delete(1.0, END)
        self.txtIndexTOC.insert(END, str(item))

    def createWidgets(self):
        self.menubar = Menu(self.master)
        self.menubar.add_command(label=self.labelMenuExit, command=self.master.quit)
        self.menubar.add_command(label=self.labelMenuAbout, command=self.about)
        self.master.config(menu=self.menubar)

        self.lblOriginalEPUB = Label(self.master)
        self.lblOriginalEPUB.configure(text=self.labelLblOriginalEPUB)
        self.lblOriginalEPUB.configure(justify=LEFT)
        self.lblOriginalEPUB.grid(row=0, column=0, sticky=W, padx=5, pady=5)

        self.txtOriginalEPUB = Text(self.master)
        self.txtOriginalEPUB.configure(height=1, width=50, state=DISABLED)
        self.txtOriginalEPUB.grid(row=0, column=1, columnspan=2, sticky=W+E, padx=5, pady=5)

        self.buttonOriginalEPUB = Button(self.master)
        self.buttonOriginalEPUB.configure(command=self.selectOriginalEPUB)
        self.buttonOriginalEPUB.configure(text=self.labelButtonOriginalEPUB)
        self.buttonOriginalEPUB.grid(row=0, column=3, sticky=W, padx=5, pady=5)


        self.lblNewEPUB = Label(self.master)
        self.lblNewEPUB.configure(text=self.labelLblNewEPUB)
        self.lblNewEPUB.configure(justify=LEFT)
        self.lblNewEPUB.grid(row=1, column=0, sticky=W, padx=5, pady=5)

        self.txtNewEPUB = Text(self.master)
        self.txtNewEPUB.configure(height=1, width=50)
        self.txtNewEPUB.grid(row=1, column=1, columnspan=2, sticky=W+E, padx=5, pady=5)

        self.buttonNewEPUB = Button(self.master)
        self.buttonNewEPUB.configure(command=self.selectNewEPUB)
        self.buttonNewEPUB.configure(text=self.labelButtonNewEPUB)
        self.buttonNewEPUB.grid(row=1, column=3, sticky=W, padx=5, pady=5)

        self.lblExLibris = Label(self.master)
        self.lblExLibris.configure(text=self.labelLblExLibris)
        self.lblExLibris.configure(justify=LEFT)
        self.lblExLibris.grid(row=2, column=0, sticky=W, padx=5, pady=5)

        self.txtExLibris = Text(self.master)
        self.txtExLibris.configure(height=1, width=50, state=DISABLED)
        self.txtExLibris.grid(row=2, column=1, columnspan=2, sticky=W+E, padx=5, pady=5)

        self.buttonExLibris = Button(self.master)
        self.buttonExLibris.configure(command=self.selectExLibris)
        self.buttonExLibris.configure(text=self.labelButtonExLibris)
        self.buttonExLibris.grid(row=2, column=3, sticky=W, padx=5, pady=5)


        self.includeDirectory = IntVar()
        self.chkIncludeDirectory = Checkbutton(self.master)
        self.chkIncludeDirectory.configure(text=self.labelCheckbuttonIncludeDirectory)
        self.chkIncludeDirectory.configure(variable=self.includeDirectory)
        self.chkIncludeDirectory.configure(command=self.changeStateIncludeDirectory)
        self.chkIncludeDirectory.grid(row=3, column=0, sticky=W, padx=5, pady=5)

        self.txtDirectory = Text(self.master)
        self.txtDirectory.configure(height=1, width=50, state=DISABLED)
        self.txtDirectory.grid(row=3, column=1, columnspan=2, sticky=W+E, padx=5, pady=5)

        self.buttonDirectory = Button(self.master)
        self.buttonDirectory.configure(command=self.selectDirectory)
        self.buttonDirectory.configure(text=self.labelButtonDirectory, state=DISABLED)
        self.buttonDirectory.grid(row=3, column=3, sticky=W, padx=5, pady=5)

        self.keepTMP = IntVar()
        self.chkKeepTMP = Checkbutton(self.master)
        self.chkKeepTMP.configure(text=self.labelCheckbuttonKeepTMP)
        self.chkKeepTMP.configure(variable=self.keepTMP)
        self.chkKeepTMP.grid(row=4, column=0, sticky=W, padx=5, pady=5)

        self.includeGuide = IntVar()
        self.chkIncludeGuide = Checkbutton(self.master)
        self.chkIncludeGuide.configure(text=self.labelCheckbuttonIncludeGuide)
        self.chkIncludeGuide.configure(variable=self.includeGuide)
        self.chkIncludeGuide.grid(row=5, column=0, sticky=W, padx=5, pady=5)
        self.chkIncludeGuide.select()
        self.txtStringGuide = Text(self.master)
        self.txtStringGuide.configure(height=1, width=15)
        self.txtStringGuide.delete(1.0, END)
        self.txtStringGuide.insert(END, self.labelStringGuide)
        self.txtStringGuide.grid(row=5, column=1, sticky=W, padx=5, pady=5)

        self.includeTOC = IntVar()
        self.chkIncludeTOC = Checkbutton(self.master)
        self.chkIncludeTOC.configure(text=self.labelCheckbuttonIncludeTOC)
        self.chkIncludeTOC.configure(variable=self.includeTOC)
        self.chkIncludeTOC.grid(row=5, column=2, sticky=W, padx=5, pady=5)
        self.chkIncludeTOC.select()
        self.chkIncludeTOC.configure(state=DISABLED)
        self.txtStringTOC = Text(self.master)
        self.txtStringTOC.configure(height=1, width=15)
        self.txtStringTOC.delete(1.0, END)
        self.txtStringTOC.insert(END, self.labelStringTOC)
        self.txtStringTOC.grid(row=5, column=3, sticky=W, padx=5, pady=5)

        self.lblSpine = Label(self.master)
        self.lblSpine.configure(text=self.labelLblSpine)
        self.lblSpine.configure(justify=LEFT)
        self.lblSpine.grid(row=6, column=0, sticky=W, padx=5, pady=5)
        self.txtIndexSpine = Text(self.master)
        self.txtIndexSpine.configure(height=1, width=15)
        self.txtIndexSpine.delete(1.0, END)
        self.txtIndexSpine.insert(END, self.labelIndexSpine)
        self.txtIndexSpine.grid(row=6, column=1, sticky=W, padx=5, pady=5)

        self.container9 = Frame(self.master)
        self.container9.grid(row=7, column=0, columnspan=2, sticky=W+E+N+S)
        
        self.listSpine = Listbox(self.container9)
        self.listSpine.configure(width=45, height=18)
        self.scrollbarSpine = Scrollbar(self.container9)
        self.scrollbarSpine.configure(orient=VERTICAL)
        self.scrollbarSpine.config(command=self.listSpine.yview)
        self.scrollbarSpine.grid(row=0, column=1, sticky=W+N+S, pady=5)
        self.listSpine.configure(yscrollcommand=self.scrollbarSpine.set)
        self.listSpine.grid(row=0, column=0, sticky=W+E+N+S, padx=5, pady=5)
        self.listSpine.bind("<Double-Button-1>", self.updateListSpine)
        
        self.container9.grid_rowconfigure(0, weight=1)
        self.container9.grid_columnconfigure(0, weight=1) 
       

        self.lblTOC = Label(self.master)
        self.lblTOC.configure(text=self.labelLblTOC)
        self.lblTOC.configure(justify=LEFT)
        self.lblTOC.grid(row=6, column=2, sticky=W, padx=5, pady=5)
        self.txtIndexTOC = Text(self.master)
        self.txtIndexTOC.configure(height=1, width=15)
        self.txtIndexTOC.delete(1.0, END)
        self.txtIndexTOC.insert(END, self.labelIndexTOC)
        self.txtIndexTOC.grid(row=6, column=3, sticky=W, padx=5, pady=5)

        self.container10 = Frame(self.master)
        self.container10.grid(row=7, column=2, columnspan=2, sticky=W+E+N+S)
        
        self.listTOC = Listbox(self.container10)
        self.listTOC.configure(width=45, height=18)
        self.scrollbarTOC = Scrollbar(self.container10)
        self.scrollbarTOC.configure(orient=VERTICAL)
        self.scrollbarTOC.config(command=self.listTOC.yview)
        self.scrollbarTOC.grid(row=0, column=1, sticky=W+N+S, pady=5)
        self.listTOC.configure(yscrollcommand=self.scrollbarTOC.set)
        self.listTOC.grid(row=0, column=0, sticky=W+E+N+S, padx=5, pady=5)
        self.listTOC.bind("<Double-Button-1>", self.updateListTOC)

        self.container10.grid_rowconfigure(0, weight=1)
        self.container10.grid_columnconfigure(0, weight=1)


        self.container11 = Frame(self.master)
        self.container11.grid(row=8, column=0, columnspan=5, sticky=W+E+N+S)

        self.lblReplacementStrings = Label(self.container11)
        self.lblReplacementStrings.configure(text=self.labelLblReplacementStrings)
        self.lblReplacementStrings.configure(justify=LEFT)
        self.lblReplacementStrings.grid(row=0, column=0, sticky=W, padx=5, pady=5)
        self.txtReplacementStrings = Text(self.container11)
        self.txtReplacementStrings.configure(height=3)
        self.txtReplacementStrings.delete(1.0, END)
        self.txtReplacementStrings.insert(END, self.labelReplacementStrings)
        self.txtReplacementStrings.grid(row=0, column=1, sticky=W+E+N+S, padx=5, pady=5)
        self.scrollbarReplacementStrings = Scrollbar(self.container11)
        self.scrollbarReplacementStrings.configure(orient=VERTICAL)
        self.scrollbarReplacementStrings.config(command=self.txtReplacementStrings.yview)
        self.scrollbarReplacementStrings.grid(row=0, column=2, sticky=W+N+S, pady=5)
        self.txtReplacementStrings.configure(yscrollcommand=self.scrollbarReplacementStrings.set)
        self.buttonAddExLibris = Button(self.container11)
        self.buttonAddExLibris.configure(text=self.labelButtonAddExLibris)
        self.buttonAddExLibris.configure(command=self.addExLibris)
        self.buttonAddExLibris.grid(row=0, column=3, sticky=W+E+N+S, padx=5, pady=5)
        self.buttonRemoveExLibris = Button(self.container11)
        self.buttonRemoveExLibris.configure(text=self.labelButtonRemoveExLibris)
        self.buttonRemoveExLibris.configure(command=self.removeExLibris)
        self.buttonRemoveExLibris.grid(row=0, column=4, sticky=W+E+N+S, padx=5, pady=5)
        
        self.container11.grid_rowconfigure(0, weight=1)
        self.container11.grid_columnconfigure(1, weight=1)


        self.statusbar = StatusBar(self.master)
        self.statusbar.setText(self.labelStatusbarReady)
        self.statusbar.grid(row=10, column=0, columnspan=4, sticky=W+E+S)

        for i in range(11):
            self.master.grid_rowconfigure(i, weight=1)
        
        for j in range(4):
           self.master.grid_columnconfigure(j, weight=1)



    def __init__(self, master=None, language='en-us'):
        self.setLanguage(language)
        
        self.master = master
        self.master.geometry("800x600")
        self.master.title(self.labelMasterTitle)
        self.master.grid()
       
        self.createWidgets()


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
    def addExLibris(self):
        try:
            self.statusbar.setText(self.labelStatusbarInsertingExLibris)
            workingDirectory = 'tmp'
            tmpEPUB = "tmp.epub"

            inputEPUB = self.txtOriginalEPUB.get(1.0, END).strip()
            outputEPUB = self.txtNewEPUB.get(1.0, END).strip()
            inputXHTML = self.txtExLibris.get(1.0, END).strip()
            insertionPointSpine = self.txtIndexSpine.get(1.0, END).strip()
            insertionPointTOC = self.txtIndexTOC.get(1.0, END).strip()
            inputDirectory = self.txtDirectory.get(1.0, END).strip()
            if (len(inputDirectory) < 1):
                inputDirectory = None
            userReplacementStrings = self.parseUserReplacementStrings(self.txtReplacementStrings.get(1.0, END).strip().replace('\n',';'))
            exlibrisGuideString = self.txtStringGuide.get(1.0, END).strip()
            exlibrisTOCString = self.txtStringTOC.get(1.0, END).strip()
            includeInGuide = (self.includeGuide.get() == 1)

            # remove previous ex libris
            producer = exlibris()
            producer.initialize(inputEPUB, tmpEPUB, inputEPUB, '1', '1', None, workingDirectory, None, None, None, None)
            producer.removeExLibris()
            producer.createNewEPUB()
            producer.clean()

            # create exlibris instance
            producer = exlibris()
            producer.initialize(tmpEPUB, outputEPUB, inputXHTML, insertionPointSpine, insertionPointTOC, inputDirectory, workingDirectory, userReplacementStrings, exlibrisGuideString, exlibrisTOCString, includeInGuide)
            
            # actually insert the ex libris 
            producer.insertExLibris()
            
            # output
            producer.createNewEPUB()

            # remove tmp dir
            if (self.keepTMP.get() == 0):
                producer.clean()
            
            # remove tmp EPUB
            os.remove(tmpEPUB)

            # print done message
            self.statusbar.setText(self.labelStatusbarMessageInsertingDone)

        except Exception as msg:
            self.statusbar.setText(msg.args[0])

    def removeExLibris(self):
        try:
            self.statusbar.setText(self.labelStatusbarRemovingExLibris)
            workingDirectory = 'tmp'

            inputEPUB = self.txtOriginalEPUB.get(1.0, END).strip()
            outputEPUB = self.txtNewEPUB.get(1.0, END).strip()

            # create exlibris instance
            producer = exlibris()
            producer.initialize(inputEPUB, outputEPUB, inputEPUB, '1', '1', None, workingDirectory, None, None, None, None)
            
            # actually remove the ex libris 
            producer.removeExLibris()

            # output
            producer.createNewEPUB()

            # remove tmp dir
            if (self.keepTMP.get() == 0):
                producer.clean()

            # print done message
            self.statusbar.setText(self.labelStatusbarMessageRemovingDone)

        except Exception as msg:
            self.statusbar.setText(msg.args[0])
        
    
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
            workingDirectory = 'tmp'
            producer = exlibris()
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

            self.listSpine.delete(0, END)
            for l in spineList:
                index = str(l[0]).zfill(nod)
                idref = l[1]
                pageFileName = pageDictionary.get(idref, 'UNKNOWN')
                #string = "%s  %s  %s" % (index, idref.ljust(maxLen), pageFileName)
                string = "%s  %s (%s)" % (index, idref, pageFileName)
                self.listSpine.insert(END, string)
            self.listSpine.insert(END, self.labelAddAsLast)

            # remove tmp dir
            producer.clean()

        except Exception as msg:
            self.statusbar.setText(msg.args[0])


    def populateTOCList(self, fileName):
        try:
            # create exlibris instance
            inputEPUB = fileName
            workingDirectory = 'tmp'
            producer = exlibris()
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

            self.listTOC.delete(0, END)
            for l in tocList:
                index = str(l[0]).zfill(nod)
                text = l[1]
                spaces = " " + ("-" * (l[2] * 3)) + " "
                string = "%s%s%s" % (index, spaces, text.ljust(maxLen))
                self.listTOC.insert(END, string)
            self.listTOC.insert(END, self.labelAddAsLast)

            # remove tmp dir
            producer.clean()

        except Exception as msg:
            self.statusbar.setText(msg.args[0])


    def generateNewName(self, string):
        index = string.rfind('.')
        return string[:index] + ".new" + string[index:]
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
### APPLICATION CLASS ###


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
def main():

    # language: ENGLISH
    lang = 'en'

    # lingua: ITALIANO
    #lang = 'it'
    
    # the above can be overridden by the first command line argument
    # (use 'en' or 'it')
    if (len(sys.argv) > 1 and (sys.argv[1] == 'en' or sys.argv[1] == 'it')):
        lang = sys.argv[1]

    root = Tk()
    app = Application(master=root, language=lang)
    root.mainloop()
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
if __name__ == '__main__':

    reload(sys)
    sys.setdefaultencoding("utf-8")
    
    main()
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
