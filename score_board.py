from PyQt5.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QLabel, \
    QGroupBox  # TODO import additional Widget classes as desired
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import time
from board import Board

from PyQt5.uic.properties import QtWidgets, QtGui


class ScoreBoard(QDockWidget):
    '''# base the score_board on a QDockWidget'''



    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        '''initiates ScoreBoard UI'''
        self.resize(100, 200)
        self.center()
        self.setWindowTitle('ScoreBoard')

        #create a widget to hold other widgets
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()

        self.mainWidget.setLayout(self.mainLayout)
        players = QVBoxLayout()
        self.add_players(players)

        self.mainLayout.addLayout(players)

        self.setWidget(self.mainWidget)

        self.show()

        self.Board = Board

    def add_players(self, layout):

        #create two labels which will be updated by signals
        self.group_box_p1 = QGroupBox("Player 1")
        self.group_box_p1.setObjectName("ColoredGroupBox")
        self.label_clickLocation = QLabel("Click Location: ")
        self.label_timeRemaining_P1 = QLabel("Time remaining: ")
        self.v_box1 = QVBoxLayout()
        self.v_box1.addWidget(self.label_clickLocation)
        self.group_box_p1.setLayout(self.v_box1)

        self.group_box_p2 = QGroupBox("Player 2")
        self.label_clickLocation = QLabel("Click Location: ")
        self.group_box_p2.setObjectName("ColoredGroupBox")
        # self.label_timeRemaining_P2 = QLabel("Time remaining: ")
        self.v_box2 = QVBoxLayout()
        self.v_box2.addWidget(self.label_clickLocation)

        resetButton = QPushButton('Reset')
        resetButton.clicked.connect(self.reset)
        self.v_box2.addWidget(resetButton)


        self.group_box_p2.setLayout(self.v_box2)

        self.setStyleSheet('QGroupBox#ColoredGroupBox {font-size: 20px; '   # font size
                                'font-weight:bold;'   # font wight 
                                'color: rgb(77, 77, 77);'   # color
                                'font-family: Arial, Helvetica, sans-serif;'     # font
                                'background-color: white;}')   # background color

        layout.addWidget(self.group_box_p1)
        layout.addWidget(self.group_box_p2)

    def reset(self):
        print("Button reset clicked")
        Board.resetGame(Board)

    def center(self):
        '''centers the window on the screen, you do not need to implement this method'''

    def make_connection(self, board):
        '''this handles a signal sent from the board class'''
        # when the clickLocationSignal is emitted in board the setClickLocation slot receives it
        board.clickLocationSignal.connect(self.setClickLocation)
        # when the updateTimerSignal is emitted in the board the setTimeRemaining slot receives it
         #  board.updateTimerSignal.connect(self.setTimeRemaining)

    @pyqtSlot(str) # checks to make sure that the following slot is receiving an argument of the type 'int'
    def setClickLocation(self, clickLoc):
        '''updates the label to show the click location'''
        self.label_clickLocation.setText("Click Location:" + clickLoc)
        print('slot ' + clickLoc)

    ''' 
    @pyqtSlot(int)
    
    def setTimeRemaining(self, t):
     updates the time remaining label to show the time remaining
        while t:
            mins, secs = divmod(t, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            print(timeformat, end='\r')
            t -= 1
        update = "Time Remaining:" + str(t)
        self.label_timeRemaining_P1.setText(update)
    '''

        # self.redraw()


