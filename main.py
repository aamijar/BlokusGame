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
        self.grid = np.full((rows, cols), -1)
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
                elif col == "-1":
                    print(".", end=" ")
                else:
                    print(col, end=" ")
            print("")
        print("")

    # startPiece: corner of the piece the player wants to place
    def isValidMove(self, player: int, startBlock: tuple, startPiece: tuple, pieces: List[tuple]) -> bool:
        for p in pieces:
            x = np.subtract(p, startPiece)
            y = np.add(startBlock, x)
            if (y[0] >= len(self.grid) or y[0] < 0) or (y[1] >= len(self.grid[0]) or y[1] < 0) \
                    or self.grid[y[0]][y[1]] != -1:
                return False
            if y[1] - 1 >= 0 and self.grid[y[0]][y[1] - 1] == player:
                return False
            if y[1] + 1 < len(self.grid[0]) and self.grid[y[0]][y[1] + 1] == player:
                return False
            if y[0] - 1 >= 0 and self.grid[y[0] - 1][y[1]] == player:
                return False
            if y[0] + 1 < len(self.grid) and self.grid[y[0] + 1][y[1]] == player:
                return False
        return True

    def playPiece(self, player: int, startBlock: tuple, startPiece, pieces: List[tuple], corners: List[tuple]):
        for p in pieces:
            y = np.add(startBlock, np.subtract(p, startPiece))
            self.grid[y[0], y[1]] = player
        self.avail_blocks[player].remove(startBlock)

        for a in self.avail_blocks[player]:
            if not self.isValidMove(player, a, (0, 0), [(0, 0)]):
                self.avail_blocks[player].remove(a)

        for c in corners:
            y = np.add(startBlock, np.subtract(c, startPiece))
            if y[1] - 1 >= 0 and y[0] - 1 >= 0 and self.isValidMove(player, (y[0] - 1, y[1] - 1), (0, 0), [(0, 0)]):
                self.avail_blocks[player].append((y[0] - 1, y[1] - 1))
            if y[1] - 1 >= 0 and y[0] + 1 < len(self.grid) and self.isValidMove(player, (y[0] + 1, y[1] - 1), (0, 0), [(0, 0)]):
                self.avail_blocks[player].append((y[0] + 1, y[1] - 1))
            if y[1] + 1 < len(self.grid[0]) and y[0] - 1 >= 0 and self.isValidMove(player, (y[0] - 1, y[1] + 1), (0, 0), [(0, 0)]):
                self.avail_blocks[player].append((y[0] - 1, y[1] + 1))
            if y[1] + 1 < len(self.grid[0]) and y[0] + 1 < len(self.grid) and self.isValidMove(player, (y[0] + 1, y[1] + 1), (0, 0), [(0, 0)]):
                self.avail_blocks[player].append((y[0] + 1, y[1] + 1))


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

    last = pieces[len(pieces) - 1]
    cornerlast = last.all_corners[len(last.all_corners) - 3]
    coordslast = last.all_coords[len(last.all_coords) - 3]
    print(coordslast)
    print(cornerlast)
    print("")
    v = g.isValidMove(0, (4, 0), cornerlast[0], coordslast)
    if v:
        g.playPiece(0, (4, 0), cornerlast[0], coordslast, cornerlast)
    g.print()
    v = g.isValidMove(0, (2, 2), cornerlast[0], coordslast)
    if v:
        g.playPiece(0, (2, 2), cornerlast[0], coordslast, cornerlast)
    g.print()

if __name__ == '__main__':
    main()
