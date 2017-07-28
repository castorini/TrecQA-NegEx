import nltk.data
import fnmatch
import os
import sys

import string
import operator

import unicodedata
reload(sys)  
sys.setdefaultencoding('utf8')

def removeTag(data):
	cleanData = ''
	for word in data.split():
		if '<' and '>' in word:
			word = '. '
		cleanData = cleanData + word + ' '
	return cleanData


if __name__=="__main__":
	#  python splitSentence.py ~/TREC/classfication/Corpus/20ng ~/Project/20ngSentences
	tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

	input = sys.argv[1]
	output = sys.argv[2]


	ansDict = {}
	posAnsDict = {}
	with open("allQAAnswers.topics.list", 'r') as ansF:
		for line in ansF:
			ansId = line.split('\t')[1]
			text = line.split('\t')[3:]
			ansDict[ansId] = ' '.join(text)
			label = line.split('\t')[2]
			if label == '1':
				posAnsDict[ansId] = ' '.join(text)




	with open(input) as listF:
		for line in listF:
			ansId = line.split()[0]
			doc = line.split()[1]
			start = int(line.split()[3])
			end = int(line.split()[4])

			if ansId not in posAnsDict:
				continue

			# Print original answer
			answer = ansDict[ansId].lower().translate(None, string.punctuation)


			ansWordDict = {}
			ansLen = 0
			for word in answer.split():
				ansWordDict[word] = 1
				ansLen = ansLen + 1




			fp = open("QADataFile/"+doc)

			data = fp.read()

			
			data = removeTag(data)

			data = unicode(data.strip(), errors='ignore')
			

			count = 0

			maxScore = 0
			bestSent = ""
			bestIdx = 0

			sentList = []

			sentDict = {}
			for sentence in tokenizer.tokenize(data):
				sentenceASCII = unicodedata.normalize('NFKD', sentence).encode('ascii','ignore')
				sentence_data = sentenceASCII.lower().translate(None, string.punctuation)


				if len(sentence_data.strip()) == 0:
					continue


				sentList.append(sentence)

				# print sentence_data
				matchCnt = 0
				sentenceLen = 0
				for word in sentence_data.split():
					sentenceLen = sentenceLen + 1
					if word in ansWordDict:
						matchCnt = matchCnt+1

				curScore = 1.0* matchCnt/sentenceLen * matchCnt/ansLen


				sentDict[count] = curScore

					
				count = count + 1

			sorted_sentDict = sorted(sentDict.items(), key=operator.itemgetter(1),reverse=True)

			# print sorted_sentDict

			negativeIdx = 0

			if sorted_sentDict[0][1] >= 0.1:

				writeF = open(output+'/'+ansId+'.1.'+doc+'.'+str(sorted_sentDict[0][0]), 'w')
				# sentence = unicode(sentence.strip(), errors='ignore')
				writeF.write(sentList[sorted_sentDict[0][0]]) 
				negativeIdx = 1
				writeF.close()
			
			for idx in range(negativeIdx,min(negativeIdx+7,len(sorted_sentDict))):
				writeF = open(output+'/'+ansId+'.0.'+doc+'.'+str(sorted_sentDict[idx][0]), 'w')
				# sentence = unicode(sentence.strip(), errors='ignore')
				writeF.write(sentList[sorted_sentDict[idx][0]]) 
				writeF.close()


				
