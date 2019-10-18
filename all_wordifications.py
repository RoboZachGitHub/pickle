# all_wordifications() takes in a string representing a phone number
# it outputs a list of strings, constituting all possible wordifications of the number
# the wordifications may be single or multi-word, the words may be contiguous or separated by a number

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


def return_all_word_combos(words_indeces_basis, max_len=7, starting_results=[], results=[]):
    # number_len = 7, for normal 7 digit phone numbers
    # 7-0 split, then 6-1 split, 5-2 split, 4-3 split, 3-4 split, ...
    # Ex: 222-2222 --> a-a-a-a-a-a-a, a-22-2222, and so on
    for index_word in words_indeces_basis:
        tmp_results = starting_results + [index_word]
        results.append(tmp_results)

        # find minimum index for next word
        word_ind, word_str = index_word
        word_len = len(word_str)
        min_next_index = word_ind + word_len

        trimmed_basis = filter(lambda x: x[0] >= min_next_index, words_indeces_basis)
        return_all_word_combos(trimmed_basis,
                               max_len=max_len,
                               starting_results=tmp_results,
                               results=results)

    return results


def all_wordifications(phone_number_string):
    """ takes input as a string
     cleans the string into only numbers, transforms it into a list of integers
     runs through a word searching routine
     returns a list of all possible single-word or multiple-word options for the number """

    prep_data = ptw.preparation_routine(phone_number_string)
    if not prep_data:
        print('input string likely does not resemble U.S. phone-number.')
        return ['None']
    else:
        # prefix_string is a string like '', '1-800-', '(617)-'
        # seven_digit_list, in the form [6,1,7,8,5,2,5,2,8,9]
        prefix_string, seven_digit_list = prep_data

    # in the following code, seven_digit_list comprises the numerical data used to search for words

    # letter_options is a list with elements of type:
    # ex: ['A', 'B', 'C'] corresponding to mapping from digit 2
    letter_options = [numeric_to_alpha_dict.get(str(digit)) for digit in seven_digit_list]

    # return_word_slices returns a list of tuples in the form (index, string)
    # ex: (2, 'DOG')  means DOG can be formed using the 3rd, 4th, & 5th digits of the number
    # the full list represents all words that can be imposed over the original 7 digit number
    words_w_indeces = ptw.return_word_slices(letter_options, word_list_primary)

    # we now want to construct things like 1-800-RAG-OVER, 1-800-PAINTER
    # i.e. we want to find all combinations of words that are possible
    results = return_all_word_combos(words_w_indeces)
    if len(results) == 0:
        print('no wordifications found.')
        return [phone_number_string]

    # results is a list of lists
    # each sublist is made up of a list of (index, string) tuples like (2, 'DOG')
    # if the list has more than one tuple, the words of the tuples will not over-lap
    # the indeces super-impose them over the original characters
    # for example 1-800-724-6837 yields a result [(0, 'RAG'), (3,'NU'), (5, 'ER') ]
    # transforms to 1-800-RAG-NU-ER  whatever that means  :)
    # the result result [(0, 'SAINT')] should transform to 1-800-SAINT-37
    transformed_results = []
    # not to forget the original number, which is in principle a correct solution
    transformed_results.append(phone_number_string)
    for result in results:
        transformed_result = ptw.transform_to_outstring(result, seven_digit_list, prefix_string)
        transformed_results.append(transformed_result)
        print(transformed_result)
    return transformed_results


#ex_number = '1-800-724-6837'
#ex_number = '222-2222'
#ex_number = '1'
#ex_number = "1-800-123!!!!!"
#ex_number = '244-2287'
#string_results_list = all_wordifications(ex_number)
#print(len(string_results_list))

