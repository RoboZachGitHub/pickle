# this is the basic logic needed to take a list of words with their starting indeces
# then find all the combinations without any over--lapping of words

# this recursive logic is useful for the return_all_wordifications() function



def word_combos_recursion(word_basis, max_len=5, starting_str='', results = []):
    for x in word_basis:
        string_1 = starting_str + "  " + str(x)
        results.append(string_1)
        
        # calculate minimum index of next word(s)
        s_ind, s_str = x
        s_len = len(s_str)
        min_next_index = s_ind + s_len
        
        # filter out invalid words, recursively search valid combos
        trimmed_basis = filter(lambda x: x[0]>=min_next_index, word_basis)
        combos(trimmed_basis,
               max_len=max_len,
               starting_str = string_1,
               results = results)
    return results

# fake data
max_length = 5

data_set = [(0,'OH'),
            (0, 'WOW'),
            (4, 'A'),
            (1, 'I'),
            (2, 'BE'),
            (3, 'I'),
            ]

    
word_combos_recursion(data_set, max_length)



