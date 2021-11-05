import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import urllib.request as urllib
import pickle



def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    #parsed = urlparse(url)
    #parsed.fragment = ""

    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    url_links = []

    if resp.status == 200 and resp.raw_response and is_valid(resp.raw_response.url):
        
        soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
        text = soup.get_text()

        #Pages with high textual informational content (based on text)
        if len(text) >= 1300:

            numberOfWords = wordCount(text)

            with open("urlWordCount.txt", 'a') as file:
                
                file.write(url + " " + str(numberOfWords) + "\n")              #"cs.uci.edu: 10"

            for link in soup.find_all('a', href=True):
                
                link = link.get('href')

                if link != None:

                    link = link.split('#')[0]

                    url_links.append(link)

            
        return url_links

    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    else:
        #print("Status Error: ", resp.status)
        #print("Error: ", resp.error)
        return []

def canCrawl(url):

    domains = ["ics.uci.edu", "cs.uci.edu", "informatics.uci.edu", "stat.uci.edu", "today.uci.edu"]

    for domain in domains:
        if domain in url:
            return True

def wordCount(urlText):

    words = urlText.replace("_", " ")
    words = re.split("\W+", words.strip())
    
    return len(words)


def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        
        if parsed.scheme not in set(["http", "https"]):
            return False
        if not canCrawl(url):              #Call canCrawl to check whether we can crawl this url or not
            return False


        if parsed.path:         
            path = parsed.path.split("/")

            if len(path) > 2:
                for i in range(1, len(path) - 1):

                    if path[i] == path[i+1]:

                        return False

        if 'replytocom' in parsed.query: 
            return False

        if "people" in parsed.path:
            return False

        if "honors" in parsed.path:
            return False
        
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|ppsx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
