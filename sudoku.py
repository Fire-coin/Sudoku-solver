class SudokuCell:
    def __init__(self, minimalValue: int, maximalValue: int) -> None:
        self.min = minimalValue
        self.max = maximalValue
        self.possible = set([x for x in range(minimalValue, maximalValue + 1)])
        self.value = -1
    
    
    def remove(self, value: int) -> None:
        if value in self.possible:
            self.possible.remove(value)
    
    
    def check(self) -> bool:
        if (self.value != -1):
            return False
        if (len(self.possible) == 1):
            self.setValue(self.possible.pop())
            return True
        return False
    
    def getValue(self) -> int:
        return self.value
    
    def setValue(self, val: int) -> None:
        self.value = val
    
    def __eq__(self, value: object) -> bool:
        if value.value == self.value and value.possible == self.possible:
            return True
        return False
    
    def setPossible(self, value: list[int] | None):
        if value == None:
            self.possible = set([x for x in range(self.min, self.max + 1)])
        else:
            self.possible = value
    

class SudokuCellMatrix:
    def __init__(self, size: int, minimalValue: int, maximalValue: int) -> None:
        self.size = size
        self.min = minimalValue
        self.max = maximalValue
        self.matrix: list[list[SudokuCell]] = []
        for i in range(size):
            row = []
            for j in range(size):
                row.append(SudokuCell(self.min, self.max))
            self.matrix.append(row)
        
    def setValue(self, rowIndex: int, columnIndex: int, value: int) -> None:
        self.matrix[rowIndex][columnIndex].setValue(value)
    
    def getValue(self, rowIndex: int, columnIndex: int) -> int:
        return self.matrix[rowIndex][columnIndex].getValue()
    
    def setMatrix(self, mat: list[list[int]], minimal: int):
        if len(mat) != self.size:
            raise ValueError(f"Trying to use matrix of size {len(mat)} with matrix of size {self.size}")
        elif len(mat[0]) != self.size:
            raise ValueError(f"Matrix is not square matrix")

        for i in range(self.size):
            for j in range(self.size):
                if mat[i][j] < minimal:
                    self.matrix[i][j].setValue(-1)
                    self.matrix[i][j].setPossible(None)
                else:
                    self.matrix[i][j].setPossible(list((mat[i][j],)))
    
    def __eq__(self, value: object) -> bool:
        if value.matrix == self.matrix:
            return True
        return False
    
    def getCell(self, rowIndex, columnIndex) -> SudokuCell:
        return self.matrix[rowIndex][columnIndex]
    
    def showMatrix(self):
        for i in range(self.size):
            arr = list(map(lambda x: x.getValue(), self.matrix[i]))
            print(*arr)
    
    def full(self) -> bool:
        for i in range(self.size):
            for j in range(self.size):
                if self.matrix[i][j].getValue() == -1:
                    return False
        return True

class SudokuCellAdjacencyMatrix:
    def __init__(self, size: int, shapeWidth: int, shapeHeight: int) -> None:
        self.size = size
        self.matrix = []
        self.matrix2 = []
        self.helping = []
        for i in range(size * size):
            row = [0] * (size * size)
            self.matrix.append(row)
        
        # Connecting cells in rows
        for k in range(size):
            for i in range(size):
                for j in range(i + 1, size):
                    self.matrix[i + size * k][j + size * k] = 1
                    self.matrix[j + size * k][i + size * k] = 1
        
        # Connecting cells in collumns
        for k in range(size - 1):
            for i in range(size):
                for j in range(1, size - k):
                    self.matrix[i + k * size][i + size * j + k * size] = 1
                    self.matrix[i + size * j + k * size][i + k * size] = 1
        
        # Connecting cells in shape
        increment = 0
        for a in range(size // shapeWidth):
            for b in range(size // shapeHeight):
                for i in range(shapeWidth):
                    for j in range(shapeHeight):
                        for k in range(shapeWidth):
                            for l in range(shapeHeight):
                                if i == k and j == l:
                                    continue
                                self.matrix[i + j * size + increment][k + l * size + increment] = 1
                                self.matrix[k + l * size + increment][i + j * size + increment] = 1
                increment += shapeWidth
            increment += (size * (size // shapeWidth - 1))
        
        
        for i in range(size * size):
            s = set()
            for j in range (size * size):
                if self.matrix[i][j] != 0:
                    s.add(j)
            self.helping.append(s)

        for i in range(size):
            self.matrix2.append(self.helping[size * i: (i + 1) * size])
        
    
    def showMatrix(self) -> None:
        for i in range(self.size ** 2):
            print(*self.matrix[i])
        for i in range(self.size):
            print(*self.matrix2[i])
    
    def getMatrix(self):
        return self.matrix2
    
    def getRawMatrix(self):
        return self.matrix
    
    def getValue(self, rowIndex: int, columnIndex: int):
        return self.matrix2[rowIndex][columnIndex]


class SudokuSizeError(Exception):
    ...

class SudokuNotSetError(Exception):
    ...

class Sudoku:
    def __init__(self, minimalValue: int, maximalValue: int, shapeWidth= 3, shapeHeight= 3) -> None:
        if minimalValue < 1:
            print("Entered invalid minimal value, adjusting to 1")
            self.min = 1
        else:
            self.min = minimalValue
        self.max = maximalValue
        self.shapeWidth = shapeWidth
        self.shapeHeight = shapeHeight
        self.size = self.max - self.min + 1
        if self.size < 1:
            raise SudokuSizeError(f"Invalid sudoku size of {self.size}")

        self.valueMatrix = SudokuCellMatrix(self.size, self.min, self.max)
        self.connectionMatrix = SudokuCellAdjacencyMatrix(self.size, self.shapeWidth, self.shapeHeight)
    
    
    def setSudoku(self, fromInput= True, mat = []):
        if fromInput:
            mat = []
            print(f"Enter {self.size}x{self.size} matrix with values from sudoku, if there is no value enter 0:")
            for i in range(self.size):
                row = [int(_) for _ in input().split()]
                mat.append(row)
        else:
            if mat == []:
                raise ValueError("Expected list[list[int]] got []")
        self.valueMatrix.setMatrix(mat, self.min)
    
    
    def solveSudoku(self):
        if self.valueMatrix == SudokuCellMatrix(self.size, self.min, self.max):
            raise SudokuNotSetError("Sudoku has not been set or is empty, cannot solve empty sudoku")
        else:
            for i in range(self.size):
                var = True
                for j in range(self.size):
                    for k in range(self.size):
                        if (self.valueMatrix.getCell(j, k).check()):
                            var = False
                            cellValue = self.valueMatrix.getValue(j, k)
                            connections = self.connectionMatrix.getValue(j, k)
                            for l in connections:
                                r, c = divmod(l, self.size)
                                self.valueMatrix.getCell(r, c).remove(cellValue)
                if var:
                    if self.valueMatrix.full():
                        break
                    print("Sudoku cannot be solved")
                    break        
            if not self.valueMatrix.full():
                print('Could not solve sudoku, need more detail')
    
    def showSudoku(self) -> None:
        self.valueMatrix.showMatrix()
            
if __name__ == "__main__":
    s = Sudoku(1, 4, 2, 2)
    s.setSudoku(fromInput= False, mat= [[0, 0, 0, 4], [0, 3, 0, 0], [0, 0, 4, 0], [2, 0, 0, 0]])
    s.solveSudoku()
    print("Solved sudoku: ")
    s.showSudoku()