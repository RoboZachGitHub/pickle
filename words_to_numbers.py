from phone_to_words_dicts import alpha_to_numeric_dict
import re


def number_to_words(wordified_string):
    # takes input as a string
    # converts the wordified input string to its native phone number format
    # outputs it as a string

    index_letter_list = [(i, char.upper()) for i, char in enumerate(wordified_string) if char.isalpha()]
    index_number_list = [(i_l[0], alpha_to_numeric_dict.get(str(i_l[1]))) for i_l in index_letter_list]

    digitified_string_list = list(wordified_string[:])
    for i_n in index_number_list:
        i, n = i_n
        digitified_string_list[i] = str(n)
    #print digitified_string_list

    digitified_string = ''.join(char for char in digitified_string_list)
    #print digitified_string

    # for now, simply return pure digit string
    # not super important to have perfect format at the moment
    number_string = re.sub('[^0-9]', '', digitified_string)  # type: str
    #print number_string
    return number_string


ex_string = '1-800-94-jenny'

number_to_words(ex_string)
