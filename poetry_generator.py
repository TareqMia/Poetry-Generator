# IAE 101
# Project 04 - Poetry Generator
# Tareq Mia
# TMIA
# 12/9/19
# poetry_generator.py (v.3)

import nltk
import pronouncing
import random

my_corpus = nltk.corpus.gutenberg.words("shakespeare-hamlet.txt")
bigrams = nltk.bigrams(my_corpus)
cfd = nltk.ConditionalFreqDist(bigrams)

# This function takes two inputs:
# source - a word represented as a string
# num - an integer
# The function will generate num random related words using
# the CFD based on the bigrams in our corpus, starting from
# source. So, the first word will be generated from the CFD
# using source as the key, the second word will be generated
# using the first word as the key, and so on.
# If the CFD list of a word is empty, then a random word is
# chosen from the entire corpus.
# The function returns a num-length list of words.
def random_word_generator(source = None, num = 1):
    result = []
    while source == None or not source[0].isalpha():
        source = random.choice(my_corpus)
    word = source
    result.append(word)
    while len(result) < num:
        if word in cfd:
            init_list = list(cfd[word].keys())
            choice_list = [x for x in init_list if x[0].isalpha()]
            if len(choice_list) > 0:
                newword = random.choice(choice_list)
                result.append(newword)
                word = newword
            else:
                word = None
                newword = None
        else:
            newword = None
            while newword == None or not newword[0].isalpha():
                newword = random.choice(my_corpus)
            result.append(newword)
            word = newword
    return result

# This function takes a single input:
# word - a string representing a word
# The function returns the number of syllables in word as an
# integer.
# If the return value is 0, then word is not available in the CMU
# dictionary.
def count_syllables(word):
    phones = pronouncing.phones_for_word(word)
    count_list = [pronouncing.syllable_count(x) for x in phones]
    if len(count_list) > 0:
        result = max(count_list)
    else:
        result = 0
    return result

# This function takes a single input:
# word - a string representing a word
# The function returns a list of words that rhyme with
# the input word.
def get_rhymes(word):
    result = pronouncing.rhymes(word)
    return result

# This function takes a single input:
# word - a string representing a word
# The function returns a list of strings. Each string in the list
# is a sequence of numbers. Each number corresponds to a syllable
# in the word and describes the stress placed on that syllable
# when the word is pronounced.
# A '1' indicates primary stress on the syllable
# A '2' indicates secondary stress on the syllable
# A '0' indicates the syllable is unstressed.
# Each element of the list indicates a different way to pronounce
# the input word.
def get_stresses(word):
    result = pronouncing.stresses_for_word(word)
    return result

# Use this function to generate each line of your poem.
# This is where you will implement the rules that govern
# the construction of each line.
# For example:
#     -number of words or syllables in line
#     -stress pattern for line (meter)
#     -last word choice constrained by rhyming pattern
# Add any parameters to this function you need to bring in
# information about how a particular line should be constructed.
def generate_line():
    syllables = 0
    words = []
    starting_word = random.choice(my_corpus)
    words.append(starting_word)
    syllables += count_syllables(starting_word)
    rest_of_line = random_word_generator(starting_word, 13)
    
    skip = False
    for x in rest_of_line[1:]:
        if syllables + count_syllables(x) > 10:
            skip = True
            continue
        if skip:
            skip = False
            continue
        syllables += count_syllables(x)
        words.append(x)


    words_in_line = []
    for x in words:
        if x in ",.?:!;'-":
            pass
        else:
            words_in_line.append(x)
    return words_in_line
    

# Use this function to construct your poem, line by line.
# This is where you will implement the rules that govern
# the structure of your poem.
# For example:
#     -The total number of lines
#     -How the lines relate to each other (rhyming, syllable counts, etc)
def generate_poem():
    # attempts of creating a sonnet
    # first stanza (repeats 3 times becasue of quatrains) 
    for x in range(3):
        line1 = generate_line()
        line2 = generate_line()
        line3 = generate_line()
        line4 = generate_line()
        last_word1 = line1[-1]
        last_word2 = line2[-1]
        if len(get_rhymes(last_word1)) >= 1:
            rhyme1 = random.choice(get_rhymes(last_word1))
            line3.append(rhyme1)
        else:
            pass
        if len(get_rhymes(last_word2)) >= 1:
            rhyme2 = random.choice(get_rhymes(last_word2))
            line4.append(rhyme2)
        else:
            pass

        def line_converter(line):
            result = ''
            for x in line:
                result += x + " "
                result = result.capitalize()
            return result

        print(line_converter(line1))
        print(line_converter(line2))
        print(line_converter(line3))
        print(line_converter(line4))
        print()

    couplet1 = generate_line()
    couplet2 = generate_line()

    last_word = couplet1[-1]
    if len(get_rhymes(last_word)) >= 2:
        rhyme = random.choice(get_rhymes(last_word))
        couplet2.append(rhyme)
    else:
        pass

    print(line_converter(couplet1))
    print(line_converter(couplet2))
    print()

    return "by Tareq Mia"
    

def test():
    keep_going = True
    while keep_going:
        word = input("Please enter a word (Enter '0' to quit): ")
        if word == '0':
            keep_going = False
        elif word == "":
            pass
        else:
            print(cfd[word].keys(), cfd[word].values())
            print()
            print("Random 5 words following", word)
            print(random_word_generator(word, 5))
            print()
            print("Pronunciations of", word)
            print(pronouncing.phones_for_word(word))
            print()
            print("Syllables in", word)
            print(count_syllables(word))
            print()
            print("Rhymes for", word)
            print(get_rhymes(word))
            print()
            print("Stresses for", word)
            print(get_stresses(word))
            print()

if __name__ == "__main__":
    #test()
    my_poem = generate_poem()
    print(my_poem)
