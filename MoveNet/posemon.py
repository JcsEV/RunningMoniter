# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'posemon.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QComboBox, QLabel,
    QMainWindow, QPushButton, QSizePolicy, QStatusBar,
    QTabWidget, QTextEdit, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QSize(800, 600))
        MainWindow.setMaximumSize(QSize(800, 600))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.textEdit = QTextEdit(self.centralwidget)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setGeometry(QRect(90, 20, 661, 31))
        self.textEdit.setMinimumSize(QSize(661, 31))
        self.textEdit.setMaximumSize(QSize(661, 31))
        self.textEdit.setLayoutDirection(Qt.LeftToRight)
        self.textEdit.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(90, 70, 81, 31))
        self.comboBox.setMinimumSize(QSize(0, 31))
        self.comboBox.setMaximumSize(QSize(100, 31))
        self.comboBox.setStyleSheet(u"QComboBox::view::item {text-align: center;}")
        self.comboBox.setMaxCount(2147483647)
        self.comboBox.setInsertPolicy(QComboBox.InsertAtBottom)
        self.comboBox_2 = QComboBox(self.centralwidget)
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.setObjectName(u"comboBox_2")
        self.comboBox_2.setGeometry(QRect(270, 70, 241, 31))
        self.comboBox_2.setMinimumSize(QSize(241, 31))
        self.comboBox_2.setMaximumSize(QSize(241, 31))
        self.comboBox_2.setStyleSheet(u"QComboBox::view::item {text-align: center;}")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 70, 71, 31))
        self.label.setMinimumSize(QSize(71, 31))
        self.label.setMaximumSize(QSize(71, 31))
        self.label.setLayoutDirection(Qt.LeftToRight)
        self.label.setAlignment(Qt.AlignCenter)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 20, 71, 31))
        self.label_2.setMinimumSize(QSize(71, 31))
        self.label_2.setMaximumSize(QSize(71, 31))
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(200, 70, 71, 31))
        self.label_3.setMinimumSize(QSize(71, 31))
        self.label_3.setMaximumSize(QSize(71, 31))
        self.label_3.setAlignment(Qt.AlignCenter)
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(750, 20, 21, 31))
        self.pushButton.setMinimumSize(QSize(21, 31))
        self.pushButton.setMaximumSize(QSize(21, 31))
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(560, 70, 211, 31))
        self.pushButton_2.setMinimumSize(QSize(211, 31))
        self.pushButton_2.setMaximumSize(QSize(211, 31))
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(20, 120, 751, 451))
        self.tabWidget.setMinimumSize(QSize(751, 451))
        self.tabWidget.setMaximumSize(QSize(751, 451))
        self.tab_1 = QWidget()
        self.tab_1.setObjectName(u"tab_1")
        self.textEdit_1 = QTextEdit(self.tab_1)
        self.textEdit_1.setObjectName(u"textEdit_1")
        self.textEdit_1.setGeometry(QRect(30, 30, 681, 361))
        self.textEdit_1.setMinimumSize(QSize(681, 361))
        self.textEdit_1.setMaximumSize(QSize(681, 361))
        self.textEdit_1.setMouseTracking(False)
        self.textEdit_1.setReadOnly(True)
        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.textEdit_2 = QTextEdit(self.tab_2)
        self.textEdit_2.setObjectName(u"textEdit_2")
        self.textEdit_2.setGeometry(QRect(30, 30, 681, 361))
        self.textEdit_2.setMinimumSize(QSize(681, 361))
        self.textEdit_2.setMaximumSize(QSize(681, 361))
        self.textEdit_2.setMouseTracking(False)
        self.textEdit_2.setReadOnly(True)
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"\u56fe\u7247\u4f30\u8ba1", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"\u89c6\u9891\u4f30\u8ba1", None))

        self.comboBox_2.setItemText(0, QCoreApplication.translate("MainWindow", u"movenet_singlepose_thunder_int8", None))
        self.comboBox_2.setItemText(1, QCoreApplication.translate("MainWindow", u"movenet_singlepose_thunder_fp16", None))

        self.label.setText(QCoreApplication.translate("MainWindow", u"\u529f\u80fd\u9009\u62e9\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6\u8def\u5f84\uff1a", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u6a21\u578b\u9009\u62e9\uff1a", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u2026\u2026", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u4f30\u8ba1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), QCoreApplication.translate("MainWindow", u"Result_Messages", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Warning_Messages", None))
    # retranslateUi

