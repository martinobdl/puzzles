import turtle
import numpy as np
import sys

def print_board(board_data,triangle_data,pic_file="TriTriAgain.ps"):
    board = np.loadtxt(open(board_data, "rb"), delimiter=";")
    triangles = np.loadtxt(open(triangle_data, "rb"), delimiter=";")
    N = board.shape[0] # N by N grid
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
        for x in range(board.shape[0]):
            for y in range(board.shape[1]):
                n = int(board[x,y])
                if n!=0:
                    turtle.goto(-N * LENGTH/2 + LENGTH*(y+1/2), N * LENGTH/2 - LENGTH*(x+3/4))
                    turtle.write(n, font=("Arial", int(LENGTH/2), "normal"), align="center")

    def draw_triangle(turtle, fill=False):
        turtle.pencolor(65, 105, 225) # blue
        turtle.fillcolor(204, 221, 255) # lblue
        turtle.pensize(3)
        for t in triangles:
            turtle.penup()
            turtle.goto(-N * LENGTH/2 + t[1]*LENGTH, N * LENGTH/2 - t[0]*LENGTH)
            turtle.pendown()
            if fill: turtle.begin_fill()
            turtle.goto(-N * LENGTH/2 + t[3]*LENGTH, N * LENGTH/2 - t[2]*LENGTH)
            turtle.goto(-N * LENGTH/2 + t[5]*LENGTH, N * LENGTH/2 - t[4]*LENGTH)
            turtle.goto(-N * LENGTH/2 + t[1]*LENGTH, N * LENGTH/2 - t[0]*LENGTH)
            if fill: turtle.end_fill()
            turtle.penup()

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

    turtle.update()

    cv = turtle.getcanvas()
    cv.postscript(file=pic_file, colormode='color')

    screen.exitonclick()

if __name__=="__main__":
    board_filename = sys.argv[1]
    triangle_data = sys.argv[2]
    print_board(board_filename,triangle_data)

