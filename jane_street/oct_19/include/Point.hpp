#ifndef POINT_H
#define POINT_H
#include <iostream>

class Point{
private:
    int x;
    int y;
public:
    Point(const int& x_, const int& y_);
    bool is_on_line(const Point& A, const Point& B) const;
    void add_x(const int& dx);
    void add_y(const int& dy);
    void shift(const int& dx, const int& dy);
    int get_x(void) const;
    int get_y(void) const;
    bool operator==(const Point& other) const;
    friend std::ostream& operator<<(std::ostream& os, const Point& p);
};

#endif
