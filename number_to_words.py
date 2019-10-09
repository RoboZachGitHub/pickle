#this code pertains to the following assignment:
#create a function number_to_words(), which takes as an argument a string representing a US phone
#number and which outputs a string which has transformed part or all of the phone
#number into a single "wordified" phone number that can be typed on a US telephone (for
#example, a valid output of number_to_words("1-800-724-6837") could be
#"1-800-PAINTER"). If you find it makes things simpler, feel free to constrain this function
#to only output "wordifications" in English.

#this version successfully locates PAINTER
#this version only looks ofr 7-letter words
#this version returns no solution for any number with a 0 or 1

import re
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

def is_number_valid(digits_list):
    # tests the digits list for validity, returns True of False
    # for now, only test if phone number is 7, 10, or 11 digits long
    # other conditions could be implemented
    len_digits_list = len(digits_list)
    if (len_digits_list != 7 and \
        len_digits_list != 10 and \
        len_digits_list != 11):
        print 'phone number seems invalid, length is not 7, 10, or 11 digits.\n'
        return False
    else:
        return True
    

def preparation_routine(phone_number_string):
    # checks if the number is valid
    # converts the format into a list of integers
    # separates pre-fix/area code from 7 digit phone number
    # returns either None or two lists of integers: prefix_string, seven_digits_list
    
    # remove all non-numerics from the string
    # using regex according to: https://stackoverflow.com/a/17337613
    number_string = re.sub('[^0-9]','', phone_number_string)

    # make it into a list of digits for compatibility with the code that follows
    digits_list = [int(digit) for digit in number_string]
    
    # check that the number fits basic requirements, if not, returns None
    if not is_number_valid(digits_list):
        return None
    
    # divide the phone_number_string into 2 pieces
    # 1) prefix_string: a properly formatted prefix/area code string ('1-800-', '617-'')
    # 2) seven_digit_list: a list of seven integers used for the word searching    
    prefix_digits_list = digits_list[:-7]
    seven_digits_list = digits_list[-7:]
    
    if len(prefix_digits_list) == 0:
        prefix_string = ''
    elif len(prefix_digits_list) == 3:
        prefix_string = '({})-'.format(''.join(str(d) for d in prefix_digits_list))
    elif len(prefix_digits_list) == 4:
        prefix_string = '{}-{}-'.format(str(prefix_digits_list[0]),
                                          ''.join(str(d) for d in prefix_digits_list[1:]))
    else:
        print "the prefix/area-code has incorrect formatting"
        return None
    
    return prefix_string, seven_digits_list



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



def number_to_words(phone_number_string):
    # takes input as a string
    # cleans the string into only numbers, transforms it into a list of integers
    # runs through a word searching routine
    # returns a list of possible single-word or multiple-word options for the number
    
    # for now, the code only works for 7-digit words!!!
    
    prep_data = preparation_routine(phone_number_string)
    if not prep_data:
        print "input string does not resemble U.S. phone-number."
        return None
    else:
        prefix_string, seven_digit_list = prep_data

    # we now have 1) prefix_string, which is a string like '', '1-800-', '(617)-'
    #             2) seven_digit_list, in the form [6,1,7,8,5,2,5,2,8,9]
    # prefix_string is used to construct the output string at the end of this function
    # seven_digit_list is the data we need to search for words
    
    # construct a list of lists from the digits
    # the sub_lists are the associated letters for a given digit
    # None is returned for digits 0 and 1 (see definition of alphanumeric_dict)
    # ex: 8670000 yields [['T','U','V'], ['M','N','O'], ..., None]
    letter_options = [alphanumeric_dict.get(str(digit)) for digit in seven_digit_list]
    
    # check to be sure there were no 0 or 1 in the number
    if not all(letter_options):
        # enters here if there are None/False-y values in the list
        print "not all digits in phone number correspond to letters"
        print "no contiguous word is associated with the number"
        return None                                                  
    
    # start by looking for seven letter words
    # then 6-1 split
    # then 5-2 split
    # then 4-3 split
    # then 3-4 split
    # then 2-5 split
    # then 1-6 split

    # do the same sort of procedure for up to 7 single-letter words
    # (for example 222-2222 should return [aaa-aaaa])
    
    valid_words_list = word_searcher(letter_options) 
    #print valid_words_list
    
    if len(valid_words_list) > 0:
           wordifieds_list = [prefix_string + x for x in valid_words_list]
    else:
        print 'no wordification found.'
        return 'no 7-letter wordification.'
    
    return wordifieds_list[0]                              

           
example_number_str = '(617)-724-6837'
wordified_number = number_to_words(example_number_str)
print wordified_number

