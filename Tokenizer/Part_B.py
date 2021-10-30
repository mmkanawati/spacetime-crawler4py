import re
import sys

import Part_A

#Runtime complexity: O(n), since making both lists into sets are O(n) + O(n) = O(n)
# and finding the intersection of sets O(min(m, n)) let n be m >= n = O(n), which just equals O(n)
def mutualWords(List_token_one, List_token_two):   #returns the number of common words between file 1 and file 2
    unique_1 = set(List_token_one)
    unique_2 = set(List_token_two)

    common = unique_1.intersection(unique_2)    #finds the intersection of both sets
    #print(common)
    print(len(common))


if __name__ == "__main__":
    fileOne = Part_A.tokenize(sys.argv[1]) 
    fileTwo = Part_A.tokenize(sys.argv[2])
    mutualWords(fileOne, fileTwo)
