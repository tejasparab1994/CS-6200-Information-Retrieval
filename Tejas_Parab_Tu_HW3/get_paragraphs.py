import requests
from bs4 import BeautifulSoup
import re



def get_paras(count, start_url): #gets the text content of the page
    seed = requests.get(start_url)
    soup = BeautifulSoup(seed.content, "html.parser")
    search_para = soup.find_all(["p", "h1", "h2", "h3", "h4"])
    mydata = []

    for data in search_para:
        mydata.append(data.text) #get the data in text format#cleaning the data further

    utffolded = caseFolding(mydata) #list obtained after caseFolding operation
    utfclean = punctuation(utffolded) #list obtained after punctuation
    print(utfclean)

    write(soup, utfclean, count)

def caseFolding(nonutfTrial): #casefolding the words within the list
    trial = []
    for word in nonutfTrial:
        trial.append(word.lower())

    return trial


def punctuation(list1): #removing punctuation using the regular expression
    random = []
    for elements in list1:
        random.append(re.sub('\W(?=\s|$)', '', elements))
    for index, item in enumerate(random):
        random[index] = item.replace('[', '').replace(']', '').replace(',','').replace('{','').replace('}','').replace('(','').replace('\\', '')
    for index, item in enumerate(random):
        random[index] = item.replace('“', '').replace('"', '').replace('”', '').replace('\n', '').replace(')', '').replace('ˈ', '')

    return random


def write(soup, list1, count):   #write the file into the Para directory
     file = open("Para/"+ str(count+1) + ".txt", 'a') #get filename without spaces
     for single in list1:  #since the elements have been stored as list of strings
         try:
            file.write(str(single)+" ")
         except:
             pass
     file.write("\n")


def main_paras():
    links=[]
    file = open("Task 1-E.txt", 'r') #runs the the task1 file
    links  = file.readlines()
    links = [x.strip("\n") for x in links]
    count = 0
    for link in links:
        try:
            get_paras(count, link)
            count  = count + 1
        except:
            pass

main_paras();