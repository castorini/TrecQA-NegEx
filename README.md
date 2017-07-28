# TrecQA-NegEx


## Prepare TrecQA DataSet 
Please refer: https://github.com/castorini/data/tree/master/TrecQA

Extract answers for all the answers in the train-all folder: 
```python extractAnswer.py ```
It will extract all the questions/answers from TrecQA train-all set and tranfer them to TREC topic xml format.

##  Index the raw documents 

1. Download TREC8-13 datasets to `QAData` folder according to http://trec.nist.gov/data/qa.html

2. Install Anserini: https://github.com/castorini/Anserini

3. Build Index for TrecQA documentes set:
```
/path-to-Anserini/target/appassembler/bin/IndexCollection -collection TrecCollection -generator JsoupGenerator -input  ./QAData/  -index ./QAindex  -threads 32

```

4. Rankding documents using BM25 for all the TrecQA answers/questions:

```
 sh /path-to-Anserini/target/appassembler/bin/SearchWebCollection -topicreader Trec -index ./QAindex -bm25  -topics allQAAnswers.topics.xml -output QAAns.bm25.trec.txt

```