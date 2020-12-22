from appJar import gui

from Config import Config
from Constant import Constant

const = Constant()


class ConfigGUI:
    def __init__(self):
        self.config = None
        self.algorithm = None

        self.app = gui("Configuration of GhostBuster")

        self.app.setBg("gray")
        self.app.setResizable(False)
        self.app.setFont(size=10, family="Verdana", underline=False, slant="roman")
        self.app.setInPadding([10, 0])
        self.app.addLabel("l", "")

        self.app.setPadding([20, 0])
        self.app.addLabelEntry("Dimension: ")
        self.app.setEntry("Dimension: ", "5")

        self.app.setPadding([20, 10])
        self.app.addLabelEntry("Neighbour Probability: ")
        self.app.setEntry("Neighbour Probability: ", "0.24")

        self.app.setPadding([20, 2])
        self.app.addRadioButton("algorithm", const.HMM)
        self.app.addRadioButton("algorithm", const.PF)

        self.app.setPadding([20, 5])
        self.app.addButton("Ok", self.okPressed)
        self.app.setButtonBg("Ok", "green")
        self.app.setButtonFg("Ok", "white")
        self.app.go()

    def okPressed(self):
        try:
            dim = int(self.app.getEntry("Dimension: "))
            neighbourProb = float(self.app.getEntry("Neighbour Probability: "))
            self.config = Config(dim, neighbourProb)
            self.algorithm = self.app.getRadioButton("algorithm")
            self.app.stop()
        except:
            self.app.warningBox("Wrong input", "Please correctly.")
