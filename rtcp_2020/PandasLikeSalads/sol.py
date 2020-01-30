import math
import string

plain_pigpen = "ysay{hjkahr_qqgdia_unr_kw_yrq_pm_nnfb}"

key = "cuteness"

"""
The cipher is clearly polyalphabetic and not simply a substitution cypher, since we know that ysay{} --> rtcp{}

the first step is a plain pigpen (discoverd by googling "rotation cipher key")

then we need a polyalphabetic cipher and the simplest would be: vigenere

since we have a key (CUTENESS) ===> keyed vigenere
"""

def print_matrix(M):
    for letter_row in M.keys():
        for letter_col in M[letter_row].keys():
            print(M[letter_row][letter_col],end=" ")
        print()

matrix = {}

def shift_letter(letter,n):
    if letter not in string.ascii_lowercase:
        return letter
    return chr((ord(letter)+n-97)%26+97)

for n,letter_row in enumerate(string.ascii_lowercase):
    matrix[letter_row] = {}
    for letter_col in string.ascii_lowercase:
        matrix[letter_row][letter_col] = shift_letter(letter_col,n)

# print_matrix(matrix)

def padding(key,message):
    n = len(message.replace("{","").replace("}","").replace("_",""))
    l = len(key)
    m = math.ceil(n/l)
    return (key*m)[:n]

padded_key = padding(key,plain_pigpen)

print()

def vigenere_encrypt(message, key):
    s = ""
    padded_key = padding(key,message)
    for l,k in zip(message, padded_key):
        if l not in string.ascii_lowercase:
            s+=l
        else:
            s+=matrix[k][l]
    return s

def vigenere_decrypt(message, key):
    s = ""
    padded_key = padding(key,message)
    c = 0
    for m in message:
        if m not in string.ascii_lowercase:
            s+=m
        else:
            k = padded_key[c]
            row = matrix[k]
            inv_row = {v:k for k,v in row.items()}
            s+=inv_row[m]
            c+=1
    return s



tmp = vigenere_encrypt("rtcp",key)

shift = ord(tmp[0])-ord(plain_pigpen[0])

shifted_string = "".join(list(map(lambda x: shift_letter(x,shift), plain_pigpen)))

print("SHIFT:",shifted_string)

print("FLAG: ", vigenere_decrypt(shifted_string, key))
