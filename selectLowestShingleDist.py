#!/usr/bin/env python
# -*- coding: UTF-8  -*-

"""docstring
"""

__revision__ = '0.1'

import sys,os
import getopt
import gzip
import unlzw
# import zlib
# import matplotlib.pyplot as plt
# import matplotlib.ticker as mtick

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
        opts, args = getopt.getopt(argv,"h",["help","input="])
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
  
    scoreDict = {}
    docDict = {}
    restDict={}
    with open(input, 'r') as BMF:
    	for line in BMF:
            tid = line.split()[0]
            did = line.split()[1]
            score = float(line.split()[7])
            if tid in scoreDict:
                if scoreDict[tid] < score:
                    scoreDict[tid] = score
                    restDict[tid] = line.split()[2:]
                    docDict[tid] = did
            else:
                scoreDict[tid] = score
                restDict[tid] = line.split()[2:]
                docDict[tid] = did

    for topic in docDict:
        print topic +'\t'+docDict[topic]+'\t'+'\t'.join(restDict[topic])


                    

                
                
