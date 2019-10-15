import numpy as np
from termcolor import colored
import sys

def print_board(k,n):
    """
    prints the board where the first values are e.g. k="4,21,16,8" and where the couple n in in red.
    """
    M = np.array(d[k].split(',')).reshape(8,7)
    for l in M:
        for num in l:
            if num==n:
                print(colored(num, 'red'), end = '\t')
            else:
                print(num, end = '\t')
        print("\n")

if __name__=="__main__":
    print("Play at https://doomed.web.ctfcompetition.com and look at the first 4 cells")
    with open("boards.csv") as f:
        A=f.read().split("\n")

    d = {}
    for l in A:
        d[",".join(l.split(',')[:4])] = l

    k = input("cells (comma separated): ")
    while True:
        n = input("look for num: ")
        print("\n"*100)
        print_board(k,n)
        print("\n"*2)
