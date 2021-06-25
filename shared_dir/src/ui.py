# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'carla2hdf5.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1152, 822)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.main_gridLayout = QGridLayout()
        self.main_gridLayout.setObjectName(u"main_gridLayout")
        self.init_groupBox = QGroupBox(self.centralwidget)
        self.init_groupBox.setObjectName(u"init_groupBox")
        self.init_groupBox.setFlat(False)
        self.init_groupBox.setCheckable(False)
        self.verticalLayout = QVBoxLayout(self.init_groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.init_horizontalLayout = QHBoxLayout()
        self.init_horizontalLayout.setObjectName(u"init_horizontalLayout")
        self.ip_address_label = QLabel(self.init_groupBox)
        self.ip_address_label.setObjectName(u"ip_address_label")

        self.init_horizontalLayout.addWidget(self.ip_address_label)

        self.ip_address_lineEdit = QLineEdit(self.init_groupBox)
        self.ip_address_lineEdit.setObjectName(u"ip_address_lineEdit")

        self.init_horizontalLayout.addWidget(self.ip_address_lineEdit)

        self.port_label = QLabel(self.init_groupBox)
        self.port_label.setObjectName(u"port_label")

        self.init_horizontalLayout.addWidget(self.port_label)

        self.port_spinBox = QSpinBox(self.init_groupBox)
        self.port_spinBox.setObjectName(u"port_spinBox")
        self.port_spinBox.setMinimum(1)
        self.port_spinBox.setMaximum(65535)
        self.port_spinBox.setValue(2000)

        self.init_horizontalLayout.addWidget(self.port_spinBox)


        self.verticalLayout.addLayout(self.init_horizontalLayout)

        self.connect_pushButton = QPushButton(self.init_groupBox)
        self.connect_pushButton.setObjectName(u"connect_pushButton")

        self.verticalLayout.addWidget(self.connect_pushButton)


        self.main_gridLayout.addWidget(self.init_groupBox, 0, 0, 1, 1)

        self.tf_groupBox = QGroupBox(self.centralwidget)
        self.tf_groupBox.setObjectName(u"tf_groupBox")
        self.verticalLayout_3 = QVBoxLayout(self.tf_groupBox)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.tf_verticalLayout = QVBoxLayout()
        self.tf_verticalLayout.setObjectName(u"tf_verticalLayout")

        self.verticalLayout_3.addLayout(self.tf_verticalLayout)


        self.main_gridLayout.addWidget(self.tf_groupBox, 1, 0, 1, 1)

        self.main_settings_groupBox = QGroupBox(self.centralwidget)
        self.main_settings_groupBox.setObjectName(u"main_settings_groupBox")
        self.verticalLayout_4 = QVBoxLayout(self.main_settings_groupBox)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.settings_1_horizontalLayout = QHBoxLayout()
        self.settings_1_horizontalLayout.setObjectName(u"settings_1_horizontalLayout")
        self.map_label = QLabel(self.main_settings_groupBox)
        self.map_label.setObjectName(u"map_label")

        self.settings_1_horizontalLayout.addWidget(self.map_label)

        self.map_comboBox = QComboBox(self.main_settings_groupBox)
        self.map_comboBox.setObjectName(u"map_comboBox")

        self.settings_1_horizontalLayout.addWidget(self.map_comboBox)

        self.weather_label = QLabel(self.main_settings_groupBox)
        self.weather_label.setObjectName(u"weather_label")

        self.settings_1_horizontalLayout.addWidget(self.weather_label)

        self.weather_comboBox = QComboBox(self.main_settings_groupBox)
        self.weather_comboBox.setObjectName(u"weather_comboBox")

        self.settings_1_horizontalLayout.addWidget(self.weather_comboBox)

        self.settings_1_horizontalLayout.setStretch(0, 1)
        self.settings_1_horizontalLayout.setStretch(1, 3)
        self.settings_1_horizontalLayout.setStretch(2, 1)
        self.settings_1_horizontalLayout.setStretch(3, 3)

        self.verticalLayout_4.addLayout(self.settings_1_horizontalLayout)

        self.line = QFrame(self.main_settings_groupBox)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line)

        self.settings_2_horizontalLayout = QHBoxLayout()
        self.settings_2_horizontalLayout.setObjectName(u"settings_2_horizontalLayout")
        self.seed_label = QLabel(self.main_settings_groupBox)
        self.seed_label.setObjectName(u"seed_label")

        self.settings_2_horizontalLayout.addWidget(self.seed_label)

        self.seed_spinBox = QSpinBox(self.main_settings_groupBox)
        self.seed_spinBox.setObjectName(u"seed_spinBox")
        self.seed_spinBox.setMaximum(429496729)
        self.seed_spinBox.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
        self.seed_spinBox.setValue(1000)

        self.settings_2_horizontalLayout.addWidget(self.seed_spinBox)

        self.num_frames_label = QLabel(self.main_settings_groupBox)
        self.num_frames_label.setObjectName(u"num_frames_label")

        self.settings_2_horizontalLayout.addWidget(self.num_frames_label)

        self.num_frames_spinBox = QSpinBox(self.main_settings_groupBox)
        self.num_frames_spinBox.setObjectName(u"num_frames_spinBox")
        self.num_frames_spinBox.setMaximum(429496729)
        self.num_frames_spinBox.setSingleStep(100)
        self.num_frames_spinBox.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
        self.num_frames_spinBox.setValue(3000)

        self.settings_2_horizontalLayout.addWidget(self.num_frames_spinBox)

        self.settings_2_horizontalLayout.setStretch(0, 1)
        self.settings_2_horizontalLayout.setStretch(1, 4)
        self.settings_2_horizontalLayout.setStretch(2, 1)
        self.settings_2_horizontalLayout.setStretch(3, 4)

        self.verticalLayout_4.addLayout(self.settings_2_horizontalLayout)

        self.line_2 = QFrame(self.main_settings_groupBox)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_2)

        self.settings_3_horizontalLayout = QHBoxLayout()
        self.settings_3_horizontalLayout.setObjectName(u"settings_3_horizontalLayout")
        self.num_npc_vehicles_label = QLabel(self.main_settings_groupBox)
        self.num_npc_vehicles_label.setObjectName(u"num_npc_vehicles_label")

        self.settings_3_horizontalLayout.addWidget(self.num_npc_vehicles_label)

        self.num_npc_vehicles_spinBox = QSpinBox(self.main_settings_groupBox)
        self.num_npc_vehicles_spinBox.setObjectName(u"num_npc_vehicles_spinBox")
        self.num_npc_vehicles_spinBox.setMaximum(429496729)
        self.num_npc_vehicles_spinBox.setStepType(QAbstractSpinBox.AdaptiveDecimalStepType)
        self.num_npc_vehicles_spinBox.setValue(50)

        self.settings_3_horizontalLayout.addWidget(self.num_npc_vehicles_spinBox)

        self.safe_spawn_checkBox = QCheckBox(self.main_settings_groupBox)
        self.safe_spawn_checkBox.setObjectName(u"safe_spawn_checkBox")
        self.safe_spawn_checkBox.setAutoRepeat(False)
        self.safe_spawn_checkBox.setTristate(False)

        self.settings_3_horizontalLayout.addWidget(self.safe_spawn_checkBox)

        self.settings_3_horizontalLayout.setStretch(0, 1)
        self.settings_3_horizontalLayout.setStretch(1, 4)

        self.verticalLayout_4.addLayout(self.settings_3_horizontalLayout)

        self.line_3 = QFrame(self.main_settings_groupBox)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_3)

        self.settings_4_horizontalLayout = QHBoxLayout()
        self.settings_4_horizontalLayout.setObjectName(u"settings_4_horizontalLayout")
        self.num_npc_walkers_label = QLabel(self.main_settings_groupBox)
        self.num_npc_walkers_label.setObjectName(u"num_npc_walkers_label")

        self.settings_4_horizontalLayout.addWidget(self.num_npc_walkers_label)

        self.num_npc_walkers_spinBox = QSpinBox(self.main_settings_groupBox)
        self.num_npc_walkers_spinBox.setObjectName(u"num_npc_walkers_spinBox")
        self.num_npc_walkers_spinBox.setMaximum(1000)
        self.num_npc_walkers_spinBox.setValue(50)

        self.settings_4_horizontalLayout.addWidget(self.num_npc_walkers_spinBox)

        self.running_walker_label = QLabel(self.main_settings_groupBox)
        self.running_walker_label.setObjectName(u"running_walker_label")

        self.settings_4_horizontalLayout.addWidget(self.running_walker_label)

        self.running_walker_doubleSpinBox = QDoubleSpinBox(self.main_settings_groupBox)
        self.running_walker_doubleSpinBox.setObjectName(u"running_walker_doubleSpinBox")
        self.running_walker_doubleSpinBox.setDecimals(1)
        self.running_walker_doubleSpinBox.setValue(10.000000000000000)

        self.settings_4_horizontalLayout.addWidget(self.running_walker_doubleSpinBox)

        self.road_crossing_walker_label = QLabel(self.main_settings_groupBox)
        self.road_crossing_walker_label.setObjectName(u"road_crossing_walker_label")

        self.settings_4_horizontalLayout.addWidget(self.road_crossing_walker_label)

        self.road_crossing_walker_doubleSpinBox = QDoubleSpinBox(self.main_settings_groupBox)
        self.road_crossing_walker_doubleSpinBox.setObjectName(u"road_crossing_walker_doubleSpinBox")
        self.road_crossing_walker_doubleSpinBox.setDecimals(1)
        self.road_crossing_walker_doubleSpinBox.setValue(2.000000000000000)

        self.settings_4_horizontalLayout.addWidget(self.road_crossing_walker_doubleSpinBox)


        self.verticalLayout_4.addLayout(self.settings_4_horizontalLayout)

        self.line_4 = QFrame(self.main_settings_groupBox)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_4)

        self.settings_5_horizontalLayout = QHBoxLayout()
        self.settings_5_horizontalLayout.setObjectName(u"settings_5_horizontalLayout")
        self.global_distance_label = QLabel(self.main_settings_groupBox)
        self.global_distance_label.setObjectName(u"global_distance_label")

        self.settings_5_horizontalLayout.addWidget(self.global_distance_label)

        self.global_distance_doubleSpinBox = QDoubleSpinBox(self.main_settings_groupBox)
        self.global_distance_doubleSpinBox.setObjectName(u"global_distance_doubleSpinBox")
        self.global_distance_doubleSpinBox.setDecimals(1)
        self.global_distance_doubleSpinBox.setValue(1.000000000000000)

        self.settings_5_horizontalLayout.addWidget(self.global_distance_doubleSpinBox)

        self.hybrid_physics_checkBox = QCheckBox(self.main_settings_groupBox)
        self.hybrid_physics_checkBox.setObjectName(u"hybrid_physics_checkBox")
        self.hybrid_physics_checkBox.setChecked(True)

        self.settings_5_horizontalLayout.addWidget(self.hybrid_physics_checkBox)

        self.hybrid_physics_radius_label = QLabel(self.main_settings_groupBox)
        self.hybrid_physics_radius_label.setObjectName(u"hybrid_physics_radius_label")

        self.settings_5_horizontalLayout.addWidget(self.hybrid_physics_radius_label)

        self.hybrid_physics_radius_doubleSpinBox = QDoubleSpinBox(self.main_settings_groupBox)
        self.hybrid_physics_radius_doubleSpinBox.setObjectName(u"hybrid_physics_radius_doubleSpinBox")
        self.hybrid_physics_radius_doubleSpinBox.setDecimals(1)
        self.hybrid_physics_radius_doubleSpinBox.setMaximum(65535.000000000000000)
        self.hybrid_physics_radius_doubleSpinBox.setValue(50.000000000000000)

        self.settings_5_horizontalLayout.addWidget(self.hybrid_physics_radius_doubleSpinBox)

        self.super_hero_checkBox = QCheckBox(self.main_settings_groupBox)
        self.super_hero_checkBox.setObjectName(u"super_hero_checkBox")
        self.super_hero_checkBox.setChecked(True)

        self.settings_5_horizontalLayout.addWidget(self.super_hero_checkBox)


        self.verticalLayout_4.addLayout(self.settings_5_horizontalLayout)

        self.add_queue_pushButton = QPushButton(self.main_settings_groupBox)
        self.add_queue_pushButton.setObjectName(u"add_queue_pushButton")

        self.verticalLayout_4.addWidget(self.add_queue_pushButton)

        self.queue_groupBox = QGroupBox(self.main_settings_groupBox)
        self.queue_groupBox.setObjectName(u"queue_groupBox")
        self.verticalLayout_5 = QVBoxLayout(self.queue_groupBox)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.queue_treeWidget = QTreeWidget(self.queue_groupBox)
        self.queue_treeWidget.setObjectName(u"queue_treeWidget")
        self.queue_treeWidget.setColumnCount(5)

        self.verticalLayout_5.addWidget(self.queue_treeWidget)


        self.verticalLayout_4.addWidget(self.queue_groupBox)

        self.verticalLayout_4.setStretch(10, 1)

        self.main_gridLayout.addWidget(self.main_settings_groupBox, 0, 1, 2, 1)

        self.main_gridLayout.setRowStretch(0, 1)
        self.main_gridLayout.setRowStretch(1, 6)
        self.main_gridLayout.setColumnStretch(0, 5)
        self.main_gridLayout.setColumnStretch(1, 5)

        self.verticalLayout_2.addLayout(self.main_gridLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1152, 28))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"CARLA2HDF5", None))
        self.init_groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Initial Settings", None))
        self.ip_address_label.setText(QCoreApplication.translate("MainWindow", u"IP Address", None))
        self.ip_address_lineEdit.setText(QCoreApplication.translate("MainWindow", u"localhost", None))
        self.port_label.setText(QCoreApplication.translate("MainWindow", u"Port", None))
        self.connect_pushButton.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
#if QT_CONFIG(shortcut)
        self.connect_pushButton.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+C", None))
#endif // QT_CONFIG(shortcut)
        self.tf_groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Transform", None))
        self.main_settings_groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.map_label.setText(QCoreApplication.translate("MainWindow", u"Map", None))
        self.weather_label.setText(QCoreApplication.translate("MainWindow", u"Weather", None))
        self.seed_label.setText(QCoreApplication.translate("MainWindow", u"Seed", None))
        self.num_frames_label.setText(QCoreApplication.translate("MainWindow", u"# Frames", None))
        self.num_frames_spinBox.setSuffix("")
        self.num_npc_vehicles_label.setText(QCoreApplication.translate("MainWindow", u"# NPC Vehicles", None))
        self.safe_spawn_checkBox.setText(QCoreApplication.translate("MainWindow", u"Safe Spawn", None))
        self.num_npc_walkers_label.setText(QCoreApplication.translate("MainWindow", u"# NPC Walkers", None))
        self.running_walker_label.setText(QCoreApplication.translate("MainWindow", u"Running Walker", None))
        self.running_walker_doubleSpinBox.setSuffix(QCoreApplication.translate("MainWindow", u" [%]", None))
        self.road_crossing_walker_label.setText(QCoreApplication.translate("MainWindow", u"Road Crossing Walker", None))
        self.road_crossing_walker_doubleSpinBox.setSuffix(QCoreApplication.translate("MainWindow", u" [%]", None))
        self.global_distance_label.setText(QCoreApplication.translate("MainWindow", u"Global Distance", None))
        self.global_distance_doubleSpinBox.setSuffix(QCoreApplication.translate("MainWindow", u" [m]", None))
        self.hybrid_physics_checkBox.setText(QCoreApplication.translate("MainWindow", u"Hybrid Physics (HP)", None))
        self.hybrid_physics_radius_label.setText(QCoreApplication.translate("MainWindow", u"HP Radius", None))
        self.hybrid_physics_radius_doubleSpinBox.setSuffix(QCoreApplication.translate("MainWindow", u" [m]", None))
        self.super_hero_checkBox.setText(QCoreApplication.translate("MainWindow", u"Super Hero", None))
        self.add_queue_pushButton.setText(QCoreApplication.translate("MainWindow", u"Add Queue", None))
#if QT_CONFIG(shortcut)
        self.add_queue_pushButton.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+E", None))
#endif // QT_CONFIG(shortcut)
        self.queue_groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Queue", None))
        ___qtreewidgetitem = self.queue_treeWidget.headerItem()
        ___qtreewidgetitem.setText(4, QCoreApplication.translate("MainWindow", u"Status", None));
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("MainWindow", u"# Frames", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("MainWindow", u"Seed", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MainWindow", u"Weather", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"Map", None));
    # retranslateUi

