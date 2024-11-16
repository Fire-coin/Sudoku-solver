This is basic sudoku solver.
It uses graph thoery to solve sudoku, every cell of sudoku is connected to all cells that can affect it, like all cell in a row are connected, all cells in a column are connected and all cell in a shape are connected. 
By the term shape I mean what is ussually a 3x3 square in normal 9x9 sudoku, but I have also seen shapes like 2x3, so I added possibility to make different shapes in there, but I haven't tested those though. I have to find those type and test it.
The square shape works well, but for it to function correctly it needs to be a multiple of sudoku.
Created sudoku has form of a square which is calculated based on range of available values to use. 
