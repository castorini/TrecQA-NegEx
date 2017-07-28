# TrecQA-NegEx


## Prepare TrecQA DataSet 
Please refer to: https://github.com/castorini/data/tree/master/TrecQA

After parsing the TrecQA dataset, the `data/` directory contains the following splits in a pseudo-XML format:

+ `TRAIN.xml`
+ `TRAIN-ALL.xml`
+ `DEV.xml`
+ `TEST.xml`


Then extract answers for all the questions/answers in the train-all folder: 
```python extractAnswer.py ```
It will extract all the questions/answers from TrecQA train-all set and tranfer them to TREC topic xml format.


##  Index and extract the raw documents from TREC 8-13

1. Download TREC 8-13 datasets to `QAData/` folder. Unfortunately, we will not provide the TREC 8-13 dataset. Please refer to http://trec.nist.gov/data/qa.html and find the corresponding resources to download.

2. Install Anserini. Please refer to: https://github.com/castorini/Anserini

3. Build Index for TrecQA documentes set:
```
/path-to-Anserini/target/appassembler/bin/IndexCollection -collection TrecCollection -generator JsoupGenerator -input  ./QAData/  -index ./QAindex  -threads 32

```
4. Extract every single document from `QAData/` folder to `QADataFile/`. 
``` 
python splitTRECDoc.py --input=QAData/ --output=QADataFile/ 
```



## Retrieve documents and rank sentences  

1. Ranking documents using BM25 for all the answers/questions in train-all set:

```
 sh /path-to-Anserini/target/appassembler/bin/SearchWebCollection -topicreader Trec -index ./QAindex -bm25  -topics allQAAnswers.topics.xml -output QAAns.bm25.txt
```

2. Calculate the shingle matching scores for each document with corresponding question/answer.
```
python shingleDistance.py --BM25Run=QAAns.bm25.txt --queryList=allQAAnswers.topics.list > shingledist.qaans.list
```

3. Select the document which has the lowest shingle matching scores with each question/answer.
```
python selectLowestShingleDist.py --input=shingledist.qaans.list > shingledist.ans.doc.pair.top1.list
```

4.Select the sentences in the document with the lowest shingle matching scores matching the question/answer. 
```
python splitSentence.py shingledist.ans.doc.pair.top1.list splitDoc
```