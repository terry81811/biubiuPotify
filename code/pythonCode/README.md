Dependency map

Matlab

featureExtraction.m

Python scripts:

WordCount_reviews.py
bigram.py
allCapitalCount.py
countCapital.py
ratioPPwordCount.py
excSentenceCount.py
sentimentAnalysis.py
uniGram.py
codeTable.py


##

note: 
found bug
	1. datestr(C{6}) will return type character, which causes error when using unique
		solution: date = cellfun(@datestr, C{6},'un',0);
	2. NR.m and PR.m will have error when there are only positive/ negative reviews


package installed:

cant find module nltk

====

The problem may be that MATLAB is not seeing your PYTHONPATH, which normally stores Python libraries and modules. For custom modules, PYTHONPATH should also include the path to your custom folders.

You can try setting the value of PYTHONPATH from within a MATLAB running session:

PATH_PYTHON = '<python_lib_folder>' 
setenv('PYTHONPATH', PATH_PYTHON); % set env path (PYTHONPATH) for this session
system('python program.py'); 


http://stackoverflow.com/questions/30605179/why-cant-matlab-import-this-python-library

====

sentiment analysis require nltk.wordnet