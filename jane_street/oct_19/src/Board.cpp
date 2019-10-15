#include <armadillo>
#include <iostream>
#include "Board.hpp"

Board::Board(const unsigned& size_):size(size_)
{
    this->matrix = arma::Mat<int>(static_cast<unsigned>(this->size),static_cast<unsigned>(this->size),arma::fill::zeros);
}

Board::Board(const std::string &filename)
{
    unsigned rows=0;
    std::ifstream file(filename);
    std::string line;
    while (getline(file, line))
    rows++;
    *this = Board(rows);
    read_from_csv(filename);
}

void Board::set_number(const std::tuple<unsigned, unsigned>& coord, const int& n)
{
    this->matrix(std::get<0>(coord),std::get<1>(coord)) = n;

    if(this->numbers.size()==0)
    {
        this->numbers.push_back(n);
        this->coordinates.push_back(coord);
    }
    else
    {
        auto it_c = this->coordinates.begin();
        auto it_n=this->numbers.begin();
        for( ; it_n != this->numbers.end(); it_n++)
        {
            if(n <= *it_n)
            {
                this->numbers.insert(it_n, n);
                this->coordinates.insert(it_c, coord);
                return;
            }
            it_c++;
        }
        this->numbers.insert(it_n, n);
        this->coordinates.insert(it_c, coord);
    }
}

void Board::read_from_csv(const std::string &filename)
{
    std::ifstream in( filename );
    std::string line;
    unsigned i=0;
    unsigned j=0;
    while ( getline( in, line ) )
    {
        std::stringstream ss( line );
        std::string data;
        while ( getline( ss, data, ';' ) )
        {
            int n = std::stoi(data);
            if(n!=0)
            {
                this->set_number(std::tuple<unsigned,unsigned>(i,j),n);
            }
            j++;
        }
        i++;
        j=0;
    }
}

void Board::print(void) const
{
    this->matrix.print("Board: ");
}

void Board::print_data(void) const
{
    for(unsigned i=0; i<this->numbers.size(); i++)
    {
        std::cout << "(" << std::get<0>(this->coordinates[i]) << "," << std::get<1>(this->coordinates[i]) << ") -> "
        << this->numbers[i] << std::endl;
    }
}

bool Board::tri_is_inside_board(const Triangle& tri) const
{
    return tri.get_x_max() <= static_cast<int>(this->size) && tri.get_y_max() <= static_cast<int>(this->size) && tri.get_x_min() >= 0 && tri.get_y_min() >= 0;
}

std::vector<Triangle> Board::generate_triangles(const unsigned& x, const unsigned& y) const
{
    std::vector<Triangle> tri;
    int area = this->matrix(x,y);
    if(area == 0)
    {
        return tri;
    }
    std::vector<std::tuple<int,int>> sides = all_sides(area);
    for(auto it=sides.begin(); it!= sides.end(); it++)
    {
        int a = std::get<0>(*it);
        int b = std::get<1>(*it);
        Point A(0,0);
        Point B(a,0);
        Point C(0,b);
        Triangle t(A,B,C);
        Triangle t_=t;
        for(int i=0; i<4; i++)
        {
            tri.push_back(t_);
            t_ = t_.rotate();
        }
        if (a!=b)
        {
            t_ = t_.mirror();
            for(int i=0; i<4; i++)
            {
                tri.push_back(t_);
                t_ = t_.rotate();
            }
        }

    }
    return tri;
}

std::vector<Triangle> Board::legal_triangles(   const unsigned& x,
                                                const unsigned& y,
                                                std::vector<Triangle>& fixed_tri) const
{
    std::vector<Triangle> legal_triangles;
    int area = this->matrix(x,y);
    if(area == 0)
    {
        return legal_triangles;
    }

    int x_int = static_cast<int>(x);
    int y_int = static_cast<int>(y);

    std::vector<Triangle> tri = this->generate_triangles(x,y);

    for(auto it_tri=tri.begin(); it_tri!=tri.end(); it_tri++)
    {
        std::pair<std::vector<Point>,std::vector<Point>> touched_point = it_tri->get_touched_point();
        std::vector<Point> contained_points = std::get<0>(touched_point);
        std::vector<Point> boundary_points = std::get<1>(touched_point);
        for(auto it_point=contained_points.begin(); it_point!=contained_points.end(); it_point++)
        {
            Triangle t_=*it_tri;
            t_.shift(x_int-it_point->get_x(),y_int-it_point->get_y());

            std::vector<Point> shifted_inside_points = contained_points;
            std::vector<Point> shifted_boundary_points = boundary_points;

            for(auto tmp=shifted_inside_points.begin(); tmp!=shifted_inside_points.end(); tmp++)
            {
                tmp->shift(x_int-it_point->get_x(),y_int-it_point->get_y());
            }
            for(auto tmp=shifted_boundary_points.begin(); tmp!=shifted_boundary_points.end(); tmp++)
            {
                tmp->shift(x_int-it_point->get_x(),y_int-it_point->get_y());
            }

            shifted_inside_points.insert(shifted_inside_points.end(),
                                        shifted_boundary_points.begin(),
                                        shifted_boundary_points.end());

            if(this->tri_is_inside_board(t_) and
                not(t_.overlap_multiple(fixed_tri)) and
                this->contain_one_number(shifted_inside_points))
            {
                legal_triangles.push_back(t_);
            }
        }
    }
    return legal_triangles;
}

bool Board::contain_one_number(std::vector<Point>& points) const
{
    int count = 0;
    for(auto it_c=this->coordinates.begin(); it_c!=this->coordinates.end(); it_c++)
    {
        for(auto it_p=points.begin(); it_p!=points.end(); it_p++)
        {
            if( static_cast<int>(std::get<0>(*it_c))==it_p->get_x() and
                static_cast<int>(std::get<1>(*it_c))==it_p->get_y())
            {
                count ++;
                if(count==2)
                {
                    return false;
                }
            }
        }
    }
    return true;
}

std::vector<std::tuple<unsigned, unsigned>> Board::get_coordinates(void)
{
    return this->coordinates;
}
