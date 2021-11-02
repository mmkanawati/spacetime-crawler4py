from urllib.parse import urlparse
from collections import defaultdict
import requests
from bs4 import BeautifulSoup
import re

def maxWord():

    maxCount = 0
    maxUrl = ""

    with open("urlWordCount.txt", "r") as file:

        line = file.readline()

        while line: 

            contents = line.split(" ")
            count = int(contents[1])
            url = contents[0]

            if count > maxCount:
                maxCount = count
                maxUrl = url

            line = file.readline()

    return maxUrl

def subDomains():

    subDomain = defaultdict(int)

    with open("urlWordCount.txt", "r") as file:

        line = file.readline()

        while line:

            url = line.split(" ")[0]

            if "ics.uci.edu" in url and not "informatics.uci.edu" in url:

                parsed = urlparse(url)
                subDomain[parsed.scheme + "://" + parsed.netloc] += 1

            line = file.readline()
            
    for key,value in subDomain.items():
        print(f"{key}, {value}")

    print("subdomain done")

def uniquePages():

    pages = set()

    with open("urlWordCount.txt", "r") as file:

        line = file.readline()

        while line:

            url = line.split(" ")[0]
            
            link = url.split('#')[0]

            pages.add(link)

            line = file.readline()

    return len(pages)

def commonWords():

    wordFreq = defaultdict(int)
    f = open("stopWords.txt", "r")

    stopWords = f.read()
    #print(stopWords)

    with open("urlWordCount.txt", "r") as file:

        line = file.readline()

        while line:

            url = line.split(" ")[0]
            #print(url)

            f = requests.get(url)

            soup = BeautifulSoup(f.text, 'html.parser')               
            text = soup.get_text()

            words = text.replace("_", " ")
            words = re.split("\W+", words.strip())

            for word in words:

                if not word in stopWords:

                    wordFreq[word] += 1                    

            line = file.readline()

    sortedFreq = sorted(wordFreq.items(), key=lambda x: x[1], reverse=True)

    f.close()
    return sortedFreq[:50]

if __name__ == '__main__':
    print(maxWord(), "maxUrl")
    subDomains()
    print(commonWords())
    print(uniquePages())