from urllib.parse import urlparse
from collections import defaultdict

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

    subDomain = {}

    with open("urlWordCount.txt", "r") as file:

        line = file.readline()

        while line:

            url = line.split(" ")[0]

            if "ics.uci.edu" in url:

                parsed = urlparse(url)
                subDomain[parsed.scheme + "://" + parsed.netloc] += 1

            line = file.readline()
    
    for key,value in subDomain.items():
        print(f"{key}, {value}")

if __name__ == '__main__':
    print(maxWord())
    subDomain()