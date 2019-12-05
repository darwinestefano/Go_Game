class GameLogic:
    print("Game Logic Object Created")
    # TODO add code here to manage the logic of your game

    # Turn: Game starts with Black going first
    # white = 1, black = 2
    turn = 2
    #hasLiberty = True

    # Method that return an array of liberties of one piece given its location
    '''
    def getLiberties(self, row, col):
        print("Print liberties:")
        self.liberties = []
        self.liberties.append([row-1, col])
        self.liberties.append([row+1, col])
        self.liberties.append([row, col-1])
        self.liberties.append([row, col+1])
        return self.liberties'''

    # Method that will check if one piece has any liberty free
    # It gets the array of liberties and the board array as args
    '''
    def hasLiberty(self, libertiesArr, boardArr):
        x = -1
        y = -1
        libertyPieces = []
        for lib in libertiesArr:
            x = lib[0]
            y = lib[1]
            libertyPieces.append(boardArr[x][y])

        print(libertyPieces)'''

    # Method that checks the state of the board in each turn
    '''
    def checkBoard(self, boardArr):
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in boardArr]))
        for row in range(0, len(boardArr)):
            for col in range(0, len(boardArr[0])):
                if row != 0 and col != 0 and row != 7 and col != 7:
                    if  boardArr[row-1][col] != 0 and boardArr[row-1][col] == boardArr[row][col+1] and boardArr[row][col+1] == boardArr[row+1][col] and boardArr[row+1][col] == boardArr[row][col-1]:
                        if boardArr[row][col] == 2:
                            print("Comeu peca BLACK ")
                            
                        elif boardArr[row][col] == 1:
                            print("Comeu peca WHITE ")'''
