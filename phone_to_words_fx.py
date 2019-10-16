import re
from phone_to_words_dicts import one_letter_eng_words
from phone_to_words_dicts import two_letter_eng_words




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
    number_string = re.sub('[^0-9]', '', phone_number_string)

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


def word_searcher(letters_lists, english_words_list):
    word_length = len(letters_lists)
    # the current full dictionary used is defined above as word_list_seven_letter_max
    # this is a trimmed version of the nltk dictionary to only include up to 7 letter words
    # special words lists for ! letter and 2 letter words are used to save time
    if word_length == 1:
        words_list = one_letter_eng_words
        #print one_letter_eng_words
    elif word_length == 2:
        words_list = two_letter_eng_words
        #print two_letter_eng_words
    else:
        words_list = english_words_list
        words_list = filter(lambda x: len(x) == word_length, words_list)
    # iteratively trim down the words_list, keeping only words matching the allowed criteria at each index
    for i in range(word_length):
        words_list = [filter(lambda x: x[i] == letter, words_list) for letter in letters_lists[i]]
        words_list = [item for sub_list in words_list for item in sub_list]  # flattened list
    return words_list


def return_word_slices(letter_options_list, english_words_list):
    # takes in a list of letter options ex: [['T','U','V'], ['M','N','O'], ..., None]
    # english_words_list is a list of all english words, perhaps somewhat pre-filtered and sorted...
    # ... usually allowing max word length 7 for our purposes
    # returns all possible word slices along with their starting index 0-6 (0-length)

    len_list = len(letter_options_list)
    indeces_and_words = []  # will be filled with tuples ex: (3, 'dog')
    # 3 being index of the word, it begins at the 4th digit
    for i in reversed(range(len_list)):
        slots_to_grab = i + 1
        index_f = len_list
        while index_f - slots_to_grab >= 0:
            index_i = index_f - slots_to_grab
            tmp_letter_options = letter_options_list[index_i:index_f]

            # now perform the word search for this slice
            tmp_words = word_searcher(tmp_letter_options, english_words_list)

            for word in tmp_words:
                indeces_and_words.append((index_i, word))
                # print index_i
                # print word
            index_f -= 1

    return indeces_and_words


def transform_to_outstring(word_combo, seven_digit_list, prefix_string=''):
    # still needs some comments to explain the function  :)

    out_chars = seven_digit_list[:]

    previous_end_i = -1
    for word in word_combo:
        word_i, word_string = word
        word_len = len(word_string)

        # replace the numbers in the digit list appropriately with letter or dashes
        # conditional statements solve a host of small formatting issues
        for i, char in enumerate(word_string):
            tmp_i = i + word_i  # word_i is the starting position of the word
            if i == 0 and tmp_i != 0:
                replacement_char = '-' + char


            #if tmp_i - 1 == previous_end_i:
            #    replacement_char = char
            #elif tmp_i == 6:  # fixes 1-800-PAINTER-
            #    replacement_char = char

            #elif i == word_len - 1:
            #    replacement_char = char + '-'
            else:
                replacement_char = char
            out_chars[tmp_i] = replacement_char
        previous_end_i = word_i + word_len - 1

    # https://stackoverflow.com/a/3590175
    out_string = prefix_string + ''.join(str(i) for i in out_chars)


    #final clean up, places '-' between letter-number errors [A-Z][0-9] (ex. 1-800-7-A468-ER)
    def formatter(text, index):
        i = index
        if i + 1 == len(text):
            return text[i]
        if text[i].isalpha() & text[i + 1].isdigit():
            return text[i] + '-'
        else:
            return text[i]

    out_string = ''.join([formatter(list(out_string), i) for i, char in enumerate(list(out_string))])

    return out_string