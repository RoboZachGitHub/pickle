from words_to_numbers import *
from number_to_words import *
from all_wordifications import *


def test_string_equality(first, second, test_id):
    """Fail if the two objects are unequal
       operator.
    """
    if first != second:
        return [first, second, "test " + test_id + " strings not equal"]
    else:
        return [first, second, "test " + test_id + " strings equal"]


def equal_strings_tests():
    """ Fail if expected result is not equal to the true result.
        useful to test words_to_numbers() """

    actual_result = words_to_numbers('1-800-PAINTER')
    expected_result = '1-800-724-6837'
    print (test_string_equality(actual_result, expected_result,'1'))

    actual_result = words_to_numbers('1-800-PAINT-37')
    expected_result = '1-800-724-6837'
    print (test_string_equality(actual_result, expected_result,'2'))

    actual_result = words_to_numbers('1')
    expected_result = 'input string may not represent US phone number'
    print (test_string_equality(actual_result, expected_result, '3'))

    return 0


from random import randrange
def random_number_to_words_tests(sample_size):
    """ Used to test number_to_words()
        Give a large sample size, the code should never fail
        The code will return 'None', but not an exit code of 1
    """

    #generate a set of fake phone-numbers ranging up to 12 digits in length
    def random_num():
        num_length = randrange(7,11) # valid numbers are of length 7, 10, and 11
        fake_phone_number = ''.join([str(randrange(10)) for i in range(num_length)])
        return fake_phone_number

    random_numbers_list = [random_num() for i in range(sample_size)]

    for test in random_numbers_list:
        print (test)
        try:
            result = number_to_words(test)
            print ('{} ---> {}'.format(test, result))
        except:
            print ('FAIL! check return value for: ')
            print (test)

def random_all_wordifications_tests(sample_size):
    """ Used to test all_wordifications()
        Give a large sample size, the code should never fail
        The code will return 'None', but not an exit code of 1
    """
    #generate fake input string of numbers ranging 7-11 digits in length
    def random_num():
        num_length = randrange(7,12) # valid numbers are of length 7, 10, and 11
        fake_phone_number = ''.join([str(randrange(10)) for i in range(num_length)])
        return fake_phone_number
    random_numbers_list = [random_num() for i in range(sample_size)]

    for test in random_numbers_list:
        print (test)
        try:
            result = all_wordifications(test)
            print result
            #if result(len) > 1:
            #    for wordification in result:
            #        print wordification
            #else:
            #    print wordification
        except:
            print ('FAIL! check return value for: ')
            print (test)



#random_number_to_words_tests(10)
#random_all_wordifications_tests(5)

#equal_strings_tests()
