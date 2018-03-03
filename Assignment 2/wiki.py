import urllib.request
from bs4 import BeautifulSoup
from collections import OrderedDict
import re
import time

counter = 0


def crawl_all(start_url):
   # time.sleep(1)
    seed = urllib.request.urlopen(start_url).read()
    soup = BeautifulSoup(seed, "html.parser")
    file = open("depth1"+".txt", 'a')
    search_links = soup.findAll('a', attrs={'href': re.compile("^/wiki/")})
    scrapped_links = []

    for link in search_links:
        link1 = link.get('href')
        soup_link = str(link1)  # converting and storing in soup_link on scrapping the page

        if ":" not in soup_link and "#" not in soup_link and "Main_Page" not in soup_link:   # removing : and # links from the scrapped links
            scrapped_links.append("https://en.wikipedia.org"+soup_link)
        else:
            continue

    unique_list = list(OrderedDict.fromkeys(scrapped_links))
    del unique_list[-1]

    for link in unique_list:
        file.write("\n")
        file.write(str(link))

    file.flush()
    file.close()

    return unique_list


def raw_doc(url):
    global counter
    f = urllib.request.urlopen(url).read()
    file = open(str(counter) + ".txt", "w")
    file.write(str(f))
    file.close()


def remove_dup(duplist):
    dup = []
    for items in duplist:
        if items not in dup:
            dup.append(items)
    return dup


def combined_list(list):
    flat_list = []
    for sublist in list:
        for item in sublist:
            flat_list.append(item)

    return flat_list


def main_crawler():
    start_url = "https://en.wikipedia.org/wiki/Tropical_cyclone"
    global counter
    depth1 = []
    depth1 = crawl_all(start_url)
    d1NotDup = remove_dup(depth1)
    temp = []
    depth2 = []
    visited = ["https://en.wikipedia.org/wiki/Tropical_cyclone"]
    for items in d1NotDup:
        if not items in visited:
            temp = crawl_all(str(items))
            unique_list = list(OrderedDict.fromkeys(temp))
            depth2.append(unique_list)
            visited.append(str(items))
            print(visited)
            counter = counter + 1
            print(counter)
        raw_doc(str(items))
    fl = combined_list(depth2)
    f = open("flat.txt", "w")
    for link in fl:
        f.write(str(link)+"\n")

     d2NotDup = remove_dup(fl)
     depth3 = []
     for items in d2NotDup:
         if not items in visited:
             temp = crawl_all(str(items))
             unique_list = list(OrderedDict.fromkeys(temp))
             depth3.append(unique_list)
             visited.append(str(items))
             counter = counter + 1
             print(counter)
             raw_doc(str(items))
             if counter == 1000:
                 break

    crawled = open("crawledpages.txt","w")
    for url in visited:
        crawled.write(str(url)+"\n")


main_crawler()