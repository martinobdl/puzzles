#include "Point.hpp"

Point::Point(const int& x_, const int& y_):x(x_),y(y_){};

bool Point::is_on_line(const Point& A, const Point& B) const
{
    if((this->y-A.get_y())*(B.get_x()-A.get_x()) == (B.get_y()-A.get_y())*(this->x-A.get_x()))
    {
        return true;
    }
    return false;
}

void Point::add_x(const int& dx)
{
    x += dx;
}

void Point::add_y(const int& dy)
{
    y += dy;
}

int Point::get_x(void) const
{
    return x;
}

int Point::get_y(void) const
{
    return y;
}

bool Point::operator==(const Point& other) const
{
    return this->x == other.get_x() && this->y == other.get_y();
}

std::ostream& operator<<(std::ostream& os, const Point& p)
{
    os << "("<<p.get_x()<<","<<p.get_y()<<")";
    return os;
}

void Point::shift(const int& dx, const int& dy)
{
    this->add_x(dx);
    this->add_y(dy);
}
