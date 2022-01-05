import copy


class BordWars:
    def __init__(self, width, height, player):
        self.width = width
        self.height = height
        self.board = [["-" for _ in range(width)] for _ in range(height)]
        self.board[0][0] = self.board[0][-1] = "X"
        self.board[-1][0] = self.board[-1][-1] = "O"
        self.player = player

    def check_win(self, player="X"):
        """
        :param player: X, O
        :return: #  0: no one ,1: player win, 2: opponent win, 3: withdraw
        """
        opponent = "O" if player == "X" else "X"
        count_p1, count_p2 = 0, 0
        for row in self.board:
            count_p1 += row.count(player)
            count_p2 += row.count(opponent)
        if self.is_full():
            if count_p1 > count_p2:
                return 1,count_p1,count_p2
            elif count_p2 > count_p1:
                return 2,count_p1,count_p2
            else:
                return 3,count_p1,count_p2

        if count_p2 == 0:
            return 1,count_p1,count_p2
        if count_p1 == 0:
            return 2,count_p1,count_p2
        return 0,count_p1,count_p2

    # Check if the player can push the button or not
    def is_free(self, i, j):
        return self.board[i][j] == "-"

    # Check the board is full or not
    def is_full(self):
        board = self.board
        for row in board:
            if row.count("-") > 0:
                return False
        return True

    def update_cell(self, i, j):
        opponent = self.next_turn()
        if self.board[i][j] == opponent:
            self.board[i][j] = self.player
            return True
        return False

    def move(self, fi, fj, ti, tj):
        first_boarder, second_boarder = self.get_boarder(fi, fj, 1), self.get_boarder(
            fi, fj, 2
        )
        if (ti, tj) in first_boarder:
            self.first_move(fi, fj, ti, tj)
        elif (ti, tj) in second_boarder:
            self.second_move(fi, fj, ti, tj)
        else:
            print("error move" + str((fi, fj)) + " " + str((ti, tj)))
            raise ValueError("error move" + str((fi, fj)) + " " + str((ti, tj)))
        updated = self.update_board(ti, tj)
        self.player = self.next_turn()

        return updated

    def first_move(self, fi, fj, ti, tj):
        self.board[ti][tj] = self.player

    def second_move(self, fi, fj, ti, tj):
        self.board[fi][fj] = "-"
        self.board[ti][tj] = self.player
        pass

    def update_board(self, i, j):
        start_x, end_x, start_y, end_y = self.calc_indexes(i, j)
        updated = []
        player = self.player
        # self.board[i][j] = player
        for c in range(start_y, end_y + 1):
            if self.update_cell(start_x, c):
                updated.append((start_x, c))
            if self.update_cell(end_x, c):
                updated.append((end_x, c))

        if self.update_cell(i, start_y):
            updated.append((i, start_y))
        if self.update_cell(i, end_y):
            updated.append((i, end_y))

        return updated

    def calc_indexes(self, i, j, num=1):

        start_x = i - num if i - num >= 0 else 0
        end_x = i + num if i + num < self.height else self.height - 1
        start_y = j - num if j - num >= 0 else 0
        end_y = j + num if j + num < self.width else self.width - 1
        return start_x, end_x, start_y, end_y

    def __str__(self):
        out = ""
        for row in self.board:
            for item in row:
                out = out + item + " "
            out += "\n"
        return out

    def get_boarder(self, i, j, size):
        start_x, end_x, start_y, end_y = self.calc_indexes(i, j, size)
        l = set()
        for c in [start_y, end_y]:
            if c != j:
                for r in range(start_x, end_x + 1):
                    if self.board[r][c] == "-":
                        l.add((r, c))

        for r in [start_x, end_x]:
            if r != i:
                for c in range(start_y, end_y + 1):
                    if self.board[r][c] == "-":
                        l.add((r, c))

        return l

    def is_end(self):
        return bool(self.check_win()[0])

    def next_turn(self):
        return "O" if self.player == "X" else "X"

    def next_states(self):
        if self.is_end():
            return {}
        out = {}
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == self.player:
                    out[(i, j)] = self.next_states_at(i, j)
        return out

    def next_states_at(self, i, j):
        out = {}
        first_move = self.get_boarder(i, j, 1)
        second_move = self.get_boarder(i, j, 2)
        for n, m in first_move | second_move:
            # try:
            state = copy.deepcopy(self)
            state.move(i, j, n, m)
            out[n, m] = state
        # except:
        #    print(f"ignored state at {n},{m}")
        return out

    def eval(self, player):
        cx, co = 0, 0
        for c in range(self.width):
            for r in range(self.height):
                cx += self.board[r][c] == "X"
                co += self.board[r][c] == "O"
        return cx - co if player == "X" else co - cx


if __name__ == "__main__":
    game = BordWars(10, 12, "X")
