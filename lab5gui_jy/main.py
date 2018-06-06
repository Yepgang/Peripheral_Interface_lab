import random
import sys
import re

import matplotlib.pyplot as plt
import serial
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtWidgets, QtCore

from Ui_ADT7420 import Ui_MplMainWindow


class App(QtWidgets.QWidget, Ui_MplMainWindow):

    def __init__(self, parent=None):
        # initialization of the superclass
        super(App, self).__init__()
        # setup the GUI --> function generated by pyuic4
        self.setupUi(self)
        # connect the signals with the slots
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.read_data)
        self.serial = serial.Serial('COM6', 115200, timeout=1)
        if False == self.serial.isOpen():
            print("faild to open serial port!\n")
        else:
            self.timer.start(1000)
        self.data = list()


    def read_data(self):
        text = self.serial.read_all()
        print(text)
        #self.textEdit_log.clear()

        temp = re.findall(r" (?P<temp>[0-9]*\.00) C", text.decode())

        for t in temp:
            print(float(t))
            if len(self.data) >= 60:
                del self.data[0]
            self.data.append(float(t)/16)
        self.mplfigure.canvas.ax.clear()
        self.mplfigure.canvas.ax.plot(self.data, 'o-r',)
        self.mplfigure.canvas.draw()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
