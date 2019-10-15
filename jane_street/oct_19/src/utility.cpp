#include "utility.hpp"

double area_triangle(const int& Ax,const int& Ay,const int& Bx,const int& By,const int& Cx,const int& Cy)
{
    return abs(Ax*(By-Cy)+Bx*(Cy-Ay)+Cx*(Ay-By))/2.;
}

int floorSqrt(const int &x)
{
    if (x == 0 || x == 1)
    {
        return x;
    }

    int i = 1, result = 1;
    while (result <= x)
    {
        i++;
        result = i * i;
    }
    return i - 1;
}

std::vector<std::tuple<int,int>> all_sides(const int &area)
{
    std::vector<std::tuple<int,int>> sides;
    int sqare_root = floorSqrt(2*area);
    for (int i = 2; i <= sqare_root; ++i)
    {
        if (2*area % i == 0)
        {
            sides.push_back(std::tuple<int,int>(i,2*area/i));
        }
    }
    return sides;
}

void save_triangles_to_file(const std::vector<Triangle>& tri, const std::string& filename)
{
    std::ofstream of;
    of.open (filename);
    for(auto t=tri.begin(); t!=tri.end(); t++)
    {
        of <<   t->get_Ax() << ";" << t->get_Ay() << ";" <<
                t->get_Bx() << ";" << t->get_By() << ";" <<
                t->get_Cx() << ";" << t->get_Cy() << "\n";
    }
    of.close();
}
