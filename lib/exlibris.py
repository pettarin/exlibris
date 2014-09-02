#!/usr/bin/env python
# -*- coding: utf-8 -*-

__license__     = 'GPLv3'
__author__      = 'Alberto Pettarin (alberto AT albertopettarin DOT it)'
__copyright__   = '2012-2014 Alberto Pettarin (alberto AT albertopettarin DOT it)'
__version__     = 'v1.0.19'
__date__        = '2014-09-02'
__description__ = 'exlibris - add a nice ex libris to your EPUB eBook'


### BEGIN changelog ###
#
# 1.01      2012-06-01  Initial release
# 1.02      2012-06-02  Added third command line argument
#                       Insertion at the end of TOC
# 1.03      2012-06-02  Fixed a bug replacing '\n' and '\r' in content and toc files,
#                       Additional files (images, CSS) can be included via -d option
# 1.04      2012-06-07  Split CLI and library, code cleanup, fixed backslash bug under Windows
# 1.05      2012-06-13  Check before uncompressing EPUB, support for string templates
# 1.06      2012-06-14  Fixed CDATA bug, computation of TOC levels
# 1.07      2012-06-16  Added TOC insertion point, user-defined guide and TOC strings, --no-guide switch
# 1.08      2012-06-20  Minor updates, added GUI
# 1.09                  Alignment between CLI, GUI and Calibre versions
# 1.10      2012-08-25  Bug fixes
# 1.11                  Alignment between CLI, GUI and Calibre versions
# 1.12      2012-08-31  Bug fix: replaced open(file, 'r') with codecs.open(file, encoding='utf-8')
# 1.13      2012-09-01  Bug fix: fixed metadata extraction
# 1.14      2012-10-21  Added ex libris removal
# 1.15      2012-11-11  Added calibre fields support
# 1.16      2012-11-14  Added series-index field
# 1.0.17    2013-08-25  Switched from zipfile to calibre.utils.zipfile to fix a bug in zipfile in Python 2.7.4
# 1.0.18    2014-08-30  Courtesy of @davidfor of MobileRead, this plugin now works with Calibre 2
# 1.0.19    2014-09-02  Alignment between CLI, GUI and Calibre versions; uploaded to GitHub
#
### END changelog ###

### BEGIN TODO ###
#
# 01 [DONE 1.03] Including image/css files in the final EPUB file
# 02 [DONE 1.02] Specify output EPUB instead of backupping the original one
# 03 [DONE 1.06] Compute TOC levels (to correctly show its structure at interactive use)
# 04 [DONE 1.07] Let user select insertion point of ex libris into TOC
# 05 [DONE 1.04] Check that all the paths written into OPF and TOC files have forward slashes
# 06 [DONE 1.05] Check that it is safe to uncompress original EPUB file
# 07 [DONE 1.05] Support for string templates in the ex libris, both from metadata and user-defined
# 08 [DONE 1.06] Fixed a problem with CDATA in metadata
# 09 Let the user insert an image as the ex libris (i.e. builds a suitable XHTML page around it)
# 10 [DONE 1.07] Let the user specify the spine/TOC strings for the ex libris
# 11 [DONE 1.07] Let the user avoid inserting the ex libris in the guide section
# 12 Code clean-up (remove replicated code)
# 13 [DONE 1.14] Let the user remove an added exlibris
# 14 [DONE 1.15] Let the user specify calibre metadata as placeholders
# 15 Perform "real" EPUB parsing using an XML parser
#
### END TODO ###

import codecs, math, os, re, shutil, sys

class exlibris:
    
    ### FIELDS ###
    isCalibre = False
    inputEPUB = ''
    outputEPUB = ''
    inputXHTML = ''
    insertionPointSpine = ''
    insertionPointTOC = ''
    inputDirectory = ''
    workingDirectory = ''
    containerRL = ''
    contentRL = ''
    pageDictionary = ''
    spineList = ''
    navPointList = ''
    mimetypeList = ''
    metadataList = ''
    calibreMetadataList = ''
    metadata = ''
    exlibrisDirectoryRL = ''
    exlibrisFileRL = ''
    exlibrisFileRLToContent = ''
    exlibrisFileRLToTOC = ''
    additionalFiles = ''
    exlibrisGuideString = ''
    exlibrisTOCString = ''
    includeInGuide = ''
    ### FIELDS ###
    
    ### CONSTANTS ###
    exlibrisIdref = 'exlibris'
    exlibrisDirectory = 'exlibris'
    ### CONSTANTS ###
    
    
    
    ### FILE OPERATIONS ###
    def fileExists(self, fileName):
        return os.path.isfile(fileName)

    def dirExists(self, dirName):
        return os.path.isdir(dirName)

    def clearFile(self, fileName):
        if self.fileExists(fileName):
            os.remove(fileName)

    def clearDirectory(self, dir):
        if (os.path.exists(dir)):
            self.deleteDirectory(dir)
        os.makedirs(dir)

    def deleteDirectory(self, dir):
        if (os.path.exists(dir)):
            shutil.rmtree(dir)

    def computeRelativePosition(self, first, second):
        second = os.path.dirname(second)
        return os.path.relpath(first, second)

    def copyFile(self, fileName, dir, dirRL):
        actualDir = self.sanitize(dir) + dirRL
        shutil.copy(fileName, actualDir)
        return dirRL + '/' + os.path.basename(fileName)

    def sanitize(self, dir):
        if ((dir == None) or (len(dir) == 0)):
            return './'
        if ((dir != None) and (dir[-1] != '/')):
            return dir + '/'
        else:
            return dir
    
    def correctSlashes(self, string):
        return string.replace('\\', '/')
    ### FILE OPERATIONS ###



    ### ZIP/UNZIP  ###
    def unzipEPUB(self, inputEPUB, workingDirectory):
        if (self.isCalibre):
            from calibre.utils import zipfile
        else:
            import zipfile
        zip = zipfile.ZipFile(inputEPUB)
        fileList = zip.namelist()
        # check that we do not extract possibly dangerous files
        for file in fileList:
            if ((len(file) >= 1) and (file[0] == '/')):
                raise Exception("Your EPUB files contains one or more files whose path starts with '/'. Extracting them is dangerous!")
            if ((len(file) >= 2) and (file[0:2] == './')):
                raise Exception("Your EPUB files contains one or more files whose path starts with './'. Extracting them is dangerous!")
            if ((len(file) >= 3) and (file[0:3] == '../')):
                raise Exception("Your EPUB files contains one or more files whose path starts with '../'. Extracting them is dangerous!")
        zip.extractall(path=workingDirectory)

    def zipEPUB(self, fileName, dir):
        if (self.isCalibre):
            from calibre.utils import zipfile
        else:
            import zipfile
        fileEPUB = zipfile.ZipFile(fileName, 'w')
        fileEPUB.write(self.sanitize(dir) + 'mimetype', 'mimetype', zipfile.ZIP_STORED)
       
        if (dir[-1] == '/'):
            rootlen = len(dir)
        else:
            rootlen = len(dir) + 1
        for base, dirs, files in os.walk(dir):
           for file in files:
              if (file != 'mimetype'):
                  fn = os.path.join(base, file)
                  fileEPUB.write(fn, fn[rootlen:], zipfile.ZIP_DEFLATED)
    ### ZIP/UNZIP ###


    ### BASIC XHTML PARSING FUNCTIONS ###
    def getValue(self, text, tag, attribute, start=0, closed=True):
        searchText = text[start:]
        match = re.search('<.*?' + tag + ' ', searchText)
        
        if (match == None):
            return [ None, None, None ]

        tagStart = match.start()
        searchText = text[tagStart:]

        if (closed):
            match = re.search('/[ ]*?>', searchText)
        else:
            match = re.search('>', searchText)

        if (match == None):
            return [ None, None, None ]

        tagStop = tagStart + match.start() + len(match.group(0))
        tagContent = text[tagStart:tagStop]
        
        match = re.search(attribute + '[ ]*?=[ ]*?"(.*?)"', searchText)    

        if (match == None):
            return [ None, None, None ]

        return [ match.group(1).strip(), tagContent, tagStop ]


    def determineNameSpacePrefix(self, string, tag):
        indexOpen = string.find('<')
        indexStart = string.find(tag)
        return string[indexOpen+1:indexStart].strip()
    ### BASIC XHTML PARSING FUNCTIONS ###


    ### COMPUTE FILE LOCATIONS ###
    def computeContainerRL(self):
        containerRL = 'META-INF/container.xml'
        containerFile = self.workingDirectory + containerRL
        
        if (not self.fileExists(containerFile)):
            raise Exception("File %s does not exist inside the EPUB file." % (containerRL))

        self.containerRL = containerRL


    def computeContentRL(self):
        containerFile = self.workingDirectory + self.containerRL
        #container = open(containerFile, 'r')
        container = codecs.open(containerFile, encoding='utf-8')
        text = container.read()
        container.close()
       
        text = text.replace('\n', ' ').replace('\r', ' ').replace('>', '>\n')

        contentRL, contentTag, contentStart = self.getValue(text, 'rootfile', 'full-path')
        if (contentRL == None):
            raise Exception("File container.xml in the EPUB file does not seem to reference a valid OPF content file.")
        
        contentFile = self.workingDirectory + contentRL
        if (not self.fileExists(contentFile)):
            raise Exception("File container.xml in the EPUB file refers to %s which does not exist inside the EPUB file." % (contentRL))

        self.contentRL = contentRL


    def computeTocRL(self):
        contentFile = self.workingDirectory + self.contentRL
        contentRelativeDirectory = self.sanitize(os.path.dirname(self.contentRL))

        #content = open(contentFile, 'r')
        content = codecs.open(contentFile, encoding='utf-8')
        text = content.read()
        content.close()

        text = text.replace('\n', ' ').replace('\r', ' ').replace('>', '>\n')

        tags = re.findall('<.*?item .*?/[ ]*?>', text)
      
        if (len(tags) < 1):
            raise Exception("The OPF content file in the EPUB does not seem to contain valid items.")

        for t in tags:
            itemValue, itemTag, itemStop = self.getValue(t, 'item', 'media-type')
            if (itemValue == 'application/x-dtbncx+xml'):
                fileValue, fileTag, fileStart = self.getValue(itemTag, 'item', 'href')
                tocRL = contentRelativeDirectory + fileValue
                tocFile = self.workingDirectory + tocRL
                
                if (not self.fileExists(tocFile)):
                    raise Exception("The OPF content file in the EPUB file refers to %s which does not exist inside the EPUB file." % (tocRelativeLocation))

                self.tocRL = tocRL
                return

        raise Exception("The OPF content file in the EPUB file does not contain an item with media-type=\'application/x-dtbncx+xml\'.")
    ### COMPUTE FILE LOCATIONS ###


    ### COMPUTE SPINE/TOC LIST AND METADATA ###
    def computePageList(self):
        contentFile = self.workingDirectory + self.contentRL
        contentRelativeDirectory = os.path.dirname(self.contentRL)

        #content = open(contentFile, 'r')
        content = codecs.open(contentFile, encoding='utf-8')
        text = content.read()
        content.close()

        text = text.replace('\n', ' ').replace('\r', ' ').replace('>', '>\n')

        tags = re.findall('<.*?item .*?/[ ]*?>', text)
        
        if (len(tags) < 1):
            raise Exception("The OPF content file in the EPUB does not seem to contain valid item tags.")

        pageList = []
        for t in tags:
            itemValue, itemTag, itemStop = self.getValue(t, 'item', 'media-type')
            if (itemValue == 'application/xhtml+xml'):
                hrefValue, hrefTag, hrefStart = self.getValue(itemTag, 'item', 'href')
                idValue, idTag, idStart = self.getValue(itemTag, 'item', 'id')
                pageList += [ [idValue, hrefValue] ]
        
        if (len(pageList) < 1):
            raise Exception("The OPF content file in the EPUB file does not contain an item with media-type=\'application/xhtml+xml\'.")

        self.pageDictionary = self.listToDictionary(pageList)


    # convert [ ['k1','v1'], [k_2, v_2], ... ] in a suitable dictionary with keys k_i's and values v_i's
    def listToDictionary(self, pairList):
        d = dict()
        for p in pairList:
            d[ p[0] ] = p[1]
        return d

    def initializeMetadataList(self):
        meta = dict()
        meta['title'] = ['title', 'title']
        meta['creator'] = [ 'creator', 'creator' ]
        for xyz in ['adp', 'ann', 'arr', 'art', 'asn', 'aut', 'aqt', 'aui', 'ant', 'bkr', 'clb', 'cmm', 'dsr', 'edt', 'ill', 'lyr', 'mdc', 'mus', 'nrt', 'oth', 'pht', 'prt', 'red', 'rev', 'spn', 'ths', 'trc', 'trl']:
            meta[xyz] = [ "creator.*?role.*?=.*?\".*?" + xyz + ".*?\"", "creator" ]

        meta['subject'] = [ 'subject', 'subject' ]
        meta['description'] = [ 'description', 'description' ]
        meta['publisher'] = [ 'publisher', 'publisher' ]
        meta['contributor'] = [ 'contributor', 'contributor' ]
        meta['type'] = [ 'type', 'type' ]
        meta['format'] = [ 'format', 'format' ]
        meta['date'] = [ 'date', 'date' ]
        for xyz in ['original-publication', 'ops-publication', 'creation', 'publication', 'modification']:
            meta[xyz] = [ "date.*?event.*?=.*?\".*?" + xyz + ".*?\"", "date" ]

        meta['identifier'] = [ 'identifier', 'identifier' ]
        for xyz in ['doi', 'isbn', 'uri', 'urn', 'uuid']:
            meta[xyz] = [ "identifier.*?scheme.*?=.*?\".*?" + xyz + ".*?\"", "identifier" ]

        meta['source'] = [ 'source', 'source' ]
        meta['language'] = [ 'language', 'language' ]
        meta['relation'] = [ 'relation', 'relation' ]
        meta['coverage'] = [ 'coverage', 'coverage' ]
        meta['rights'] = [ 'rights', 'rights' ]
        self.metadataList = meta

    def initializeCalibreMetadataList(self):
        calibre_meta = dict()
        calibre_meta['calibre-title'] = ['title', '']
        calibre_meta['calibre-author'] = ['authors', '']
        calibre_meta['calibre-authors'] = ['authors', '']
        calibre_meta['calibre-date'] = ['timestamp', '']
        calibre_meta['calibre-timestamp'] = ['timestamp', '']
        calibre_meta['calibre-size'] = ['size', '']
        calibre_meta['calibre-rating'] = ['rating', '']
        calibre_meta['calibre-tags'] = ['tags', '']
        calibre_meta['calibre-series'] = ['series', '']
        calibre_meta['calibre-series-index'] = ['series-index', '']
        calibre_meta['calibre-publisher'] = ['publisher', '']
        calibre_meta['calibre-published'] = ['pubdate', '']
        calibre_meta['calibre-pubdate'] = ['pubdate', '']
        calibre_meta['calibre-languages'] = ['languages', '']
        calibre_meta['calibre-identifiers'] = ['identifiers', '']
        calibre_meta['calibre-comments'] = ['comments', '']
        calibre_meta['calibre-rights'] = ['rights', '']
        self.calibreMetadataList = calibre_meta

    def initializeMimetypeList(self):
        mime = dict()
        mime['css']   = 'text/css'
        mime['gif']   = 'image/gif'
        mime['jpg']   = 'image/jpeg'
        mime['jpeg']  = 'image/jpeg' 
        mime['png']   = 'image/png'
        mime['svg']   = 'image/svg+xml'
        mime['tif']   = 'image/tiff'
        mime['tiff']  = 'image/tiff'
        mime['ttf']   = 'application/x-font-ttf'
        mime['otf']   = 'application/vnd.ms-opentype'
        mime['xml']   = 'application/xml'
        mime['xhtml'] = 'application/xhtml+xml'
        mime['xpgt']  = 'application/vnd.adobe-page-template+xml'
        self.mimetypeList = mime


    def computeMetadata(self):
        contentFile = self.workingDirectory + self.contentRL
        contentRelativeDirectory = os.path.dirname(self.contentRL)

        #content = open(contentFile, 'r')
        content = codecs.open(contentFile, encoding='utf-8')
        text = content.read()
        content.close()

        text = text.replace('\n', ' ').replace('\r', ' ').replace('>', '>\n')
        
        metadataValues = self.getTagValue(text, 'metadata', 'metadata')
        
        pairs = dict()

        if (metadataValues != None):
            for key in self.metadataList.keys():
                value = self.getTagValue(metadataValues, (self.metadataList[key])[0], (self.metadataList[key])[1], True)
                if (value != None):
                    pairs[key] = value.strip()
       
        self.metadata = pairs


    def getTagValue(self, text, start, end, ignoreCase=False):
        matchStart = -1
        matchEnd = -1
        value = None

        start = "<[^/ ]*?" + start + ".*?>"
        end = "</.*?" + end + ".*?>"
        
        flag = 0
        if (ignoreCase):
            flag = re.IGNORECASE
        match = re.search(start, text, flag)
        if (match != None):
            matchStart = match.end()

        if (matchStart > -1):
            text = text[matchStart:]
            match = re.search(end, text, flag)
            if (match != None):
                matchEnd = match.start()

            if (matchEnd > -1):
                value = text[0:matchEnd]

        return value


    def computeSpineList(self):
        contentFile = self.workingDirectory + self.contentRL
        contentRelativeDirectory = os.path.dirname(self.contentRL)

        #content = open(contentFile, 'r')
        content = codecs.open(contentFile, encoding='utf-8')
        text = content.read()
        content.close()

        text = text.replace('\n', ' ').replace('\r', ' ').replace('>', '>\n')

        tags = re.findall('<.*?itemref .*?/[ ]*?>', text)
        
        if (len(tags) < 1):
            raise Exception("The OPF content file in the EPUB file has an empty spine tag.")

        spineIndex = 1
        spineList = []
        for t in tags:
            itemrefValue, itemrefTag, itemrefStop = self.getValue(t, 'itemref', 'idref')
            spineList += [ [spineIndex, itemrefValue] ]
            spineIndex += 1

        if (len(spineList) < 1):
            raise Exception("The spine in the content file in the EPUB does not contain any valid itemref tag.")

        self.spineList = spineList

        
    def computeNavPointList(self):
        tocFile = self.workingDirectory + self.tocRL
        
        #toc = open(tocFile, 'r')
        toc = codecs.open(tocFile, encoding='utf-8')
        text = toc.read()
        toc.close()

        text = text.replace('\n', ' ').replace('\r', ' ').replace('>', '>\n')
        
        tags = re.findall('<[^/]*?navPoint.*?>', text)
        if (len(tags) < 1):
            raise Exception("TOC file in the EPUB does not seem to contain valid navPoint tags.")

        navPointList = []
        patternNavPoint = re.compile("<[^/]*?navPoint.*?>")
        patternEndNavPoint = re.compile("<[ ]*?/.*?navPoint.*?>")
        patternNavLabel = re.compile("<[^/]*?navLabel.*?>")
        patternTextStart = re.compile("<[^/]*?text.*?>")
        patternTextStop = re.compile("<[ ]*?/.*?text.*?>")

        currentLevel = 0
        absolutePos = 0
        tagStart = 0
        tagEnd = 1

        for t in tags:

            match = patternNavPoint.search(text, absolutePos)
            if (match == None):
                raise Exception("Your TOC file seems to be badly formatted (6).")
            absolutePos = match.end()

            currentLevel += 1

            match = patternNavLabel.search(text, absolutePos)
            if (match == None):
                raise Exception("Your TOC file seems to be badly formatted (7).")
            absolutePosBegin = match.end()

            match = patternTextStart.search(text, absolutePosBegin)
            if (match == None):
                raise Exception("Your TOC file seems to be badly formatted (8).")
            absolutePosBegin = match.end()

            match = patternTextStop.search(text, absolutePosBegin)
            if (match == None):
                raise Exception("Your TOC file seems to be badly formatted (9).")
            absolutePosEnd = match.start()

            navPointList += [ [self.getNavPointIndex(t), text[absolutePosBegin:absolutePosEnd].strip(), currentLevel, tagStart] ]

            absolutePos = absolutePosEnd

            ### TEST WHETHER IN A NESTED NavPoint ###
            matchNextNavPoint = patternNavPoint.search(text, absolutePos)
            matchNextEndNavPoint = patternEndNavPoint.search(text, absolutePos)
            
            if (matchNextEndNavPoint == None):
                raise Exception("Your TOC file seems to be badly formatted (10).")

            if (matchNextNavPoint == None):
                    break
                    
            while ((matchNextEndNavPoint != None) and (matchNextEndNavPoint.start() < matchNextNavPoint.start())):
                absolutePos = matchNextEndNavPoint.end()
                currentLevel -= 1
                matchNextEndNavPoint = patternEndNavPoint.search(text, absolutePos)
            ### TEST WHETHER IN A NESTED NavPoint ###

        self.navPointList = navPointList


    def getNavPointIndex(self, tag):
        playOrder, playOrderTag, playOrderStop = self.getValue(tag, 'navPoint', 'playOrder', 0, False)

        if (not playOrder.isdigit()):
            raise Exception("TOC file in the EPUB does not seem to contain valid playOrder attribute for the following navPoint tag: %s." % (tag))

        return playOrder
    ### COMPUTE SPINE/TOC LIST AND METADATA ###


    ### TOC INSERTION ###
    def setInsertionPointTOC(self, ip):
        self.insertionPointTOC = ip


    def getLastInsertionPointTOC(self):
        return len(self.navPointList)


    def validateInsertionPointTOC(self):
                
        last = self.getLastInsertionPointTOC()
        
        if (self.insertionPointTOC == 'last'):
            self.insertionPointTOC = last + 1
        if (self.insertionPointTOC == 'first'):
            self.insertionPointTOC = 1
        self.insertionPointTOC = int(self.insertionPointTOC)
        
        if ((self.insertionPointTOC < 1) or (self.insertionPointTOC > last + 1)):
            raise Exception("The specified \'%s\' TOC insertion point is invalid: it must be between %s and %s" % (self.insertionPointTOC, 1, last + 1))


    def checkInsertionPointTOC(self, ip):
        last = self.getLastInsertionPointTOC()
        
        if (self.insertionPointTOC == 'first'):
            return 1

        if (self.insertionPointTOC == 'last'):
            return last + 1

        if ((ip == None) or (ip == 'ask')):
            return None

        if (ip.isdigit()):
            ip = int(ip)
            if ((ip >= 1) and (ip <= last + 1)):
                return ip
        
        return None

    def removeFromTOCFile(self, referencedFiles):

        tocFile = self.workingDirectory + self.tocRL
        tocRelativeDirectory = os.path.dirname(self.tocRL)

        #toc = open(tocFile, 'r')
        toc = codecs.open(tocFile, encoding='utf-8')
        text = toc.read()
        toc.close()

        text = text.replace('\n', ' ').replace('\r', ' ').replace('>', '>|||\n|||')

        for file in referencedFiles:
            match = re.search("<.*?src=\"%s\".*?>" % (file), text)
            if (match != None):
                # found the matching item
                position = text.find(match.group(0))
                
                # find begin of this navPoint
                start = text.rfind("navPoint", 0, position)
                start = text.rfind("<", 0, start)
                
                # find end of this navPoint
                stop = text.find("navPoint", position)
                stop = text.find(">", stop) + 1
                
                # remove it
                text = text[:start] + text[stop:]
        
        # recalculate playOrder
        listOfPlayOrder = re.findall("playOrder=\"[0-9]*\"", text)
        index = 1
        for l in listOfPlayOrder:
            text = text.replace(l, "playOrder=\"%s\"" % str(index))
            index += 1
        
        text = text.replace('>|||\n|||', '>').replace('|||', '')

        toc = open(tocFile, 'w')
        toc.write(text)
        toc.close()

    
    def insertIntoTOCFile(self):

        self.exlibrisFileRLToTOC = self.correctSlashes(self.computeRelativePosition(self.exlibrisFileRL, self.tocRL))

        tocFile = self.workingDirectory + self.tocRL
        tocRelativeDirectory = os.path.dirname(self.tocRL)

        #toc = open(tocFile, 'r')
        toc = codecs.open(tocFile, encoding='utf-8')
        text = toc.read()
        toc.close()

        text = text.replace('\n', ' ').replace('\r', ' ').replace('>', '>|||\n|||')
        
        absolutePos = 0
        counter = 1
        patternNavPoint = re.compile("<[^/]*?navPoint.*?>")
        patternEndNavPoint = re.compile("<[ ]*?/.*?navPoint.*?>")
        patternPlayOrder = re.compile(r"playOrder.*?=.*?\"(.*?)\"")
        patternNavMap = re.compile("<[^/]*?navMap.*?>")
        patternEndNavMap = re.compile("<[ ]*?/.*?navMap.*?>")

        match = patternNavMap.search(text, absolutePos)
        if (match == None):
            raise Exception("Your TOC file seems to be badly formatted (0).")
        absolutePos = match.end()
        namespacePrefix = self.determineNameSpacePrefix(match.group(0), 'navMap')

        while (counter < self.insertionPointTOC):
            match = patternNavPoint.search(text, absolutePos)
            if (match == None):
                raise Exception("Your TOC file seems to be badly formatted (1).")
            absolutePos = match.end()
            counter += 1

        if (self.insertionPointTOC <= self.getLastInsertionPointTOC()):
            match = patternNavPoint.search(text, absolutePos)
            if (match == None):
                raise Exception("Your TOC file seems to be badly formatted (2).")
            absolutePos = match.start()
        else:
            match = patternEndNavMap.search(text, absolutePos)
            if (match == None):
                raise Exception("Your TOC file seems to be badly formatted (3).")
            absolutePos = match.start()

        textPre = text[:absolutePos]
        textPost = text[absolutePos:]

        playOrder = self.insertionPointTOC
        navPointId = 'navPoint-' + str(playOrder)
        newItem = ''
        newItem += "<%snavPoint id=\"%s\" playOrder=\"%s\">\n" % (namespacePrefix, navPointId, playOrder)
        newItem += " <%snavLabel>\n" % (namespacePrefix)
        newItem += "  <%stext>%s</%stext>\n" % (namespacePrefix, self.exlibrisTOCString, namespacePrefix)
        newItem += " </%snavLabel>\n" % (namespacePrefix)
        newItem += " <%scontent src=\"%s\" />\n" % (namespacePrefix, self.exlibrisFileRLToTOC)
        newItem += "</%snavPoint>\n" % (namespacePrefix)

        absolutePos = 0 
        while (counter < self.getLastInsertionPointTOC() + 1):
            match = patternNavPoint.search(textPost, absolutePos)
            if (match == None):
                raise Exception("Your TOC file seems to be badly formatted (4).")
            oldNavPoint = match.group(0)
            oldNavPointEnd = match.end()
           
            match = patternPlayOrder.search(oldNavPoint)
            if (match == None):
                raise Exception("Your TOC file seems to be badly formatted (5).")
            
            oldIndex = int(match.group(1))
            oldIndexStart = match.start(1)
            oldIndexEnd = match.end(1)
            newIndex = oldIndex + 1
            newNavPoint = oldNavPoint[:oldIndexStart] + str(newIndex) + oldNavPoint[oldIndexEnd:]

            textPost = textPost.replace(oldNavPoint, newNavPoint)
            absolutePos = oldNavPointEnd
            counter += 1
        
        text = textPre + newItem + textPost 
        
        text = text.replace('>|||\n|||', '>').replace('|||', '')

        toc = open(tocFile, 'w')
        toc.write(text)
        toc.close()
    ### TOC INSERTION ###


    ### SPINE INSERTION ###
    def setInsertionPointSpine(self, ip):
        self.insertionPointSpine = ip


    def getLastInsertionPointSpine(self):
        return len(self.spineList)


    def validateInsertionPointSpine(self):
                
        last = self.getLastInsertionPointSpine()
        
        if (self.insertionPointSpine == 'last'):
            self.insertionPointSpine = last + 1
        if (self.insertionPointSpine == 'first'):
            self.insertionPointSpine = 1
        self.insertionPointSpine = int(self.insertionPointSpine)
        
        if ((self.insertionPointSpine < 1) or (self.insertionPointSpine > last + 1)):
            raise Exception("The specified \'%s\' insertion point is invalid: it must be between %s and %s" % (self.insertionPointSpine, 1, last + 1))


    def checkInsertionPointSpine(self, ip):
        last = self.getLastInsertionPointSpine()
        
        if (self.insertionPointSpine == 'first'):
            return 1

        if (self.insertionPointSpine == 'last'):
            return last + 1

        if ((ip == None) or (ip == 'ask')):
            return None

        if (ip.isdigit()):
            ip = int(ip)
            if ((ip >= 1) and (ip <= last + 1)):
                return ip
        
        return None

    def removeFromContentFile(self, referencedFiles):
        contentFile = self.workingDirectory + self.contentRL
        contentRelativeDirectory = os.path.dirname(self.contentRL)
        
        #content = open(contentFile, 'r')
        content = codecs.open(contentFile, encoding='utf-8')
        text = content.read()
        content.close()
        
        text = text.replace('\n', ' ').replace('\r', ' ').replace('>', '>|||\n|||')
        
        # remove from manifest
        for file in referencedFiles:
            match = re.search("<.*?href=\"%s\".*?>" % (file), text)
            if (match != None):
                text = text.replace(match.group(0), "")
        
        # remove from guide
        for file in referencedFiles:
            match = re.search("<.*?href=\"%s\".*?>" % (file), text)
            if (match != None):
                text = text.replace(match.group(0), "")
        
        # remove from spine
        match = re.search("<.*?idref=\"exlibris\".*?>", text)
        if (match != None):
                text = text.replace(match.group(0), "")
        
        text = text.replace('>|||\n|||', '>').replace('|||', '')
        
        content = open(contentFile, 'w')
        content.write(text)
        content.close()
        
    def insertIntoContentFile(self):
        contentFile = self.workingDirectory + self.contentRL
        contentRelativeDirectory = os.path.dirname(self.contentRL)

        #content = open(contentFile, 'r')
        content = codecs.open(contentFile, encoding='utf-8')
        text = content.read()
        content.close()

        text = text.replace('\n', ' ').replace('\r', ' ').replace('>', '>|||\n|||')

        # insert into manifest tag
        match = re.search('<.*?manifest.*?>', text)
        if (match == None):
            raise Exception("Your content file seems to be badly formatted (4).")
        namespacePrefix = self.determineNameSpacePrefix(match.group(0), 'manifest')

        match = re.search('<.*?/.*?manifest.*?>', text)
        if (match == None):
            raise Exception("Your content file seems to be badly formatted (5).")
        manifestEnd = match.start()
        newItem = "<%sitem id=\"%s\" href=\"%s\" media-type=\"application/xhtml+xml\"/>\n" % (namespacePrefix, self.exlibrisIdref, self.exlibrisFileRLToContent)
        
        # insert additional files
        fileCounter = 0
        for file in self.additionalFiles:
            fileIdref = 'exlibris-resource-' + str(fileCounter)
            fileHref = self.correctSlashes(file[0])
            fileMediaType = file[1]
            newItem += "<%sitem id=\"%s\" href=\"%s\" media-type=\"%s\"/>\n" % (namespacePrefix, fileIdref, fileHref, fileMediaType)
            fileCounter += 1

        text = text[:manifestEnd] + newItem + text[manifestEnd:]

        # insert into guide tag, if already present
        if (self.includeInGuide):
            match = re.search('<.*?guide.*?>', text)
            if (match != None):
                namespacePrefix = self.determineNameSpacePrefix(match.group(0), 'guide')
                match = re.search('<.*?/.*?guide.*?>', text)
                if (match != None):
                    guideEnd = match.start()
                    newItem = "<%sreference type=\"colophon\" title=\"%s\" href=\"%s\"/>\n" % (namespacePrefix, self.exlibrisGuideString, self.exlibrisFileRLToContent)
                    text = text[:guideEnd] + newItem + text[guideEnd:]

        # insert into spine tag
        match = re.search('<.*?itemref.*?>', text)
        if (match == None):
            raise Exception("Your content file seems to be badly formatted (7).")
        namespacePrefix = self.determineNameSpacePrefix(match.group(0), 'itemref')

        tags = re.findall('<.*?itemref .*?/[ ]*?>', text)

        if (self.insertionPointSpine > len(tags)):
            # insert after last
            insertionIndex = text.find(tags[-1]) + len(tags[-1])
        else:
            # insert as the specified tag
            insertionIndex = text.find(tags[self.insertionPointSpine-1])

        newItem = "<%sitemref idref=\"%s\" />\n" % (namespacePrefix, self.exlibrisIdref)
        text = text[:insertionIndex] + newItem + text[insertionIndex:]
        
        text = text.replace('>|||\n|||', '>').replace('|||', '')

        content = open(contentFile, 'w')
        content.write(text)
        content.close()


    def getListAdditionalFiles(self, dir, exlibris):
        fileList = []
        
        if (dir != None):    
            for file in os.listdir(dir):
                file = dir + file
                if (file != exlibris):
                    item = self.getProperFileMediaType(file)
                    if (item != None):
                        fileList += [ [ file, item ] ]
        return fileList
    
    def getListFiles(self, dir, dirRL):
        fileList = []
        
        if (dir != None):    
            for file in os.listdir(dir):
                file = dirRL + file
                fileList += [ file ]
        return fileList

    def getProperFileMediaType(self, file):
        ext = os.path.splitext(file)[1]
        pos = ext.find('.')
        if (pos > -1):
            ext = ext[pos+1:].lower()
            if (ext in self.mimetypeList):
                return self.mimetypeList[ext]
        return None
    ### SPINE INSERTION  ###


    ### CREATE EXLIBRIS DIR ###
    def createExlibrisDirectory(self):
        contentDirectoryRL = self.sanitize(os.path.dirname(self.contentRL))
        self.exlibrisDirectoryRL = contentDirectoryRL + self.exlibrisDirectory
        exlibrisDirectory = self.workingDirectory + self.exlibrisDirectoryRL
        self.clearDirectory(exlibrisDirectory)
    ### CREATE EXLIBRIS DIR ###


    ### REMOVE EXLIBRIS DIR ###
    def removeExlibrisDirectory(self):
        referencedFiles = []
        
        contentDirectoryRL = self.sanitize(os.path.dirname(self.contentRL))
        self.exlibrisDirectoryRL = contentDirectoryRL + self.exlibrisDirectory
        fullExlibrisDirectory = self.sanitize(self.workingDirectory + self.exlibrisDirectoryRL)
        
        if (self.dirExists(fullExlibrisDirectory)):
            referencedFiles = self.getListFiles(fullExlibrisDirectory, self.sanitize(self.exlibrisDirectory))
            self.deleteDirectory(fullExlibrisDirectory)
        
        return referencedFiles
    ### REMOVE EXLIBRIS DIR ###


    ### INPUT CHECKS ###
    def checkInputFiles(self):
        if (not self.fileExists(self.inputEPUB)):
            raise Exception("File %s does not exist." % (self.inputEPUB))

        if (not self.fileExists(self.inputXHTML)):
            raise Exception("File %s does not exist." % (self.inputXHTML))
        
        if (self.inputDirectory != None):
            self.inputDirectory = self.sanitize(self.inputDirectory)
            if (not self.dirExists(self.inputDirectory)):
                raise Exception("Directory %s does not exist." % (self.inputDirectory))

    def checkInputInsertionPoint(self, ip):
        valid = False
        valid = valid or ip.isdigit()
        valid = valid or ip == 'first'
        valid = valid or ip == 'last'
        valid = valid or ip == 'ask'
        
        if (not valid):
            raise Exception("The specified \'%s\' insertion point is invalid." % (insertionPoint))
    ### INPUT CHECKS ###


    ### UNCOMPRESS INTO TMP ###
    def uncompressIntoWorkingDirectory(self):
        self.clearDirectory(self.workingDirectory)
        self.unzipEPUB(self.inputEPUB, self.workingDirectory)
    ### UNCOMPRESS INTO TMP ###


    ### COPY EX LIBRIS FILES ###
    def copyExLibrisFiles(self):
        self.createExlibrisDirectory()
        
        exlibrisFileRL = self.copyFile(self.inputXHTML, self.workingDirectory, self.exlibrisDirectoryRL)
        exlibrisFileRLToContent = self.computeRelativePosition(exlibrisFileRL, self.contentRL)
        
        # copy the specified additional files into the newly created directory
        additionalFiles = self.getListAdditionalFiles(self.inputDirectory, self.inputXHTML)
        for file in additionalFiles:
            fileRL = self.copyFile(file[0], self.workingDirectory, self.exlibrisDirectoryRL)
            file[0] = self.computeRelativePosition(fileRL, self.contentRL)
            
        self.exlibrisFileRL = exlibrisFileRL
        self.exlibrisFileRLToContent = self.correctSlashes(exlibrisFileRLToContent)
        self.additionalFiles = additionalFiles
    ### COPY EX LIBRIS FILES ###


    ### REPLACE PLACEHOLDER STRINGS ###
    def replacePlaceholderStrings(self):
        exlibrisFile = self.workingDirectory + self.exlibrisFileRL
        #exlibris = open(exlibrisFile, 'r')
        exlibris = codecs.open(exlibrisFile, encoding='utf-8')
        text = exlibris.read()
        exlibris.close()
        
        for key in self.metadata.keys():
            replaceString = "[%" + key + "%]"        
            replaceWith = self.metadata[key]
            #print("KEY: %s\nVALUE: %s" % (key, replaceWith))
            replaceWith = replaceWith.replace("<![CDATA[", "")
            replaceWith = replaceWith.replace("]]>", "")
            replaceWith = replaceWith.replace("&amp;apos;", "'")
            replaceWith = replaceWith.replace("&lt;", "<")
            replaceWith = replaceWith.replace("&gt;", ">")
            replaceWith = replaceWith.replace("&amp;", "&")
            text = text.replace(replaceString, replaceWith)

        ### some heuristic fixes to common metadata imprecisions ###
        ### TODO: better handling of these issues
        if ("aut" not in self.metadata and text.find("[%aut%]") > -1 and "creator" in self.metadata):
            replaceString = "[%aut%]"
            replaceWith = self.metadata["creator"]
            text = text.replace(replaceString, replaceWith)

        if ("date" not in self.metadata and text.find("[%date%]") > -1 and "original-publication" in self.metadata):
            replaceString = "[%date%]"
            replaceWith = self.metadata["original-publication"]
            text = text.replace(replaceString, replaceWith)
        ### some heuristic fixes to common metadata imprecisions ###
        
        for key in self.userReplacementStrings.keys():
            replaceString = "[%" + key + "%]"
            replaceWith = self.userReplacementStrings[key]
            #print("KEY: %s\nVALUE: %s" % (key, replaceWith))
            replaceWith = replaceWith.replace("<![CDATA[", "")
            replaceWith = replaceWith.replace("]]>", "")
            replaceWith = replaceWith.replace("&amp;apos;", "'")
            replaceWith = replaceWith.replace("&lt;", "<")
            replaceWith = replaceWith.replace("&gt;", ">")
            replaceWith = replaceWith.replace("&amp;", "&")
            text = text.replace(replaceString, replaceWith)

        exlibris = open(exlibrisFile, 'w')
        exlibris.write(text)
        exlibris.close()
    ### REPLACE PLACEHOLDER STRINGS ###

    ### CREATE NEW EPUB ###
    def createNewEPUB(self):
        self.clearFile(self.outputEPUB)
        self.zipEPUB(self.outputEPUB, self.workingDirectory)
    ### CREATE NEW EPUB ###

    
    ### INIT ###
    def __init__(self, calibre=False):
        self.isCalibre = calibre
        self.initializeMimetypeList()
        self.initializeMetadataList()
        self.initializeCalibreMetadataList()
    ### INIT ###


    ### INITIALIZE ###
    def initialize(self, inputEPUB, outputEPUB, inputXHTML, insertionPointSpine, insertionPointTOC, inputDirectory, workingDirectory, userReplacementStrings, exlibrisGuideString, exlibrisTOCString, includeInGuide):
        
        self.inputEPUB = inputEPUB
        self.outputEPUB = outputEPUB
        self.inputXHTML = inputXHTML
        self.insertionPointSpine = insertionPointSpine
        self.insertionPointTOC = insertionPointTOC
        self.inputDirectory = self.sanitize(inputDirectory)
        self.workingDirectory = self.sanitize(workingDirectory)
        self.userReplacementStrings = userReplacementStrings
        self.exlibrisGuideString = exlibrisGuideString
        self.exlibrisTOCString = exlibrisTOCString
        self.includeInGuide = includeInGuide
        
        self.checkInputFiles()
        self.checkInputInsertionPoint(insertionPointSpine)
        self.checkInputInsertionPoint(insertionPointTOC)
        
        self.uncompressIntoWorkingDirectory()
        
        self.computeContainerRL()     
        self.computeContentRL()
        self.computeTocRL()
        
        self.computePageList()
        self.computeSpineList()
        self.computeNavPointList()

        self.computeMetadata()
    ### INITIALIZE ###


    ### INSERT EX LIBRIS ###
    def insertExLibris(self):
        self.validateInsertionPointSpine()
        self.validateInsertionPointTOC()
        
        self.copyExLibrisFiles()
        
        self.replacePlaceholderStrings()
        
        self.insertIntoContentFile()
        self.insertIntoTOCFile()        
    ### INSERT EX LIBRIS ###

    ### REMOVE EX LIBRIS ###
    def removeExLibris(self):
        referencedFiles = self.removeExlibrisDirectory()
        self.removeFromContentFile(referencedFiles)
        self.removeFromTOCFile(referencedFiles)
    ### REMOVE EX LIBRIS ###

    ### CLEAN UP ###
    def clean(self):
        self.deleteDirectory(self.workingDirectory)
    ### CLEAN UP ###


    ### RETURN SPINE/TOC LIST ###
    def getSpineList(self):
        return self.spineList

    def getPageDictionary(self):
        return self.pageDictionary

    def getTOCList(self):
        return self.navPointList
    ### RETURN SPINE/TOC LIST ###


    ### RETURN SUPPORTED METADATA LIST ###
    def getSupportedMetadataList(self):
        supp = []
        for key in self.metadataList.keys():
            supp += [ key ]
        for key in self.calibreMetadataList.keys():
            supp += [ key ]
        supp.sort()
        return supp
    ### RETURN SUPPORTED METADATA LIST ###


    ### RETURN SUPPORTED MIMETYPE LIST ###
    def getSupportedMimetypeList(self):
        supp = []
        for key in self.mimetypeList.keys():
            supp += [ key ]
        supp.sort()
        return supp
    ### RETURN SUPPORTED MIMETYPE LIST ###



