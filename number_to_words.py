#this code pertains to the following assignment:
#create a function number_to_words(), which takes as an argument a string representing a US phone
#number and which outputs a string which has transformed part or all of the phone
#number into a single "wordified" phone number that can be typed on a US telephone (for
#example, a valid output of number_to_words("1-800-724-6837") could be
#"1-800-PAINTER"). If you find it makes things simpler, feel free to constrain this function
#to only output "wordifications" in English.

#in this version, the code uses a list of 7 integers as input, not a string
#in this version, the code only searches for valid 7 letter words
#this version successfully locates PAINTER

import itertools
import nltk
nltk.download('words')
from nltk.corpus import words  # list of all words in the american english language
# https://www.datasciencebytes.com/bytes/2014/11/03/get-a-list-of-all-english-words-in-python/
# must install ntlk for this code to work
# https://www.nltk.org/
# sudo apt-get install python-numpy python-nltk

# a dictionary mapping digits with corresponding phone-letters
alphanumeric_dict = {"0": None,
                     "1": None,
                     "2": ('A','B','C'),
                     "3": ('D','E','F'),
                     "4": ('G','H','I'),
                     "5": ('J','K','L'),
                     "6": ('M','N','O'),
                     "7": ('P','Q','R','S'),
                     "8": ('T','U','V'),
                     "9": ('W','X','Y','Z')}

word_list_full = words.words() # 236,736 words

# for now we need to parse out all words longer than 7 letters, also capitalize everything
word_list_seven_letter_max = [word.upper() for word in word_list_full if len(word) <= 7]  
word_list_seven_letter_max.sort() # makes sure list is in alphabetical order
#print len(word_list_seven_letter_max) # 59,458 words


def word_searcher(letters_lists):
    # takes a list of lists of letter options ex: [['A','B','C'],['W','X','Y','Z'],...]
    # returns a list of possible words using one character from each list entry, in order
    
    # the current dictionary i am using, set it to words_list,
    # words list will then be trimmed down
    words_list = word_list_seven_letter_max
    
    # first delete all words without length != len(letters_list)
    # i.e. we are searching for words with a specific length
    word_length = len(letters_lists)    
    words_list = filter(lambda x: len(x) == word_length, words_list)
    
    # iteratively trim down the words_list, keeping only words matching the allowed criteria at each index
    for i in range(word_length):
        words_list = [filter(lambda x: x[i] == letter, words_list) for letter in letters_lists[i]]
        words_list = [item for sub_list in words_list for item in sub_list] #flattened list
 
    return words_list



# for now just work with 7 digits, forget about the 1-800 1-(XYZ)
# deal with string to integer conversion later
# assume a list of integers between and including 0-9 for now
def number_to_words(seven_digit_list):
    # takes input as a 7 digit list
    # returns a list of possible single-word or multiple-word options for the number
    
    # for now, the code only works for full 7-digit words
    
    # should convert to work with a string as input 
    # (as is specified by the problem prompt)

    # construct a list of lists
    # the sub_lists are the associated letters with a given digit
    # None is returned for digits 0 and 1 (see definition of alphanumeric_dict)
    letter_options_lists = [alphanumeric_dict.get(str(digit)) for digit in seven_digit_list]
    
    if not all(letter_options_lists):
        # enters here if there are None/False-y values in the list
        print "not all digits in phone number correspond to letters"
        print "no contiguous word is associated with the number"
        return None                                                  

    # at this point we have the basis to construct words
    
    # start by looking for seven letter words
    valid_words_list = word_searcher(letter_options_lists)                                      
    return valid_words_list                              


example_number = [7,2,4,6,8,3,7]  # can make the word "painter"
# we need to parse out all words longer than 7 letters, also capitalize everything
word_list_seven_letter_max = [word.upper() for word in word_list_full if len(word) <= 7]  
word_list_seven_letter_max.sort() # makes sure list is in alphabetical order
word_list = word_list_seven_letter_max

words_list = number_to_words(example_number)
for word in words_list:
    print word


