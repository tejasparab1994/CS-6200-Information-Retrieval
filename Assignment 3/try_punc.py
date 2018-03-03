import re

# def punctuation(list1): #removing punctuation using the regular expression
#     # mydata = []
#     # for data in list1:
#     #     mydata.append(data.text)
#     #print(list1)
#     random = []
#     for elements in list1:
#         try:
#             re.sub('\W(?=\s|$)', '', elements)
#             print(elements)
#         except:
#             pass
        #random.append(elements)



def remove fun():
    file = open("try.txt", 'r')
    f = file.readlines()
    links = [x.strip("\n") for x in f]
    parts = []
    print(links)
    for single_elements in links:
        oyp = re.sub('\W(?=\s|$)', '', single_elements)
    print(oyp)
    #print(oyp)

main_fun()