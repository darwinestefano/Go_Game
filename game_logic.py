from piece import Piece

class GameLogic:

    turn = 2

    def getTurn(self, pieceColour):
        ''' Turn: Game starts with Black going first
            pieceColour is an integer as follows:
            white = 1
            black = 2'''
        self.turn = pieceColour
        # Display who turn it is
        if self.turn == 1:
            print("===== WHITE TURN =====")
        elif self.turn == 2:
            print("===== BLACK TURN =====")

        return self.turn

    def get_liberties_positions(self, row, col):
        ''' Gets the list of liberties' positions (row, column):
        [top, bottom, left, right] '''
        libertiesPositions = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]

        # if Piece is located at an edge, remove non-existing liberties
        # checking x and y for row and column
        for point in libertiesPositions:
            if not -1 < point[0] < 8 or not -1 < point[1] < 8:
                libertiesPositions.remove(point)

        return libertiesPositions

    def get_liberties_pieces(self, board, libertiesPos):
        ''' return list of the pieces placed on the liberties
        (0: no piece, 1: white, 2: black) given the board and
        the liberties' positions '''
        libertiesPieces = []
        for positions in libertiesPos:
            libertiesPieces.append(board[positions[0]][positions[1]])
        return libertiesPieces

    def place_piece_on_board(self, libertiesPieces, turn):
        ''' Check if is possible to place a Piece on the board.
        If there is no empty liberties and all liberties are occupied by the opponent piece,
        it is NOT possible to place your piece (suicidal rule)
        Suicidal rule: you cannot place a piece which will immediately have no liberties
        This code also handles the KO rule: previous game state are not allowed (eternity rule)  '''
        placePiece = True
        if not libertiesPieces.count(0) > 0 and not libertiesPieces.count(turn) > 0:
            # check length of array to prevent indexOutOfBounds Exception (crash app)
            if len(libertiesPieces) == 2:
                if libertiesPieces[0] == libertiesPieces[1]:
                    placePiece = False
            elif len(libertiesPieces) == 3:
                if libertiesPieces[0] == libertiesPieces[1] and libertiesPieces[1] == libertiesPieces[2]:
                    placePiece = False
            else:
                if libertiesPieces[0] == libertiesPieces[1] and libertiesPieces[1] == libertiesPieces[2] and libertiesPieces[2] == libertiesPieces[3]:
                    placePiece = False
        return placePiece


    def get_opponent_group(self, libertiesPos, row, col, boardArray):
        ''' return an array of liberties of the placed piece'''
        # array to store locations of the opponent's (clear array in each click)
        # 2D array to store multiple separate groups:
        # row 0: Group found at the top of the piece
        # row 1: bottom, row 2: left, row 3: right
        self.opponentGroup = []
        for x in range(0, 4):                   #initializing the array
            self.opponentGroup.append([])
            for y in range(0, 32):              # 32: half of the board filled with the same colour
                self.opponentGroup[x].append([])

        self.countX = 0  # counter to keep track of the row number
        self.countY = 0  # counter to keep track of the column number

        # loop through liberties to find an opponent Piece
        # loop will be in the order: top, bottom, left and right
        for piece in libertiesPos:
            ''' if an opponent is found in some liberty, add it to the group of opponent's group
            if found at the top liberty: add to the first row
            if found at the bottom liberty: add to the second row and so on
            self.turn will be the opponent '''
            if boardArray[piece[0]][piece[1]] == self.turn:
                self.opponentGroup[self.countX][self.countY].append((piece[0], piece[1]))
                self.countY += 1    # increment column counter so next piece won't overwrite existing piece
                self.scanOpponent(self, piece, row, col, boardArray)    # keep checking if there is more to add to the group
            self.countX += 1    # increment row counter so next group will be added to a different group
            self.countY = 0     # reset column counter

        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.opponentGroup]))
        return self.opponentGroup

    def scanOpponent(self, p, row, col, boardArray):
        ''' This method will recursively check if there is more pieces to be added
        to the opponent's group (if the opponent has any free liberty it will break the checking
        as it still can collect more pieces to its group)'''
        # get positions of the opponent's liberties
        libertiesPos = self.get_liberties_positions(self, p[0], p[1])

        print("ENTRANDO NO METODO SCAN OPPONENT. ROW: ", self.countX)
        print("CURRENT PIECE: ", p[0], p[1])
        print("CURRENT PIECE LIBERTIES: ", libertiesPos)

        # loop through each liberty
        for piece in libertiesPos:
            if piece[0] == row and piece[1] == col:
                print("Scan Opponent: SKIP", piece[0], piece[1])
                continue              # prevents to keep scanning the same Piece over and over
            elif boardArray[piece[0]][piece[1]] == 0:    # opponent has free liberties
                print("Scan Opponent: opponent has free liberties")
                return
            elif boardArray[piece[0]][piece[1]] == self.turn:   # more to be added to the group
                print((piece[0], piece[1]))

                if self.opponentGroup[self.countX].count([(piece[0], piece[1])]) > 0:  # check if the piece wasn't already added
                    #todo IF WAS ALREADY ADDED KEEP XXXXXXXXXXXXXXXXXX
                    print("Scan Opponent: piece was already added to the group")
                    return
                print("Scan Opponent: adding", piece[0], piece[1])
                # if it wasn't already added to the group, add it
                self.opponentGroup[self.countX][self.countY].append((piece[0], piece[1]))
                self.countY += 1    # increment column counter so next piece won't overwrite existing piece
                self.scanOpponent(self, piece, p[0], p[1], boardArray)      # recursive call


        print(self.opponentGroup[self.countX])
        return

    def isSurrounded(self, group, board):
        ''' check if opponent is surrounded without free liberties
        param group = the opponent's group'''
        # temporary array to ckeck if all the liberties of the group (opponent's group)
        # are not empty and surrounded by the player's piece
        groupLiberties = []

        # Check each row in group (array 2D)
        for i in range(0, len(group)):
            for piece in group[i]:
                ''' for each piece in the opponent's group, a checking in its liberties
                will be performed'''
                # get the list of liberties' positions
                liberties = self.get_liberties_positions(self, piece[0], piece[1])

                for pos in liberties:       # pos: position (row, col)
                    # if it's not the opponent's piece
                    # (it's the player's piece or an empty space, add to the groupLiberties array)
                    if not board[pos[0]][pos[1]] == self.turn:
                        groupLiberties.append(board[pos[0]][pos[1]])

        ''' Check the groupLiberties array: if array is not empty and there is no empty Pieces
        surrounding the group, meaning the group is surrounded by the player's pieces, return TRUE
        (The player scores and the opponent's loses territory).'''
        if not groupLiberties.count(Piece.NoPiece) > 0 and not groupLiberties == []:
            return True
        else:
            return False
