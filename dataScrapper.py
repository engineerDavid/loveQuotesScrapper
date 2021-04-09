import requests
import re
from bs4 import BeautifulSoup
import json
my_dict = {}
quotesCounts =0 
for r in range(100):
    
    URL = 'https://www.goodreads.com/quotes/tag/love?page={}'.format(r+1)
    print(URL)
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'lxml')

    #Looks for all the dividers which contain the quoteText class
    quotes = soup.find_all('div', attrs={"class": "quoteText"})


    UnformattedQ =[]

    #used to keep track of all the data

    for quote in quotes:
        UnformattedQ.append(str(quote))

    #get rid of all the extra html elements in string
    def cleanhtml(raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext

    CleanQ = list(map(cleanhtml,UnformattedQ) )



    def dataExtraction(CleanQuotes, quotesCounts):

        for quoteNum in range(len(CleanQuotes)):
            
            string = CleanQuotes[quoteNum]
            
            try:
                #get rid of some extra text that is not needed
                quote = string[:string.index("//<![CDATA[")]
                #get the author from the html tag
                author = re.search('([^―]*$)', quote)
                author = author.group(1)
                author=''.join(author.split())
                #used to get the quote text betweeen the qutation marks
                quote = re.search('“(.*?)”', quote)
                try:
                    quote = quote.group(1)
                except:
                    print(quote)
                    continue
               #adds the quotes to dict 
                my_dict[quotesCounts+quoteNum] = {'Quote': quote, 'Author':author}
                
                
                
                
            except:
                #the website has the first 1-3 quotes and authors generted diffrently so this is used to account for the outliers
                quote = re.search('“(.*?)”', string)
                author = re.search('([^―]*$)', string)
                author = author.group(1)
                author=''.join(author.split())
                quote = quote.group(1)
                
                my_dict[quotesCounts+quoteNum] = {'Quote': quote, 'Author':author}
                continue
        return my_dict
  
    dataExtraction(CleanQ, quotesCounts)
    #there are 30 quotes per page and need update the count
    quotesCounts = quotesCounts + 30

#only uncoment when you are ready to save the data to a json file
# with open('Sample.json', 'w') as fp:
#     json.dump(my_dict, fp)



