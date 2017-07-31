# TrecQA-NegEx
This repo contains the implementation of extracting high quality training examples for TrecQA dataset, described in the following paper:

+ Haotian Zhang, Jinfeng Rao, Jimmy Lin and Mark Smucker. Automatically Extracting High-Quality Negative Examples for Answer Selection in Question Answering. SIGIR 2017.


# Negative Example DataSet 
* We provided top k={1,3,5,7} negative examples for each (question,answer) pair in the TrecQA train-all set. The different examples sets locate in `NegExSets/` folder and are named as `splitDocNegTopk.tgz`.

* After you uncompress each NegExSet by ```tar zxvf splitDocNegTopk.tgz```, you will see our negative examples for each (question,answer) pair. Each negative example is one sentence which is extracted from the same document containing the answer. Each example is named as:

    * `ID of answer` + `relevance` + `ID of doc` + `ID of sentence` (Seperated by `.`)

* `ID of answer` is the ID of each answer. For train-all set of Trec-QA, there are 56082 (question,answer) pairs in total. The ID of the answers range from 1 to 56082.  
* `relevance` is the relevance of each extracted example answer. If the relevance is 1, this example is the answer itself. Otherwise, it is one of the top k negative examples of the answer.
* `ID of doc` is the ID of the document which contains the answer. All the negative examples sentences come from this document.
* `ID of sentence` is the ID of the extracted sentence. The range of ID is decided by the number of sentences in the document. It starts from 0. And 0th sentence means it is the first sentence of the document.
* For example, there is one negative example:`26877.0.FBIS4-45077.45`. The name of this example indicates that it is for the answer `26877`. The relevance is `0` so that it is a negative example. And it is the 46th sentence (ID of sentence starts from 0) of document `FBIS4-45077`. 

## Prepare TrecQA DataSet 
Please download the TrecQA Dataset and refer to: https://github.com/castorini/data/tree/master/TrecQA

After parsing the TrecQA dataset, the `data/` directory contains the following splits in a pseudo-XML format:

+ `TRAIN.xml`
+ `TRAIN-ALL.xml`
+ `DEV.xml`
+ `TEST.xml`


Then extract answers for all the questions/answers in the train-all folder: 

```$ python extractAnswer.py ```

It will extract all the questions/answers from TrecQA train-all set and tranfer them to TREC topic format.


##  Index and extract the raw documents from TREC 8-13

1. Download TREC 8-13 datasets to `QAData/` folder. Unfortunately, we will not publicly share the TREC 8-13 dataset. Please refer to http://trec.nist.gov/data/qa.html and find the corresponding resources to download.

2. Install Anserini. Please refer to: https://github.com/castorini/Anserini

3. Build Index for TrecQA documentes set:
```
/install-path-to-Anserini/target/appassembler/bin/IndexCollection -collection TrecCollection -generator JsoupGenerator -input  ./QAData/  -index ./QAindex  -threads 32

```
4. Extract every single document from `QAData/` folder into `QADataFile/`. 
``` 
$ python splitTRECDoc.py --input=QAData/ --output=QADataFile/ 
```



## Retrieve documents and rank sentences  

1. Ranking documents using BM25 for all the answers/questions in train-all set:

```
 sh /path-to-Anserini/target/appassembler/bin/SearchWebCollection -topicreader 
 Trec -index ./QAindex -bm25  -topics allQAAnswers.topics.xml -output QAAns.bm25.txt
```

2. Calculate the shingle matching scores between each retrieved document with its corresponding question/answer.
```
$ python shingleDistance.py --BM25Run=QAAns.bm25.txt --queryList=allQAAnswers.topics.list
> shingledist.qaans.list
```

3. Select the document which has the lowest shingle matching scores with each question/answer.
```
$ python selectLowestShingleDist.py --input=shingledist.qaans.list 
> shingledist.ans.doc.pair.top1.list
```

4.Select the sentences in the document with the lowest shingle matching scores matching the question/answer. 
```
$ python splitSentence.py shingledist.ans.doc.pair.top1.list splitDoc
```
