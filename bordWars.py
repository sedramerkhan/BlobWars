class BordWars:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [['-' for _ in range(width)] for _ in range(width)]
        self.board[0][0] = self.board[0][height - 1] = 'X'
        self.board[width - 1][0] = self.board[width - 1][height - 1] = 'O'
        # self.board[3][3] = 'X'
        self.updated =[]
        print(self)

    def check_win(self, player= 'X'):
        '''

        :param player: X, O
        :return: #  0: no one ,1: player win, 2: opponent win, 3: withdraw
        '''
        opponent = 'O' if player == 'X' else 'X'
        count_p1,count_p2 = 0, 0
        for row in self.board:
            count_p1 += row.count(player)
            count_p2 += row.count(opponent)
        if self.is_full():
            if count_p1 > count_p2:
                return 1
            elif count_p2 > count_p1:
                return 2
            else:
                return 3

        if count_p2 == 0: return 1
        if count_p1 == 0: return 2
        return 0

    # Check if the player can push the button or not
    def is_free(self, i, j):
        return self.board[i][j] == '-'

    # Check the board is full or not
    def is_full(self, board=None):
        if board is None:
            board = self.board
        for row in board:
            if row.count('-') > 0:
                return False
        return True

    def update_cell(self,i,j,player):
        opponent = 'O' if player == 'X' else 'X'
        if self.board[i][j] == opponent:
            self.board[i][j] = player
            self.updated.append((i,j))

    def move(self,i,j):
        self.board[i][j] = '-'

    def update_board(self,i,j,player):
        start_x, end_x, start_y, end_y = self.calc_indexes(i, j)
        self.updated = []
        self.board[i][j] = player
        for c in range(start_y, end_y + 1):
            self.update_cell(start_x,c,player)
            self.update_cell(end_x,c,player)

        self.update_cell(i, start_y, player)
        self.update_cell(i, end_y, player)
        print(self)
        return self.updated

    def calc_indexes(self, i, j, num=1):

        start_x = i - num if i - num >= 0 else i
        end_x = i + num if i + num < self.height else i
        start_y = j - num if j - num >= 0 else j
        end_y = j + num if j + num < self.width else j
        return start_x, end_x, start_y, end_y


    def __str__(self):
        for row in self.board:
            for item in row:
                print(item, end=" ")
            print("")
        return ""


if __name__ == '__main__':
    game = BordWars(10, 12)
