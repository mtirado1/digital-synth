import audio
import signals
import time
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic

oscillators = {'Sine Wave': signals.sinewave}

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self, parent = None)
        uic.loadUi('main.ui', self)
        self.setWindowTitle('Digital Synthetizer')

        self.osc1Type.addItems(list(oscillators.keys()))
        self.osc2Type.addItems(list(oscillators.keys()))

        self.osc1Gain.valueChanged.connect(self.updateValues)
        self.osc1Freq.valueChanged.connect(self.updateValues)

    def updateValues(self):
        self.osc1GainLabel.setText('Gain: ' + str(self.osc1Gain.value()/100*0.5))
        self.osc1FreqLabel.setText('Frequency: ' + str(self.osc1Freq.value()/200*4000) + ' Hz')

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    audio.start()
    audio.audioFunction = lambda t: window.osc1Gain.value()/100 * 0.5 * signals.sinewave(window.osc1Freq.value()/200 * 4000, t) * signals.sinewave(2, t)
    sys.exit(app.exec_())
    audio.stop()
    audio.terminate()
