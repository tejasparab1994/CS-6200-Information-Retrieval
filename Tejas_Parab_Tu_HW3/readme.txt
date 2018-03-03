1) Setup needed: I have used python 3.6.1 and Pycharm to write the code. Certain libraries
   need to be added in order to run the code.

2) Libraries used: import requests
		   from bs4 import BeautifulSoup
		   import re
		   from collections import defaultdict
		   import os
		   from collections import OrderedDict

3) - These are the libraries used in the code and would be required for successful 	       execution.

4) Top right green button to run the file.

5) The wikipedia pages consist of certain texts that are encoded in utf-8 format which when opened in certain text editors appear decoded whereas appear encoded in certain text editors, such characters have been ignored and not added to the indexing lists.

6) The get_paragraphs.py file would have to be executed in order to get the necessary text files as per the punctuation and casefolding done. This would be the output of task 1

7) Initially I had used the prettyTable library to get the tables for unigram, bigram and trigram. Since there are lots of contents to be added the table generated using the prettyTable library appeared disoriented. In order to get around this issue I had to fall back to the basic approach of iterating over individual elements of the dictionary and mapping their key:value pairs into the file.

8) The file names obtained from get_paragraphs are numbered through 1 to 1000. But the links they associate with have been provided through the 'map.txt' file.

9) In order to accomodate the multiple docID's associated with a term, the values part of dictionary had to be implemented as a list of values.

10)Even after removing the punctuations there were certain empty spaces left which weren't detected by the punctuation handler in get_paragraphs.py but have been later removed in the indexer.py file.

11) In order to run the code, there are certain places where the directory has to be mentioned, currently my submission consists of the directories associated with my system.
For successful execution, the directory name should be modified as necessary.
