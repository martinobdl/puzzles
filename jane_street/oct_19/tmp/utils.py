import numpy as np
import turtle
from itertools import product

def memoize(f):
    memo = {}
    def helper(x):
        if x not in memo:
            memo[x] = f(x)
        return memo[x]
    return helper

@memoize
def generate_sides_length(area):
    """
    generates all the couple (a,b) of int that
    represent the sides of tirangule of area: area
    """
    primes = prime_factors(area)
    primes.append(2)
    n = len(primes)
    masks = product([0,1], repeat=n)
    res = set()
    for m in masks:
        a = np.prod([p for (p,z) in zip(primes,m) if z])
        if a and a>=2:
            b = int(2*area/a)
            if b>=2:
                res.add((min(a,b),max(a,b)))
    return res

@memoize
def prime_factors(nr):
    """
    prime decomposition of a number: nr into prim factors
    """
    i = 2
    factors = []
    while i <= nr:
        if (nr % i) == 0:
            factors.append(i)
            nr = nr / i
        else:
            i = i + 1
    return factors

def print_board(board, triangles=[], points=[], filename="file_name.ps"):
    N = board.size  # N by N grid
    LENGTH = max(int(300/N),30)  # each grid element will be LENGTH x LENGTH pixels

    def grid(turtle, n, length):
        turtle.pencolor(0, 0, 0)
        turtle.pensize(1)
        sign = 1
        for _ in range(2):

            for _ in range(n):
                turtle.forward(length * n)
                turtle.left(sign * 90)
                turtle.forward(length)
                turtle.left(sign * 90)
                sign = 0 - sign

            turtle.forward(length * n)
            [turtle.right, turtle.left][n % 2](90)
            sign = 0 - sign

    def draw_numbers(turtle):
        turtle.pencolor(0, 0, 0)
        turtle.pensize(1)
        yertle.penup()
        for c in board.coordinates:
            n = board.matrix[c]
            turtle.goto(-N * LENGTH/2 + LENGTH*(c[1]+1/2), N * LENGTH/2 - LENGTH*(c[0]+3/4))
            turtle.write(n, font=("Arial", int(LENGTH/2), "normal"), align="center")

    def draw_triangle(turtle, fill=False):
        turtle.pencolor(65, 105, 225) # blue
        turtle.fillcolor(204, 221, 255) # lblue
        turtle.pensize(3)
        for t in triangles:
            turtle.penup()
            turtle.goto(-N * LENGTH/2 + t.A.y*LENGTH, N * LENGTH/2 - t.A.x*LENGTH)
            turtle.pendown()
            if fill: turtle.begin_fill()
            turtle.goto(-N * LENGTH/2 + t.B.y*LENGTH, N * LENGTH/2 - t.B.x*LENGTH)
            turtle.goto(-N * LENGTH/2 + t.C.y*LENGTH, N * LENGTH/2 - t.C.x*LENGTH)
            turtle.goto(-N * LENGTH/2 + t.A.y*LENGTH, N * LENGTH/2 - t.A.x*LENGTH)
            if fill: turtle.end_fill()
            turtle.penup()

    def draw_points(turtle):
        turtle.pencolor(255, 0, 0)
        for p in points:
            turtle.goto(-N * LENGTH/2 + p.y*LENGTH, N * LENGTH/2 - p.x*LENGTH)
            turtle.dot()

    screen = turtle.Screen()
    yertle = turtle.Turtle(visible=False)
    screen.colormode(255)
    yertle.speed('fastest')
    screen.tracer(False)

    draw_triangle(yertle, fill=True)
    yertle.penup()
    yertle.goto(-N * LENGTH/2, -N * LENGTH/2)  # center our grid (optional)
    yertle.pendown()

    grid(yertle, N, LENGTH)
    draw_triangle(yertle, fill=False)
    draw_numbers(yertle)
    draw_points(yertle)

    turtle.update()

    cv = turtle.getcanvas()
    cv.postscript(file=filename, colormode='color')

    # screen.exitonclick()
