__author__ = 'reaver'

import sys
import xmlrpclib
import datetime
import time
from PyQt4 import QtCore, QtGui, uic

server = xmlrpclib.ServerProxy('http://10.112.254.161:8000', use_datetime=True)
today = datetime.datetime.today()
timeofday = time.clock()

form_class = uic.loadUiType("mes_interface.ui")[0]
dialog_class = uic.loadUiType("conn_error_msg.ui")[0]
setorder_class = uic.loadUiType("set_order.ui")[0]
app = QtGui.QApplication(sys.argv)


class orderWindowClass(QtGui.QMainWindow, setorder_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.ok_btn.clicked.connect(self.ok_btn_clicked)
        self.cncl_btn.clicked.connect(self.cncl_btn_clicked)

    def ok_btn_clicked(self):
        order = [
            dict(color='COLOR_RED', size=6, count=self.redSpinBox.value),
            dict(color='COLOR_BLUE', size=6, count=self.blueSpinBox.value),
            dict(color='COLOR_YELLOW', size=6, count=self.yellowSpinBox.value)]
        server.add_order(order)
        orderWin.close()

    def cncl_btn_clicked(self):
        orderWin.close()
orderWin = orderWindowClass(None)


class errorWindowClass(QtGui.QMainWindow, dialog_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.ok_btn.clicked.connect(self.ok_btn_clicked)

    def ok_btn_clicked(self):
        errorWin.close()
errorWin = errorWindowClass(None)


class MyWindowClass(QtGui.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.exit_button.clicked.connect(self.exit_button_clicked)  # Bind the event handlers
        self.generate_order.clicked.connect(self.generate_order_clicked)  # to the buttons
        self.start_btn.clicked.connect(self.start_btn_clicked)

    def exit_button_clicked(self):
        mainWin.close()

    def generate_order_clicked(self):
        orderWin.show()
        # generate order

    def start_btn_clicked(self):
        server = xmlrpclib.ServerProxy('http://10.112.254.161:8000', use_datetime=True)
        #errorWin.show()
mainWin = MyWindowClass(None)


def startWin():
    mainWin.show()
    app.exec_()


def main():
    startWin()

if __name__ == "__main__":
    main()