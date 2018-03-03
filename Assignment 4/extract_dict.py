from sys import exit
import ast
from collections import defaultdict
from collections import defaultdict
import os
from collections import OrderedDict

def main():

    corpus = dict()
    # user input, based on the user selection, uni, bi or trigram works
    # get all the files in the directory mentioned
    text_files = [f for f in os.listdir('/Users/tejasparab/Desktop/Python/Assignment 4/Para') if f.endswith('.txt')]
    text_files.reverse()
    unigram(text_files)


def unigram(text_files):
    words = []
    dict_words = defaultdict(list)
    for i in text_files:            #opens and reads the contents of a single file and enters the key:value information
                                    #in the dict_words, does so for the entire corpus passed.
        with open("Para/" + i, 'r') as f:
            val = f.readlines()
        print(f.name)
        text = ''.join(val)
        words.append(text.lower().split(" ")) #cross checking whether all terms lower yet again
        flat_words = combined_list(words)
        #print(flat_words)
        while '' in flat_words:
            flat_words.remove('')
        for entry in flat_words: #check if the docid, count pair already present for the key
            if [os.path.splitext(os.path.basename(f.name))[0], flat_words.count(entry)] in dict_words[entry]:
                continue
            else:               #else append to the values
                dict_words[entry].append([os.path.splitext(os.path.basename(f.name))[0], flat_words.count(entry)])
        words.clear()  #clearing the word_list for the next iteration with a new file
    print(dict_words)
    write_uni(dict_words)

def write_uni(dict_words):
    file = open("unigram" + ".txt", 'a', encoding="ascii",
                errors="surrogateescape")  # write unigram to unigram.txt file
    for k, v in dict_words.items():
        try:
            file.write(str(k), str(v))  # as mentioned in the assignment format
        except:
            pass

    file.flush()
    file.close()


def combined_list(list1):
    flat_list = []
    for sublist in list1:
        for item in sublist:
            flat_list.append(item)

    return flat_list


main()