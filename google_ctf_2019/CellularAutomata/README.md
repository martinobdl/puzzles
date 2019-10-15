# Cellular Automata

The task is to decipher the encrypted key using as the key the previous step of a given cellular automata (CA).

The CA is a 1-dimensional 2-colors (binary) CA with 1-size neighborhoods. This is a picture of the rule 126 which defines how to convert the central point of the neighborhood:

![alt text](http://mathworld.wolfram.com/images/eps-gif/ElementaryCARule126_1200.gif)

we are given the 64bit state of the CA by the hex: 0x66de3c1bf87fdfcf which translates to the state: 110011011011110001111000001101111111000011111111101111111001111.

We can simply recover the states sequentially.

## Example

Suppose we are given 0111

We can read bit by bit and keep track of all neighborhood that could have originated the current bit and are consistent with the sequences reconstructed so far.


<img src="https://github.com/martinobdl/google_ctf_2019/blob/master/CellularAutomata/cellautomata_diagram.jpg" width="500" height="400">

This is the tree of possibilities, the states are then cyclical (first and last element are neighbors) and so we can discard most of the results, leaving us with 0010 and 1101, which in fact lead to the state 0111 after application of rule126. Implementing this algorithm would leave us with a O(N) algorithm to find all possible previous states and write to a csv all possible states in hex.
Then we brute force all possible keys by grepping CTF with openssl suggested by the instructions  at https://cellularautomata.web.ctfcompetition.com

## code snippets

```python

# reverse 126 rules
d1 = {  '0':['000','111'],
        '1':['001','010','011','100','101','110']}

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
    s1 is a string of '01's
    """
    strings = d1[s1[0]]
    for cur_bit in s1[1:]:
        tmp = []
        for poss_str in strings:
            tmp.extend([poss_str[:-2]+x for x in possibile(poss_str[-2:],cur_bit)])
        strings = tmp
    consistent_states = list(map(lambda x: x[1:-1], filter(lambda x: x[:2]==x[-2:], strings)))
    return consistent_states
```
