# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(307, 175)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit_cookie = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_cookie.setMinimumSize(QtCore.QSize(200, 0))
        self.lineEdit_cookie.setObjectName("lineEdit_cookie")
        self.gridLayout.addWidget(self.lineEdit_cookie, 1, 1, 1, 1)
        self.lineEdit_api = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_api.setMinimumSize(QtCore.QSize(200, 0))
        self.lineEdit_api.setObjectName("lineEdit_api")
        self.gridLayout.addWidget(self.lineEdit_api, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_shot = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_shot.setMaximumSize(QtCore.QSize(80, 16777215))
        self.pushButton_shot.setObjectName("pushButton_shot")
        self.horizontalLayout.addWidget(self.pushButton_shot)
        self.pushButton_exit = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_exit.setMaximumSize(QtCore.QSize(80, 16777215))
        self.pushButton_exit.setObjectName("pushButton_exit")
        self.horizontalLayout.addWidget(self.pushButton_exit)
        self.verticalLayout.addWidget(self.groupBox_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "图床设置"))
        self.label.setText(_translate("MainWindow", "cookie"))
        self.label_2.setText(_translate("MainWindow", "图床api"))
        self.pushButton_shot.setText(_translate("MainWindow", "开始截图"))
        self.pushButton_exit.setText(_translate("MainWindow", "退出程序"))
