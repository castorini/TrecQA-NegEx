#!/usr/bin/env python
# -*- coding: UTF-8  -*-

"""docstring
"""

__revision__ = '0.1'

import sys,os
import getopt
import string


# python splitTRECDoc.py --input=test/ --output=QAData/

def usage():
    print """python yourFile.py
    --help
    --BM25Run=BM25 ranking results
    --queryList=Questions/Answers XML 
    """

def error():
    usage()
    sys.exit(-1)

def cmdProcess(argv):
    myArgs={
        "defaulArgument1":"",
    }
    try:
        opts, args = getopt.getopt(argv,"h",["help","BM25Run=","queryList="])
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

    input=myArgs['BM25Run']
    queryFile=myArgs['queryList']

    topicDict ={}

    with open(queryFile, 'r') as qF:
        for line in qF:
            tid = int(line.split('\t')[1])
            topic = line.split('\t')[3]
            topicDict[tid] = topic.lower().strip()


    # qrels =myArgs['qrels']
    # python wordDistance.py --BM25Run=QAAns.bm25.txt --queryList=allQAAnswers.topics.list 
    with open(input, 'r') as BM25F:
        for line in BM25F:
            tid = int(line.split()[0].strip())
            did = line.split()[2].strip()
            rank = line.split()[3].strip()

            topic = topicDict[tid].translate(None, string.punctuation).split()
            # print did

            wordPos ={}
            for queryWord in topic:
                wordPos[queryWord] = []

            if os.path.exists('./QADataFile/'+did):
                with open('./QADataFile/'+did, 'r') as docF:
                    doc_data = docF.read().lower().translate(None, string.punctuation)
                    pos = 0
                    for word in doc_data.split():

                        if word.strip() in topic:
                            wordPos[word.strip()].append(pos)
                            
                        pos = pos + 1

            posList = []

            matchCnt = 0
            for word in wordPos:
                if len(wordPos[word]) > 0:
                    matchCnt = matchCnt+1
                    posList.append(sorted(wordPos[word]))


            indexList = []
            for i in range(len(posList)):
                indexList.append(0)
            
            if len(indexList) == 0:
                continue

                
            gloabelMinSpan = sys.maxint
            gloabelLowIdx = 0
            gloabelHighIdx = 0
            while True:

                minIdx =0
                maxIdx =0
                minNum = sys.maxint
                maxNum = 0

                for i in range(len(posList)):
                    if posList[i][indexList[i]] < minNum:
                        minNum = posList[i][indexList[i]]
                        minIdx = i
                    if posList[i][indexList[i]] > maxNum:
                        maxNum = posList[i][indexList[i]]
                        maxIdx = i

                indexList[minIdx] = indexList[minIdx] +1


                if maxNum - minNum + 1 < gloabelMinSpan:
                    gloabelMinSpan = maxNum -minNum + 1
                    gloabelLowIdx = minNum
                    gloabelHighIdx = maxNum


                if indexList[minIdx] >= len(posList[minIdx]):
                    break

            print str(tid) +'\t'+ did + '\t'+rank + '\t'+str(gloabelLowIdx) + '\t'+str(gloabelHighIdx) + '\t'+str(gloabelMinSpan)+ '\t'+str(matchCnt) + '\t'+str(1.0*matchCnt*matchCnt/gloabelMinSpan) 

           


                    

                
                
