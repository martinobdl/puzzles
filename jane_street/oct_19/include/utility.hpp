#ifndef UTILITY_H
#define UTILITY_H

#include <stdlib.h>
#include <vector>
#include "Point.hpp"
#include "Triangle.hpp"
#include "Board.hpp"

class Board;
class Triangle;
class Point;

double area_triangle(const int& Ax,const int& Ay,const int& Bx,const int& By,const int& Cx,const int& Cy);
unsigned floorSqrt(const unsigned &x);
std::vector<std::tuple<int,int>> all_sides(const int &area);
void save_triangles_to_file(const std::vector<Triangle>& tri, const std::string& filename);

#endif
