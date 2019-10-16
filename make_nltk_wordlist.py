import numpy as np
import nltk
nltk.download('words')
from nltk.corpus import words  # list of all words in the american english language
# https://www.datasciencebytes.com/bytes/2014/11/03/get-a-list-of-all-english-words-in-python/
# must install ntlk for this code to work
# https://www.nltk.org/
# sudo apt-get install python-numpy python-nltk

word_list_full = words.words() # 236,736 words

# for now we need to parse out all words longer than 7 letters, also capitalize everything
# 1 letter and 2 letter words also parsed out
# this allows the code to search smaller 1 and 2 letter word lists defined elsewhere
# also the nltk word list has very strange 2 letter words
word_list_7letter_max_3letter_min = [word.upper() for word in word_list_full if len(word) <= 7 and len(word) > 2]  
word_list_7letter_max_3letter_min.sort() # makes sure list is in alphabetical order
#print len(word_list_7letter_max_3letter_min) # 59,228 words


# remove duplicates using list comprehension 
# https://www.geeksforgeeks.org/python-ways-to-remove-duplicates-from-list/
x = word_list_7letter_max_3letter_min
word_list_trimmed = [] 
[word_list_trimmed.append(word) for word in x if word not in word_list_trimmed]
#print len(word_list_trimmed) #57,440 words


out_string = ''
for word in word_list_trimmed:
    out_string += word + "\n"

out_file = open("nltk_eng_words_3to7letters.txt", 'w')
out_file.write(out_string)
out_file.close()
