import phone_to_words_fx as ptw_fx
from phone_to_words_dicts import numeric_to_alpha_dict


# nltk_eng_words_3to7letters.txt is a word list of 3-7 letter english words
# nltk is python's natural language processing tool kit module

# read in the 3-7 letter word list, 1 and 2 letter word lists were imported from phone_to_words_dicts
in_file = open("nltk_eng_words_3to7letters.txt", 'r')
in_lines = in_file.readlines()
word_list_primary = tuple(line.rstrip() for line in in_lines)
in_file.close()



def return_all_word_combos(words_indeces_basis, max_len=7, starting_results=[], results=[]):
    # number_len = 7, for normal 7 digit phone numbers
    # 7-0 split, then 6-1 split, 5-2 split, 4-3 split, 3-4 split, ...
    # also more words are possible for example 222-2222 --> a-a-a-a-a-a-a
    # additional possibilities include separations of words around digits 0 and 1
    # that needs to be implemented later

    for index_word in words_indeces_basis:
        # print index_word
        tmp_results = starting_results + [index_word]
        # print tmp_results
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
    # prefix_string is used to construct the output string at the end of this function
    # seven_digit_list is the data we need to search for words

    # construct a list of lists from the digits
    # the sub_lists are the associated letters for a given digit
    # None is returned for digits 0 and 1 (see definition of alphanumeric_dict)
    # ex: 8670000 yields [['T','U','V'], ['M','N','O'], ..., None]
    letter_options = [numeric_to_alpha_dict.get(str(digit)) for digit in seven_digit_list]

    words_w_indeces = ptw_fx.return_word_slices(letter_options, word_list_primary)

    # we now want to construct things like 1-800-RAG-OVER, 1-800-PAINTER
    # i.e. we want to find all combinations of words that are possible
    results = return_all_word_combos(words_w_indeces)

    # results is a list of word or word-sets along with their indeces
    # the indeces super-impose them over the original characters
    # for example 1-800-724-6837 yields a result [(0, 'RAG'), (3,'NU'), (5, 'ER') ]
    # transforms to 1-800-RAG-NU-ER  whatever that means  :)
    # the result result [(0, 'SAINT')] should transform to 1-800-SAINT-37
    transformed_results = []
    for result in results:
        transformed_results.append(ptw_fx.transform_to_outstring(result, seven_digit_list, prefix_string))

    return transformed_results


ex_num_str_w_one = '1-800-724-6837'
string_results = all_wordifications(ex_num_str_w_one)

for x in string_results:
    print x
