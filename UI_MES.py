__author__ = 'reaver'

import sys
import xmlrpclib
import datetime
import time
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import *
from PyQt4.QtCore import QObject, pyqtSignal


server = xmlrpclib.ServerProxy('http://127.0.0.1:8000', use_datetime=True) #server = xmlrpclib.ServerProxy('http://192.168.1.50:8000', use_datetime=True)
today = datetime.datetime.today()
timeofday = time.clock()

form_class = uic.loadUiType("mes_interface.ui")[0]
dialog_class = uic.loadUiType("conn_error_msg.ui")[0]
support_class = uic.loadUiType("support_msg.ui")[0]
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
            time.sleep(5)
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
        try:
            server.add_order(order)
        except:
            errorWin.show()

        self.redSpinBox.setValue(0)
        self.blueSpinBox.setValue(0)
        self.yellowSpinBox.setValue(0)
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


class supportWindowClass(QtGui.QMainWindow, support_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.ok_btn.clicked.connect(self.ok_btn_clicked)

    def ok_btn_clicked(self):
        supportWin.close()
supportWin = supportWindowClass(None)


class MyWindowClass(QtGui.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        #super(UpdateThread, self).__init__()
        self.setupUi(self)
        self.exit_button.clicked.connect(self.exit_button_clicked)  # Bind the event handlers
        self.generate_order.clicked.connect(self.generate_order_clicked)  # to the buttons
        self.support_btn.clicked.connect(self.support_btn_clicked)

        self.cell1_label.setStyleSheet('background-color: red;')
        self.cell2_label.setStyleSheet('background-color: red;')
        self.cell3_label.setStyleSheet('background-color: red;')
        self.mobile1_label.setStyleSheet('background-color: red;')
        self.mobile2_label.setStyleSheet('background-color: red;')
        self.mobile3_label.setStyleSheet('background-color: red;')
        self.dispencer_label.setStyleSheet('background-color: red;')
        self.conn_label.setStyleSheet('background-color: red;')

        self.update_thread = UpdateThread(self)
        self.update_thread.start()

    def exit_button_clicked(self):
        mainWin.close()

    def generate_order_clicked(self):
        orderWin.show()
        # generate order

    def support_btn_clicked(self):
        supportWin.show()

    def update_status(self):
        try:
            status = server.get_status()
            self.conn_label.setStyleSheet('background-color: green;')

            # status log from server
            log_text = server.get_log()
            self.status_log_box.append(log_text)

            # OEE from server
            oee = server.get_OEE_data()
            uptime = oee['uptime']
            orders_waiting = oee['orders_waiting']
            orders_processed = oee['orders_processed']
            self.oee_log_box.setText("Uptime: " + "\n" + uptime + "\n\n" +
                                    "Orders Waiting: " + str(orders_waiting) + "\n\n" +
                                    "Orders Processed: " + str(orders_processed) + "\n\n")

            # light control
            if status['Cell1']['alive']:
                if status['Cell1']['order'] != 0:
                    self.cell1_label.setStyleSheet('background-color: green;')
                else:
                    self.cell1_label.setStyleSheet('background-color: yellow;')
            else:
                self.cell1_label.setStyleSheet('background-color: red;')

            if status['Cell2']['alive']:
                if status['Cell2']['order'] != 0:
                    self.cell2_label.setStyleSheet('background-color: green;')
                else:
                    self.cell2_label.setStyleSheet('background-color: yellow;')
            else:
                self.cell2_label.setStyleSheet('background-color: red;')

            if status['Cell3']['alive']:
                if status['Cell3']['order'] != 0:
                    self.cell3_label.setStyleSheet('background-color: green;')
                else:
                    self.cell3_label.setStyleSheet('background-color: yellow;')
            else:
                self.cell3_label.setStyleSheet('background-color: red;')

            if status['Mobile1']['alive']:
                if status['Mobile1']['order'] != 0:
                    self.mobile1_label.setStyleSheet('background-color: green;')
                else:
                    self.mobile1_label.setStyleSheet('background-color: yellow;')
            else:
                self.mobile1_label.setStyleSheet('background-color: red;')

            if status['Mobile2']['alive']:
                if status['Mobile2']['order'] != 0:
                    self.mobile2_label.setStyleSheet('background-color: green;')
                else:
                    self.mobile2_label.setStyleSheet('background-color: yellow;')
            else:
                self.mobile2_label.setStyleSheet('background-color: red;')

            if status['Mobile3']['alive']:
                if status['Mobile3']['order'] != 0:
                    self.mobile3_label.setStyleSheet('background-color: green;')
                else:
                    self.mobile3_label.setStyleSheet('background-color: yellow;')
            else:
                self.mobile3_label.setStyleSheet('background-color: red;')

            print 'Status Updated'

            if status['Dispenser']:
                self.dispencer_label.setStyleSheet('background-color: green;')
            else:
                self.dispencer_label.setStyleSheet('background-color: red;')
        except:
            self.conn_label.setStyleSheet('background-color: red;')
mainWin = MyWindowClass(None)


def main():
    mainWin.show()
    app.exec_()

if __name__ == "__main__":
    main()