with open("Task 1-E.txt") as f:
    urls = f.readlines()

urls = [x.strip("\n") for x in urls]

writeFile = open("G1.txt", "w")

for url in urls:
    graph = []
    urlToCheck = str(url)[30:]
    graph.append(urlToCheck)
    for link in urls:
        index = urls.index(link)
        #print link
        with open("BSF/"+str(index+1)+".txt") as f:
            getLinks = f.readlines()
        finalLinks = [x.strip("\n") for x in getLinks]
        if str(url) in finalLinks:
            if str(urls[index])[30:] not in graph:
                graph.append(str(urls[index])[30:])
    #print graph
    checkForDuplicates = graph[1:]
    unique = []
    [unique.append(item) for item in checkForDuplicates if item not in unique]
    toPrint = []
    toPrint.append(graph[0])
    for item in unique:
        toPrint.append(item)
    print (toPrint)

    writeFile.write(" ".join(graph))
    writeFile.write("\n")

print ("Done")
