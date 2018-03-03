import urllib.request
from bs4 import BeautifulSoup
from collections import OrderedDict
import re


def crawl_all(start_url):
   # time.sleep(1)
    seed = urllib.request.urlopen(start_url).read()
    soup = BeautifulSoup(seed, "html.parser")

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



    return unique_list


def remove_dup(duplist):
    dup = []
    for items in duplist:
        if items not in dup:
            dup.append(items)
    return dup

def main_crawler():
    seed = "https://en.wikipedia.org/wiki/Tropical_cyclone"
    links_seen = []
    tropical_cyclone = crawl_all(seed)
    links_seen.append(seed)
    #print(depth1)
    print("at depth 1", links_seen)
    print((tropical_cyclone[0]))

    hurricane_ambi = crawl_all(tropical_cyclone[0])
    links_seen.append(tropical_cyclone[0])
    #print(depth2)
    print("at depth 2", links_seen)
    print(hurricane_ambi[0])

    hurricane = crawl_all(hurricane_ambi[0])
    links_seen.append(hurricane_ambi[0])
    #print(hurricane)
    print("at depth 3", links_seen)
    print(hurricane[1])

    hurricane_isabel = crawl_all(hurricane[1])
    links_seen.append(hurricane[1])
    #print(depth4)
    print("at depth 4", links_seen)
    print(hurricane_isabel[0])

    extratropical_cyclone = crawl_all(hurricane_isabel[0])
    links_seen.append(hurricane_isabel[0])
    print(extratropical_cyclone)
    print("at depth 5", links_seen)
    print(extratropical_cyclone[0])

    pacific_ocean = crawl_all(extratropical_cyclone[0])
    links_seen.append(extratropical_cyclone[0])
    #print(depth6)
    print("at depth 6", links_seen)
    print(pacific_ocean[0])

    for item in extratropical_cyclone:
        if item not in links_seen:
            if len(links_seen) == 1000:
                break
            links_seen.append(item)
    print(links_seen)

    eye_cyclone = crawl_all(extratropical_cyclone[1])

    for item in eye_cyclone:
        if item not in links_seen:
            if len(links_seen) == 1000:
                break
            links_seen.append(item)
    print(links_seen)


    file = open("links" + ".txt", 'a')
    for link in links_seen:
        file.write("\n")
        file.write(str(link))
    file.flush()
    file.close()

    file = open("eye_cyclone" + ".txt", 'a')
    for link in eye_cyclone:
        file.write("\n")
        file.write(str(link))
    file.flush()
    file.close()

    for link in eye_cyclone:
        if not link in links_seen:
            next_depth = crawl_all(link)
        links_seen.append(next_depth[0])

    #print(links_seen)
main_crawler()