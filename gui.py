# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Temp_prj\Python_prj\cloud_img_cut\gui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(386, 290)
        self.textEdit_log = QtWidgets.QTextEdit(Form)
        self.textEdit_log.setGeometry(QtCore.QRect(10, 140, 361, 141))
        self.textEdit_log.setObjectName("textEdit_log")
        self.pushButton_open = QtWidgets.QPushButton(Form)
        self.pushButton_open.setGeometry(QtCore.QRect(250, 20, 75, 23))
        self.pushButton_open.setObjectName("pushButton_open")
        self.pushButton_log_clear = QtWidgets.QPushButton(Form)
        self.pushButton_log_clear.setGeometry(QtCore.QRect(250, 100, 75, 23))
        self.pushButton_log_clear.setObjectName("pushButton_log_clear")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 201, 121))
        self.groupBox.setObjectName("groupBox")
        self.pushButton_show_img = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_show_img.setEnabled(False)
        self.pushButton_show_img.setGeometry(QtCore.QRect(90, 90, 75, 23))
        self.pushButton_show_img.setCheckable(False)
        self.pushButton_show_img.setChecked(False)
        self.pushButton_show_img.setObjectName("pushButton_show_img")
        self.checkBox_show_mean_img = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_show_mean_img.setGeometry(QtCore.QRect(30, 60, 101, 16))
        self.checkBox_show_mean_img.setChecked(True)
        self.checkBox_show_mean_img.setObjectName("checkBox_show_mean_img")
        self.widget = QtWidgets.QWidget(self.groupBox)
        self.widget.setGeometry(QtCore.QRect(30, 20, 151, 22))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.spinBox_img_cnt = QtWidgets.QSpinBox(self.widget)
        self.spinBox_img_cnt.setAlignment(QtCore.Qt.AlignCenter)
        self.spinBox_img_cnt.setMinimum(-1)
        self.spinBox_img_cnt.setProperty("value", -1)
        self.spinBox_img_cnt.setObjectName("spinBox_img_cnt")
        self.horizontalLayout.addWidget(self.spinBox_img_cnt)

        self.retranslateUi(Form)
        self.pushButton_log_clear.clicked.connect(Form.click_log_clear)
        self.pushButton_open.clicked.connect(Form.click_open)
        self.pushButton_show_img.clicked.connect(Form.click_show_img)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "云判数据挑选工具"))
        self.pushButton_open.setText(_translate("Form", "打开"))
        self.pushButton_log_clear.setText(_translate("Form", "清除"))
        self.groupBox.setTitle(_translate("Form", "图像显示"))
        self.pushButton_show_img.setText(_translate("Form", "显示图像"))
        self.checkBox_show_mean_img.setText(_translate("Form", "显示平均值图像"))
        self.label.setText(_translate("Form", "865P2图像序号"))

