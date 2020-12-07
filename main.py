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

        # UI Signals
        self.osc1Type.addItems(list(signals.oscillators.keys()))
        self.osc2Type.addItems(list(signals.oscillators.keys()))
        
        self.mod1Mode.addItems(list(signals.modulationModes.keys()))
        self.mod1Type.addItems(list(signals.modulators.keys()))
        self.mod2Mode.addItems(list(signals.modulationModes.keys()))
        self.mod2Type.addItems(list(signals.modulators.keys()))

        self.osc1Enable.stateChanged.connect(self.updateModules)
        self.osc2Enable.stateChanged.connect(self.updateModules)
        
        self.osc1Type.currentIndexChanged.connect(self.updateModules)
        self.osc2Type.currentIndexChanged.connect(self.updateModules)

        controls = [self.osc1Gain, self.osc1Freq, self.osc2Gain, self.osc2Freq,
                    self.mod1Gain, self.mod1Freq, self.mod2Gain, self.mod2Freq]
        for c in controls:
            c.valueChanged.connect(self.updateValues)

        self.osc1 = signals.Oscillator(None, 0, 0, False)
        self.osc2 = signals.Oscillator(None, 0, 0, False)
        self.updateModules()




    def updateValues(self):
        self.osc1GainLabel.setText('Gain: ' + str(self.osc1Gain.value()/100*0.5))
        self.osc2GainLabel.setText('Gain: ' + str(self.osc2Gain.value()/100*0.5))
        self.osc1FreqLabel.setText('Frequency: ' + str(self.osc1Freq.value() / 200 * 4000) + ' Hz')
        self.osc2FreqLabel.setText('Frequency: ' + str(self.osc2Freq.value() / 200 * 4000) + ' Hz')
        self.mod1GainLabel.setText('Gain: ' + str(self.mod1Gain.value()/200))
        self.mod2GainLabel.setText('Gain: ' + str(self.mod2Gain.value()/200))
        self.mod1FreqLabel.setText('Frequency: ' + str(self.mod1Freq.value()/8) + 'Hz')
        self.mod2FreqLabel.setText('Frequency:' + str(self.mod2Freq.value()/8) + 'Hz')
        self.updateModules()

    def updateModules(self):
        self.osc1.function = signals.oscillators[self.osc1Type.currentText()]
        self.osc1.gain = self.osc1Gain.value() / 200
        self.osc1.frequency = self.osc1Freq.value() / 200 * 4000
        self.osc1.enabled = self.osc1Enable.isChecked()

        self.osc2.function = signals.oscillators[self.osc2Type.currentText()]
        self.osc2.gain = self.osc2Gain.value() / 200
        self.osc2.frequency = self.osc2Freq.value() / 200 * 4000
        self.osc2.enabled = self.osc2Enable.isChecked()

    def getAudioFunction(self,n):
        m1Gain = self.mod1Gain.value()/200
        m2Gain = self.mod2Gain.value()/200 # 0 - 0.1
        m1Freq = self.mod1Freq.value() / 8
        m2Freq = self.mod2Freq.value() / 8
       
        # Modulator 1
        m1 = lambda n: self.osc1.value(n) + self.osc2.value(n) 
        if self.mod1Enable.isChecked():
            m1 = lambda n: signals.modulationModes[self.mod1Mode.currentText()](self.getOscillator, signals.modulators[self.mod1Type.currentText()], m1Gain, m1Freq, n)
        
        # Modulator 2
        m2 = m1
        if self.mod2Enable.isChecked():
            m2 = lambda n : signals.modulationModes[self.mod2Mode.currentText()](m1, signals.modulators[self.mod2Type.currentText()], m2Gain, m2Freq, n)
        
        # Low pass filter
        f1 = m2
        if self.lowPassFilterEnable.isChecked():
            f1 = lambda n: signals.lowPassFilter(m2, self.lowPassFilterGain.value()/200, self.lowPassFilterFreq.value()/200, n)
        
        # High pass filter
        f2 = f1
        if self.highPassFilterEnable.isChecked():
            f2 = lambda n: signals.highPassFilter(f1, self.highPassFilterGain.value()/200, self.highPassFilterFreq.value()/200, n)

        y = f2(n)
        if y < -1:
            return -1
        if y > 1:
            return 1
        return y


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    audio.start()
    audio.audioFunction = lambda n: window.getAudioFunction(n)
    sys.exit(app.exec_())
    audio.stop()
    audio.terminate()
