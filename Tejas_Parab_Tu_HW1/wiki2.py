import urllib.request
from bs4 import BeautifulSoup
from collections import OrderedDict
import re
import time

counter = 0


def crawl_all(start_url, keyword):
    time.sleep(1)
    seed = urllib.request.urlopen(start_url).read()
    soup = BeautifulSoup(seed, "html.parser")
    file = open("crawl_all"+".txt", 'a')
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


def rain_check(url, key):
    kl = str(key).lower()
    ku = str(key).upper()
    kt = str(key).title()
    kl0 = kl[0]
    ku0 = ku[0]

    if kl in url or kt in url or ku in url:
        if re.search("/" + ku0, url) or re.search("/" + kl0, url) or re.search("_" + ku0, url) or re.search("_" + kl0,url):
            return True
        else:
            return False
    else:
        return False

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
    keyword = "rain"
    global counter
    depth1 = []
    depth1 = crawl_all(start_url, keyword)
    d1NotDup = remove_dup(depth1)
    temp = []
    depth2 = []
    visited = ["https://en.wikipedia.org/wiki/Tropical_cyclone"]
    for items in d1NotDup:                                                            #depth 1
        if not items in visited:
            if rain_check(str(items), keyword):
                temp = crawl_all(str(items), keyword)
                unique_list = list(OrderedDict.fromkeys(temp))
                depth2.append(unique_list)
                visited.append(str(items))
                counter = counter + 1
                print(counter)
                print(str(items))
                raw_doc(str(items))


    fl = combined_list(depth2)
    f = open("flat2.txt", "w")
    for link in fl:
        f.write(str(link)+"\n")

    d2NotDup = remove_dup(fl)                                                         #depth 2
    depth3 = []
    for items in d2NotDup:
        if not items in visited:
            if rain_check(str(items), keyword):
                temp = crawl_all(str(items), keyword)
                unique_list = list(OrderedDict.fromkeys(temp))
                depth3.append(unique_list)
                visited.append(str(items))
                counter = counter + 1
                print(counter)
                print(str(items))
                raw_doc(str(items))


    fl2 = combined_list(depth3)
    f2 = open("depth2.txt","w")
    for url in fl2:
        f2.write(str(url)+"\n")


    d3NotDup = remove_dup(fl2)                                                       #depth3
    depth4 = []
    for items in d3NotDup:
        if not items in visited:
            if rain_check(str(items), keyword):
                temp = crawl_all(str(items), keyword)
                unique_list = list(OrderedDict.fromkeys(temp))
                depth4.append(unique_list)
                visited.append(str(items))
                counter = counter + 1
                print(counter)
                print(str(items))
                raw_doc(str(items))


    fl3 = combined_list(depth4)
    f3 = open("depth3.txt", "w")
    for url in fl3:
        f3.write(str(url)+"\n")


    d4NotDup = remove_dup(fl3)                                                           #depth_4
    depth5 = []
    for items in d4NotDup:
        if not items in visited:
            if rain_check(str(items), keyword):
                temp = crawl_all(str(items), keyword)
                unique_list = list(OrderedDict.fromkeys(temp))
                depth5.append(unique_list)
                visited.append(str(items))
                counter = counter + 1
                print(counter)
                print(str(items))
                raw_doc(str(items))

    fl4 = combined_list(depth5)
    f4 = open("depth4.txt", "w")
    for url in fl4:
        f4.write(str(url)+"\n")


    d5NotDup = remove_dup(fl4)                                                           #depth_5
    depth6 = []
    for items in d5NotDup:
        if not items in visited:
            if rain_check(str(items), keyword):
                temp = crawl_all(str(items), keyword)
                unique_list = list(OrderedDict.fromkeys(temp))
                depth6.append(unique_list)
                visited.append(str(items))
                counter = counter + 1
                print(counter)
                print(str(items))
                raw_doc(str(items))


    fl5 = combined_list(depth6)
    f5 = open("depth5.txt", "w")
    for url in fl5:
        f5.write(str(url) + "\n")


    d6NotDup = remove_dup(fl5)                                                              #depth6
    depth7 = []
    for items in d6NotDup:
        if not items in visited:
            if rain_check(str(items), keyword):
                temp = crawl_all(str(items), keyword)
                unique_list = list(OrderedDict.fromkeys(temp))
                depth7.append(unique_list)
                visited.append(str(items))
                counter = counter + 1
                print(counter)
                print(str(items))
                raw_doc(str(items))
                if counter == 1000:
                    break

    crawled = open("crawledpages2.txt", "w")
    for url in visited:
        crawled.write(str(url) + "\n")


main_crawler()


