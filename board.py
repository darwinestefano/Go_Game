from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QPoint
from PyQt5.QtGui import *
from piece import Piece
from game_logic import GameLogic

class Board(QFrame):  # base the board on a QFrame widget
    updateTimerSignal = pyqtSignal(int) # signal sent when timer is updated
    clickLocationSignal = pyqtSignal(str) # signal sent when there is a new click location

    # TODO set the board width and height to be square
    boardWidth  = 7     # board is 7 squares wide
    boardHeight = 7     #
    timerSpeed  = 1     # the timer updates ever 1 second
    counter     = 10    # the number the counter will count down from

    score_white = 0     # Scores variables for each player
    score_black = 0

    turn = 2            # black piece starts (1: white, 2: black)
    boardArray = []     # array to store the state of the game

    def __init__(self, parent):
        super().__init__(parent)
        print("===== BLACK goes first =====")
        self.opponentGroup = []     # array to store locations of the opponent's
        self.initBoard()

    def initBoard(self):
        '''initiates board'''
        self.timer = QBasicTimer()  # create a timer for the game
        self.isStarted = False      # game is not currently started
        self.start()                # start the game which will start the timer

        self.boardArray =[]        # 2d int/Piece array to store the state of the game
        # Initially the board will be empty (no pieces)
        for x in range(0, 8):       # initializing the 7 rows (board is 7x7)
            self.boardArray.append([])
            for y in range(0, 8):   # initializing the 7 columns (board is 7x7)
                self.boardArray[x].append(Piece.NoPiece)
        self.printBoardArray()

    def printBoardArray(self):
        '''prints the boardArray in an attractive way'''
        print("boardArray:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.boardArray]))

    def mousePosToColRow(self, x, y):
        '''convert the mouse click event to a row and column
        to find the position of the piece '''
        row = 0
        col = 0
        # get the row
        if y >= 70 and y < 140:
            row = 0
        elif y >= 140 and y < 210:
            row = 1
        elif y >= 210 and y < 280:
            row = 2
        elif y >= 280 and y < 350:
            row = 3
        elif y >= 350 and y < 420:
            row = 4
        elif y >= 420 and y < 490:
            row = 5
        elif y >= 490 and y < 560:
            row = 6
        elif y >= 560 and y <= 665:
            row = 7
        # get the column
        if x >= 70 and x < 140:
            col = 0
        elif x >= 140 and x < 210:
            col = 1
        elif x >= 210 and x < 280:
            col = 2
        elif x >= 280 and x < 350:
            col = 3
        elif x >= 350 and x < 420:
            col = 4
        elif x >= 420 and x < 490:
            col = 5
        elif x >= 490 and x < 560:
            col = 6
        elif x >= 560 and x <= 665:
            col = 7

        return row, col

    def squareWidth(self):
        '''returns the width of one square in the board'''
        return self.contentsRect().width() / self.boardWidth

    def squareHeight(self):
        '''returns the height of one square of the board'''
        return self.contentsRect().height() / self.boardHeight

    def start(self):
        '''starts game'''
        self.isStarted = True                       # set the boolean which determines if the game has started to TRUE
        self.resetGame()                            # reset the game
        self.timer.start(self.timerSpeed, self)     # start the timer with the correct speed
        print("start () - timer is started")

    def timerEvent(self, event):
        '''this event is automatically called when the timer is updated. based on the timerSpeed variable '''
        # TODO adapter this code to handle your timers
        if event.timerId() == self.timer.timerId():  # if the timer that has 'ticked' is the one in this class
            if Board.counter == 0:
                print("Game over")
            self.counter -= 1
            #print('timerEvent()', self.counter)
            self.updateTimerSignal.emit(self.counter)
        else:
            super(Board, self).timerEvent(event)      # if we do not handle an event we should pass it to the super
                                                        # class for handelingother wise pass it to the super class for handling

    def paintEvent(self, event):
        '''paints the board and the pieces of the game'''
        painter = QPainter(self)
        self.drawBoardSquares(painter)
        self.drawPieces(painter)

    def mousePressEvent(self, event):
        '''this event is automatically called when the mouse is pressed'''
        clickLoc = "click location ["+str(event.x())+","+str(event.y())+"]"     # the location where a mouse click was registered
        print("mousePressEvent() - "+clickLoc)
        self.tryMove(event.x(), event.y())          # sends the location of the click to try to place the Piece on the board

        self.clickLocationSignal.emit(clickLoc)     # emits signal to ScoreBoard

    def resetGame(self):
        # reset scores
        self.score_white = 0
        self.score_black = 0
        # black piece starts
        self.turn = GameLogic.getTurn(GameLogic, 2)
        '''clears pieces from the board'''
        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                self.boardArray[row][col] = Piece.NoPiece

    def tryMove(self, newX, newY):
        '''tries to move a piece'''
        # Get the position of the click to place the piece on the board
        row, col = self.mousePosToColRow(newX, newY)

        # list of liberties' positions (row, col) of the piece just placed on the board
        # (top, bottom, left, right)
        libertiesPos = GameLogic.get_liberties_positions(self, row, col)
        # list of the pieces placed on the liberties (0: no piece, 1: white, 2: black)
        libertiesPieces = GameLogic.get_liberties_pieces(self, self.boardArray, libertiesPos)

        # Check if is possible to place a Piece on the board (true: it's possible, false otherwise)
        placePiece = GameLogic.place_piece_on_board(GameLogic, libertiesPieces, self.turn)

        # piece can be placed/moved
        if placePiece:
            '''Check who turn it is and store the white or black piece in the array
            Only if the space is available (Piece.NoPiece)
            Give the turn for the opponent piece.'''
            if self.turn == 1 and self.boardArray[row][col] == 0:
                self.boardArray[row][col] = Piece.White
                self.turn = GameLogic.getTurn(GameLogic, 2)
            elif self.turn == 2 and self.boardArray[row][col] == 0:
                self.boardArray[row][col] = Piece.Black
                self.turn = GameLogic.getTurn(GameLogic, 1)

            # print the board array to vizualize the placed piece (state of the board)
            self.printBoardArray()

            '''liberties of the placed piece will be checked in each click in order to
            check if it will gain the opponent's territories '''
            # get a list of the group of opponent's positions (2D array to store multiple separate groups)
            self.opponentGroup = GameLogic.get_opponent_group(GameLogic, libertiesPos, row, col, self.boardArray)
            self.check_opponent_is_surrounded()     # check if opponent is surrounded without free liberties

    def check_opponent_is_surrounded(self):
        ''' Checks if opponent is surrounded without free liberties
        Each row in the 2D array self.opponentGroup corresponds to a group found at
        the top, bottom, left and right of the placed piece'''
        isSurrounded = False
        for i in range(0, 4):
            if not self.opponentGroup[i][0]:    # if no group was found, do nothing
                continue
            else:
                # check if the group is surrounded by its opponent
                isSurrounded = GameLogic.isSurrounded(GameLogic, self.opponentGroup[i], self.boardArray)
                ''' if the opponent group is surrounded, each piece in this group will be
                 set to Piece.NoPiece (empty) and points will be added for each piece. '''
                if isSurrounded:
                    for j in range(0, len(self.opponentGroup[i])):
                        for piece in self.opponentGroup[i][j]:
                            self.boardArray[piece[0]][piece[1]] = Piece.NoPiece
                            if self.turn == 1:
                                self.score_black += 1
                            elif self.turn == 2:
                                self.score_white += 1
                # Debuging prints
                #print("White score: ", self.score_white)
                #print("Black score: ", self.score_black)

    def drawBoardSquares(self, painter):
        '''draw all the squares on the board'''
        # Default brush is a black solid line, line weight 2
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        for row in range(0, Board.boardHeight):
            for col in range(0, Board.boardWidth):
                painter.save()
                colTransformation = self.squareWidth() * col   # transformation in the column direction
                rowTransformation = self.squareHeight() * row  # transformation in the row direction
                # Draw the squares on the board
                # first 2 params: x, y values on the axis
                # (the 105 is offset, so board won't be sticky to the edges of the wooden background image)
                # last 2 params:  fixed size 70x70 of each square
                painter.drawRect(105 + (70 * row), 105 + (70 * col), 70, 70)
                painter.translate(colTransformation, rowTransformation)
                painter.restore()
                # colour of the brush (black) so that a checkered board is drawn
                painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))

    def drawPieces(self, painter):
        '''draw the pieces on the board'''
        colour = Qt.transparent  # empty square could be modeled with transparent pieces
        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                painter.save()
                painter.translate(70 * col, 70 * row)   # each square is 70x70
                # set the painter brush to the correct colour (white or black for pieces, transparent for none)
                if self.boardArray[row][col] == 1:
                    colour = Qt.white
                elif self.boardArray[row][col] == 2:
                    colour = Qt.black
                else:
                    colour = Qt.transparent

                painter.setPen(QPen(colour, 1, Qt.SolidLine))         # set the pen as a black solid line, line weight 1
                painter.setBrush(QBrush(colour, Qt.SolidPattern))     # set the brush to fill up the circle with the correct colour

                radius = (self.squareWidth() - 15) / 2                # calculate the radius of the circle
                center = QPoint(80 + radius, 80 + radius)             # calculate the centre of the circle
                painter.drawEllipse(center, radius, radius)

                painter.restore()
                self.update()