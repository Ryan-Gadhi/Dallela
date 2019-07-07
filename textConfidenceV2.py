import string
string.ascii_lowercase
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy as np
from time import time

# todo: convert to numPy

all_chars = list(string.ascii_lowercase)
all_chars.append(" ")
numbers = ['0','1','2','3','4','5','6','7','8','9']
all_chars += ['\'','\"',",","-","_","."]
all_chars += numbers
all_chars = np.array(all_chars)
stopwords = set(stopwords.words("english"))
stopwords = np.array(stopwords)


def compare(src,target):  # returns confidence

    # 65% confidence for char appearance match
    # 20% for how small is the distance difference
    # 15% ?
    difference_weight_perc = 100

    difference_weight = appreance(src=src, target=target)

    confidence = difference_weight * (difference_weight_perc/100)

    return confidence


def appreance(src,target):
    '''

    this compare the char count regardless of anything else

    '''

    src = src.lower()
    target = target.lower()
    size = len(all_chars)
    # splited_src = np.char.split(src, sep=' ')
    splited_src = src.split(" ")
    splited_src = np.array(splited_src)

    # splited_target = np.char.split(target, sep=' ')
    splited_target = target.split(" ")
    splited_target = np.array(splited_target)

    max_len = splited_target.size
    # similar_words = []
    similar_words = [''] * max_len
    similar_words = np.array(similar_words)
    iterator = 0

    for word in splited_src:
        if word in splited_target:
            similar_words[iterator] = word
            splited_target[np.where(splited_target == word)] = '' # removing element
        iterator += 1


    added_length = 0
    for word in similar_words:
        if word in stopwords:
            added_length += len(word)

    temp = [0] * size
    src_chars = np.array(temp)
    target_chars = np.zeros((size,), dtype=int)

    for char in src:
        index = np.where(all_chars == char)
        src_chars[index] += 1

    for char in target:
        index = np.where(all_chars == char)
        target_chars[index] += 1

    difference = [0] * size
    difference = np.array(difference)

    for i in range(size):
        difference[i] = abs(src_chars[i] - target_chars[i])

    # print(difference)
    difference_total = 0

    for element in difference:
        difference_total += element
    # relative : size vs no match

    target_len = len(target)
    src_len = len(src)

    # increasing confidence in case stop words are used
    target_len += added_length * 2 # can be removed if needed, magic number 2
    src_len += added_length * 2 # can be removed if needed

    target_diff_weight = 1 - difference_total/ target_len
    src_diff_weight = 1 - difference_total / src_len

    # print(target_diff_weight, ' target weight')
    # print(src_diff_weight, ' src weight')

    avarage_diff = (target_diff_weight + src_diff_weight) / 2  # todo: can be improved

    return avarage_diff

t = 'the i am talking the right now'
t2 = 'i am walking right now the'

start = time()
confidence = compare(t,t2)

print("--- %s seconds ---" % (time() - start))

print('src is close to target with confidence: ', confidence)


