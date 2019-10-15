#ifndef BOARD_H
#define BOARD_H

#include <armadillo>
#include "Triangle.hpp"
#include "Point.hpp"
#include "utility.hpp"

class Triangle;

class Board{
private:
    unsigned size;
    arma::Mat<int> matrix;
    std::vector<int> numbers;
    std::vector<std::tuple<unsigned, unsigned>> coordinates;
public:
    Board(const unsigned& size_);
    Board(const std::string &filename);
    void set_number(const std::tuple<unsigned, unsigned>& coord, const int& n);
    bool tri_is_inside_board(const Triangle& tri) const;
    std::vector<Triangle> generate_triangles(const unsigned& x, const unsigned& y) const;
    std::vector<Triangle> legal_triangles(const unsigned& x, const unsigned& y, std::vector<Triangle>& fixed_tri) const;
    void print(void) const;
    void print_data(void) const;
    void read_from_csv(const std::string &filename);
    std::vector<std::tuple<unsigned, unsigned>> get_coordinates(void);
    bool contain_one_number(std::vector<Point>& points) const;
};

#endif
