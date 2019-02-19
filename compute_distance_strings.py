__author__ = 'Saeid SOHILY-KHAH'
"""
Compute distance between two strings using different methods 
"""
import numpy as np

#Calculates the SequenceMatcher between a and b
def similar(a, b):
    from difflib import SequenceMatcher

    #return round(SequenceMatcher(None, a, b).ratio(),3)
    return round(SequenceMatcher(lambda x: x == " ", a, b).ratio(),3)

#Calculates the Levenshtein distance between a and b
def levenshtein(a, b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a, b = b, a
        n, m = m, n

    current = range(n + 1)
    for i in range(1, m + 1):
        previous, current = current, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete = previous[j] + 1, current[j - 1] + 1
            change = previous[j - 1]
            if a[j - 1] != b[i - 1]:
                change = change + 1
            current[j] = min(add, delete, change)

    return current[n]

#Convert a character into a string of bits
def char_to_bits(text):
    ''' Convert a character into a string of bits

    For example the letter 'a' would be returned as '01100001'

    '''
    import binascii

    text = str.encode(text)
    bits = bin(int(binascii.hexlify(text), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

#Calculates the Hamming Edit distance between a and b
def computeHammingDistance(a,b):
    '''
    Return the Hamming distance between equal-length sequences
    Calculate the number of bits which differ between two strings (also known as the edit distance)
    '''
    if len(a) != len(b):
        return "Undefined for sequences of unequal length"
    else:
        distance = 0

        for i in range(len(a)):
            # Convert each char to a bit string
            c1 = char_to_bits(a[i])
            c2 = char_to_bits(b[i])

            # Compare each of the bits and mark whether they differ
            for bt in range(8):
                if c1[bt] != c2[bt]:
                    distance = distance + 1

        return distance

#Compute the histogram of string a
def computeHistogram(a):
    ascii_lst = []
    for j in range(len(a)):
        ascii_lst.append(ord(a[j]))

    return np.histogram(ascii_lst, density=True)[0]

#Calculates the Text distance using Build-in pachakge textdistance
def text_distance(a,b, algo, method):
    '''
    Python library for comparing distance between two or more sequences by many algorithms such as:
    Edit based, Token based, Sequence based, Compression based, Phonetic, Simple
    All algorithms have some common methods:
    .distance(*sequences) – calculate distance between sequences.
    .similarity(*sequences) – calculate similarity for sequences.
    .maximum(*sequences) – maximum possible value for distance and similarity: distance + similarity == maximum.
    .normalized_distance(*sequences) – normalized distance between sequences.
    .normalized_similarity(*sequences)
    input: a,b the two sequences and algo the algorithm name
    '''
    import textdistance

    return getattr(getattr(textdistance, algo), method)(a,b)


#------------------------------------------------ MAIN ----------------------------------------------------
if __name__ == '__main__':
    str1 = 'Saeid SOHEILY KHAH'
    str2 = 'SOHEILY'

    #SequenceMatcher distance
    SequenceMatcher_dist = similar(str1,str2)
    print("SequenceMatcher distance between '%s' and '%s' is: %f" % (str1, str2, SequenceMatcher_dist))

    #Levenshtein distance
    try:
        levenshtein_dist = round(levenshtein(str1, str2) / (len(str1) + len(str2)), 3)
    except ZeroDivisionError:
        levenshtein_dist = levenshtein(str1, str2)
    print("Levenshtein distance between '%s' and '%s' is: %f" % (str1, str2, levenshtein_dist))

    #Hamming edit distance
    Hamming_edit_distance = computeHammingDistance(str1,str2)
    print("Hamming edit-based distance between '%s' and '%s' is: %s" %(str1, str2, str(Hamming_edit_distance)))

    # Calculate distance based on the string's histogram
    hst_dist = np.sum(abs(computeHistogram(str1) - computeHistogram(str2)))
    print("Histogram-based distance between '%s' and '%s' is: %s" % (str1, str2, round(hst_dist, 6)))

    #Textdistance build-in package: pip install textdistance
    algo_lst = ['hamming', 'jaro', 'jaccard', 'bag', 'lcsseq', 'editex', 'prefix', 'matrix']
    method_lst = ['distance', 'similarity', 'normalized_similarity']
    for algo in algo_lst:
        for method in method_lst:
            try:
                t_dist = round(text_distance(str1, str2, algo, method), 6)
            except:
                t_dist = 'None'
            print("%s %s between '%s' and '%s' is: %s" % (algo, method, str1, str2, str(t_dist)))

    #Fuzzy String Matching build-in package: pip install fuzzywuzzy
    from fuzzywuzzy import fuzz
    #Usage: Simple Ratio, Partial Ratio, Token Sort Ratio, Token Set Ratio
    simple_ratio_dist = fuzz.ratio(str1, str2)
    percentage = '%'
    print("Simple ratio fuzzy distance between '%s' and '%s' is: %s%s" % (str1, str2, str(simple_ratio_dist), percentage))