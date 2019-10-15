#ifndef TRIANGLE_H
#define TRIANGLE_H

#include <vector>
#include "utility.hpp"
#include "Point.hpp"

class Triangle{
private:
    Point A;
    Point B;
    Point C;
    double area;
public:
    Triangle(const Point& A_,
            const Point& B_,
            const Point& C_);
    int get_x_max(void) const;
    int get_y_max(void) const;
    int get_x_min(void) const;
    int get_y_min(void) const;
    double get_area(void) const;
    int get_Ax(void) const;
    int get_Ay(void) const;
    int get_Bx(void) const;
    int get_By(void) const;
    int get_Cx(void) const;
    int get_Cy(void) const;
    bool is_inside_tri(const Point& p) const;
    bool is_pointing_out(const Point& p) const;
    std::pair<std::vector<Point>,std::vector<Point>> get_touched_point(void) const; //<----
    void shift(const int& dx, const int& dy);
    Triangle rotate(void) const;
    Triangle mirror(void) const;
    bool overlap(Triangle& other);
    bool overlap_multiple(std::vector<Triangle>& triangles);
    void anti_clockwise(void);
    std::tuple<Point,Point> get_diagonal_point(void) const;
    bool is_on_diagonal(const Point& p) const;
    friend std::ostream& operator<<(std::ostream& os, const Triangle& t);
};

#endif
