# words_to_numbers() takes as an argument a string representing a "wordified" US phone number
# it outputs a string which has transformed it to its digit representation
# example: a valid output of words_to_numbers("1-800-PAINTER") could be "1-800-724-6837")

# import custom dict
from phone_to_words_dicts import alpha_to_numeric_dict


def words_to_numbers(wordified_string):
    """ takes input as a string
     converts the wordified input string to its native phone number format
     outputs it as a string """

    index_letter_list = [(i, char.upper()) for i, char in enumerate(wordified_string) if char.isalpha()]
    index_number_list = [(i_l[0], alpha_to_numeric_dict.get(str(i_l[1]))) for i_l in index_letter_list]

    digitified_string_list = list(wordified_string[:])
    for i_n in index_number_list:
        i, n = i_n
        digitified_string_list[i] = str(n)

    # remove non digit characters
    digitified_string_list = [d for d in digitified_string_list if d.isdigit()]

    num_len = len(digitified_string_list)
    # if num_len not 7, 10, or 11, this is not a US phone number
    if num_len != 7 and num_len != 10 and num_len != 11:
        print ('error.')
        print ('input string may not represent US phone number')
        return 'input string may not represent US phone number'

        # add dashes appropriately
        # if num_len = 11, the form should be 1-800-333-3333
        # if num_len = 10, the form should be 800-333-3333
        # if num_len = 7, the form should be 333-3333
        # parenthesis forms are not necessary here. (i.e. (800)333-3333 is not an improvement)
    def dash_formatter(phone_number_len, i, d):
        l = phone_number_len
        if l == 11:
            if i == 1 or i == 4 or i == 7:
                return '-' + d
            else:
                return d
        elif l == 10:
            if i == 3 or i == 6:
                return '-' + d
            else:
                return d
        elif l == 7:
            if i == 3:
                return '-' + d
            else:
                return d

    digitified_string_list = [dash_formatter(num_len, i, d) for i, d in enumerate(digitified_string_list)]
    # convert from a list of chars to a single string
    digitified_string = ''.join(char for char in digitified_string_list)

    return digitified_string


#ex_string = '1-800-94-jenny'
#ex_string = '1-800-PAINTER'
#ex_string = '!!!!!'
#x = words_to_numbers(ex_string)
#print (x)
