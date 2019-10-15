#include <vector>
#include <stdlib.h>
#include "Point.hpp"
#include "Triangle.hpp"
#include "Board.hpp"

bool solve( const Board& board,
            std::vector<std::tuple<unsigned,unsigned>>& coordinates,
            std::vector<Triangle>& solution_set,
            bool log)
{
    if(coordinates.size()==0)
    {
        return true;
    }

    std::tuple<unsigned,unsigned> coord = coordinates[coordinates.size()-1];
    coordinates.pop_back();
    std::vector<Triangle> legal_tri = board.legal_triangles(std::get<0>(coord),
                                                            std::get<1>(coord),
                                                            solution_set);

    if(log)
    {
        std::cout << "coordinates ramaining: " << coordinates.size() << std::endl;
        std::cout << "coord: " << std::get<0>(coord)<<","<<std::get<1>(coord) << std::endl;
        std::cout << "legal tri: " << std::endl;
        for(auto it=legal_tri.begin(); it!=legal_tri.end(); it++ )
        {
                std::cout << *it << std::endl;
        }
        std::cout << "solution set: " << std::endl;
        for(auto it=solution_set.begin(); it!=solution_set.end(); it++ )
        {
            std::cout << *it << std::endl;
        }
        std::cout << std::endl;
    }

    if(legal_tri.size()==0)
    {
        coordinates.push_back(coord);
        return false;
    }

    for(auto tri_it=legal_tri.begin(); tri_it!=legal_tri.end(); tri_it++)
    {
        solution_set.push_back(*tri_it);
        if(solve(board, coordinates, solution_set, log))
        {
            return true;
        }
        solution_set.pop_back();
    }

    coordinates.push_back(coord);
    return false;
}

int main(){

    std::cout << "SOLVING..." << std::endl;
    // Board board(17);
    Board board("data/data.csv");
    std::vector<Triangle> solution_set;
    std::vector<std::tuple<unsigned, unsigned>> coordinates = board.get_coordinates();
    if(solve(board, coordinates, solution_set, false))
    {
        for( auto it=solution_set.begin(); it !=solution_set.end(); it++ )
        {
            std::cout << *it << std::endl;
        }
    }
    else
    {
        std::cout << "No solution" << std::endl;
    }

    save_triangles_to_file(solution_set,"triangles.csv");

    return 0;
}
