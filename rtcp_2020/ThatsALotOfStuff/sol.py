import base64

# hex --> octal --> ascii --> decode base64

def octal_to_str(octal_str):
    '''
    It takes an octal string and return a string
        :octal_str: octal str like "110 145 154"
    '''
    str_converted = ""
    for octal_char in octal_str.split(" "):
        str_converted += chr(int(octal_char, 8))
    return str_converted

data = [31,34,33,20,31,35,36,20,31,32,32,20,31,35,32,20,31,34,33,20,31,31,30,20,31,36,34,20,31,35,32,20,31,31,35,20,31,30,37,20,36,35,20,36,32,20,31,31,35,20,36,33,20,31,31,32,20,31,37,32,20,31,31,35,20,31,32,34,20,31,30,32,20,31,36,35,20,31,34,33,20,36,31,20,37,31,20,31,35,30,20,31,34,33,20,31,35,32,20,31,31,36,20,31,34,36,20,31,31,36,20,31,30,36,20,37,31,20,31,35,32,20,31,31,35,20,31,30,34,20,31,30,32,20,31,31,35,20,31,33,30,20,36,32,20,31,31,35,20,36,30,20,31,34,34,20,31,31,30,20,31,31,36,20,37,31]

octal = bytearray.fromhex("".join(list(map(str, data)))).decode()

print("octal: ",octal)

ascii = octal_to_str(octal)

print("ascii: ", ascii)

print("FLAG: ", base64.b64decode(ascii).decode('utf-8'))


