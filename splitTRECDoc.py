#!/usr/bin/env python
# -*- coding: UTF-8  -*-

"""docstring
"""

__revision__ = '0.1'

import sys,os
import getopt
import gzip
import unlzw

# python splitTRECDoc.py --input=test/ --output=QAData/

def usage():
    print """python yourFile.py
    --help
    --baseline=baseline dump
    --new=new dump
    --topic=topic id
    --maxn=max N
    """

def error():
    usage()
    sys.exit(-1)

def cmdProcess(argv):
    myArgs={
        "defaulArgument1":"",
    }
    try:
        opts, args = getopt.getopt(argv,"h",["help","input=","output="])
    except getopt.GetoptError:
        error()
    for opt, arg in opts:
        if opt in ("--help","-h"):
            usage()
            sys.exit()
        else:
            opt="".join(opt[2:])
            myArgs[opt]=arg
    return myArgs




if __name__=="__main__":

    argvNum=1
    if len(sys.argv)<=argvNum:
        error()
    myArgs=cmdProcess(sys.argv[1:])

    input=myArgs['input']
    output =myArgs['output']

    for root, dirnames, filenames in os.walk(input):
        for filename in filenames:
            # Read .z file
            if '.' in filename and 'z' in filename:
                f = open(os.path.join(root, filename), 'r')
                compressed_data = f.read()
                file_content = unlzw.unlzw(compressed_data)
            else:
                f = open(os.path.join(root, filename), 'r')
                file_content = f.read()

            print filename

            docContent = ""
            docNo=""
            for line in file_content.split('\n'):
                if "<DOC>" in line:
                    docContent = ""

                docContent= docContent+ line +'\n'
                if "</DOCNO>" in line:
                    docNo = (docContent.split('<DOCNO>')[1]).split('</DOCNO>')[0].strip()

                    # print docNo
                
                if "</DOC>" in line:
                    # print filename
                    if docNo != "":
                        writeF = open(output+'/'+docNo, 'w')
                        # sentence = unicode(sentence.strip(), errors='ignore')
                        writeF.write(docContent.strip())
                        writeF.close()
             
                