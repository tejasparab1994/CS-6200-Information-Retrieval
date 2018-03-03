import urllib.request
from bs4 import BeautifulSoup
from collections import OrderedDict
import re

def crawl_all(start_url):
    # time.sleep(1)
    try:
        seed = urllib.request.urlopen(start_url).read()
        soup = BeautifulSoup(seed, "html.parser")

        search_links = soup.findAll('a', attrs={'href': re.compile("^/wiki/")})
        scrapped_links = []
    except:
        pass

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


# READ URLs FROM FILE

with open("DFS_Links.txt") as f:
    urls = f.readlines()

urls = [x.strip("\n") for x in urls]

urlCount = len(urls)

for i in range(0,urlCount):
    urlsFromEachPage = crawl_all(urls[i])
    writeFile = open("DFS/"+str(i+1)+".txt", "w")
    listWithWiki = [link for link in urlsFromEachPage]
    writeFile.write("\n".join(listWithWiki))
    print(urls[i])