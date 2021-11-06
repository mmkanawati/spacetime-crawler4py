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

            print(line)
            contents = line.split(" ")
            count = int(contents[-1])
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

            if ("ics.uci.edu") in url and (not "informatics.uci.edu" in url):

                parsed = urlparse(url)
                #subDomain[parsed.scheme + "://" + parsed.netloc] += 1
                subDomain[parsed.netloc] += 1

            line = file.readline()
            
    #for key,value in subDomain.items():
        #print(f"{key}, {value}")

    #print("subdomain done")
    return sorted(subDomain.items())

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

    with open("urlWordCount.txt", "r") as file:

        line = file.readline()

        while line:

            url = line.split(" ")[0]

            f = requests.get(url)

            soup = BeautifulSoup(f.text, 'html.parser')               
            text = soup.get_text()

            words = text.replace("_", " ")
            words = re.split("\W+", words.strip())

            for word in words:
                word = word.lower()

                if not word in stopWords and len(word) > 1 and word.isalnum():

                    wordFreq[word] += 1     

            sortedDict = sorted(wordFreq.items(), key=lambda x: x[1], reverse=True)
            sortedDict = sortedDict[:100]
            tempDict = dict(sortedDict)

            wordFreq = defaultdict(int, tempDict)

            #print("next file", wordFreq)

            line = file.readline()

    sortedFreq = sorted(wordFreq.items(), key=lambda x: x[1], reverse=True)

    f.close()
    return sortedFreq[:50]

if __name__ == '__main__':
    with open("reportFile.txt", "w") as file:
        file.write("Names: Lauren Pamintuan, Andrew Yusuf, Yocelyne Hernandez, Mohammad Kanawati\n")
        file.write("1. Number of Unique Pages: " + uniquePages())
        file.write("2. Page with most amount of words: " + maxWord() + "\n")
        #file.write("3. 50 Most common words: " + commonWords())
        file.write("4. Subdomains: ")
        sub = subDomains()
        for key,value in sub.items():
            file.write(f"{key}, {value}\n")
        file.write("Subdomain count: " + str(len(sub)))

    commonWords()