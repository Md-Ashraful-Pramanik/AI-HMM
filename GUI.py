from appJar import gui

from Board import Board
from Config import Config
from Constant import Constant
from ConfigGUI import ConfigGUI

const = Constant()


class GUI:
    def __init__(self):
        self.playAgain = False

        conf = ConfigGUI()

        if conf.config is None:
            exit(0)

        self.config = conf.config
        self.game = Config.getBoard(conf.algorithm, self.config)
        self.wantToCatch = False

        self.app = gui("GhostBuster", f'{self.config.dim * 60}' + "x" + f'{self.config.dim * 60 + 60}')
        self.app.setResizable(False)
        self.app.setFont(size=10, family="Verdana", underline=False, slant="roman")

        self.app.startFrame("BOX", row=self.config.dim + 2, column=self.config.dim)
        self.app.addLabel("status", "Advance Time", 0, 0, self.config.dim)

        for i in range(self.config.dim):
            for j in range(self.config.dim):
                self.app.addButton(GUI.getButtonID(i, j), self.addEvidence, i + 1, j)

        self.app.thread(self.updateBoardInGUI)
        self.app.addNamedButton("Time++", "time", self.timePlusPlusClicked, self.config.dim + 1, 0,
                                int(self.config.dim / 2), 0)

        if self.config.dim % 2:
            self.app.addNamedButton("", "indent", None, self.config.dim + 1, int(self.config.dim / 2))
            self.app.addNamedButton("Catch", "catch", self.catchGhost, self.config.dim + 1,
                                    int(self.config.dim / 2) + 1, int(self.config.dim / 2), 0)

            self.app.setButtonBg("indent", "black")
        else:
            self.app.addNamedButton("Catch", "catch", self.catchGhost, self.config.dim + 1,
                                    int(self.config.dim / 2), int(self.config.dim / 2), 0)

        # setting up colors
        self.app.setLabelBg("status", "yellow")
        self.app.setButtonBg("time", "skyblue")
        self.app.setButtonBg("catch", "skyblue")

        # setting up images
        # self.app.setButtonImage("indent", "images/ghost.jpg", align="center")

        self.app.stopFrame()
        self.app.go()

    def timePlusPlusClicked(self):
        if self.game.turn == const.TIME:
            self.game.advanceTime()
            self.app.thread(self.updateBoardInGUI)
            self.app.setLabel("status", "Take Evidence")

    def addEvidence(self, btn):
        selectedPosition = btn.split(",")
        selectedPosition[0] = int(selectedPosition[0])
        selectedPosition[1] = int(selectedPosition[1])

        if self.wantToCatch:
            if selectedPosition[0] == self.game.ghostPosition[0] and \
                    selectedPosition[1] == self.game.ghostPosition[1]:
                msg = "You win!!!"
            else:
                msg = "You loose. Try again."

            msg += "\nDo you want to play again?"

            if self.app.questionBox("Game Over", msg, parent=None):
                self.playAgain = True

            self.app.stop()

        elif self.game.turn == const.EVIDENCE:
            self.game.useEvidence(selectedPosition)
            self.app.thread(self.updateBoardInGUI, btn, selectedPosition)
            self.app.setLabel("status", "Advance Time")

    def catchGhost(self):
        self.wantToCatch = True
        self.app.setLabel("status", "Catch The Ghost")

    def updateBoardInGUI(self, colorButton=None, selectedPosition=None):
        for i in range(self.config.dim):
            for j in range(self.config.dim):
                buttonID = GUI.getButtonID(i, j)
                if self.game.board[i][j] < 0.01:
                    self.app.setButton(buttonID, "<.01")
                else:
                    self.app.setButton(buttonID, f'{self.game.board[i][j]:.2f}')
                self.app.setButtonBg(buttonID, GUI.getBgGrayScaleColorInRGB(self.game.board[i][j]))
                self.app.setButtonFg(buttonID, GUI.getFgGrayScaleColorInRGB(self.game.board[i][j]))

        if colorButton is not None:
            color = self.game.getColor(Board.manhattanDistancePoint(selectedPosition, self.game.ghostPosition))
            if color == const.RED:
                self.app.setButtonBg(colorButton, "red")
                self.app.setButtonFg(colorButton, "white")
            if color == const.ORANGE:
                self.app.setButtonBg(colorButton, "orange")
                self.app.setButtonFg(colorButton, "black")
            if color == const.GREEN:
                self.app.setButtonBg(colorButton, "green")
                self.app.setButtonFg(colorButton, "white")

    @staticmethod
    def getBgGrayScaleColorInRGB(val):
        val = int(val * 255)
        val = min(val + 50, 255)
        val = 255 - val
        return '#%02x%02x%02x' % (val, val, val)

    @staticmethod
    def getFgGrayScaleColorInRGB(val):
        val = int(val * 255)
        val = max(val - 50, 0)
        return '#%02x%02x%02x' % (val, val, val)

    @staticmethod
    def getButtonID(x, y):
        return str(x) + "," + str(y)


while True:
    g = GUI()
    if not g.playAgain:
        break
