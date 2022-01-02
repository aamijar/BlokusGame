from typing import List
import numpy as np


class Piece:

    def __init__(self, matrix: List[List[int]]) -> None:
        self.coords = [[]]
        self.corners = [[]]

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
        # print(self.corners[0])
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
            # if self.coords[0][x] in self.corners[0]:
            #     self.corners[0].remove(self.coords[0][x])
            #     self.corners[0].add((-self.coords[0][x][1], self.coords[0][x][0]))

            self.coords[0][x] = (-self.coords[0][x][1], self.coords[0][x][0])
            if self.coords[0][x][1] < yMin:
                yMin = self.coords[0][x][1]
            if self.coords[0][x][0] < xMin:
                xMin = self.coords[0][x][0]
        for x in range(len(self.corners[0])):
            self.corners[0][x] = (-self.corners[0][x][1] - xMin, self.corners[0][x][0] - yMin)
        for x in range(len(self.coords[0])):
            # if self.coords[0][x] in self.corners[0]:
            #     print(self.corners[0], self.coords[0][x])
            #     self.corners[0].remove(self.coords[0][x])
            #     self.corners[0].add((self.coords[0][x][0] - xMin, self.coords[0][x][1] - yMin))
            #     print(self.coords[0][x][0] - xMin, self.coords[0][x][1] - yMin)
            #     print(self.corners[0])

            self.coords[0][x] = (self.coords[0][x][0] - xMin, self.coords[0][x][1] - yMin)

    def flip(self) -> None:

        yMin = 0

        for x in range(len(self.coords[0])):
            # if self.coords[0][x] in self.corners[0]:
            #     self.corners[0].remove(self.coords[0][x])
            #     self.corners[0].add((self.coords[0][x][0], -self.coords[0][x][1]))

            self.coords[0][x] = (self.coords[0][x][0], -self.coords[0][x][1])
            if self.coords[0][x][1] < yMin:
                yMin = self.coords[0][x][1]
        for x in range(len(self.corners[0])):
            self.corners[0][x] = (self.corners[0][x][0], -self.corners[0][x][1] - yMin)
        for x in range(len(self.coords[0])):
            # if self.coords[0][x] in self.corners[0]:
            #     self.corners[0].remove(self.coords[0][x])
            #     self.corners[0].add((self.coords[0][x][0], self.coords[0][x][1] - yMin))

            self.coords[0][x] = (self.coords[0][x][0], self.coords[0][x][1] - yMin)


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
        p.print_piece()
        p.flip()
        p.print_piece()
        p.rotate90_clockwise()
        p.print_piece()
        # p.flip()
        # p.print_piece()

    # a = [[1, 1], [1, 1]]
    # a = np.array(a)
    # b = [[0, -1], [1, 0]]
    # b = np.array(b)
    # print(a.dot(b))


if __name__ == '__main__':
    main()
