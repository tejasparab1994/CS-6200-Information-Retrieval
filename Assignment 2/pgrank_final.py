from collections import defaultdict
from math import log, pow
import operator

perplexity = []
pageRank = {}
sinkNodes = []
d = 0.85
pageRankSorted = []
ILSorted = []
IL = {}
L = {}
P = []
inLinks_dict = {}
outLinks_dict = {}
newpageRank = {}
per =[]


def main():
    sinkNodes, inLinks_dict, L, IL, P, outLinks_dict = get_graph()
    print(calculatePagerank(sinkNodes, inLinks_dict, L, IL, P, outLinks_dict, perplexity, pageRank, newpageRank))

    pageRankSorted = sorted(pageRank.items(), key=operator.itemgetter(1), reverse=True)
    ILSorted = sorted(IL.items(), key=operator.itemgetter(1), reverse=True)
    print("\n Top 50 Pages Sorted by PageRank Values:\n")
    for i in range(50):
        print(pageRankSorted[i])
    file = open("G1_TOP_50" + ".txt", "w")
    for i in range(50):
        file.write(str(pageRankSorted[i]) + "\n")
    file.flush()
    file.close()
    print("\n Top 50 Pages Sorted by Inlink Count:\n")
    for i in range(50):
        print(ILSorted[i])


def calculatePagerank(sinkNodes, inLinks_dict, L, IL, P, outLinks_dict, perplexity, pageRank, newpageRank):
    N = len(P)
    for p in P:
        pageRank[p] = 1.0/N

    i = 0
    #print("perplexity values:")
    #print("P",P)
    while not isconverged(i, perplexity, pageRank):
        sinkPR = 0
        for p in sinkNodes:
            sinkPR += pageRank[p]
        for p in P:
            newpageRank[p] = (1.0 - d) / N
            newpageRank[p] += d * sinkPR / N
            for q in inLinks_dict[p]:
                newpageRank[p] += d * pageRank[q]/L[q]
        for p in P:
            pageRank[p] = newpageRank[p]
        i += 1
    #print("while loops end")
    return pageRank


def isconverged(i, perplexity, pageRank):
    change = 0
    count = 0
    perplexity.append(calculate_perplexity(i, perplexity, pageRank))
    if i > 0:
        change = abs(perplexity[i] - perplexity[i - 1])
        if change < 1 and count <= 4:
            count += 1
            return True
        else:
            return False
    else:
        return False


def calculate_perplexity(i, perplexity, pageRank):
    H = 0
    perplexity = 0
    for page in pageRank.keys():
        H += pageRank[page] * log(1/pageRank[page], 2)
       ##print(H)
    perplexity = pow(2,H)
    print(i+1, perplexity)
    per.append(perplexity)
    outputfile = open('Perplexity.txt', 'w')

    for j in range(len(per)):
        row = str(per[j]) + "\n"
        outputfile.write(row)
    outputfile.close()
    return perplexity


def get_graph():
    counter = 0  # no. of iterations
    inLinks = defaultdict(list)  # inLinkGraph data Structure
    outLinks = defaultdict(list)  # outLinkGraph data Structure
    nodes = []  # LIST OF Nodes in graph
    outLinks = {}

    # read, get graph in list
    with open("G1.txt") as f:
        lines = f.readlines()

    graph = []
    for item in lines:
        if "\n" in item:
            graph.append(item[:-1])
        else:
            graph.append(item)

    # create inLinkGraph
    for node in graph:
        everynode = node.split(" ")
        inLinks[everynode[0]] = everynode[1:]

    j = set()
    for k, v in inLinks.items():
        for l in v:
            j.add(l)

    some_dict = {}
    final_list = []
    #create outlinkGraph
    for l in j:
        f = []
        for k, v in inLinks.items():
            if l in v:
                f.append(k)
            else:
                pass
        some_dict = {l: f}
        final_list.append(some_dict)

    outLinks = final_list
    # the necessary values for PageRank Algorithm

    inLinks_dict.update(inLinks)
    #print("inLinks", inLinks_dict)
    for d in outLinks:
        outLinks_dict.update(d)
    #print("outlinks", outLinks_dict)
    P = list(inLinks_dict.keys())
    #print("P", P)
    for keys in inLinks_dict.keys():
        IL[keys] = len(inLinks_dict.get(keys))
    #print("IL", IL)
    for keys in outLinks_dict.keys():
        L[keys] = len(outLinks_dict.get(keys))
    #print("L", L)
    for key in L.keys():
        if L.get(key) == 0:
            sinkNodes.append(key)
    #print("sinknodes", sinkNodes)

    return sinkNodes, inLinks_dict, L, IL, P, outLinks_dict

if __name__ == '__main__':
    main()