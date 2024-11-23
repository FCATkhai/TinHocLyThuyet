from collections import Counter
from itertools import permutations

def cau1(str1, str2):
    lst1 = list(str1)
    lst2 = list(str2)
    temp = lst1[0:2]
    lst1[0:2] = lst2[0:2]
    lst2[0:2] = temp
    
    return ''.join(lst1)+ ' ' + ''.join(lst2)

# print(cau1('abc', 'efg'))

def cau2(string):
    return string[1::2]

# print(cau2('python'))

def cau3(string):
    lst = string.split(' ')
    counter = Counter(lst)
    return dict(counter)
    
# print(cau3('no pain no gain'))

def cau4(ciphertext, shift = 3):
    deciphered_text = ""
    
    for char in ciphertext:
        # Check if the character is an uppercase letter
        if char.isupper():
            deciphered_text += chr((ord(char) - shift - 65) % 26 + 65)
        # Check if the character is a lowercase letter
        elif char.islower():
            deciphered_text += chr((ord(char) - shift - 97) % 26 + 97)
        else:
            # If it's not a letter, don't change it
            deciphered_text += char
    
    return deciphered_text

# print(cau4('def'))

def cau5(string, inputS):
    for c in string:
        if c not in inputS:
            return False
    return True

# print(cau5('0011', {'0', '1', '2'}))
# print(cau5('123', {'0', '1', '2'}))

def cau6(string):
    return string.split(' ')

# print(cau6('This is a list'))

def cau7(string):
    counter = Counter(string)
    for k, v in counter.items():
        if v == 1:
            return k
    return None

# print(cau7('abcdef'))
# print(cau7('abcabcdef'))
# print(cau7('aabbbcc'))

def cau8(string):
    return string.replace(' ', '')

# print(cau8('a b c'))

def cau9(string):
    words = string.split() 
    seen_words = set()  
    
    for word in words:
        if word in seen_words:  
            return word
        seen_words.add(word)  
    return None  

# print(cau9('ab ca bc ca ab bc'))
# print(cau9('ab ca bc ab'))

def cau10(binary_string):
    # Tách chuỗi nhị phân dựa trên '1' để lấy các chuỗi con toàn là '0'
    zero_groups = binary_string.split('1')
    
    # Tìm chuỗi '0' có độ dài lớn nhất
    max_zeros = max(len(group) for group in zero_groups)
    
    return max_zeros

# print(cau10('1110001110000'))

# Bai tap nang cao

def cau1NangCao(lstA, lstB):
    permA = permutations(lstA)
    permB = permutations(lstB)
    
    setA = {''.join(x) for x in permA}
    setB = {''.join(x) for x in permB}
    
    if setA & setB:
        return True
    else:
        return False

# print(cau1NangCao(['110', '0011', '0110'], ['110110', '00', '110']))
# print(cau1NangCao(['0011', '11', '1101'], ['101', '011', '110']))
# print(cau1NangCao(['100', '0', '1'], ['1', '100', '0']))


def split_into_chunks(s, chunk_size):
    # Use list comprehension to generate chunks of the specified size
    return [s[i:i+chunk_size] for i in range(0, len(s), chunk_size)]

def cau2NangCao(genString):
    
    for c in genString:
        if c not in {'A', 'C', 'G', 'T'}:
            return False
    
    if len(genString) % 3 != 0:
        return False
    else:
        start_codon = 'ATG'
        end_codon = {'TAA', 'TAG', 'TGA'}
        condonList = split_into_chunks(genString, 3)
        if condonList[0] == start_codon and condonList[-1] in end_codon:
            for condon in condonList[1:-1]:
                    if len(set(condon)) == 1:
                        return False
            return True
        else:
            return False
        
# print(cau2NangCao('ATGCCCTAG'))
# print(cau2NangCao('ATGCGTTGA'))