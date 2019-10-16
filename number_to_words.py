# this code is related to the following assignment:
# create a function number_to_words(), which takes as an argument a string representing a US phone
# number and which outputs a string which has transformed part or all of the phone
# number into a single "wordified" phone number that can be typed on a US telephone (for
# example, a valid output of number_to_words("1-800-724-6837") could be
# "1-800-PAINTER"). If you find it makes things simpler, feel free to constrain this function
# to only output "wordifications" in English.

# this version only does wordifications in English
# this version uses a word list, based on the natural language proccessing tool kit's english word list
import phone_to_words_fx as ptw_fx
from phone_to_words_dicts import numeric_to_alpha_dict


# nltk_eng_words_3to7letters.txt is a word list of 3-7 letter english words
# nltk is python's natural language processing tool kit module

# read in the 3-7 letter word list, 1 and 2 letter word lists were imported from phone_to_words_dicts
in_file = open("nltk_eng_words_3to7letters.txt", 'r')
in_lines = in_file.readlines()
word_list_primary = tuple(line.rstrip() for line in in_lines)
in_file.close()


def number_to_words(phone_number_string):
    # takes input as a string
    # cleans the string into only numbers, transforms it into a list of integers
    # runs through a word searching routine
    # returns a list of all possible single-word or multiple-word options for the number

    prep_data = ptw_fx.preparation_routine(phone_number_string)
    if not prep_data:
        print "input string does not resemble U.S. phone-number."
        return None
    else:
        prefix_string, seven_digit_list = prep_data

    # we now have 1) prefix_string, which is a string like '', '1-800-', '(617)-'
    #             2) seven_digit_list, in the form [6,1,7,8,5,2,5,2,8,9]
    # prefix_string is saved to construct the output string at the end of this function
    # it is not the intention of this code to search for wordifications with prefix numbers in the basis
    # in the following code, seven_digit_list comprises the numerical data used to search for words

    # construct a list, letter_options, with element type:
    # ex: ['A', 'B', 'C'] corresponding to digit 2
    # ex: 8600 yields [['T','U','V'], ['M','N','O'], [], []]
    letter_options = [numeric_to_alpha_dict.get(str(digit)) for digit in seven_digit_list]

    # return_word_slices takes in letter_options and a list of strings
    # it returns a list with every possible word and the associated index as a tuple
    # (2, 'DOG')  = DOG can be formed using the 3rd, 4th, & 5th digits of the number
    index_word = ptw_fx.return_single_word_slice(letter_options, word_list_primary)  # expects input in list form

    # transform to outstring format
    wordified_result = ptw_fx.transform_to_outstring([index_word], seven_digit_list, prefix_string)
    return wordified_result


ex_number = '1-800-724-6837'
wordified_string = number_to_words(ex_number)
print wordified_string

