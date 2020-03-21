# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(439, 305)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_shot = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_shot.sizePolicy().hasHeightForWidth())
        self.label_shot.setSizePolicy(sizePolicy)
        self.label_shot.setText("")
        self.label_shot.setScaledContents(False)
        self.label_shot.setObjectName("label_shot")
        self.verticalLayout.addWidget(self.label_shot)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_markdown = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_markdown.setObjectName("pushButton_markdown")
        self.horizontalLayout.addWidget(self.pushButton_markdown)
        self.pushButton_clipboard = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_clipboard.setObjectName("pushButton_clipboard")
        self.horizontalLayout.addWidget(self.pushButton_clipboard)
        self.pushButton_save = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_save.setObjectName("pushButton_save")
        self.horizontalLayout.addWidget(self.pushButton_save)
        self.pushButton_cancel = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.horizontalLayout.addWidget(self.pushButton_cancel)
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton_markdown.setText(_translate("Dialog", "markdown"))
        self.pushButton_clipboard.setText(_translate("Dialog", "clipboard"))
        self.pushButton_save.setText(_translate("Dialog", "save"))
        self.pushButton_cancel.setText(_translate("Dialog", "cancel"))
