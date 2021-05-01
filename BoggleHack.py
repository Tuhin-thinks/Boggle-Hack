from random import sample
import random

D = ["aaeegn", "abbjoo", "achops", "affkps", "aoottw", "cimotu", "deilrx", "delrvy",
     "distty", "eeghnw", "eeinsu", "ehrtvw", "eiosst", "elrtty", "himnqu", "hlnnrz"]


class Boggle():
    def __init__(self, board=None):
        self.lpfxs = []
        self.solns = set()
        self.words = []
        self.readwords('words.dat')
        if not board:
            self.board = []
            self.newgame()
        else:
            self.board = [list(map(lambda x: x.lower(), row)) for row in board]

    def readwords(self, filename):
        with open(filename, 'r') as word_file:
            for line in word_file.read().split('\n'):
                if line.strip('\n '):
                    self.words.append(line.strip('\n ').lower())
        print(f"Read {len(self.words)} words.")

    def newgame(self):
        for i in range(4):
            dice_word = sample(D, 1)[0]
            words_ = list(dice_word)
            random.shuffle(words_)
            self.board.append(list(map(lambda x: x.lower(), words_[:4])))
            self.lpfxs.extend([''.join(words_[0:x]) for x in range(1, len(words_) - 1)])  # storing legal word prefixes

    def extract(self, path):
        word = ""
        for i in path:
            word += self.board[i[0]][i[1]]
        return ''.join([self.board[i][j] for i, j in path])  # the word from board

    def solve(self):
        def adjacencies(loc, path):
            r, c = loc
            valid_positions = []
            adjacent_elems = [
                [(r - 1, c - 1), (r - 1, c), (r - 1, c + 1)],
                [(r, c - 1), (r, c + 1)],
                [(r + 1, c - 1), (r + 1, c), (r + 1, c + 1)]
            ]
            if c == 0:
                valid_positions = [n[1:] for n in adjacent_elems]
            elif c == 3:
                valid_positions = [adjacent_elems[0][0:2], [adjacent_elems[1][0]], adjacent_elems[2][0:2]]
            elif 0 < c < 3:
                # all adjacent positions in the board
                valid_positions = adjacent_elems
            else:
                pass

            if r == 0:
                # first row of the board
                valid_positions = valid_positions[1:]
            elif r == 3:
                # keep the upper 2 rows
                valid_positions = valid_positions[0:2]
            else:
                valid_positions = valid_positions[0:r] + valid_positions[r:]

            if loc not in [j for sub in path for j in sub]:
                return valid_positions

            return []

        def extend(loc, path=[]):
            word = ""
            if path:
                word = self.extract(path)
            if word in self.words and word not in self.solns:
                print(word, path)
                self.solns.add(word)
                return
            if len(word) > 5:
                return
            adjacent_pos = adjacencies(loc, path)
            # print(f"adjacent_pos:{adjacent_pos}")
            for pos in adjacent_pos:
                for coor in pos:
                    if coor in path:
                        # print("discarded option:", self.extract(path))
                        continue
                    extend(coor, path + [coor])

        for r in range(4):  # find possible word for each board position
            for c in range(4):
                extend(loc=(r, c))

    def show_board(self):
        for row in self.board:  # print the board
            print(" ".join(row))

    def checkpath(self, path):
        valid_positions = last = track = []
        last = path[0]
        for pos in path[1:]:
            r, c = last
            adjacent_elems = [
                [(r - 1, c - 1), (r - 1, c), (r - 1, c + 1)],
                [(r, c - 1), (r, c + 1)],
                [(r + 1, c - 1), (r + 1, c), (r + 1, c + 1)]
            ]
            if c == 0:
                valid_positions = [n[1:] for n in adjacent_elems]
            elif c == 3:
                valid_positions = [adjacent_elems[0][0:2], [adjacent_elems[1][0]], adjacent_elems[2][0:2]]
            elif 0 < c < 3:
                # all adjacent positions in the board
                valid_positions = adjacent_elems

            if r == 0:
                # first row of the board
                valid_positions = valid_positions[1:]
            elif r == 3:
                # keep the upper 2 rows
                valid_positions = valid_positions[0:2]
            else:
                valid_positions = valid_positions[0:r] + valid_positions[r:]

            valid_pos = [j for sub in valid_positions for j in sub]
            if pos in valid_pos and pos not in track:
                last = pos
                track.append(pos)
            else:
                return False
        track.insert(0, path[0])
        word = self.extract(track)
        result = word if word.lower() in self.words else False  # returns the word if valid else returns False
        return result


# -----------------------------------TEST CHECK_PATH()-----------------------
# b = Boggle([['Y', 'P', 'S', 'V'], ['T', 'O', 'U', 'W'], ['S', 'W', 'W', 'E'], ['U', 'M', 'N', 'E']])
# res = b.checkpath([(3, 1), (3, 2), (2, 3), (1, 2), (2, 1)])
# print(res)
# res = b.checkpath([(3, 3), (2, 2), (2, 1), (1, 1), (0, 1)])
# print(res)
# res = b.checkpath([(3, 3), (2, 2), (2, 1), (1, 1), (2, 0)])
# print(res)
# res = b.checkpath([(3, 3), (2, 2), (1, 3), (1, 2), (2, 1)])
# print(res)
# ===============================================================

# ---------------------------------TEST SOLVE()-----------------------------
board = []
with open('boards.txt', 'r') as file:
    for line in file.read().split('\n'):
        if line.strip('\n '):
            board.append(line.strip('\n ').split())

b = Boggle(board)
b.show_board()
b.solve()
print(f"{len(b.solns)} solutions found.")
print("solutions: ", b.solns)
print(b.board)
