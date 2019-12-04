from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QPoint
from PyQt5.QtGui import *
from piece import Piece
from game_logic import GameLogic

class Board(QFrame):  # base the board on a QFrame widget
    updateTimerSignal = pyqtSignal(int) # signal sent when timer is updated
    clickLocationSignal = pyqtSignal(str) # signal sent when there is a new click location

    # TODO set the board width and height to be square
    boardWidth  = 7     # board is 0 squares wide # TODO this needs updating
    boardHeight = 7     #
    timerSpeed  = 1     # the timer updates ever 1 second
    counter     = 10    # the number the counter will count down from


    def __init__(self, parent):
        super().__init__(parent)
        print("GAME LOGIC: ", GameLogic.turn)
        self.initBoard()

    def initBoard(self):
        '''initiates board'''
        self.timer = QBasicTimer()  # create a timer for the game
        self.isStarted = False      # game is not currently started
        self.start()                # start the game which will start the timer


        #r, c = 8, 8
        #self.boardArray = [[0 for x in range(r)] for y in range(c)]
        self.boardArray =[]        # TODO - create a 2d int/Piece array to store the state of the game
        for x in range(0, 8):
            self.boardArray.append([])
            for y in range(0, 8):
                self.boardArray[x].append(Piece.NoPiece)

        self.printBoardArray()    # TODO - uncomment this method after create the array above

    def printBoardArray(self):
        '''prints the boardArray in an attractive way'''
        print("boardArray:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.boardArray]))

    def mousePosToColRow(self, event):
        '''convert the mouse click event to a row and column'''
        row = 0
        col = 0
        # get the row
        if event.y() >= 70 and event.y() < 140:
            row = 0
            print("ROW 1")
        elif event.y() >= 140 and event.y() < 210:
            row = 1
            print("ROW 2")
        elif event.y() >= 210 and event.y() < 280:
            row = 2
            print("ROW 3")
        elif event.y() >= 280 and event.y() < 350:
            row = 3
            print("ROW 4")
        elif event.y() >= 350 and event.y() < 420:
            row = 4
            print("ROW 5")
        elif event.y() >= 420 and event.y() < 490:
            row = 5
            print("ROW 6")
        elif event.y() >= 490 and event.y() < 560:
            row = 6
            print("ROW 7")
        elif event.y() >= 560 and event.y() <= 665:
            row = 7
            print("ROW 8")
        # get the column
        if event.x() >= 70 and event.x() < 140:
            col = 0
            print("COLUMN 1")
        elif event.x() >= 140 and event.x() < 210:
            col = 1
            print("COLUMN 2")
        elif event.x() >= 210 and event.x() < 280:
            col = 2
            print("COLUMN 3")
        elif event.x() >= 280 and event.x() < 350:
            col = 3
            print("COLUMN 4")
        elif event.x() >= 350 and event.x() < 420:
            col = 4
            print("COLUMN 5")
        elif event.x() >= 420 and event.x() < 490:
            col = 5
            print("COLUMN 6")
        elif event.x() >= 490 and event.x() < 560:
            col = 6
            print("COLUMN 7")
        elif event.x() >= 560 and event.x() <= 665:
            col = 7
            print("COLUMN 8")

        # Check who turn it is and store the white or black piece in the array
        if GameLogic.turn == 1 and self.boardArray[row][col] == 0:
            self.boardArray[row][col] = Piece.White
            GameLogic.turn = 2
        elif GameLogic.turn ==2 and self.boardArray[row][col] == 0:
            self.boardArray[row][col] = Piece.Black
            GameLogic.turn = 1
        print(self.boardArray[row][col])

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
        # TODO you could call some game logic here
        self.mousePosToColRow(event)                    # adicionei
        self.clickLocationSignal.emit(clickLoc)

    def resetGame(self):
        '''clears pieces from the board'''
        # TODO write code to reset game

    def tryMove(self, newX, newY):
        '''tries to move a piece'''

    def drawBoardSquares(self, painter):
        '''draw all the square on the board'''
        # TODO set the default colour of the brush
        #painter.begin(self)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        for row in range(0, Board.boardHeight):
            for col in range (0, Board.boardWidth):
                painter.save()
                colTransformation = self.squareWidth()* col # TODO set this value equal the transformation in the column direction
                rowTransformation = self.squareHeight()* row # TODO set this value equal the transformation in the row direction
                # first value is offset (so board wont be sticky to the edges)
                painter.drawRect(105 + (70 * row), 105 + (70 * col), 70, 70)
                #painter.drawRect(30 + (self.squareWidth() * row), 30 + (self.squareHeight() * col), self.squareWidth(), self.squareHeight())
                #print("SQAUREEEEEEEEEEEEEEEEEEEEEEEE")
                #print(self.squareWidth()) #67
                #print(self.squareHeight()) #98 NAO ESQUECER DE APAGAR!!!!!!!!!!!
                painter.translate(colTransformation, rowTransformation)
                painter.restore()
                # TODO change the colour of the brush so that a checkered board is drawn
                painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))

    def drawPieces(self, painter):
        '''draw the prices on the board'''
        colour = Qt.transparent # empty square could be modeled with transparent pieces
        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                painter.save()
                painter.translate(70* col, 70* row)
                # TODO draw some the pieces as ellipses
                # TODO choose your colour and set the painter brush to the correct colour
                if self.boardArray[row][col] == 1:
                    colour = Qt.white
                elif self.boardArray[row][col] == 2:
                    colour = Qt.black
                else:
                    colour = Qt.transparent

                painter.setPen(QPen(colour, 1, Qt.SolidLine))         #inclui essa linha
                painter.setBrush(QBrush(colour, Qt.SolidPattern))     #inclui essa linha

                #radius = (self.squareWidth() - 2) / 2
                radius = (self.squareWidth() - 15) / 2
                center = QPoint(80 + radius, 80 + radius)
                painter.drawEllipse(center, radius, radius)
                painter.restore()
                self.update()