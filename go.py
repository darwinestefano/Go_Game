from PyQt5.QtWidgets import QMainWindow, QDesktopWidget
from PyQt5.QtCore import Qt
from board import Board
from score_board import ScoreBoard

class Go(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def getBoard(self):
        return self.board

    def getScoreBoard(self):
        return self.scoreBoard

    def initUI(self):
        '''initiates application UI'''
        self.board = Board(self)
        self.setCentralWidget(self.board)
        self.scoreBoard = ScoreBoard()
        self.addDockWidget(Qt.RightDockWidgetArea, self.scoreBoard)
        self.scoreBoard.make_connection(self.board)

        self.resize(800, 800)
        self.setFixedSize(700, 700)
        self.center()
        self.setWindowTitle('Go')

        self.board.setStyleSheet("background-image:  url(images/wood.jpg); margin: 60px 75px")

        self.show()

    def center(self):
        '''centers the window on the screen'''
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,(screen.height() - size.height()) / 2)
