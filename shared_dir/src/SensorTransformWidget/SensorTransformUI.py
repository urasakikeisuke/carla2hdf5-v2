# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './SensorTransformWidget/sensor_transform.ui',
# licensing of './SensorTransformWidget/sensor_transform.ui' applies.
#
# Created: Mon May 31 00:25:50 2021
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_SensorTransform(object):
    def setupUi(self, SensorTransform):
        SensorTransform.setObjectName("SensorTransform")
        SensorTransform.resize(560, 280)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(SensorTransform)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.HeaderLayout = QtWidgets.QHBoxLayout()
        self.HeaderLayout.setObjectName("HeaderLayout")
        self.label = QtWidgets.QLabel(SensorTransform)
        self.label.setText("Sensor Transform")
        self.label.setObjectName("label")
        self.HeaderLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.HeaderLayout.addItem(spacerItem)
        self.addButton = QtWidgets.QPushButton(SensorTransform)
        self.addButton.setText("Add")
        self.addButton.setObjectName("addButton")
        self.HeaderLayout.addWidget(self.addButton)
        self.removeButton = QtWidgets.QPushButton(SensorTransform)
        self.removeButton.setText("Remove")
        self.removeButton.setObjectName("removeButton")
        self.HeaderLayout.addWidget(self.removeButton)
        self.verticalLayout.addLayout(self.HeaderLayout)
        self.transformTree = QtWidgets.QTreeWidget(SensorTransform)
        self.transformTree.setObjectName("transformTree")
        self.transformTree.headerItem().setText(0, "Frame ID")
        self.transformTree.headerItem().setText(1, "xyz")
        self.transformTree.headerItem().setText(2, "rpy")
        self.verticalLayout.addWidget(self.transformTree)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.viewLayout = QtWidgets.QVBoxLayout()
        self.viewLayout.setObjectName("viewLayout")
        self.modeLayout = QtWidgets.QHBoxLayout()
        self.modeLayout.setObjectName("modeLayout")
        self.carlaRadioButton = QtWidgets.QRadioButton(SensorTransform)
        self.carlaRadioButton.setText("CARLA")
        self.carlaRadioButton.setChecked(True)
        self.carlaRadioButton.setObjectName("carlaRadioButton")
        self.modeLayout.addWidget(self.carlaRadioButton)
        self.hdf5RadioButton = QtWidgets.QRadioButton(SensorTransform)
        self.hdf5RadioButton.setText("HDF5")
        self.hdf5RadioButton.setObjectName("hdf5RadioButton")
        self.modeLayout.addWidget(self.hdf5RadioButton)
        self.viewLayout.addLayout(self.modeLayout)
        self.horizontalLayout_2.addLayout(self.viewLayout)

        # self.retranslateUi(SensorTransform)
        QtCore.QMetaObject.connectSlotsByName(SensorTransform)
