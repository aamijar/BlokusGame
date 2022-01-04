from typing import List
import numpy as np


class Piece:

    def __init__(self, matrix: List[List[int]]) -> None:
        self.coords = [[]]
        self.corners = [[]]
        self.all_coords = []
        self.all_corners = []

        for x in range(len(matrix)):
            for y in range(len(matrix[x])):
                if matrix[x][y] == 1:
                    self.coords[0].append((x, y))
                    lr = False
                    tb = False
                    if y - 1 >= 0 and y + 1 < len(matrix[x]):
                        if matrix[x][y - 1] == 1 and matrix[x][y + 1] == 1:
                            lr = True
                    if x - 1 >= 0 and x + 1 < len(matrix):
                        if matrix[x - 1][y] == 1 and matrix[x + 1][y] == 1:
                            tb = True
                    if not (lr or tb):
                        self.corners[0].append((x, y))
                    # print((x, y), lr, tb)

    def print_piece(self):
        a = np.zeros((5, 5), str)
        corners = ["X" for x in range(len(self.corners[0]))]
        edges = ["I" for x in range(len(self.coords[0]))]
        rows, cols = zip(*self.coords[0])
        a[rows, cols] = edges
        rows, cols = zip(*self.corners[0])
        a[rows, cols] = corners
        print("")
        for row in a:
            for col in row:
                if col == "":
                    print(".", end=" ")
                else:
                    print(col, end=" ")
            print("")
        print("")

    def rotate90_clockwise(self):
        yMin = 0
        xMin = 0

        for x in range(len(self.coords[0])):
            self.coords[0][x] = (-self.coords[0][x][1], self.coords[0][x][0])
            if self.coords[0][x][1] < yMin:
                yMin = self.coords[0][x][1]
            if self.coords[0][x][0] < xMin:
                xMin = self.coords[0][x][0]
        for x in range(len(self.corners[0])):
            self.corners[0][x] = (-self.corners[0][x][1] - xMin, self.corners[0][x][0] - yMin)
        for x in range(len(self.coords[0])):
            self.coords[0][x] = (self.coords[0][x][0] - xMin, self.coords[0][x][1] - yMin)

    def flip(self) -> None:

        yMin = 0

        for x in range(len(self.coords[0])):
            self.coords[0][x] = (self.coords[0][x][0], -self.coords[0][x][1])
            if self.coords[0][x][1] < yMin:
                yMin = self.coords[0][x][1]
        for x in range(len(self.corners[0])):
            self.corners[0][x] = (self.corners[0][x][0], -self.corners[0][x][1] - yMin)
        for x in range(len(self.coords[0])):
            self.coords[0][x] = (self.coords[0][x][0], self.coords[0][x][1] - yMin)

    def all_transformations(self):
        self.all_coords.append(self.coords[0].copy())
        self.all_corners.append(self.corners[0].copy())
        self.add_transform()
        for x in range(4):
            self.rotate90_clockwise()
            self.add_transform()
        self.flip()
        self.add_transform()
        for x in range(4):
            self.rotate90_clockwise()
            self.add_transform()

    def add_transform(self):
        isUniqueGlobal = False
        for all_coords in self.all_coords:
            isUnique = False
            for coords in self.coords[0]:
                if coords not in all_coords:
                    isUnique = True
                    break
            if not isUnique:
                isUniqueGlobal = False
                break
            else:
                isUniqueGlobal = True
        if isUniqueGlobal:
            self.all_coords.append(self.coords[0].copy())
            self.all_corners.append(self.corners[0].copy())

    def print_all_pieces(self):
        for x in range(len(self.all_coords)):
            a = np.zeros((5, 5), str)
            corners = ["X" for x in range(len(self.all_corners[x]))]
            edges = ["I" for x in range(len(self.all_coords[x]))]
            rows, cols = zip(*self.all_coords[x])
            a[rows, cols] = edges
            rows, cols = zip(*self.all_corners[x])
            a[rows, cols] = corners
            print("")
            for row in a:
                for col in row:
                    if col == "":
                        print(".", end=" ")
                    else:
                        print(col, end=" ")
                print("")
            print("")


class Grid:
    def __init__(self, rows, cols, players):
        self.grid = np.zeros((rows, cols), int)
        self.avail_blocks = {}
        bl = (rows - 1, cols - 1)
        for p in range(players):
            bl = (bl[1], bl[1] + ((p - 1) * ((rows - 1) * (1 - (p % 2)))))
            self.avail_blocks[p] = [bl]

    def print(self):
        a = np.asarray(self.grid, str)
        corners_coords = [y for x in self.avail_blocks for y in self.avail_blocks[x]]
        corners = ["X" for x in range(len(corners_coords))]
        rows, cols = zip(*corners_coords)
        a[rows, cols] = corners
        print("")
        for row in a:
            for col in row:
                if col == "":
                    print(".", end=" ")
                elif col == "0":
                    print(".", end=" ")
                else:
                    print(col, end=" ")
            print("")
        print("")


# start program here
def main() -> None:
    blocks = [
        [[1, 0, 0],
         [1, 0, 0],
         [1, 1, 0]],

        [[1, 0, 0],
         [1, 0, 0],
         [1, 1, 1]],

        [[1, 0, 0],
         [1, 1, 0],
         [1, 1, 0]],

        [[1, 1, 0],
         [1, 1, 0],
         [0, 0, 0]],

        [[1, 0, 0],
         [1, 1, 0],
         [1, 0, 0]]
    ]

    pieces = [Piece(b) for b in blocks]
    for p in pieces:
        p.all_transformations()
        p.print_all_pieces()
    g = Grid(5, 5, players=4)
    print(g.avail_blocks)
    g.print()


if __name__ == '__main__':
    main()
