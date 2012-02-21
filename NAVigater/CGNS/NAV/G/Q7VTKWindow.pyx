# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CGNS/NAV/T/Q7VTKWindow.ui'
#
# Created: Mon Feb 20 16:44:41 2012
#      by: pyside-uic 0.2.13 running on PySide 1.0.9
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Q7VTKWindow(object):
    def setupUi(self, Q7VTKWindow):
        Q7VTKWindow.setObjectName("Q7VTKWindow")
        Q7VTKWindow.resize(803, 679)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Q7VTKWindow.sizePolicy().hasHeightForWidth())
        Q7VTKWindow.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/icons/cgSpy.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Q7VTKWindow.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(Q7VTKWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cViews = QtGui.QComboBox(Q7VTKWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cViews.sizePolicy().hasHeightForWidth())
        self.cViews.setSizePolicy(sizePolicy)
        self.cViews.setEditable(True)
        self.cViews.setMaxCount(16)
        self.cViews.setInsertPolicy(QtGui.QComboBox.InsertAtTop)
        self.cViews.setObjectName("cViews")
        self.horizontalLayout.addWidget(self.cViews)
        self.bAddView = QtGui.QPushButton(Q7VTKWindow)
        self.bAddView.setMinimumSize(QtCore.QSize(25, 25))
        self.bAddView.setMaximumSize(QtCore.QSize(25, 25))
        self.bAddView.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/images/icons/camera-add.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bAddView.setIcon(icon1)
        self.bAddView.setObjectName("bAddView")
        self.horizontalLayout.addWidget(self.bAddView)
        self.bSaveView = QtGui.QPushButton(Q7VTKWindow)
        self.bSaveView.setMinimumSize(QtCore.QSize(25, 25))
        self.bSaveView.setMaximumSize(QtCore.QSize(25, 25))
        self.bSaveView.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/images/icons/camera-snap.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bSaveView.setIcon(icon2)
        self.bSaveView.setObjectName("bSaveView")
        self.horizontalLayout.addWidget(self.bSaveView)
        self.bRemoveView = QtGui.QPushButton(Q7VTKWindow)
        self.bRemoveView.setMinimumSize(QtCore.QSize(25, 25))
        self.bRemoveView.setMaximumSize(QtCore.QSize(25, 25))
        self.bRemoveView.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/images/icons/camera-remove.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bRemoveView.setIcon(icon3)
        self.bRemoveView.setObjectName("bRemoveView")
        self.horizontalLayout.addWidget(self.bRemoveView)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.bSnapshot = QtGui.QPushButton(Q7VTKWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bSnapshot.sizePolicy().hasHeightForWidth())
        self.bSnapshot.setSizePolicy(sizePolicy)
        self.bSnapshot.setMinimumSize(QtCore.QSize(25, 25))
        self.bSnapshot.setMaximumSize(QtCore.QSize(25, 25))
        self.bSnapshot.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/images/icons/snapshot.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bSnapshot.setIcon(icon4)
        self.bSnapshot.setObjectName("bSnapshot")
        self.horizontalLayout.addWidget(self.bSnapshot)
        self.bSaveVTK = QtGui.QPushButton(Q7VTKWindow)
        self.bSaveVTK.setMinimumSize(QtCore.QSize(25, 25))
        self.bSaveVTK.setMaximumSize(QtCore.QSize(25, 25))
        self.bSaveVTK.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/images/icons/save.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bSaveVTK.setIcon(icon5)
        self.bSaveVTK.setObjectName("bSaveVTK")
        self.horizontalLayout.addWidget(self.bSaveVTK)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line = QtGui.QFrame(Q7VTKWindow)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.bX = QtGui.QPushButton(Q7VTKWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bX.sizePolicy().hasHeightForWidth())
        self.bX.setSizePolicy(sizePolicy)
        self.bX.setMinimumSize(QtCore.QSize(25, 25))
        self.bX.setMaximumSize(QtCore.QSize(25, 25))
        self.bX.setObjectName("bX")
        self.horizontalLayout_3.addWidget(self.bX)
        self.bY = QtGui.QPushButton(Q7VTKWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bY.sizePolicy().hasHeightForWidth())
        self.bY.setSizePolicy(sizePolicy)
        self.bY.setMinimumSize(QtCore.QSize(25, 25))
        self.bY.setMaximumSize(QtCore.QSize(25, 25))
        self.bY.setObjectName("bY")
        self.horizontalLayout_3.addWidget(self.bY)
        self.bZ = QtGui.QPushButton(Q7VTKWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bZ.sizePolicy().hasHeightForWidth())
        self.bZ.setSizePolicy(sizePolicy)
        self.bZ.setMinimumSize(QtCore.QSize(25, 25))
        self.bZ.setMaximumSize(QtCore.QSize(25, 25))
        self.bZ.setObjectName("bZ")
        self.horizontalLayout_3.addWidget(self.bZ)
        self.cMirror = QtGui.QCheckBox(Q7VTKWindow)
        self.cMirror.setObjectName("cMirror")
        self.horizontalLayout_3.addWidget(self.cMirror)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.bSuffleColors = QtGui.QPushButton(Q7VTKWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bSuffleColors.sizePolicy().hasHeightForWidth())
        self.bSuffleColors.setSizePolicy(sizePolicy)
        self.bSuffleColors.setMinimumSize(QtCore.QSize(25, 25))
        self.bSuffleColors.setMaximumSize(QtCore.QSize(25, 25))
        self.bSuffleColors.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/images/icons/colors.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bSuffleColors.setIcon(icon6)
        self.bSuffleColors.setObjectName("bSuffleColors")
        self.horizontalLayout_3.addWidget(self.bSuffleColors)
        self.bBlackColor = QtGui.QPushButton(Q7VTKWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bBlackColor.sizePolicy().hasHeightForWidth())
        self.bBlackColor.setSizePolicy(sizePolicy)
        self.bBlackColor.setMinimumSize(QtCore.QSize(25, 25))
        self.bBlackColor.setMaximumSize(QtCore.QSize(25, 25))
        self.bBlackColor.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/images/icons/colors-bw.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bBlackColor.setIcon(icon7)
        self.bBlackColor.setObjectName("bBlackColor")
        self.horizontalLayout_3.addWidget(self.bBlackColor)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.display = QVTKRenderWindowInteractor(Q7VTKWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.display.sizePolicy().hasHeightForWidth())
        self.display.setSizePolicy(sizePolicy)
        self.display.setObjectName("display")
        self.verticalLayout_2.addWidget(self.display)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.bBackControl = QtGui.QPushButton(Q7VTKWindow)
        self.bBackControl.setMinimumSize(QtCore.QSize(25, 25))
        self.bBackControl.setMaximumSize(QtCore.QSize(25, 25))
        self.bBackControl.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/images/icons/top.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bBackControl.setIcon(icon8)
        self.bBackControl.setObjectName("bBackControl")
        self.horizontalLayout_2.addWidget(self.bBackControl)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.bUpdate = QtGui.QPushButton(Q7VTKWindow)
        self.bUpdate.setMinimumSize(QtCore.QSize(25, 25))
        self.bUpdate.setMaximumSize(QtCore.QSize(25, 25))
        self.bUpdate.setText("")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/images/icons/undo-last-modification.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bUpdate.setIcon(icon9)
        self.bUpdate.setObjectName("bUpdate")
        self.horizontalLayout_2.addWidget(self.bUpdate)
        self.cCurrentPath = QtGui.QComboBox(Q7VTKWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cCurrentPath.sizePolicy().hasHeightForWidth())
        self.cCurrentPath.setSizePolicy(sizePolicy)
        self.cCurrentPath.setEditable(True)
        self.cCurrentPath.setObjectName("cCurrentPath")
        self.horizontalLayout_2.addWidget(self.cCurrentPath)
        self.cRevert = QtGui.QCheckBox(Q7VTKWindow)
        self.cRevert.setObjectName("cRevert")
        self.horizontalLayout_2.addWidget(self.cRevert)
        self.cSync = QtGui.QCheckBox(Q7VTKWindow)
        self.cSync.setObjectName("cSync")
        self.horizontalLayout_2.addWidget(self.cSync)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.bPrevious = QtGui.QPushButton(Q7VTKWindow)
        self.bPrevious.setMinimumSize(QtCore.QSize(25, 25))
        self.bPrevious.setMaximumSize(QtCore.QSize(25, 25))
        self.bPrevious.setText("")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/images/icons/control.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bPrevious.setIcon(icon10)
        self.bPrevious.setObjectName("bPrevious")
        self.horizontalLayout_2.addWidget(self.bPrevious)
        self.bReset = QtGui.QPushButton(Q7VTKWindow)
        self.bReset.setMinimumSize(QtCore.QSize(25, 25))
        self.bReset.setMaximumSize(QtCore.QSize(25, 25))
        self.bReset.setText("")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/images/icons/node-sids-leaf.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bReset.setIcon(icon11)
        self.bReset.setObjectName("bReset")
        self.horizontalLayout_2.addWidget(self.bReset)
        self.bNext = QtGui.QPushButton(Q7VTKWindow)
        self.bNext.setMinimumSize(QtCore.QSize(25, 25))
        self.bNext.setMaximumSize(QtCore.QSize(25, 25))
        self.bNext.setText("")
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/images/icons/node-sids-closed.gif"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.bNext.setIcon(icon12)
        self.bNext.setObjectName("bNext")
        self.horizontalLayout_2.addWidget(self.bNext)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Q7VTKWindow)
        QtCore.QMetaObject.connectSlotsByName(Q7VTKWindow)

    def retranslateUi(self, Q7VTKWindow):
        Q7VTKWindow.setWindowTitle(QtGui.QApplication.translate("Q7VTKWindow", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.bX.setText(QtGui.QApplication.translate("Q7VTKWindow", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.bY.setText(QtGui.QApplication.translate("Q7VTKWindow", "Y", None, QtGui.QApplication.UnicodeUTF8))
        self.bZ.setText(QtGui.QApplication.translate("Q7VTKWindow", "Z", None, QtGui.QApplication.UnicodeUTF8))
        self.cMirror.setText(QtGui.QApplication.translate("Q7VTKWindow", "Mirror", None, QtGui.QApplication.UnicodeUTF8))
        self.cRevert.setText(QtGui.QApplication.translate("Q7VTKWindow", "Revert", None, QtGui.QApplication.UnicodeUTF8))
        self.cSync.setText(QtGui.QApplication.translate("Q7VTKWindow", "Sync", None, QtGui.QApplication.UnicodeUTF8))

from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import Res_rc
