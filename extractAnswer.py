import re
import os
import numpy as np
import cPickle
import subprocess
from collections import defaultdict



UNKNOWN_WORD_IDX = 0

xml='''<top>

<num> Number: %s

<title> %s

<desc> Description:

<narr> Narrative:

</top>


'''


def load_data(fname):
    lines = open(fname).readlines()
    qids, questions, answers, labels = [], [], [], []
    num_skipped = 0
    prev = ''
    qid2num_answers = {}
    for i, line in enumerate(lines):
        line = line.strip()

        qid_match = re.match('<QApairs id=\'(.*)\'>', line)

        if qid_match:
            qid = qid_match.group(1)
            qid2num_answers[qid] = 0

        if prev and prev.startswith('<question>'):
            question = line.lower().split('\t')

        label = re.match('^<(positive|negative)>', prev)
        if label:
            label = label.group(1)
            label = 1 if label == 'positive' else 0
            answer = line.lower().split('\t')
            # if len(answer) > 60:
            #   num_skipped += 1
            #   continue
            labels.append(label)
            answers.append(answer)
            questions.append(question)
            qids.append(qid)
            qid2num_answers[qid] += 1
        prev = line
    # print sorted(qid2num_answers.items(), key=lambda x: float(x[0]))
    print 'num_skipped', num_skipped
    return qids, questions, answers, labels




if __name__ == '__main__':

    stoplist = None


    train = 'data/train.xml'
    train_all = 'data/train-all.xml'
    # train_files = [train, train_all]
    train_files = [train_all]
    for train in train_files:
        print train

    train_basename = os.path.basename(train)
    name, ext = os.path.splitext(train_basename)
    # outdir = '{}'.format(name.upper())
    # print 'outdir', outdir


    # all_fname = train
    all_fname = "/tmp/trec-merged.txt"
    files = ' '.join([train])
    subprocess.call("/bin/cat {} > {}".format(files, all_fname), shell=True)

    # qids, questions, answers, labels = load_data(all_fname, stoplist)
    qids, questions, answers, labels = load_data(all_fname)



    writeAnsF = open("allQAAnswers.topics.xml",'w')
    writeAnsListF = open("allQAAnswers.topics.list",'w')

    writeQueF = open("allQAQuestions.topics.xml",'w')
    writeQueListF = open("allQAQuestions.topics.list",'w')

    count = 0
    preQid = 0
    for qid, ans, que, label in zip( qids, answers, questions, labels):
        count += 1
        ansXml = xml%(count,' '.join([str(x) for x in ans]))
        writeAnsF.write(ansXml)
        writeAnsListF.write(qid+ '\t' +str(count)+ '\t'+str(label)  +'\t'+ ' '.join([str(x) for x in ans])+'\n')

        queXml = xml%(count,' '.join([str(x) for x in que]))
        writeQueF.write(queXml)
        writeQueListF.write(qid+ '\t' +str(count)+ '\t'+str(label)  +'\t'+ ' '.join([str(x) for x in que])+'\n')

    writeAnsF.close()
    writeAnsListF.close()

    writeQueF.close()
    writeQueListF.close()

