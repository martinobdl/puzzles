import copy
from utils import *
import timeit
import bisect
from methodtools import lru_cache
"""
Prototipe for the c++ impolementation
"""

class board:
    def __init__(self,board_dimension):
        self.size = board_dimension
        self.matrix = np.zeros((self.size, self.size)).astype(int)
        self.coordinates = []
        self.numbers = []

    def set_number(self, coord, number, ordered=False):
        if ordered:
            index = bisect.bisect(self.numbers, number)
            self.numbers.insert(index, number)
            self.coordinates.insert(index, coord)
        else:
            self.coordinates.append(coord)
        self.matrix[coord] = number

    def __repr__(self):
        return self.matrix.__repr__()

    def tri_is_inside_board(self,t_):
        """
        check wether the triangle t_ is inside the board
        """
        return t_.x_max <= self.size and t_.y_max <= self.size and t_.x_min >= 0 and t_.y_min >= 0

    @lru_cache(maxsize=50)
    def generates_all_tri(self, coord):
        """
        all the permutations of the triangles ceneterd in (0,0) that can be
        contained in the square indicated by coord
        """
        tri = []
        area = self.matrix[coord]
        if area == 0:
            return tri
        sides = generate_sides_length(area)
        for (a,b) in sides:
            A = point(0,0)
            B = point(0,0)
            C = point(0,0)
            B.add_x(a)
            C.add_y(b)
            t = triangle(A,B,C)
            t_ = t.copy()
            for i in range(4):
                t_ = t_.copy()
                tri.append(t_)
                t_.rotate()
            if (a!=b):
                t_ = t.copy()
                t_.mirror()
                for i in range(4):
                    t_ = t_.copy()
                    tri.append(t_)
                    t_.rotate()
        return tri

    def all_legal_triangles(self, coord, fixed_tri = []):
        """
        all legal triangles that are around the number
        in coord and conform with the fixed triangles: fixed_tri
        """
        legal_triangles = []
        area = self.matrix[coord]
        if area == 0:
            return legal_triangles

        tri = self.generates_all_tri(coord)

        for tmp in tri:
            legal_p_strict,boundary_p = tmp._generate_inside_points()
            for p in legal_p_strict:
                t_ = tmp.copy()
                t_.shift(coord[0]-p.x,coord[1]-p.y)

                new_p = [point(pp.x+coord[0]-p.x,pp.y+coord[1]-p.y) for pp in legal_p_strict]
                new_p.extend([point(pp.x+coord[0]-p.x,pp.y+coord[1]-p.y) for pp in boundary_p])

                if  self.tri_is_inside_board(t_) \
                    and not(t_.overlap_multiple(fixed_tri)) \
                    and self.just_number_tri(new_p):
                    legal_triangles.append(t_)

        return legal_triangles

    def just_number_tri(self, all_p_inside):
        """
        return True if the tri contains just one number
        """
        count = 0
        for c in self.coordinates:
            for p in all_p_inside:
                if c[0]==p.x and c[1]==p.y:
                    count += 1
                    if count==2:
                        return False
        return True

class point:
    """
    simple point class
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        assert(x==int(x))
        assert(y==int(y))

    def is_on_line(self,A,B):
        if (self.y-A.y)*(B.x-A.x)==(B.y-A.y)*(self.x-A.x):
            return True;

        return False;

    def is_inside_triangle(self, t):
        """
        check wether the point is inside a triangle defined by t
        and if it on boundary diagonal
        """
        A1 = triangle(t.A,t.B,self,fast=True).area
        A2 = triangle(t.A,self,t.C,fast=True).area
        A3 = triangle(self,t.B,t.C,fast=True).area

        return ((A1 + A2 + A3) == t.area, ((A1 + A2 + A3) == t.area) and self.is_on_line(t.diagonals[0],t.diagonals[1]))

    def is_pointing_out(self, t):
        """
        is it refers to a square outside the rectangle that inscribe the triangle t_
        """
        if self.y == t.y_max or self.x == t.x_max:
            return True
        else:
            return False

    def __repr__(self):
        return "("+str(self.x)+","+str(self.y)+")"

    def add_x(self, dx):
        assert(dx==int(dx))
        self.x += dx

    def add_y(self, dy):
        assert(dy==int(dy))
        self.y += dy

class triangle:
    """
    simple triangle class
    """
    def __init__(self,A,B,C,fast=False):
        """
        if we just want to check that area there no need to ensure the anti-clockwise property
        """
        self.A = A
        self.B = B
        self.C = C

        if not(fast):
            self.anti_clockwise_tri()

        self.area = 0.5*abs(A.x*(B.y-C.y)+B.x*(C.y-A.y)+C.x*(A.y-B.y))
        self.x_min = min(self.A.x, self.B.x, self.C.x)
        self.x_max = max(self.A.x, self.B.x, self.C.x)
        self.y_min = min(self.A.y, self.B.y, self.C.y)
        self.y_max = max(self.A.y, self.B.y, self.C.y)

    def anti_clockwise_tri(self):
        """
        to make sure the triangle is defined as anti-clockwise
        """
        dy1 = self.B.y - self.A.y
        dx1 = self.B.x - self.A.x
        dy2 = self.C.y - self.B.y
        dx2 = self.C.x - self.B.x

        if dy1*dx2 > dy2*dx1:
            self.B, self.C = self.C, self.B

        if self.B.x - self.A.x != 0 and self.B.y - self.A.y != 0:
            self.diagonals = [self.A, self.B]
            self.right_point = self.C

        elif self.B.x - self.C.x != 0 and self.B.y - self.C.y != 0:
            self.diagonals = [self.B, self.C]
            self.right_point = self.A

        else:
            self.diagonals = [self.C, self.A]
            self.right_point = self.B

        self.M = np.ones((3,3))
        self.M[0,0] = self.A.x
        self.M[0,1] = self.A.y
        self.M[1,0] = self.B.x
        self.M[1,1] = self.B.y
        self.M[2,0] = self.C.x
        self.M[2,1] = self.C.y

    def _generate_inside_points(self):
        """
        returns the right up most point of the squares that are
        fully contained in the triangle and the points crossed by the diagonal
        """
        fully_intern_points = []
        boundary_points = []
        fully_out = []

        for x in range(self.x_min, self.x_max+1):
            for y in range(self.y_min, self.y_max+1):
                p1 = point(x,y)
                p2 = point(x+1,y)
                p3 = point(x,y+1)
                p4 = point(x+1,y+1)

                p1_inside, p1_on_diagonal = p1.is_inside_triangle(self)
                p2_inside, p2_on_diagonal = p2.is_inside_triangle(self)
                p3_inside, p3_on_diagonal = p3.is_inside_triangle(self)
                p4_inside, p4_on_diagonal = p4.is_inside_triangle(self)

                if  p1_inside and \
                    p2_inside and \
                    p3_inside and \
                    p4_inside:
                    fully_intern_points.append(p1)

                elif (not(p1_inside) or p1_on_diagonal) and \
                    (not(p2_inside) or p2_on_diagonal) and \
                    (not(p3_inside) or p3_on_diagonal) and \
                    (not(p4_inside) or p4_on_diagonal):
                    # fully_out.append(p1)
                    pass

                elif p1.is_pointing_out(self):
                    pass

                else:
                    boundary_points.append(p1)

        return fully_intern_points, boundary_points

    def __repr__(self):
        return  "[A: " + self.A.__repr__() + \
                "\tB: " + self.B.__repr__() + \
                "\tC: " + self.C.__repr__() + "]\n"

    def shift(self, dx, dy):
        self.A.add_x(dx)
        self.A.add_y(dy)
        self.B.add_x(dx)
        self.B.add_y(dy)
        self.C.add_x(dx)
        self.C.add_y(dy)
        self.__init__(self.A,self.B,self.C)

    def rotate(self):
        """90° clockwise rotation around A"""
        new_B_x = self.A.x + (self.B.y - self.A.y)
        new_B_y = self.A.y - (self.B.x - self.A.x)
        new_B = point(new_B_x, new_B_y)

        new_C_x = self.A.x + (self.C.y - self.A.y)
        new_C_y = self.A.y - (self.C.x - self.A.x)
        new_C = point(new_C_x, new_C_y)

        self.__init__(self.A, new_B, new_C)

    def mirror(self):
        """
        mirror the triangle around the y axis passing to A
        """
        new_B_x = self.A.x - (self.B.x - self.A.x)
        new_B = point(new_B_x, self.B.y)

        new_C_x = self.A.x - (self.C.x - self.A.x)
        new_C = point(new_C_x, self.C.y)

        self.__init__(self.A, new_B, new_C)

    def overlap(self, other):
        """
        check if the triangle overlaps with the triangle defined in other
        """

        if self.x_min > other.x_max or self.x_max < other.x_min:
            return False

        if self.y_min > other.y_max or self.y_max < other.y_min:
            return False

        chkEdge = lambda x: np.linalg.det(x) <= 0
        for i in range(3):
            edge = np.roll(self.M, i, axis=0)[:2,:]

            #Check all points of trangle 2 lay on the external side of the edge E. If
            #they do, the triangles do not collide.
            if (chkEdge(np.vstack((edge, other.M[0]))) and
                chkEdge(np.vstack((edge, other.M[1]))) and
                chkEdge(np.vstack((edge, other.M[2])))):
                return False

        for i in range(3):
            edge = np.roll(other.M, i, axis=0)[:2,:]

            #Check all points of trangle 1 lay on the external side of the edge E. If
            #they do, the triangles do not collide.
            if (chkEdge(np.vstack((edge, self.M[0]))) and
                chkEdge(np.vstack((edge, self.M[1]))) and
                chkEdge(np.vstack((edge, self.M[2])))):
                return False

        # overlap
        return True

    def overlap_multiple(self, multiple_tri):
        """
        check overlap with triangles in the multiple_tri list
        """
        if len(multiple_tri)==0:
            return False
        for t in multiple_tri:
            if self.overlap(t):
                return True
        return False

    def copy(self):
        return copy.deepcopy(self)

def solve(board, coordinates, solution_set, log=False):
    """
    backtraking algorithm
    """

    if len(coordinates)==0:
        return True

    coord = coordinates.pop() #starting from big
    legal_tri = board.all_legal_triangles(coord, solution_set)

    if log:
        print("coord: ", coord)
        print("coordinates: ", coordinates)
        print("legal_tri: ", legal_tri)
        print("solution set: ", solution_set)
        print()

    if len(legal_tri)==0:
        coordinates.append(coord)
        return False

    for t in legal_tri:

        solution_set.append(t)
        if solve(board, coordinates, solution_set, log):
            return True
        solution_set.pop()

    coordinates.append(coord)
    return False

if __name__=="__main__":

    M = np.loadtxt(open("./data/data_toy.csv", "rb"), delimiter=";")
    n = M.shape[0]
    b = board(n)
    for i in range(n):
        for j in range(n):
            if M[i,j] != 0:
                b.set_number((i,j),M[i,j],ordered=True)

    # t = b.all_legal_triangles((8,8))
    # index = 0
    # (aa,bb) = t[index]._generate_inside_points()

    # print_board(b, t, bb)

    # all_t={}
    # for c in b.coordinates:
    #     all_t[c] = b.all_legal_triangles(c)

    # for k,v in all_t.items():
    #     print(k,len(v))


    tic = timeit.default_timer()
    solution_set = []
    coordinates = b.coordinates.copy()
    if solve(b, coordinates, solution_set, log=True):
        print_board(b, solution_set, filename="toy.ps")
    else:
        print("No solution")
    toc = timeit.default_timer()
    print("time (s): ", toc-tic)
