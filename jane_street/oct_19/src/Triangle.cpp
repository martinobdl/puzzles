#include <iostream>
#include <armadillo>
#include "Triangle.hpp"

Triangle::Triangle( const Point& A_,
                    const Point& B_,
                    const Point& C_):A(A_),B(B_),C(C_)
{
    this->area = area_triangle(A.get_x(),A.get_y(),B.get_x(),B.get_y(),C.get_x(),C.get_y());
}

bool Triangle::is_inside_tri(const Point& p) const
{
    double A0 = this->get_area();
    double A1 = area_triangle(p.get_x(),p.get_y(),this->get_Bx(),this->get_By(),this->get_Cx(),this->get_Cy());
    double A2 = area_triangle(this->get_Ax(),this->get_Ay(),p.get_x(),p.get_y(),this->get_Cx(),this->get_Cy());
    double A3 = area_triangle(this->get_Ax(),this->get_Ay(),this->get_Bx(),this->get_By(),p.get_x(),p.get_y());
    return A0 == A1+A2+A3;
}

bool Triangle::is_on_diagonal(const Point& p) const
{
    std::tuple<Point,Point> diagonal = this->get_diagonal_point();
    return p.is_on_line(std::get<0>(diagonal),std::get<1>(diagonal));
}

bool Triangle::is_pointing_out(const Point& p) const
{
    return (p.get_y()==this->get_y_max() || p.get_x()==this->get_x_max());
}

int Triangle::get_x_max(void) const
{
    return std::max({A.get_x(),B.get_x(),C.get_x()});
}

int Triangle::get_y_max(void) const
{
    return std::max({A.get_y(),B.get_y(),C.get_y()});
}

int Triangle::get_x_min(void) const
{
    return std::min({A.get_x(),B.get_x(),C.get_x()});
}

int Triangle::get_y_min(void) const
{
    return std::min({A.get_y(),B.get_y(),C.get_y()});
}

double Triangle::get_area(void) const
{
    return area;
}

int Triangle::get_Ax(void) const
{
    return A.get_x();
}

int Triangle::get_Ay(void) const
{
    return A.get_y();
}

int Triangle::get_Bx(void) const
{
    return B.get_x();
}

int Triangle::get_By(void) const
{
    return B.get_y();
}

int Triangle::get_Cx(void) const
{
    return C.get_x();
}

int Triangle::get_Cy(void) const
{
    return C.get_y();
}

std::tuple<Point,Point> Triangle::get_diagonal_point(void) const
{

    if(this->B.get_x() != this->A.get_x() && this->B.get_y() != this->A.get_y()){
        return std::tuple<Point,Point>(this->A, this->B);
    }

    if(this->B.get_x() != this->C.get_x() && this->B.get_y() != this->C.get_y()){
        return std::tuple<Point,Point>(this->B, this->C);
    }

    return std::tuple<Point,Point>(this->C, this->A);

}

std::pair<std::vector<Point>,std::vector<Point>> Triangle::get_touched_point(void) const
{
    std::vector<Point> all_inside_points;
    std::vector<Point> boundary_points;
    for(int x = this->get_x_min(); x<this->get_x_max(); x++)
    {
        for(int y = this->get_y_min(); y<this->get_y_max(); y++)
        {
            Point p1(x,y);
            Point p2(x+1,y);
            Point p3(x,y+1);
            Point p4(x+1,y+1);
            bool p1_inside = this->is_inside_tri(p1);
            bool p2_inside = this->is_inside_tri(p2);
            bool p3_inside = this->is_inside_tri(p3);
            bool p4_inside = this->is_inside_tri(p4);
            if(p1_inside && p2_inside && p3_inside && p4_inside)
            {
                all_inside_points.push_back(p1);
            }
            else if((not(p1_inside) || this->is_on_diagonal(p1)) &&
                    (not(p2_inside) || this->is_on_diagonal(p2)) &&
                    (not(p3_inside) || this->is_on_diagonal(p3)) &&
                    (not(p4_inside) || this->is_on_diagonal(p4))){;}
            else if (this->is_pointing_out(p1)){;}
            else
            {
                boundary_points.push_back(p1);
            }
        }
    }
    return std::make_pair(all_inside_points,boundary_points);
}

void Triangle::shift(const int& dx, const int& dy)
{
    A.add_x(dx);
    A.add_y(dy);
    B.add_x(dx);
    B.add_y(dy);
    C.add_x(dx);
    C.add_y(dy);
}

Triangle Triangle::rotate(void) const
{
    // 90° clockwise rotation around A
    int new_B_x = this->A.get_x() + (this->B.get_y() - this->A.get_y());
    int new_B_y = this->A.get_y() - (this->B.get_x() - this->A.get_x());

    int new_C_x = this->A.get_x() + (this->C.get_y() - this->A.get_y());
    int new_C_y = this->A.get_y() - (this->C.get_x() - this->A.get_x());
    // have the same orientation then before
    return Triangle(this->A,Point(new_B_x,new_B_y),Point(new_C_x,new_C_y));
}

Triangle Triangle::mirror(void) const
{
    int new_B_x = this->A.get_x() - (this->B.get_x() - this->A.get_x());
    int new_B_y = this->B.get_y();

    int new_C_x = this->A.get_x() - (this->C.get_x() - this->A.get_x());
    int new_C_y = this->C.get_y();

    return Triangle(this->A,Point(new_C_x,new_C_y),Point(new_B_x,new_B_y));
}

void Triangle::anti_clockwise(void)
{

    if  ((this->A.get_y()-this->B.get_y())*(this->B.get_x()-this->C.get_x()) >
        (this->B.get_y()-this->C.get_y())*(this->A.get_x()-this->B.get_x()))
    {
        std::swap(this->B, this->C);
    }
}

bool Triangle::overlap(Triangle& other)
{

    if(this->get_x_min() >= other.get_x_max() or this->get_x_max() <= other.get_x_min())
    {
        return false;
    }

    if(this->get_y_min() >= other.get_y_max() or this->get_y_max() <= other.get_y_min())
    {
        return false;
    }

    this->anti_clockwise();
    other.anti_clockwise();

    arma::Mat<double> matrix_this = {  {static_cast<double>(this->A.get_x()), static_cast<double>(this->A.get_y()), 1},
                                    {static_cast<double>(this->B.get_x()), static_cast<double>(this->B.get_y()), 1},
                                    {static_cast<double>(this->C.get_x()), static_cast<double>(this->C.get_y()), 1}};

    arma::Mat<double> matrix_other = {  {static_cast<double>(other.A.get_x()), static_cast<double>(other.A.get_y()), 1},
                                    {static_cast<double>(other.B.get_x()), static_cast<double>(other.B.get_y()), 1},
                                    {static_cast<double>(other.C.get_x()), static_cast<double>(other.C.get_y()), 1}};

    for(unsigned i=0; i<3; i++)
    {
        arma::Mat<double> edge = arma::shift( matrix_this, i );
        if ((arma::det(join_vert( edge.rows( 0,1 ), matrix_other.row(0)))<=0) and
            (arma::det(join_vert( edge.rows( 0,1 ), matrix_other.row(1)))<=0) and
            (arma::det(join_vert( edge.rows( 0,1 ), matrix_other.row(2)))<=0))
        {
            return false;
        }
    }

    for(unsigned i=0; i<3; i++)
    {
        arma::Mat<double> edge = arma::shift( matrix_other, i );
        if ((arma::det(join_vert( edge.rows( 0,1 ), matrix_this.row(0)))<=0) and
            (arma::det(join_vert( edge.rows( 0,1 ), matrix_this.row(1)))<=0) and
            (arma::det(join_vert( edge.rows( 0,1 ), matrix_this.row(2)))<=0))
        {
            return false;
        }
    }

    return true;
}

bool Triangle::overlap_multiple(std::vector<Triangle>& triangles)
{
    for (auto ptr = triangles.begin(); ptr != triangles.end(); ptr++)
    {
        if(this->overlap(*ptr)){
            return true;
        }
    }
    return false;
}

std::ostream& operator<<(std::ostream& os, const Triangle& t)
{
    os << "A: " << t.A << " B: " << t.B << " C: " << t.C;
    return os;
}
