# number_to_words() takes as an argument a string representing a US phone number
# and outputs a string which has transformed part or all of the phone number
# into a single "wordified" phone number that can be typed on a US telephone
# example: a valid output of number_to_words("1-800-724-6837") could be "1-800-PAINTER")

# this version only does wordifications in English

# import custom functions and dicts
import phone_to_words_fx as ptw
from phone_to_words_dicts import numeric_to_alpha_dict

# import custom word list nltk_eng_words_3to7letters.txt
# nltk_eng_words_3to7letters.txt is a word list of 3-7 letter english words
# nltk is python's natural language processing tool kit module
# 1 and 2 letter word lists are imported when explicitly useful
in_file = open("nltk_eng_words_3to7letters.txt", 'r')
in_lines = in_file.readlines()
in_file.close()
# primary word list should be globally defined
word_list_primary = tuple(line.rstrip() for line in in_lines)


def number_to_words(phone_number_string):
    """ takes input as a string
     cleans the string into only numbers, transforms it into a list of integers
     runs through a word searching routine
     returns a list of all possible single-word or multiple-word options for the number """

    prep_data = ptw.preparation_routine(phone_number_string)
    if not prep_data:
        print('input string does not resemble U.S. phone-number.')
        return 'None'
    else:
        # prefix_string is a string like '', '1-800-', '(617)-'
        # seven_digit_list, in the form [6,1,7,8,5,2,5,2,8,9]
        prefix_string, seven_digit_list = prep_data

    # in the following code, seven_digit_list comprises the numerical data used to search for words

    # letter_options is a list with elements of type:
    # ex: ['A', 'B', 'C'] corresponding to mapping from digit 2
    letter_options = [numeric_to_alpha_dict.get(str(digit)) for digit in seven_digit_list]

    # return_word_slices takes in letter_options and a word list
    # it returns a tuple in the form: (index, string)
    # ex: (2, 'DOG')  means DOG can be formed using the 3rd, 4th, & 5th digits of the number
    index_word = ptw.return_single_word_slice(letter_options, word_list_primary)

    # transform to outstring format
    # index_word must be give as [index_word] for compatibility with transform_to_outstring
    try:
    	wordified_result = ptw.transform_to_outstring([index_word], seven_digit_list, prefix_string)
    except:
    	wordified_result = 'None'
    return wordified_result

#ex_number = '1-800-724-6837'
#ex_number = '760-599-0766'
#ex_number = '244-2287'
#wordified_string = number_to_words(ex_number)
#print(wordified_string)
