import re
import sys

#Runtime complexity: O(n) where n is the number of lines there is in the text file
def tokenize(TextFilePath):  #returns a token list
    tokens = []
    
    with open(TextFilePath, "r", encoding="utf-8") as file:
        contents = file.readline().lower()          #reads line and applies lower case function
        
        while contents:                                     #will stop reading if there is no more to read from file
            match = re.findall(r"[a-z0-9]+", contents)      #finds alphanumeric tokens
            tokens.extend(match)
            contents = file.readline().lower()               #reads next line
            
    return tokens 

#Runtime complexity: O(n) where n is the number of elements in the token list
def computeWordFrequencies(List_token):    #counts the number of occurrences of each token
    frequencies = {}
    
    for word in List_token:                     #loop through the token list
        
        if word in frequencies:                 #if token in dictionary, increament if not, put it in dictionary
            
            frequencies[word] += 1
        else:
            frequencies[word] = 1
            
    return frequencies

#Runtime complexity: O(n log n), The built-in function uses a special version of merge sort, called Timsort, which runs in O(n log n)
def printFrequencies(Frequencies):     #prints out the word frequency count onto the screen
    sortedFreq = sorted(Frequencies.items(), key=lambda x: x[1], reverse=True)  #takes Frequencies makes it into tuple and key applys lambda function to sort by the value which is 1st index
    
    for word in sortedFreq:
        
        print(word[0], "-", word[1])


if __name__ == "__main__":
    x = tokenize(sys.argv[1])
    y = computeWordFrequencies(x)
    printFrequencies(y) 

