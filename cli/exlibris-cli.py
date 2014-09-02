#!/usr/bin/env python
# -*- coding: utf-8 -*-

__license__     = 'GPLv3'
__author__      = 'Alberto Pettarin (alberto AT albertopettarin DOT it)'
__copyright__   = '2012-2014 Alberto Pettarin (alberto AT albertopettarin DOT it)'
__version__     = 'v1.0.19'
__date__        = '2014-09-02'
__description__ = 'exlibris-cli - CLI frontend to exlibris'


import getopt, os, sys
from exlibris import exlibris


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
def printError(string):
    print "[ERROR] " + string
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
def printInfo(string):
    print "[INFO] " + string
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
def printErrorUsageAndExit(string):
    printError(string)
    usage(True)
    exit(1)
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
def parseArguments(args):

    if (len(args) == 1 or args[1] == '-h' or args[1] == '--help'):
        usage()
        exit(0)

    if (len(args) == 2 and args[1] == '--supported-metadata-identifiers'):
        printSupportedMetadataIdentifiers()
        exit(0)

    if (len(args) == 2 and args[1] == '--supported-mimetype-identifiers'):
        printSupportedMimetypeIdentifiers()
        exit(0)
        
    if (len(args) == 3 and args[2] == '--spine'):
        printSpine(args[1])
        exit(0)
        
    if (len(args) == 3 and args[2] == '--toc'):
        printTOC(args[1])
        exit(0)
        
    if (len(args) == 3 and args[2] == '--remove'):
        removeExLibris(args[1], args[1])
        exit(0)
    
    if (len(args) < 4):
        printErrorUsageAndExit('Too few arguments.')
    
    if (len(args) == 4 and args[3] == '--remove'):
        removeExLibris(args[1], args[2])
        exit(0)

    if (args[1] == args[2]):
        printErrorUsageAndExit('Your input and output EPUB files coincide. Please specify two different file names.')

    inputEPUB = args[1]
    outputEPUB = args[2]
    inputXHTML = args[3]
    insertionPointSpine = 'last'
    insertionPointTOC = 'last'
    inputDirectory = None
    keepTMP = False
    userReplacementStrings = dict()
    exlibrisGuideString = 'EX LIBRIS'
    exlibrisTOCString = 'EX LIBRIS'
    includeInGuide = True

    if (len(args) > 4):
        try:
            optlist, free = getopt.getopt(args[4:], 'd:kr:s:t:', ['guide-string=', 'toc-string=', 'no-guide'])
        except getopt.GetoptError, err:
            printErrorUsageAndExit(str(err))
        optdict = dict(optlist)

        if ('-d' in optdict):
            inputDirectory = optdict['-d']
        if ('-s' in optdict):
            insertionPointSpine = optdict['-s']
        if ('-t' in optdict):
            insertionPointTOC = optdict['-t']
        if ('-k' in optdict):
            keepTMP = True
        if ('-r' in optdict):
            userReplacementStrings = parseUserReplacementStrings(optdict['-r'])
        if ('--guide-string' in optdict):
            exlibrisGuideString = optdict['--guide-string']
        if ('--toc-string' in optdict):
            exlibrisTOCString = optdict['--toc-string']
        if ('--no-guide' in optdict):
            includeInGuide = False

    return [ inputEPUB, outputEPUB, inputXHTML, insertionPointSpine, insertionPointTOC, inputDirectory, keepTMP, userReplacementStrings, exlibrisGuideString, exlibrisTOCString, includeInGuide ]
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
def parseUserReplacementStrings(string):
    toReturn = dict()
    pairs = string.split(';')
    for pair in pairs:
        sep = pair.split('=')
        if (len(sep) == 2):
            key = sep[0].strip()
            value = sep[1]
            toReturn[key] = value
    return toReturn
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
def printSupportedMetadataIdentifiers():
    message = ''
    message += '' + '\n'    
    message += 'LIST OF SUPPORTED METADATA IDENTIFIERS' + '\n'
    producer = exlibris()
    tags = producer.getSupportedMetadataList()
    for tag in tags:
        message += tag + '\n'
    print message
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
  
    
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
def printSupportedMimetypeIdentifiers():
    message = ''
    message += '' + '\n'    
    message += 'LIST OF SUPPORTED EXTENSIONS' + '\n'
    producer = exlibris()
    tags = producer.getSupportedMimetypeList()
    for tag in tags:
        message += tag + '\n'
    print message
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
def printSpine(inputEPUB):
    try:
        # print reading message
        printInfo("Reading your %s eBook " % (inputEPUB))
        
        # create exlibris instance
        workingDirectory = 'tmp'
        producer = exlibris()
        producer.initialize(inputEPUB, inputEPUB, inputEPUB, '1', '1', None, workingDirectory, None, None, None, None)
        
        # get spine list
        spineList = producer.getSpineList()
        pageDictionary = producer.getPageDictionary()
        printInfo("The spine of your eBook contains the following pages:")
        printSpineList(spineList, pageDictionary)

        # remove tmp dir
        producer.clean()

    except Exception as msg:
        printErrorUsageAndExit(msg.args[0])
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
def printTOC(inputEPUB):
    try:
        # print reading message
        printInfo("Reading your %s eBook " % (inputEPUB))
        
        # create exlibris instance
        workingDirectory = 'tmp'
        producer = exlibris()
        producer.initialize(inputEPUB, inputEPUB, inputEPUB, '1', '1', None, workingDirectory, None, None, None, None)
        
        # get spine list
        tocList = producer.getTOCList()
        pageDictionary = producer.getPageDictionary()
        printInfo("The TOC of your eBook contains the entries:")
        printTOCList(tocList, pageDictionary)

        # remove tmp dir
        producer.clean()

    except Exception as msg:
        printErrorUsageAndExit(msg.args[0])
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
def removeExLibris(inputEPUB, outputEPUB):
    try:
        # print reading message
        printInfo("Reading your %s eBook to remove existing ex libris " % (inputEPUB))
        
        # create exlibris instance
        workingDirectory = 'tmp'
        producer = exlibris()
        producer.initialize(inputEPUB, outputEPUB, inputEPUB, '1', '1', None, workingDirectory, None, None, None, None)
        
        # removeExLibris
        producer.removeExLibris()
        
        # output
        producer.createNewEPUB()

        # remove tmp dir
        producer.clean()
        
        # print reading message
        printInfo("Now your eBook %s does not contain any ex libris" % (outputEPUB))

    except Exception as msg:
        printErrorUsageAndExit(msg.args[0])
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
def usage(short=False):
    
    message = ''
    message += '' + '\n'    
    message += 'NAME' + '\n'
    message += ' exlibris-cli - CLI frontend to exlibris: add a nice ex libris to your EPUB eBook' + '\n'
    message += '' + '\n'
    message += 'SYNOPSIS' + '\n'
    message += ' $ python exlibris-cli.py --help' + '\n'
    message += ' $ python exlibris-cli.py --supported-mimetype-identifiers' + '\n'
    message += ' $ python exlibris-cli.py --supported-metadata-identifiers' + '\n'
    message += ' $ python exlibris-cli.py book.epub --spine' + '\n'
    message += ' $ python exlibris-cli.py book.epub --toc' + '\n'
    message += ' $ python exlibris-cli.py book.epub [new.epub] --remove' + '\n'
    message += ' $ python exlibris-cli.py book.epub new.epub exlibris.xhtml [OPTIONS]' + '\n'
    
    if (not short):
        message += '' + '\n'
        message += 'DESCRIPTION' + '\n'
        message += '  Insert exlibris.xhtml inside book.epub and create new.epub.' + '\n'
        message += '  If -h or --help option is given, display this usage message.' + '\n'
        message += '  If -s option is not given, add the exlibris page as the last element of the spine.' + '\n'
        message += '  If -t option is not given, add the exlibris page as the last element of the TOC.' + '\n'
        message += '  If --spine (resp., --toc) option is given, print the elements of the spine (resp., TOC).' + '\n'
        message += '  If --remove option is given, remove the ex libris from book.epub [and create new.epub].' + '\n'
        message += '' + '\n'
        message += 'OPTIONS' + '\n'
        message += '  -d DIR: include all the recognized files contained in DIR.' + '\n'
        message += '          Use this option if your ex libris XHTML page references CSS or image files.' + '\n'
        message += '  -k:     do not delete the temporary directory (\'tmp\').' + '\n'
        message += '  -r DIC: replace the given strings in the ex libris page.' + '\n'
        message += '          DIC must have the following format: "key1=value1; key2=value2; ... ; keyN=valueN".' + '\n'
        message += '          exlibris will replace [%key1%] in the ex libris XHTML page with value1, and so on.' + '\n'
        message += '          exlibris automagically replaces placeholders like [%title%], [%aut%], ... with the eBook metadata.' + '\n'
        message += '          (Use --supported-metadata-identifiers to list all the supported metadata identifiers.)' + '\n'
        message += '  -s NUM: insert the exlibris as the NUM-th element of the spine.' + '\n'
        message += '          Use \'1\' or \'first\' to insert the exlibris as the first element.' + '\n'
        message += '          Use \'last\' to insert the exlibris as the last element (default behavior).' + '\n'
        message += '          Use \'ask\' to get a list of possible insertion points and select it interactively.' + '\n'
        message += '  -t NUM: insert the exlibris as the NUM-th element of the TOC.' + '\n'
        message += '          Use \'1\' or \'first\' to insert the exlibris as the first element.' + '\n'
        message += '          Use \'last\' to insert the exlibris as the last element (default behavior).' + '\n'
        message += '          Use \'ask\' to get a list of possible insertion points and select it interactively.' + '\n'
        message += '' + '\n'
        message += '  --guide-string STR: use STR as the guide string for the ex libris' + '\n'
        message += '  --keep:             do not delete the temporary directory (\'tmp\').' + '\n'
        message += '  --no-guide:         do not insert the ex libris in the guide section' + '\n'
        message += '  --toc-string STR:   use STR as the TOC string for the ex libris' + '\n'
        message += '' + '\n'
        message += 'EXAMPLES' + '\n'
        message += ' $ python exlibris-cli.py book.epub new.epub exlibris.xhtml' + '\n'
        message += ' $ python exlibris-cli.py book.epub new.epub exlibris.xhtml -s 1' + '\n'
        message += ' $ python exlibris-cli.py book.epub new.epub exlibris.xhtml -s first' + '\n'
        message += ' $ python exlibris-cli.py book.epub new.epub exlibris.xhtml -s 1984' + '\n'
        message += ' $ python exlibris-cli.py book.epub new.epub exlibris.xhtml -s last' + '\n'
        message += ' $ python exlibris-cli.py book.epub new.epub exlibris.xhtml -s first -t last' + '\n'
        message += ' $ python exlibris-cli.py book.epub new.epub exlibris.xhtml -s ask -t ask' + '\n'
        message += ' $ python exlibris-cli.py book.epub new.epub res/exlibris.xhtml -d res/' + '\n'
        message += ' $ python exlibris-cli.py book.epub new.epub res/exlibris.xhtml -s first -t first -d res/' + '\n'
        message += ' $ python exlibris-cli.py book.epub new.epub exlibris.xhtml -r "owner=Alberto; phrase=Happy Birthday! "' + '\n'
        message += ' $ python exlibris-cli.py book.epub --spine' + '\n'
        message += ' $ python exlibris-cli.py book.epub --toc' + '\n'
        message += ' $ python exlibris-cli.py book.epub --remove' + '\n'
        message += ' $ python exlibris-cli.py book.epub new.epub --remove' + '\n'
        message += ' $ python exlibris-cli.py book.epub new.epub exlibris.xhtml -s ask -t ask --toc-string "Happy Birthday!"' + '\n'
        message += ' $ python exlibris-cli.py book.epub new.epub exlibris.xhtml --guide-string "Ex Libris"' + '\n'
        message += ' $ python exlibris-cli.py book.epub new.epub exlibris.xhtml -s first -t first --no-guide' + '\n'
        message += '' + '\n'
        message += 'LIMITATIONS' + '\n'
        message += ' 1) Your eBook input file must be "EPUB 2.0.1"-compliant,' + '\n'
        message += '    and your ex libris input file must be "XHTML 1.1 strict"-compliant,' + '\n'
        message += '    otherwise exlibris is not guaranteed to work properly and might produce an invalid EPUB file.' + '\n'                 
        message += ' 2) Currently exlibris includes the additional files specified by \'-d\' option' + '\n'
        message += '    using their extension to get the proper media-type field.' + '\n'
        message += '    Please name your file consistently.' + '\n'
        message += '    For example, do not name a JPEG image \'image.svg\' but use \'image.jpg\' or \'image.jpeg\'.' + '\n'
        message += '    (Use --supported-mimetype-identifiers to list all the supported extensions.)' + '\n'
        message += '' + '\n'
        message += 'AUTHOR' + '\n'
        message += ' Written by Alberto Pettarin, suggested by Luca "Luke" Calcinai.' + '\n'
        message += '' + '\n'
        message += 'REPORTING BUGS' + '\n'
        message += ' Please file a bug report using the GitHub issue tracker' + '\n'
        message += ' <https://github.com/pettarin/exlibris>' + '\n'
        message += '' + '\n'
        message += 'COPYRIGHT' + '\n'
        message += ' Copyright (c) 2012-2014 Alberto Pettarin.' + '\n'
        message += ' License GNU GPL version 3 <http://gnu.org/licenses/gpl.html>.' + '\n'
        message += ' This is free software: you are free to change and redistribute it.' + '\n'
        message += ' There is NO WARRANTY, to the extent permitted by law.' + '\n'
        message += '' + '\n'
    
    print message
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
def askForInsertionPointSpine(last):
    print "Please provide the insertion point of your ex libris in the spine."
    print "If you enter value n, your ex libris will be added as the n-th XHTML file in the eBook."
    print "Use %s to add your ex libris after the current last XHTML file." % (last+1)
    print "Please provide an integer between 1 and %s:" % (last+1)
    ip = sys.stdin.readline().strip()
    
    if (ip.isdigit()):
        ip = int(ip)
        if ((ip >= 1) and (ip <= last+1)):
            return str(ip)
    
    return None
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
def askForInsertionPointTOC(last):
    print "Please provide the insertion point of your ex libris in the TOC."
    print "If you enter value n, your ex libris will be added as the n-th entry of the eBook TOC."
    print "Use %s to add your ex libris after the current last entry." % (last+1)
    print "Please provide an integer between 1 and %s:" % (last+1)
    ip = sys.stdin.readline().strip()
    
    if (ip.isdigit()):
        ip = int(ip)
        if ((ip >= 1) and (ip <= last+1)):
            return str(ip)
    
    return None
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
def printSpineList(spineList, pageDictionary):
    maxIndex = int(spineList[-1][0])
   
    nod = len(str(maxIndex))

    print

    maxLen = 0
    for l in spineList:
        maxLen = max(maxLen, len(l[1]))

    for l in spineList:
        index = str(l[0]).zfill(nod)
        idref = l[1]
        pageFileName = pageDictionary.get(idref, 'UNKNOWN')
        print "%s  %s  %s" % (index, idref.ljust(maxLen), pageFileName)

    print
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
def printTOCList(tocList, pageDictionary):
    maxIndex = int(tocList[-1][0])
   
    nod = len(str(maxIndex))

    print

    maxLen = 0
    for l in tocList:
        maxLen = max(maxLen, len(l[1]))

    for l in tocList:
        index = str(l[0]).zfill(nod)
        text = l[1]
        spaces = " " * (l[2] * 2)
        print "%s%s%s" % (index, spaces, text.ljust(maxLen))

    print
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###


### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
def main():

    # constants
    workingDirectory = "tmp"
    tmpEPUB = "tmp.epub"

    # get command line arguments
    inputEPUB, outputEPUB, inputXHTML, insertionPointSpine, insertionPointTOC, inputDirectory, keepTMP, userReplacementStrings, exlibrisGuideString, exlibrisTOCString, includeInGuide = parseArguments(sys.argv)

    try:
        # print reading message
        printInfo("Reading your %s eBook " % (inputEPUB))
        
        # remove already present exlibris
        removeExLibris(inputEPUB, tmpEPUB)
        
        # create exlibris instance
        producer = exlibris()
        producer.initialize(tmpEPUB, outputEPUB, inputXHTML, insertionPointSpine, insertionPointTOC, inputDirectory, workingDirectory, userReplacementStrings, exlibrisGuideString, exlibrisTOCString, includeInGuide)

        # ask for insertion point spine
        if (insertionPointSpine == 'ask'):
            lastPageIndex = producer.getLastInsertionPointSpine()
            
            spineList = producer.getSpineList()
            pageDictionary = producer.getPageDictionary()
            printInfo("The spine of your eBook contains the following pages:")
            printSpineList(spineList, pageDictionary)
            
            ip = None
            while (producer.checkInsertionPointSpine(ip) == None):
                ip = askForInsertionPointSpine(lastPageIndex)
            producer.setInsertionPointSpine(int(ip))
            insertionPointSpine = int(ip)
        printInfo("Adding your ex libris %s as the %s element of the spine..." % (inputXHTML, insertionPointSpine))
        
        # ask for insertion point TOC
        if (insertionPointTOC == 'ask'):
            lastPageIndex = producer.getLastInsertionPointTOC()
            
            tocList = producer.getTOCList()
            pageDictionary = producer.getPageDictionary()
            printInfo("The TOC of your eBook consists of the following entries:")
            printTOCList(tocList, pageDictionary)
            
            ip = None
            while (producer.checkInsertionPointTOC(ip) == None):
                ip = askForInsertionPointTOC(lastPageIndex)
            producer.setInsertionPointTOC(int(ip))
            insertionPointTOC = int(ip)
        printInfo("Adding your ex libris %s as the %s element of the TOC..." % (inputXHTML, insertionPointTOC))

        # actually insert the ex libris 
        producer.insertExLibris()
        
        # output
        producer.createNewEPUB()

        # remove tmp dir
        if (keepTMP):
            printInfo("Skipping deleting the temporary directory %s" % (workingDirectory))
        else:
            producer.clean()

        # remove tmp EPUB
        os.remove(tmpEPUB)

        # print done message
        printInfo("Congratulations, your eBook %s has a nice ex libris now!" % (outputEPUB))

    except Exception as msg:
        printErrorUsageAndExit(msg.args[0])
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###




### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###
if __name__ == '__main__':

    reload(sys)
    sys.setdefaultencoding("utf-8")
    
    main()
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ###


