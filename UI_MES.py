__author__ = 'reaver'

import sys
import xmlrpclib
import datetime
import time
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import QObject, pyqtSignal


server = xmlrpclib.ServerProxy('http://127.0.0.1:8000', use_datetime=True)
today = datetime.datetime.today()
timeofday = time.clock()

form_class = uic.loadUiType("mes_interface.ui")[0]
dialog_class = uic.loadUiType("conn_error_msg.ui")[0]
setorder_class = uic.loadUiType("set_order.ui")[0]
app = QtGui.QApplication(sys.argv)


class UpdateThread(QtCore.QThread, QObject):
    update_status = pyqtSignal()

    def __init__(self, window):
        QtCore.QThread.__init__(self)
        self.update_status.connect(window.update_status)

    def run(self):
        #QtCore.QThread.run(self)
        print 'running'
        while True:
            time.sleep(2)
            self.update_status.emit()


class orderWindowClass(QtGui.QMainWindow, setorder_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.ok_btn.clicked.connect(self.ok_btn_clicked)
        self.cncl_btn.clicked.connect(self.cncl_btn_clicked)

    def ok_btn_clicked(self):
        red = self.redSpinBox.value()
        blue = self.blueSpinBox.value()
        yellow = self.yellowSpinBox.value()
        order = [
            {'color': 'COLOR_RED', 'size': 6, 'count': red},
            {'color': 'COLOR_BLUE', 'size': 6, 'count': blue},
            {'color': 'COLOR_YELLOW', 'size': 6, 'count': yellow}]
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
        errorWin.show()
errorWin = errorWindowClass(None)


class MyWindowClass(QtGui.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        #super(UpdateThread, self).__init__()
        self.setupUi(self)
        self.exit_button.clicked.connect(self.exit_button_clicked)  # Bind the event handlers
        self.generate_order.clicked.connect(self.generate_order_clicked)  # to the buttons
        self.start_btn.clicked.connect(self.start_btn_clicked)

        self.cell1_label.setStyleSheet('background-color: red;')
        self.cell2_label.setStyleSheet('background-color: red;')
        self.cell3_label.setStyleSheet('background-color: red;')
        self.mobile1_label.setStyleSheet('background-color: red;')
        self.mobile2_label.setStyleSheet('background-color: red;')
        self.mobile3_label.setStyleSheet('background-color: red;')
        self.dispencer_label.setStyleSheet('background-color: red;')

        self.update_thread = UpdateThread(self)
        self.update_thread.start()

    def exit_button_clicked(self):
        mainWin.close()

    def generate_order_clicked(self):
        orderWin.show()
        # generate order

    def start_btn_clicked(self):
        #try:
        #server = xmlrpclib.ServerProxy('http://192.168.1.50:8000', use_datetime=True)
        #errorWin.show()
        return

    def update_status(self):
        try:
            status = server.get_status()

            if status[0] != 0:
                self.cell1_label.setStyleSheet('background-color: green;')
            else:
                self.cell1_label.setStyleSheet('background-color: red;')
            if status[1] != 0:
                self.cell2_label.setStyleSheet('background-color: green;')
            else:
                self.cell2_label.setStyleSheet('background-color: red;')
            if status[2] != 0:
                self.cell3_label.setStyleSheet('background-color: green;')
            else:
                self.cell3_label.setStyleSheet('background-color: red;')
            if status[3] != 0:
                self.mobile1_label.setStyleSheet('background-color: green;')
            else:
                self.mobile1_label.setStyleSheet('background-color: red;')
            if status[4] != 0:
                self.mobile2_label.setStyleSheet('background-color: green;')
            else:
                self.mobile2_label.setStyleSheet('background-color: red;')
            if status[5] != 0:
                self.mobile3_label.setStyleSheet('background-color: green;')
            else:
                self.mobile3_label.setStyleSheet('background-color: red;')
            print 'Status Updated'
        except:
            errorWin.show()
mainWin = MyWindowClass(None)


def main():
    mainWin.show()
    app.exec_()

if __name__ == "__main__":
    main()