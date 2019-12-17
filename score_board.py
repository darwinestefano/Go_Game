from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import *
import time

from board import Board
from game_logic import GameLogic


class ScoreBoard(QDockWidget):
    turn_pass = 1

    '''# base the score_board on a QDockWidget'''
    def __init__(self):
        super().__init__()

        self.board = Board
        self.gamelogic = GameLogic()
        self.initUI()

    '''initiates ScoreBoard UI'''
    def initUI(self):
        self.resize(100, 200)
        self.center()
        self.setWindowTitle('ScoreBoard')

        # create a widget to hold layout
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()

        # add layout player into it
        self.mainWidget.setLayout(self.mainLayout)
        players = QVBoxLayout()
        self.add_players(players)
        self.mainLayout.addLayout(players)
        self.setWidget(self.mainWidget)

        # display layout
        self.show()

    def make_connection(self, board):
        '''this handles a signal sent from the board class'''
        # when the clickLocationSignal is emitted in board the setClickLocation slot receives it
        board.clickLocationSignal.connect(self.setClickLocation)
        # when the updateScoreSignalBlack is emitted in board the emits the  current score  and the slot receives it
        board.updateScoreSignalBlack.connect(self.setCurrentScoreBlack)
        # when the updateScoreSignalWhite is emitted in board the emits the  current score  and the slot receives it
        board.updateScoreSignalWhite.connect(self.setCurrentScoreWhite)
        # when the updateSetPlayerTurn is emitted in board the emits the  who's turn  and the slot receives it
        board.updateSetPlayerTurn.connect(self.setPlayerTurn)
        # when the updateTimerSignal is emitted in the board the setTimeRemaining slot receives it
        # board.updateTimerSignal.connect(self.setTimeRemaining)

    @pyqtSlot(str)  # checks to make sure that the following slot is receiving an argument of the type 'int'
    def setClickLocation(self, clickLoc):
        self.label_clickLocation.setText("" + clickLoc)

    @pyqtSlot(int)  # checks to make sure that the following slot is receiving an argument of the type 'int'
    def setCurrentScoreBlack(self, scoreblack):
        scoreblack = str(scoreblack)
        '''update score for player BLACK'''
        self.label_clickScoreBlack.setText("Score: " + scoreblack)
        print('slot black score' + scoreblack)

    @pyqtSlot(int)  # checks to make sure that the following slot is receiving an argument of the type 'int'
    def setCurrentScoreWhite(self, scorewhite):
        scorewhite = str(scorewhite)
        '''update score for player WHITE'''
        self.label_clickScoreWhite.setText("Score: " + scorewhite)
        self.label_clickScoreWhite.setObjectName("ColoredGroupBox")
        print('slot white score ' + scorewhite)

    @pyqtSlot(int)  # checks to make sure that the following slot is receiving an argument of the type 'int'
    def setPlayerTurn(self, turn):
        '''this handles wwho's the next to play'''
        self.turn_pass = turn
        if turn == 1: # if turn equal 1 is time for white to play
            self.label_whiteTurn.show()
            self.label_whiteTurn.setText("WHITE IS YOUR TURN!")
            self.label_blackTurn.hide()
        else: # else is time for black to play
            self.label_blackTurn.show()
            self.label_blackTurn.setText("BLACK IS YOUR TURN!")
            self.label_whiteTurn.hide()

    def change_turn(self):
        print("change turn : ", self.turn_pass)
        if self.turn_pass == 1:
            GameLogic.getTurn(GameLogic, 2)
            print("work in 1")
        else:
            GameLogic.getTurn(GameLogic, 1)
            print("work in 2")


    def add_players(self, layout):
        '''this handles the players status, score and turn'''
        # set default values for variable
        self.label_clickLocation = QLabel("Click to start")
        self.label_clickLocation.setObjectName("ColoredLabelLoc")
        self.label_timeRemaining_P1 = QLabel("")

        # create group box for player black
        self.group_box_p1 = QGroupBox("\t\tBlack")
        self.group_box_p1.setObjectName("ColoredGroupBox")

        # set default for turn and score
        self.v_box1 = QVBoxLayout()
        self.label_blackTurn = QLabel("BLACK STARTS THE GAME!")
        self.label_blackTurn.setObjectName("ColoredTurn")
        self.label_clickScoreBlack = QLabel("Score: 0")
        self.label_clickScoreBlack.setObjectName("ScoreEdit")

        # add  widgets to layout
        self.v_box1.addWidget(self.label_clickScoreBlack)
        self.v_box1.addWidget(self.label_blackTurn)
        self.group_box_p1.setLayout(self.v_box1)

        # create group box for player black
        self.group_box_p2 = QGroupBox("\t\t White")
        self.group_box_p2.setObjectName("ColoredGroupBox")
        self.v_box2 = QVBoxLayout()

        # set default for turn and score
        self.label_whiteTurn = QLabel("")
        self.label_whiteTurn.setObjectName("ColoredTurn")
        self.label_clickScoreWhite = QLabel("Score: 0")
        self.label_clickScoreWhite.setObjectName("ScoreEdit")

        # add  widgets to layout
        self.v_box2.addWidget(self.label_clickScoreWhite)
        self.v_box2.addWidget(self.label_timeRemaining_P1)
        self.v_box2.addWidget(self.label_whiteTurn)
        self.group_box_p2.setLayout(self.v_box2)

        # create btn for pass
        self.button_pass = QPushButton('PASS', self)
        self.button_pass.setObjectName("PassObj")
        self.button_pass.setToolTip('Pass your turn')
        print("self turn :", self.turn_pass)
        self.button_pass.clicked.connect(self.change_turn)

        # create btn for reset
        self.button_reset = QPushButton('RESET', self)
        self.button_reset.setObjectName("PassObj")
        self.button_reset.clicked.connect(self.reset)
        self.button_reset.setToolTip('Pass your turn')


        # create btn for how to play
        self.btn_howto = QPushButton("HOW TO PLAY", self)
        self.btn_howto.setObjectName("PassObj")
        self.btn_howto.setToolTip('How to play')
        self.btn_howto.setCheckable(True)
        self.btn_howto.clicked.connect(self.btnstate)
        self.btn_howto.resize(self.btn_howto.minimumSizeHint())
        self.btn_howto.move(0, 100)

        # set stylesheet using CSS
        self.setStyleSheet('QLabel#ScoreEdit{'
                           'font-size: 20px; '  # font size
                           'font-weight:bold;'  # font wight 
                           'color: white;'  # color
                           'font-family: Arial, Helvetica, sans-serif;'  # font
                           '}'
                           'QLabel#ColoredTurn{'
                           'font-size: 20px; '  # font size
                           'font-weight:bold;'  # font wight 
                           'color: white;'  # color
                           'font-family: Arial, Helvetica, sans-serif;'  # font
                           '}'
                           'QPushButton#PassObj{'
                           'font-size: 20px; '  # font size
                           'font-weight:bold;'  # font wight 
                           'color: #808080;'
                           'border: 2px solid #a6a6a6;'
                           'padding: 4px;'
                           'border-radius: 10px;'  # color
                           'font-family: Arial, Helvetica, sans-serif;'  # font
                           '}'
                           'QGroupBox#ColoredGroupBox{'
                           'font-size: 20px;'  # font size
                           'font-weight: bold;'  # font wight 
                           'color: black;'  # color
                           'font-family: Arial, Helvetica, sans-serif;'  # font
                           'background-color: #b3b3b3;'
                           'border: 3px solid #a6a6a6;'
                           'border-radius: 10px;'
                           'text-transform: uppercase;'
                           '}'
                           'QLabel#ColoredLabelLoc{'
                           'font-size: 18px;'  # font size
                           'font-weight: bold;'  # font wight 
                           'color: black;'  # color
                           'font-family: Arial, Helvetica, sans-serif;'  # font
                           'background-color: white;'
                           'border: 1px solid #a6a6a6;'
                           'border-radius: 10px;'
                           'padding:1px;'
                           'text-align: justify;'
                           '}'
                           )  # background color

        # add all features to scoreboard layout
        layout.addWidget(self.group_box_p1)
        layout.addWidget(self.group_box_p2)
        layout.addWidget(self.label_clickLocation)
        layout.addWidget(self.button_pass)
        layout.addWidget(self.button_reset)
        layout.addWidget(self.btn_howto)

    def reset(self):
        Board.resetGame(Board)
        self.label_clickLocation.setText("Game reset, star over!")

    def btnstate(self):
        '''this method checks state of btn and connect to show how to play'''
        if self.btn_howto.isChecked():
            self.btn_howto.clicked.connect(self.show_popup)

    def center(self):
        '''centers the window on the screen, you do not need to implement this method'''

    @pyqtSlot(int)
    def setTimeRemaining(self, t):
        seconds = t
        for i in range(seconds):
            self.label_timeRemaining_P1.setText(str(seconds - i) + " seconds remain")
            print(str(seconds - i) + " seconds remain")
            time.sleep(1)

    def show_popup(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(""
                       "1. At the beginning of the game, players should consider placing the stones near handicap markers, usually located in the corners of the board. This way, the player is at an advantage of gaining corner positions that help gain territory and are easy to defend."
                       "\n\n2. Players should only play stones at the edge of the board as they are as easy to capture. Typically, the corner only needs two stones captured while side requires three stones. The open area, however, requires players to seize for stones."
                       "\n\n3. If looking to occupy an open area, consider building off a stable structure. You get to protect your stones and create a broader base for subsequent moves."
                       "\n\n4. Avoid placing your stones close to your opponent’s. You don’t want to allow them to gain more considerable influence when you are chasing stones."
                       "\n\n5. Avoid placing your stones on your opponent’s territory. You are only providing them with free stones for capture. This strategy works when you are confident of capturing his stones.w")
        msgBox.setWindowTitle("How to play!")
        msgBox.setStandardButtons(QMessageBox.Close)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Close:
            msgBox.close()


# self.redraw()
