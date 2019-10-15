import itertools

# rule 126 dictionary
d={}
for k in itertools.product("01",repeat=3):
    d["".join(k)] = "1"
d['000'] = d['111'] = "0"


# reverse 126 rules
d1 = {  '0':['000','111'],
        '1':['001','010','011','100','101','110']}

def hex_2_bin(h,n=32):
    """
    from hex to binary
    h = '0xdeadbeef'
    n is a left zero padding
    """
    a=bin(int(h, 16))[2:]
    return a.zfill(n)

def bin_2_hex(s):
    """
    from binary to hex
    s = '0111010'
    """
    return hex(int(s, 2))

def rule(s):
    """
    implementation of CA 126 rule on 01-strings
    """
    s_new = list(s)
    s_new[0]=d[s[-1]+s[0:2]]
    for i in range(1,len(s)-1):
        s_new[i]=d[s[i-1:i+2]]
    s_new[-1]=d[s[-2:]+s[0]]
    return "".join(s_new)

def possibile(prec,b):
    """
    possible states observed b and the predecessors prec
    e.g.
        perc = 10
        obs = 1
        returns [101,100] since both have prec 10 and both give as a result 1

    prec = b1b2
    b1,b2,b in (0,1)
    """
    return list(filter(lambda x: x[:2]==prec ,d1[b]))

def reverse(s1):
    """
    reversing the CA126 rule
    """
    strings = d1[s1[0]]
    for cur_bit in s1[1:]:
        tmp = []
        for poss_str in strings:
            tmp.extend([poss_str[:-2]+x for x in possibile(poss_str[-2:],cur_bit)])
        strings = tmp
    consistent_states = list(map(lambda x: x[1:-1], filter(lambda x: x[:2]==x[-2:], strings)))
    return consistent_states

def run_tests():
    """
    tests
    """
    assert('0010' in reverse(rule('0010')))
    assert('10000111' in reverse(rule('10000111')))
    assert('0xdeadbeef' in [bin_2_hex(x) for x in reverse(hex_2_bin('0x73ffe3b8'))])
    assert(hex_2_bin(bin_2_hex('11011110101011011011111011101111'))=='11011110101011011011111011101111')
    assert(bin_2_hex(hex_2_bin('0xdeadbeef'))=='0xdeadbeef')
    assert(bin_2_hex(rule(hex_2_bin('0xdeadbeef'))) == '0x73ffe3b8')
    assert(bin_2_hex(rule(hex_2_bin('0x73ffe3b8'))) == '0xde0036ec')

if __name__=="__main__":
    all_pre = [bin_2_hex(x)[2:] for x in reverse(hex_2_bin('0x66de3c1bf87fdfcf'))]
    with open("all_keys.txt","w") as f:
        f.write("\n".join(all_pre))
