import audio
import signals
import time
import sys
import math
from PyQt5 import QtCore, QtGui, QtWidgets, uic


class Main(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self, parent = None)
        uic.loadUi('main.ui', self)
        self.setWindowTitle('Digital Synthetizer')
        self.statusbar.showMessage('Sampling Frequency: ' + str(signals.samplingFrequency) + ' Hz')

        self.osc1Type.addItems(list(signals.oscillators.keys()))
        self.osc2Type.addItems(list(signals.oscillators.keys()))
        
        self.mod1Mode.addItems(list(signals.modulationModes.keys()))
        self.mod1Type.addItems(list(signals.modulators.keys()))
        self.mod2Mode.addItems(list(signals.modulationModes.keys()))
        self.mod2Type.addItems(list(signals.modulators.keys()))

        self.osc1Gain.valueChanged.connect(self.updateValues)
        self.osc2Gain.valueChanged.connect(self.updateValues)
        self.osc1Freq.valueChanged.connect(self.updateValues)
        self.osc2Freq.valueChanged.connect(self.updateValues)
        self.mod1Gain.valueChanged.connect(self.updateValues)
        self.mod1Freq.valueChanged.connect(self.updateValues)
        self.mod2Gain.valueChanged.connect(self.updateValues)
        self.mod2Freq.valueChanged.connect(self.updateValues)

    def updateValues(self):
        self.osc1GainLabel.setText('Gain: ' + str(self.osc1Gain.value()/100*0.5))
        self.osc2GainLabel.setText('Gain: ' + str(self.osc2Gain.value()/100*0.5))
        self.osc1FreqLabel.setText('Frequency: ' + str(self.osc1Freq.value() / 200 * 4000) + ' Hz')
        self.osc2FreqLabel.setText('Frequency: ' + str(self.osc2Freq.value() / 200 * 4000) + ' Hz')
        self.mod1GainLabel.setText('Gain: ' + str(self.mod1Gain.value()/200))
        self.mod2GainLabel.setText('Gain: ' + str(self.mod2Gain.value()/200))
        self.mod1FreqLabel.setText('Frequency: ' + str(self.mod1Freq.value()/8) + 'Hz')
        self.mod2FreqLabel.setText('Frequency:' + str(self.mod2Freq.value()/8) + 'Hz')


    def getOscillator(self,n):
        y = 0
        if self.osc1Enable.isChecked():
            y += self.osc1Gain.value()/200 * signals.oscillators[self.osc1Type.currentText()](self.osc1Freq.value() / 200 * 4000, n)
        if self.osc2Enable.isChecked():
            y += self.osc2Gain.value()/200 * signals.oscillators[self.osc2Type.currentText()](self.osc2Freq.value() / 200 * 4000, n)
        if y < -1:
            return -1
        if y > 1:
            return 1
        return y

    def getAudioFunction(self,n):
        m1Gain = self.mod1Gain.value()/200
        m2Gain = self.mod2Gain.value()/200 # 0 - 0.1
        m1Freq = self.mod1Freq.value() / 8
        m2Freq = self.mod2Freq.value() / 8
       
        m1 = self.getOscillator
        if self.mod1Enable.isChecked():
            m1 = lambda n: signals.modulationModes[self.mod1Mode.currentText()](self.getOscillator, signals.modulators[self.mod1Type.currentText()], m1Gain, m1Freq, n)
        m2 = m1
        if self.mod2Enable.isChecked():
            m2 = lambda n : signals.modulationModes[self.mod2Mode.currentText()](m1, signals.modulators[self.mod2Type.currentText()], m2Gain, m2Freq, n)
        
        # Filters
        f1 = lambda n:  signals.lowPassFilter(m2, self.lowPassFilterGain.value()/200, self.lowPassFilterFreq.value()/200, n) 
        if self.lowPassFilterEnable.isChecked():
            return f1(n)
        else:
            return m2(n)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    audio.start()
    audio.audioFunction = lambda n: window.getAudioFunction(n)
    sys.exit(app.exec_())
    audio.stop()
    audio.terminate()
