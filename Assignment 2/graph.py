import urllib.request
from bs4 import BeautifulSoup
from collections import OrderedDict
import re
import time

counter = 0

def crawl_all(start_url,Links):
    global counter
    # time.sleep(1)
    # print(max_depth)
    # print(depth)
    # print(start_url)
    print("entering crawl_all")
    start_req = urllib.request.urlopen(start_url).read()
    soup = BeautifulSoup(start_req, "html.parser")
    search_links = soup.findAll('a', attrs={'href': re.compile("^/wiki/")})
    scrapped_links = []

    for link in search_links:
        link1 = link.get('href')
        soup_link = str(link1)  # converting and storing in soup_link on scrapping the page

        # removing : and # links from the scrapped links
        if ":" not in soup_link and "#" not in soup_link and "Main_Page" not in soup_link:
            scrapped_links.append("https://en.wikipedia.org" + soup_link)
        else:
            continue
    crawled_list = list(OrderedDict.fromkeys(scrapped_links))
    del crawled_list[-1]
    unique_list = remove_dup(crawled_list)
    write_file(unique_list)
    print("leaving from crawl_all")
    return


def remove_dup(duplist):
    dup = []
    print("i am in dup_list")
    for items in duplist:
        if items not in dup:
            dup.append(items)
    return dup


def write_file(unique_list):
    counter = 1
    length = 0
    print("i am in write_file")
    file = open(str(counter) + ".txt", 'a')
    for link in unique_list:
        file.write("\n")
        file.write(str(link))
        counter = counter + 1
    file.flush()
    file.close()
    return

def main_crawler():
    with open('Task 1-E.txt', 'r') as f:
        Links = []
        Links = [line.strip() for line in f]
    print(str(Links) + "\n")
    # get_url : ListOfLinks -> ListOfLinks
    # GIVEN: A list of all links obtained using BFS
    # RETURNS: Lists of all links containing links of its page
    i = 0
    while (i < 2):
        print((Links[i]))
        crawl_all(Links[i], Links)
        i = i+1
main_crawler()