from collections import defaultdict
import os
from prettytable import PrettyTable
from collections import OrderedDict
from operator import itemgetter


def main():

    corpus = dict()
    # user input, based on the user selection, uni, bi or trigram works
    n = input("1. Unigram, 2. Bigram, 3. Trigram \n")
    # get all the files in the directory mentioned
    text_files = [f for f in os.listdir('/Users/tejasparab/Desktop/Python/Assignment 3/Part') if f.endswith('.txt')]
    text_files.reverse()
    if n == '1':
        unigram(text_files, n)
    if n == '2':
        bigram(text_files, n)
    if n == '3':
        trigram(text_files, n)

def unigram(text_files, n):
    words = []
    dict_words = defaultdict(list)
    for i in text_files:            #opens and reads the contents of a single file and enters the key:value information
                                    #in the dict_words, does so for the entire corpus passed.
        with open("Part/" + i, 'r') as f:
            val = f.readlines()
        #print(f.name)
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
    #print(dict_words)
    table_unigram(dict_words) #function call to the unigram table program and passing the dict_word as parameter
    #write_uni(dict_words)     #unigram.txt output file generated through this function


def table_unigram(dict_words):
    count = 0
    dict_table = {}
    dict_df = {}
    print(dict_words)
    for key, value in dict_words.items(): #this loop gets the cumulative frequency of the term in the entire corpus
        count = 0
        for val in value:
            count = count + val[1]
        dict_table[key] = count           #and stores the new value as a key:value pair in a new dictionary


    #print(dict_table)
    print(dict_table)
    #print(sorted(dict_table.items(), key= lambda  x:x[1]))
    newDict = OrderedDict(reversed(sorted(dict_table.items(), key= lambda  x:x[1])))
    print(newDict)


    file = open("unigramtfTable.txt", 'a', encoding="ascii",errors= "surrogateescape")      #write the table into a .txt file, READ THIS FILE IN PYCHARM FOR BEST RESULTS
    file.write("term -> tf" + '\n')
    for key, value in newDict.items():
        try:
            file.write(str(key) + '->' + str(value) + '\n')
        except:
            pass

    file.flush()
    file.close()

    for key, value in dict_words.items():
        df = []
        for val in value:
            try:
                df.append(val[0])               #since value for document id is available at 0th index in the list of values
            except:
                pass
        dict_df[key] = [df, len(df)]        #creating a key:value pair with the length of df since this would give us
                                            # how many document_ids are there

    print(dict_df)

    sort_dict_df = OrderedDict(sorted(dict_df.items()))

    sort_dict_df.pop('\n', None)
    file = open("unigramdfTable.txt", 'a')
    file.write("term -> docID -> df" + '\n')
    for k, v in sort_dict_df.items():
        try:
            file.write(str(k) + '->' + str(v[0]) + '->' + str(v[1]) + '\n') #as mentioned in the assignment format
        except:
            pass
    file.flush()
    file.close()


def write_uni(list1):
    file = open("unigram" + ".txt", 'a',encoding="ascii",errors= "surrogateescape")  # write unigram to unigram.txt file
    for k, v in list1.items():
        try:
            file.write(str(k) + '->' + str(v) + '\n\n') #as mentioned in the assignment format
        except:
            pass

    file.flush()
    file.close()


def bigram(text_files, n):
    words = []
    my_bigrams = []
    listoflist = []
    dict_words = defaultdict(list)
    for i in text_files:            #opens and reads the contents of a single file and enters the key:value information
                                    #in the dict_words, does so for the entire corpus passed.
        with open("Part/" + i, 'r') as f:
            val = f.readlines()
        print(f.name)
        text = ''.join(val)
        words.append(text.lower().split(" "))
        flat_words = combined_list(words)
        print(flat_words)
        while '' in flat_words:
            flat_words.remove('')

        for i in range(len(flat_words)-1): #-1 since we are checking the next element too here and would result into OutofBounds issue
            # check if the docid, count pair already present for the key
            if [os.path.splitext(os.path.basename(f.name))[0], flat_words.count(flat_words[i]) + flat_words.count(flat_words[i+1])] in dict_words[flat_words[i], flat_words[i+1]]:
                continue
            else:   #else append to the values
                dict_words[flat_words[i], flat_words[i+1]].append([os.path.splitext(os.path.basename(f.name))[0], flat_words.count(flat_words[i])+flat_words.count(flat_words[i+1])])

        words.clear() #clearing the word_list for the next iteration with a new file
    print(dict_words)
    write_bigram(dict_words)
    #table_bigram(dict_words) #function call to the bigram table program and passing the dict_word as parameter


def table_bigram(dict_words):  #works the same way as the unigram function to create table
    count = 0
    dict_table = {}
    dict_df = {}

    for key, value in dict_words.items():
        count = 0
        for val in value:
            count = count + val[1]
        dict_table[key] = count


    y =PrettyTable()
    y.field_names = ["term", "tf"]
    for key,value in dict_table.items():
        try:
            y.add_row([key,value])
        except:
            pass

    y = y.get_string(sortby="tf", reversesort=True)




    file = open("bigramtfTable.txt", 'a', encoding="ascii", errors= "surrogateescape")
    file.write(y)
    file.flush()
    file.close()

    for key, value in dict_words.items():
        df = []
        for val in value:
            try:
                df.append(val[0])
            except:
                pass
        dict_df[key] = [df, len(df)]


    x = PrettyTable()
    x.field_names = ["term", "docID", "df"]
    for key, value in dict_df.items():
        try:
            x.add_row([key, value[0], value[1]])
        except:
            pass

    x = x.get_string(sortby = "term")


    file = open("bigramdfTable.txt", 'a', encoding="ascii", errors= "surrogateescape")
    file.write(x)
    file.flush()
    file.close()


def write_bigram(list1):
    file = open("bigram" + ".txt", 'a', encoding="ascii", errors= "surrogateescape")
    for k,v in list1.items():
        try:
            file.write(str(k) + '->' + str(v) + '\n\n')
        except:
            pass

    file.flush()
    file.close()


def trigram(text_files, n):
    words = []
    my_bigrams = []
    listoflist = []
    dict_words = defaultdict(list)
    for i in text_files:
        with open("Part/" + i, 'r') as f:
            val = f.readlines()
        print(f.name)
        text = ''.join(val)
        words.append(text.lower().split(" "))
        flat_words = combined_list(words)
        print(flat_words)
        while '' in flat_words:
            flat_words.remove('')

        for i in range(len(flat_words)-2): #here we check the next 2 values too, hence len -2, or OutOfBounds issue
                            #here we check whether the docid,
            if [os.path.splitext(os.path.basename(f.name))[0], flat_words.count(flat_words[i]) + flat_words.count(flat_words[i+1]) + flat_words.count(flat_words[i+2])] in dict_words[flat_words[i], flat_words[i+1], flat_words[i+2]]:
                continue
            else:
                dict_words[flat_words[i], flat_words[i+1], flat_words[i+2]].append([os.path.splitext(os.path.basename(f.name))[0], flat_words.count(flat_words[i])+flat_words.count(flat_words[i+1])+flat_words.count(flat_words[i+2])])
        #print(flat_bigrams[0:2])
        words.clear()
    print(dict_words)
    write_trigram(dict_words)
    table_trigram(dict_words)



def table_trigram(dict_words):  #works the same as unigram and bigram table creation function, created separate for
                                #understanding better
    count = 0
    dict_table = {}
    dict_df = {}

    for key, value in dict_words.items():
        count = 0
        for val in value:
            count = count + val[1]
        dict_table[key] = count


    y =PrettyTable()
    y.field_names = ["term", "tf"]
    for key,value in dict_table.items():
        try:
            y.add_row([key,value])
        except:
            pass

    y = y.get_string(sortby = "tf", reversesort = True)



    file = open("trigramtfTable.txt", 'a', encoding="ascii",errors= "surrogateescape")
    file.write(y)
    file.flush()
    file.close()

    for key, value in dict_words.items():
        df = []
        for val in value:
            try:
                df.append(val[0])
            except:
                pass
        dict_df[key] = [df, len(df)]


    x = PrettyTable()
    x.field_names = ["term", "docID", "df"]
    for key, value in dict_df.items():
        try:
            x.add_row([key,value[0],value[1]])
        except:
            pass

    x = x.get_string(sortby = "term")


    file = open("trigramdfTable.txt", 'a', encoding="ascii",errors= "surrogateescape")
    file.write(x)
    file.flush()
    file.close()

def write_trigram(list1):
    file = open("trigram" + ".txt", 'a', encoding="ascii",errors= "surrogateescape")  # get filename without spaces
    for k,v in list1.items():
        try:
            file.write(str(k) + '->' + str(v) + '\n\n')
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