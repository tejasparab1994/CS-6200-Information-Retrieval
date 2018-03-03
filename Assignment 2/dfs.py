import urllib.request
from bs4 import BeautifulSoup
from collections import OrderedDict
import re
import time

counter = 0
max_depth = 6


def crawl_all(start_url, visited, depth):
    global counter
    #time.sleep(1)
    #print(max_depth)
    #print(depth)
    #print(start_url)
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
    visited.append(start_url)
    #print(visited)

    for link in unique_list:
        print(link)
        counter = counter + 1
        if counter == 1000:
            return
        print(counter)  #only printing and counter increase

    return unique_list

    #print(depth)
    unique_list_reversed = unique_list
    unique_list_reversed.reverse()
    temp = unique_list_reversed
    unique_list1 = url_recursion(unique_list, temp, visited, depth)
    unique_list.append(unique_list1)
    #print(unique_list)


def url_recursion(unique_list, temp, visited, depth):
    next_url = temp.pop()
    #print(unique_list)
    #print(next_url)
    #print(temp)
    if next_url == "https://en.wikipedia.org/wiki/Hurricane":
        next_url = temp.pop()
    if next_url not in visited:
        return unique_list.append(crawl_all(next_url, visited, depth+1))


def remove_dup(duplist):
    dup = []
    for items in duplist:
        if items not in dup:
            dup.append(items)
    return dup


def write_file(unique_list):
    file = open("links_skipped" + ".txt", 'a')
    for link in unique_list:
        file.write("\n")
        file.write(str(link))

    file.flush()
    file.close()


def main_crawler():
    start_url = "https://en.wikipedia.org/wiki/Tropical_cyclone"
    visited = []
    crawl_all(start_url, visited, depth=0)


main_crawler()