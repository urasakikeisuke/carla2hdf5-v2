from typing import Dict, List

import numpy as np
from pyqtgraph.opengl import GLGridItem, GLLinePlotItem, GLViewWidget
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QWidget, QTreeWidgetItem
from scipy.spatial.transform import Rotation

from .glutTextItem import GLTextItem
from .SensorTransformUI import Ui_SensorTransform
from .SensorTransformDialog import Ui_Dialog

AXIS_SCALE = 0.3
AXIS_POS = np.array([[0., 0., 0.],[1., 0., 0.],[0., 0., 0.],[0., 1., 0.],[0., 0., 0.],[0., 0., 1.]])
AXIS_COLOR = np.array([[1., 0., 0., 1.],[1., 0., 0., 1.],[0., 1., 0., 1.],[0., 1., 0., 1.],[0., 0., 1., 1.],[0., 0., 1., 1.]])

class AxisItem():
    def __init__(self, tfConfig:dict={}) -> None:
        """__init__

        コンストラクタ

        Args:
            tfConfig (dict, optional): TFの設定を格納する辞書. Defaults to {}.
        """
        self.tfConfig = tfConfig

        self.frameId:str = ''
        self.translation:np.ndarray = np.array([0., 0., 0.], dtype=np.float32)
        self.quaternion:np.ndarray = np.array([0., 0., 0., 1.], dtype=np.float32)
        self.camera = False
        self.carla = True

        self.axisItem = GLLinePlotItem()
        self.textItem = GLTextItem()
    
    def setData(self, frame_id:str='', x:float=None, y:float=None, z:float=None, roll:float=None, pitch:float=None, yaw:float=None, camera:bool=None) -> None:
        """setData

        データを格納する

        Args:
            frame_id (str, optional): 座標系のID. Defaults to ''.
            x (float, optional): CARLAの'spawn_point'の'x'の値. Defaults to None.
            y (float, optional): CARLAの'spawn_point'の'y'の値. Defaults to None.
            z (float, optional): CARLAの'spawn_point'の'z'の値. Defaults to None.
            roll (float, optional): CARLAの'spawn_point'の'roll'の値. Defaults to None.
            pitch (float, optional): CARLAの'spawn_point'の'pitch'の値. Defaults to None.
            yaw (float, optional): CARLAの'spawn_point'の'yaw'の値. Defaults to None.
            camera (bool, optional): カメラで用いる座標系の場合, True. Defaults to None.
        """
        tmpDict:Dict[str, float] = self.tfConfig.pop(self.frameId, None)

        if tmpDict is None:
            tmp_x = self.translation[0] if x is None else x
            tmp_y = -self.translation[1] if y is None else y
            tmp_z = self.translation[2] if z is None else z
            tmp_quot:Rotation = Rotation.from_quat(self.quaternion)
            tmp_rpy = tmp_quot.as_euler('xyz', degrees=True)
            tmp_roll = tmp_rpy[0] if roll is None else roll
            tmp_pitch = -tmp_rpy[1] if pitch is None else pitch
            tmp_yaw = -tmp_rpy[2] if yaw is None else yaw
            tmp_camera = self.camera if camera is None else camera

            tmpDict = {'x': tmp_x, 'y': tmp_y, 'z': tmp_z, 'roll': tmp_roll, 'pitch': tmp_pitch, 'yaw': tmp_yaw, 'camera': tmp_camera}
        else:
            if isinstance(x, float): tmpDict['x'] = x
            if isinstance(y, float): tmpDict['y'] = y
            if isinstance(z, float): tmpDict['z'] = z
            if isinstance(roll, float): tmpDict['roll'] = roll
            if isinstance(pitch, float): tmpDict['pitch'] = pitch
            if isinstance(yaw, float): tmpDict['yaw'] = yaw
            if isinstance(camera, bool): tmpDict['camera'] = camera
            tmp_x = tmpDict['x']
            tmp_y = tmpDict['y']
            tmp_z = tmpDict['z']
            tmp_roll = tmpDict['roll']
            tmp_pitch = tmpDict['pitch']
            tmp_yaw = tmpDict['yaw']
            tmp_camera = tmpDict['camera']

        if frame_id != '':
            self.frameId = frame_id
        self.tfConfig[self.frameId] = tmpDict

        self.translation[:] = [tmp_x, -tmp_y, tmp_z]
        quat:Rotation = Rotation.from_euler('xyz', [tmp_roll, -tmp_pitch, -tmp_yaw], degrees=True)
        if tmp_camera is True:
            camera_rot:Rotation = Rotation.from_euler('zyx', [0., 90., -90.], degrees=True)
            quat_data = quat * camera_rot
        else:
            quat_data = quat
        self.quaternion[:] = quat_data.as_quat()

        axisLines:np.ndarray = AXIS_POS * AXIS_SCALE
        if self.carla is True:
            axisLines *= [1., -1., 1.]
            self.axisItem.setData(pos=quat.apply(axisLines)+self.translation, color=AXIS_COLOR, mode='lines')
            self.textItem.setData(pos=self.translation, text=self.frameId)
        else:
            self.axisItem.setData(pos=quat_data.apply(axisLines)+self.translation, color=AXIS_COLOR, mode='lines')
            self.textItem.setData(pos=self.translation, text=self.frameId)

    def setMode(self, carla:bool) -> None:
        """setMode

        描画時のモードを設定する

        Args:
            carla (bool): CARLAの座標系で表示する場合, True
        """
        self.carla = carla
        self.setData()

    def addAxisItem(self, widget:GLViewWidget, frame_id:str='', x:float=None, y:float=None, z:float=None, roll:float=None, pitch:float=None, yaw:float=None, camera:bool=None) -> None:
        """addAxisItem

        指定したWidgetにAxisItemを追加する

        Args:
            widget (GLViewWidget): AxisItemを追加するWidget
            frame_id (str, optional): 座標系のID. Defaults to ''.
            x (float, optional): CARLAの'spawn_point'の'x'の値. Defaults to None.
            y (float, optional): CARLAの'spawn_point'の'y'の値. Defaults to None.
            z (float, optional): CARLAの'spawn_point'の'z'の値. Defaults to None.
            roll (float, optional): CARLAの'spawn_point'の'roll'の値. Defaults to None.
            pitch (float, optional): CARLAの'spawn_point'の'pitch'の値. Defaults to None.
            yaw (float, optional): CARLAの'spawn_point'の'yaw'の値. Defaults to None.
            camera (bool, optional): カメラで用いる座標系の場合, True. Defaults to None.
        """
        self.setData(frame_id, x, y, z, roll, pitch, yaw, camera)
        widget.addItem(self.axisItem)
        widget.addItem(self.textItem)
    
    def removeAxisItem(self, widget:GLViewWidget) -> None:
        """removeAxisItem

        指定したWidgetからAxisItemを除去する

        Args:
            widget (GLViewWidget): AxisItemを除去するWidget
        """
        self.tfConfig.pop(self.frameId, None)
        self.frameId = ''
        widget.removeItem(self.axisItem)
        widget.removeItem(self.textItem)

class SensorTransformDialog(QDialog):
    def __init__(self) -> None:
        """__init__

        コンストラクタ
        """
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.tfViewWidget = GLViewWidget(self)
        self.tfViewWidget.setFixedSize(300, 240)
        self.ui.viewLayout.addWidget(self.tfViewWidget)

        self.tfGridItem = GLGridItem()
        self.tfGridItem.setSize(5, 5)
        self.tfGridItem.setSpacing(0.2, 0.2)
        self.tfViewWidget.addItem(self.tfGridItem)

        self.baselink = AxisItem()
        self.baselink.addAxisItem(self.tfViewWidget, 'baselink', 0., 0., 0., 0., 0., 0., False)

        self.targetlink = AxisItem()
        self.targetlink.addAxisItem(self.tfViewWidget)

        self.ui.frameIdLineEdit.textChanged.connect(lambda: self.__valueUpdate_callback())
        self.ui.xDoubleSpinBox.valueChanged.connect(lambda: self.__valueUpdate_callback())
        self.ui.yDoubleSpinBox.valueChanged.connect(lambda: self.__valueUpdate_callback())
        self.ui.zDoubleSpinBox.valueChanged.connect(lambda: self.__valueUpdate_callback())
        self.ui.rollDoubleSpinBox.valueChanged.connect(lambda: self.__valueUpdate_callback())
        self.ui.pitchDoubleSpinBox.valueChanged.connect(lambda: self.__valueUpdate_callback())
        self.ui.yawDoubleSpinBox.valueChanged.connect(lambda: self.__valueUpdate_callback())
        self.ui.cameraCheckBox.stateChanged.connect(lambda: self.__valueUpdate_callback())
        self.ui.carlaRadioButton.toggled.connect(lambda: self.__carlaMode_callback())
        self.ui.hdf5RadioButton.toggled.connect(lambda: self.__hdf5Mode_callback())
        self.ui.cancelButton.clicked.connect(lambda: self.close())
    
    def setData(self, frame_id:str, x:float, y:float, z:float, roll:float, pitch:float, yaw:float, camera:bool):
        """setData

        Dialogに値を格納する

        Args:
            frame_id (str): 座標系のID
            x (float): CARLAの'spawn_point'の'x'の値
            y (float): CARLAの'spawn_point'の'y'の値
            z (float): CARLAの'spawn_point'の'z'の値
            roll (float): CARLAの'spawn_point'の'roll'の値
            pitch (float): CARLAの'spawn_point'の'pitch'の値
            yaw (float): CARLAの'spawn_point'の'yaw'の値
            camera (bool): カメラで用いる座標系の場合, True
        """
        self.ui.frameIdLineEdit.setText(frame_id)
        self.ui.xDoubleSpinBox.setValue(x)
        self.ui.yDoubleSpinBox.setValue(y)
        self.ui.zDoubleSpinBox.setValue(z)
        self.ui.rollDoubleSpinBox.setValue(roll)
        self.ui.pitchDoubleSpinBox.setValue(pitch)
        self.ui.yawDoubleSpinBox.setValue(yaw)
        self.ui.cameraCheckBox.setChecked(camera)
        self.__valueUpdate_callback()
    
    def resetData(self) -> None:
        """resetData

        Dialogの表示を初期化する
        """
        self.setData('', 0., 0., 0., 0., 0., 0., False)
    
    def __carlaMode_callback(self):
        self.baselink.setMode(True)
        self.targetlink.setMode(True)
    
    def __hdf5Mode_callback(self):
        self.baselink.setMode(False)
        self.targetlink.setMode(False)

    def __valueUpdate_callback(self):
        frame_id = self.ui.frameIdLineEdit.text()
        x = self.ui.xDoubleSpinBox.value()
        y = self.ui.yDoubleSpinBox.value()
        z = self.ui.zDoubleSpinBox.value()
        roll = self.ui.rollDoubleSpinBox.value()
        pitch = self.ui.pitchDoubleSpinBox.value()
        yaw = self.ui.yawDoubleSpinBox.value()
        camera = self.ui.cameraCheckBox.isChecked()
        
        self.targetlink.setData(frame_id, x, y, z, roll, pitch, yaw, camera)

class SensorTransformWidget(QWidget):
    def __init__(self, tfConfig:Dict[str, Dict[str, List[float]]], parent:QWidget=None) -> None:
        """__init__

        コンストラクタ

        Args:
            tfConfig (Dict[str, Dict[str, List[float]]]): TFの設定を格納する辞書
            parent (QWidget, optional): 親のWidget. Defaults to None.
        """
        super().__init__(parent=parent)
        self.ui = Ui_SensorTransform()
        self.ui.setupUi(self)
        self.tfconfig = tfConfig
        self.axisItemDict:Dict[str, AxisItem] = {}

        self.dialog = SensorTransformDialog()

        self.tfViewWidget = GLViewWidget(self)
        self.tfViewWidget.setFixedSize(280, 280)
        self.ui.viewLayout.addWidget(self.tfViewWidget)

        self.tfGridItem = GLGridItem()
        self.tfGridItem.setSize(5, 5)
        self.tfGridItem.setSpacing(0.2, 0.2)
        self.tfViewWidget.addItem(self.tfGridItem)

        self.baselink = AxisItem()
        self.baselink.addAxisItem(self.tfViewWidget, 'baselink', 0., 0., 0., 0., 0., 0.)

        self.edit = ''
        for frame_id, values in self.tfconfig.items():
            self.__editItem(frame_id, values['x'], values['y'], values['z'], values['roll'], values['pitch'], values['yaw'], values['camera'])

        self.ui.addButton.clicked.connect(lambda: self.__addButton_callback())
        self.ui.removeButton.clicked.connect(lambda: self.__removeButton_callback())
        self.ui.carlaRadioButton.toggled.connect(lambda: self.__carlaMode_callback())
        self.ui.hdf5RadioButton.toggled.connect(lambda: self.__hdf5Mode_callback())
        self.ui.transformTree.itemDoubleClicked.connect(self.__itemDoubleClicked_callback)
        self.dialog.ui.okButton.clicked.connect(lambda: self.__dialogOkButton_callback())
    
    def __addButton_callback(self) -> None:
        self.edit:str = ''
        self.dialog.resetData()
        self.dialog.exec_()
    
    def __itemDoubleClicked_callback(self, item:QTreeWidgetItem, column:int) -> None:
        frame_id = item.text(0)
        self.edit = frame_id
        values = self.tfconfig[frame_id]
        self.dialog.setData(frame_id, values['x'], values['y'], values['z'], values['roll'], values['pitch'], values['yaw'], values['camera'])
        self.dialog.exec_()
    
    def __removeButton_callback(self) -> None:
        item = self.ui.transformTree.currentItem()
        if item is None: return
        idx = self.ui.transformTree.indexOfTopLevelItem(item)
        item = self.ui.transformTree.takeTopLevelItem(idx)
        frame_id = item.text(0)
        axis = self.axisItemDict.pop(frame_id)
        axis.removeAxisItem(self.tfViewWidget)
        # print(self.tfconfig)
    
    def __dialogOkButton_callback(self) -> None:
        frame_id = self.dialog.ui.frameIdLineEdit.text()
        if frame_id == '': return
        if self.edit == '' and frame_id in self.tfconfig.keys(): return
        x = self.dialog.ui.xDoubleSpinBox.value()
        y = self.dialog.ui.yDoubleSpinBox.value()
        z = self.dialog.ui.zDoubleSpinBox.value()
        roll = self.dialog.ui.rollDoubleSpinBox.value()
        pitch = self.dialog.ui.pitchDoubleSpinBox.value()
        yaw = self.dialog.ui.yawDoubleSpinBox.value()
        camera = self.dialog.ui.cameraCheckBox.isChecked()

        self.__editItem(frame_id, x, y, z, roll, pitch, yaw, camera)

        self.dialog.close()
        # print(self.tfconfig)

    def __carlaMode_callback(self):
        self.baselink.setMode(True)
        for value in self.axisItemDict.values():
            value.setMode(True)
    
    def __hdf5Mode_callback(self):
        self.baselink.setMode(False)
        for value in self.axisItemDict.values():
            value.setMode(False)

    def __editItem(self, frame_id:str, x:float, y:float, z:float, roll:float, pitch:float, yaw:float, camera:bool) -> None:
        axis_item = self.axisItemDict.pop(self.edit, None)
        if axis_item is None:
            axis_item = AxisItem(self.tfconfig)
            axis_item.addAxisItem(self.tfViewWidget, frame_id, x, y, z, roll, pitch, yaw, camera)
            self.axisItemDict[frame_id] = axis_item

            tree_item = QTreeWidgetItem([frame_id, f'[{x:.3f}, {y:.3f}, {z:.3f}]', f'[{roll:.1f}, {pitch:.1f}, {yaw:.1f}]'])
            self.ui.transformTree.addTopLevelItem(tree_item)
        else:
            axis_item.setData(frame_id, x, y, z, roll, pitch, yaw, camera)
            self.axisItemDict[frame_id] = axis_item

            tree_item = self.ui.transformTree.currentItem()
            tree_item.setText(0, frame_id)
            tree_item.setText(1, f'[{x:.3f}, {y:.3f}, {z:.3f}]')
            tree_item.setText(2, f'[{roll:.1f}, {pitch:.1f}, {yaw:.1f}]')
            self.ui.transformTree.addTopLevelItem(tree_item)
        # print(axis_item.translation, axis_item.quaternion)

