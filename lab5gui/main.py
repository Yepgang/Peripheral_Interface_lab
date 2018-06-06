import random
import sys
import re

import matplotlib.pyplot as plt
import serial
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtWidgets,QtCore

from Ui_ADT7420 import Ui_MplMainWindow


class App(QtWidgets.QWidget, Ui_MplMainWindow):

    def __init__(self, parent=None):
        # initialization of the superclass
        super(App, self).__init__()
        # setup the GUI --> function generated by pyuic4
        self.setupUi(self)
        # connect the signals with the slots
        self.pushButton_showsettings.clicked.connect(self.DisplaySettings)
        self.pushButton_setResolution.clicked.connect(self.setResolution)
        self.pushButton_setthigt.clicked.connect(self.setTHigh)
        self.pushButton_settlow.clicked.connect(self.setTLow)
        self.pushButton_settcrit.clicked.connect(self.setTCrit)
        self.pushButton_setthyst.clicked.connect(self.setTHyst)
        self.pushButton_setfaultqueue.clicked.connect(self.setFaultQueue)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.read_data)
        self.serial = serial.Serial('COM1', 115200, timeout=1)
        if False == self.serial.isOpen():
            print("faild to open serial port!\n")
        else:
            self.timer.start(1000)

    def read_data(self):
        text = self.serial.read_all()
        print(text)
        self.textEdit_log.insertPlainText(text.decode())

        data = re.findall(r"T = (?P<temp>[0-9]*\.00) C", text.decode())
        for t in data:
            print(float(t))
            self.mplfigure

    def setResolution(self):
        self.serial.write('r'.encode())
        if self.radioButton_13bits.isChecked():
            self.serial.write('1'.encode())
        elif self.radioButton_16bits.isChecked():
            self.serial.write('2'.encode())
        else:
            print("error in setResolution")

    def setTHigh(self):
        self.serial.write('h'.encode())
        val = "%x" % self.spinBox_thigh.value()
        self.serial.write(val.encode())

    def setTLow(self):
        self.serial.write('l'.encode())
        val = "%x" % self.spinBox_tlow.value()
        self.serial.write(val.encode())

    def setTCrit(self):
        self.serial.write('c'.encode())
        val = "%x" % self.spinBox_tcrit.value()
        self.serial.write(val.encode())

    def setTHyst(self):
        self.serial.write('y'.encode())
        val = "%x" % self.spinBox_thyst.value()
        self.serial.write(val.encode())

    def setFaultQueue(self):
        self.serial.write('f'.encode())
        val = "%x" % self.spinBox_faultqueue.value()
        self.serial.write(val.encode())

    def DisplaySettings(self):
        self.serial.write('s'.encode())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
