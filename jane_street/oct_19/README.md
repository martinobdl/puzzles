# TriTriAgain

Rules: place a collection of triangles on the grid such that:
* triangles are of integer coordinates and right
* each triangle contains only one numbered square and contains it fully
* the area of a triangle is equal to the number it contains
* no triangle intersect with another

Checking if a proposed solution is valid is polynomial in time. Hence we can think to solve the problem recursively by backtracking as the simplest kind of sudoku solvers:
* add a new element to the solution
* if its valid then solve the smaller problem
* if it's not valid then go back an try another legal move
* if there are no legal moves then go back again
* repeat

This is called [algorithm X](https://en.wikipedia.org/wiki/Knuth%27s_Algorithm_X).

![Alt Text](https://github.com/martinobdl/puzzles/tree/master/jane_street/oct_19/img/Sudoku_solved_by_bactracking.gif)

Since the problem seems very similar to a sudoku, we can hope to formulate the problem in a [exact cover problem](https://en.wikipedia.org/wiki/Exact_cover) and use the efficient [dancing links algorithm](https://en.wikipedia.org/wiki/Dancing_Links).
Sadly I couldn't find a translation of the problem as an exact cover even I'm confident this can be done.
The naive solution, implemented in c++ thinking a little about efficiency, gives satisfactory performances (~7s for a 17x17 grid). Then the problem is drawn in a .ps file with turtle python module
#### run example
```
make
./bin/TriTriAgain data/data.csv
python3 draw.py data/data.csv triangles.csv
```
![Alt Text](https://github.com/martinobdl/puzzles/tree/master/jane_street/oct_19/img/TriTriAgain.png)
