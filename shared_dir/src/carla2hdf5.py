import os
import sys
import json
import random
import math
from typing import Any, List, NamedTuple, Optional
from glob import glob
from pprint import pprint
from queue import Queue, Empty, Full

import numpy
from PySide2.QtCore import QObject, QTimer, Qt, QThread, Signal, Slot
from PySide2.QtGui import QColor, QImage, QPixmap, QTextCursor
from PySide2.QtWidgets import QApplication, QFileDialog, QLabel, QMainWindow, QTreeWidgetItem
from transforms3d.euler import euler2quat

try:
    sys.path.append(glob('../opt/carla/PythonAPI/carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla
from carla import ColorConverter as cc
from carla import VehicleLightState as vls
from h5datacreator import *

from SensorTransformWidget import SensorTransformWidget
from ui import Ui_MainWindow

class Carla2HDF5(QMainWindow):
    def __init__(self, parent=None) -> None:
        super(Carla2HDF5, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.add_queue_pushButton.setEnabled(False)

        self._timer = QTimer()
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._play_spinner)

        self.weather_dict: Dict[str, Any] = {
            'ClearNoon': carla.WeatherParameters.ClearNoon,
            'CloudyNoon': carla.WeatherParameters.CloudyNoon,
            'WetNoon': carla.WeatherParameters.WetNoon,
            'WetCloudyNoon': carla.WeatherParameters.WetCloudyNoon,
            'SoftRainNoon': carla.WeatherParameters.SoftRainNoon,
            'MidRainyNoon': carla.WeatherParameters.MidRainyNoon,
            'HardRainNoon': carla.WeatherParameters.HardRainNoon,
            'ClearSunset': carla.WeatherParameters.ClearSunset,
            'CloudySunset': carla.WeatherParameters.CloudySunset,
            'WetSunset': carla.WeatherParameters.WetSunset,
            'WetCloudySunset': carla.WeatherParameters.WetCloudySunset,
            'SoftRainSunset': carla.WeatherParameters.SoftRainSunset,
            'MidRainSunset': carla.WeatherParameters.MidRainSunset,
            'HardRainSunset': carla.WeatherParameters.HardRainSunset,
        }

        # Initial settings
        self.ip_address: str = None
        self.port: int = None

        # Main settings
        self.map_name: str = None
        self.weather: str = None

        self.seed: int = None
        self.num_frames: int = None

        self.num_npc_vehicles: int = None
        self.safe_spawn: bool = None

        self.num_npc_walkers: int = None
        self.running_walker_pct: float = None
        self.road_crossing_walker_pct: float = None

        self.global_distance: float = None
        self.use_hybrid_physics: bool = None
        self.hybrid_physics_radius: float = None
        self.use_super_hero: bool = None

        # carla related vars
        self.client = None
        self.world = None
        self.traffic_manager = None
        self.traffic_manager_port: int = 8000
        self.carla_server_version: str = None
        self.carla_client_version: str = None
        self.carla_available_maps: List[str] = None
        self.carla_weather_list: List[str] = list(self.weather_dict.keys())
        self.hero_actor_list: List[Any] = []
        self.npc_vehicle_list: List[Any] = []
        self.npc_walker_controller_list: List[Any] = []
        self.all_walker_actors: List[Any] = []

        # HDF5 related vars
        self.h5file: h5py.Dataset = None
        self.save_path: str = None

        # Queue realted vars
        self.is_looping: bool = False
        self.queued_idx: int = 0
        self.queued_settings: Dict[str, Union[int, float, str, bool]] = {}

        # Some hidden settigs
        self.hero_vehicle_filter: str = 'vehicle.*'
        self.num_warmup_frames: int = 15
        self.save_path: str = None

        # Some defalut paths
        self.label_config_path: str = '/workspace/config/label-0.9.11.json'
        self.objects_definitions_path: str = '/workspace/config/objects.json'
        if os.path.exists(self.objects_definitions_path):
            with open(self.objects_definitions_path) as handle:
                self.objects_definitions: dict = json.loads(handle.read())
        else:
            self.objects_definitions = {'transforms': {}}

        self.sensor_transform_config_widget = SensorTransformWidget(self.objects_definitions['transforms'])
        self.ui.tf_verticalLayout.addWidget(self.sensor_transform_config_widget)
        
        # Connect callback finctions
        self.ui.connect_pushButton.clicked.connect(self._timer.start)
        self.ui.connect_pushButton.clicked.connect(lambda: self._connect_btn_callback())
        self.ui.add_queue_pushButton.clicked.connect(lambda: self._add_queue_btn_callback())

        self.processing = Processing(self)

    def _connect_btn_callback(self) -> None:
        # Disable to push connect btn
        self.ui.connect_pushButton.setEnabled(False)

        # Get information to run carla server
        self.ip_address = self.ui.ip_address_lineEdit.text()
        self.port = self.ui.port_spinBox.value()

        # Invoker carla client
        self.client = carla.Client(self.ip_address, self.port)
        self.client.set_timeout(5.0)

        # Get carla server and client version
        self.carla_server_version = self.client.get_server_version()
        self.carla_client_version = self.client.get_client_version()

        if self.carla_server_version != self.carla_client_version:
            raise RuntimeError(f'CARLA version mismatch. Server: {self.carla_server_version} <---> Client: {self.carla_client_version}')

        # Get available maps
        self.carla_available_maps = [map.split('/')[-1] for map in sorted(self.client.get_available_maps())]

        # Set available maps to `map_comboBox`
        self.ui.map_comboBox.addItems(self.carla_available_maps)

        # Set available weather to `weather_comboBox`
        self.ui.weather_comboBox.addItems(self.carla_weather_list)
        
        # Enable to bush add queue btn
        self.ui.add_queue_pushButton.setEnabled(True)
    
    def _add_queue_btn_callback(self) -> None:
        settings: Dict[str, Union[int, float, str, bool]] = {
            'MAP': self.ui.map_comboBox.currentText(),
            'WEATHER': self.ui.weather_comboBox.currentText(),
            'SEED': self.ui.seed_spinBox.value(),
            'NUM_FRAMES': self.ui.num_frames_spinBox.value(),
            'NUM_NPC_VEHICLES': self.ui.num_npc_vehicles_spinBox.value(),
            'SAFE_SPAWN': self.ui.safe_spawn_checkBox.isChecked(),
            'NUM_NPC_WALKERS': self.ui.num_npc_walkers_spinBox.value(),
            'RUNNING_WALKER_PCT': self.ui.running_walker_doubleSpinBox.value(),
            'CROSSING_WALKER_PCT': self.ui.road_crossing_walker_doubleSpinBox.value(),
            'GLOBAL_DISTANCES': self.ui.global_distance_doubleSpinBox.value(),
            'HYBRID_PHYSICS': self.ui.hybrid_physics_checkBox.isChecked(),
            'HYBRID_PHYSICS_RADIUS': self.ui.hybrid_physics_radius_doubleSpinBox.value(),
            'SUPER_HERO': self.ui.super_hero_checkBox.isChecked(),
        }
        items: QTreeWidgetItem = QTreeWidgetItem([f"{settings['MAP']}", f"{settings['WEATHER']}", f"{settings['SEED']}", f"{settings['NUM_FRAMES']}", f"Queued"])
        self.ui.queue_treeWidget.addTopLevelItem(items)
        self.queued_idx += 1
        settings['QITEMS'] = items
        self.queued_settings[f'{self.queued_idx}'] = settings

    def _play_spinner(self) -> None:
        # print(f'is_looping: {self.is_looping}')
        # print(f'queued_idx            : {self.queued_idx}')
        # print(f'queued_settings.keys(): {list(self.queued_settings.keys())}')
        
        if self.is_looping:
            return
        if str(self.queued_idx) not in self.queued_settings.keys():
            return
        
        self.sensor_transform_config_widget.hide()
        self.processing.start()
    
    def game_loop(self) -> None:
        self.is_looping = True
        queued_idxs: List[str] = list(self.queued_settings.keys())
        if len(queued_idxs) < 1:
            return
        settings: Dict[str, Union[int, float, str, bool]] = self.queued_settings[f'{queued_idxs[0]}']
        qitems: QTreeWidgetItem = settings['QITEMS']
        qitems.setText(4, 'Initializing...')

        random.seed(settings['SEED'])

        if os.path.isdir('/workspace/hdf5'):
            self.save_path = f"/workspace/hdf5/{settings['MAP']}_{settings['WEATHER']}_{settings['SEED']}_{settings['NUM_FRAMES']}.h5"
        else:
            self.save_path = f"./{settings['MAP']}_{settings['WEATHER']}_{settings['SEED']}_{settings['NUM_FRAMES']}.h5"

        self.h5file = H5Dataset(self.save_path, 'w')

        label_group: h5py.Group = self.h5file.get_label_group(f'carla-{self.carla_client_version}')
        with open(self.label_config_path, 'r') as f:
            label_config: dict = json.load(f)
            for key, value in label_config.items():
                set_label_config(label_group, int(key), value[H5_KEY_NAME], value['r'], value['g'], value['b'])
        
        transforms_group: h5py.Group = self.h5file.get_common_group('tf_static')
        for key, value in self.sensor_transform_config_widget.axisItemDict.items():
            set_pose(transforms_group, f'hero2{key}', value.translation, value.quaternion, f'hero', f'{key}', 0, 0)
        
        try:
            original_world_settings: Any = self._apply_world_settings(settings)

            blueprint_library = self.world.get_blueprint_library()
            spawn_points = self.world.get_map().get_spawn_points()

            bp_hero = random.choice(blueprint_library.filter(self.hero_vehicle_filter))
            bp_hero.set_attribute('role_name', 'hero')
            if bp_hero.has_attribute('color'):
                color = random.choice(bp_hero.get_attribute('color').recommended_values)
                bp_hero.set_attribute('color', color)
            hero_vehicle = self.world.spawn_actor(bp_hero, random.choice(spawn_points))
            self.hero_actor_list.append(hero_vehicle)

            sensors_dicts: Dict[str, Any] = {}
            intrinsic_group: h5py.Group = self.h5file.get_common_group('intrinsic')
            sensors_dicts = self._get_sensor_attribute(sensors_dicts, blueprint_library, intrinsic_group, hero_vehicle)

            hero_vehicle.set_autopilot(True)

            for _ in range(self.num_warmup_frames):
                self.world.tick()

            if settings['NUM_NPC_VEHICLES'] > 0:
                self._spawn_npc_vehicle(settings, spawn_points)
            
            if settings['NUM_NPC_WALKERS'] > 0:
                self._spawn_npc_walker(settings)

            try:
                for _, sensors_dict in sensors_dicts.items():
                    _ = sensors_dict['queue'].get(block=True, timeout=1.)
            except Empty:
                pass

            current_frame: int = 0
            while self.is_looping and current_frame < settings['NUM_FRAMES']:
                data_group: h5py.Group = self.h5file.get_next_data_group()
                world_frame: int = self.world.tick()

                if settings['SUPER_HERO']:
                    if hero_vehicle.is_at_traffic_light():
                        traffic_light = hero_vehicle.get_traffic_light()
                        if traffic_light.get_state() == carla.TrafficLightState.Red:
                            traffic_light.set_state(carla.TrafficLightState.Green)

                sensor_data_list: List[Any] = []
                try:
                    for _, sensors_dict in sensors_dicts.items():
                        sensor_data_list.append([sensors_dict['name'], self._retrieve_data(sensors_dict['queue'], world_frame)])
                except Empty:
                    pass
                else:
                    for idx in range(len(sensors_dicts)):
                        sensor_name, sensor_data = sensor_data_list[idx]
                        sensor_type = sensor_name.split('-')[0].split('.')[-1]
                        stamp_nsec, stamp_sec = math.modf(sensor_data.timestamp)
                        if sensor_type == 'ray_cast':
                            set_points(data_group, f'{sensor_name}', sensor_data.data, 'hero', int(stamp_sec), int(stamp_nsec), settings['MAP'])
                        elif sensor_type == 'ray_cast_semantic':
                            set_semantic3d(data_group, f'{sensor_name}', sensor_data.data[0], sensor_data.data[1], 'hero', f'carla-{self.carla_client_version}', int(stamp_sec), int(stamp_nsec), settings['MAP'])
                        elif sensor_type == 'rgb':
                            set_bgr8(data_group, f'{sensor_name}', sensor_data.data, 'hero', int(stamp_sec), int(stamp_nsec))
                        elif sensor_type == 'depth':
                            set_depth(data_group, f'{sensor_name}', sensor_data.data, 'hero', int(stamp_sec), int(stamp_nsec))
                        elif sensor_type == 'semantic_segmentation':
                            set_semantic2d(data_group, f'{sensor_name}', sensor_data.data, 'hero', f'carla-{self.carla_client_version}', int(stamp_sec), int(stamp_nsec))
                        else:
                            raise NotImplementedError
                    
                    location, rotation = self._convert_transform(hero_vehicle.get_transform())
                    set_pose(data_group, 'map2hero', location, rotation, 'map', 'hero', int(stamp_sec), int(stamp_nsec))
                    current_frame += 1
                    qitems.setText(4, f"Processing... ({100*current_frame/settings['NUM_FRAMES']:5.1f} %)")
    
        finally:
            self.world.apply_settings(original_world_settings)
            for _, sensors_dict in sensors_dicts.items():
                sensors_dict['actor'].destroy()
            self.client.apply_batch([carla.command.DestroyActor(x) for x in self.hero_actor_list])
            self.client.apply_batch([carla.command.DestroyActor(x) for x in self.npc_vehicle_list])
            for i in range(0, len(self.npc_walker_controller_list), 2):
                self.all_walker_actors[i].stop()
            self.client.apply_batch([carla.command.DestroyActor(x) for x in self.npc_walker_controller_list])
            self.hero_actor_list.clear()
            self.npc_vehicle_list.clear()
            self.npc_walker_controller_list.clear()
            try:
                self.h5file.close()
            except ValueError:
                pass
            del settings['QITEMS']
            with open(f'{self.save_path}.json', 'w') as f:
                json.dump(self.queued_settings[f'{queued_idxs[0]}'], f, indent=4, ensure_ascii=False, skipkeys=True)
            del self.queued_settings[f'{queued_idxs[0]}']
            self.is_looping = False
            qitems.setText(4, f"Done")
        
    def _convert_transform(self, transform: Any) -> numpy.ndarray:
        left_location = transform.location
        right_location: numpy.ndarray = numpy.array([left_location.x, -left_location.y, left_location.z], dtype=numpy.float32)

        left_rotation = transform.rotation
        roll: float = math.radians(left_rotation.roll)
        pitch: float = -math.radians(left_rotation.pitch)
        yaw: float = -math.radians(left_rotation.yaw)
        qw, qx, qy, qz = euler2quat(roll, pitch, yaw)
        right_rotation: numpy.ndarray = numpy.array([qx, qy, qz, qw], dtype=numpy.float32)

        return (right_location, right_rotation)
    
    def _retrieve_data(self, sensor_queue: Queue, world_frame: int) -> Any:
        while True:
            data = sensor_queue.get(timeout=1.)
            if data.frame == world_frame:
                return data
    
    def _apply_world_settings(self, settings: Dict[str, Union[int, float, str, bool]]) -> Any:
        self.client.load_world(settings['MAP'])
        self.client.set_timeout(10.0)

        self.world = self.client.get_world()
        self.world.set_weather(self.weather_dict[settings['WEATHER']])

        self.traffic_manager = self.client.get_trafficmanager(self.traffic_manager_port)
        self.traffic_manager.set_global_distance_to_leading_vehicle(settings['GLOBAL_DISTANCES'])
        self.traffic_manager.set_synchronous_mode(True)
        self.traffic_manager.set_hybrid_physics_mode(settings['HYBRID_PHYSICS'])
        self.traffic_manager.set_hybrid_physics_radius(settings['HYBRID_PHYSICS_RADIUS'])
        self.traffic_manager.set_random_device_seed(settings['SEED'])
        self.traffic_manager.global_percentage_speed_difference(-10.)

        original_world_settings = self.world.get_settings()
        world_settings = self.world.get_settings()
        world_settings.fixed_delta_seconds = 0.1
        world_settings.synchronous_mode = True
        world_settings.deterministic_ragdolls = True
        world_settings.no_rendering_mode = True
        self.world.apply_settings(world_settings)

        return original_world_settings
    
    def _get_sensor_attribute(self, sensors_dicts: Dict[str, Any], bp_library: Any, intrinsic_group: h5py.Group, vehicle: Any) -> Dict[str, Any]:
        for sensor_definitions in self.objects_definitions["sensors"]:
            sensor_type: str = sensor_definitions['type']
            sensor_id: str = sensor_definitions['id']
            bp = bp_library.find(sensor_type)
            for key, value in sensor_definitions.items():
                if key == 'type' or key == 'id': break
                try:
                    bp.set_attribute(key, str(value))
                except IndexError:
                    raise RuntimeError(f'No such attribute: {key} in Objects Definition File')
            
            for key, value in self.objects_definitions["transforms"].items():
                if key == f'{sensor_id}':                    
                    transform = carla.Transform(carla.Location(x=value['x'], y=value['y'], z=value['z']), 
                                                carla.Rotation(roll=value['roll'], pitch=value['pitch'], yaw=value['yaw']))
            if sensor_type.split('.')[1] == 'camera':
                width: int = bp.get_attribute('image_size_x').as_int()
                height: int = bp.get_attribute('image_size_y').as_int()
                cx: float = width / 2.0
                cy: float = height / 2.0
                f: float = width / (2.0 * numpy.tan(bp.get_attribute('fov').as_float() * numpy.pi / 360.0))
                set_intrinsic(intrinsic_group, f'{sensor_type}-{sensor_id}', f, f, cx, cy, height, width, sensor_id)
            sensor_queue: Queue = Queue()
            sensor_actor = self.world.spawn_actor(bp, transform, attach_to=vehicle)
            sensor_actor.listen(lambda data, sq=sensor_queue, st=sensor_type: self._sensor_callback(data, st, sq))
            sensor_dicts: Dict[str, Any] = {
                    'name': f'{sensor_type}-{sensor_id}',
                    'queue': sensor_queue,
                    'actor': sensor_actor,
                    'blueprint': bp,
                    'transform': transform
            }
            sensors_dicts[f'{sensor_type}-{sensor_id}'] = sensor_dicts
        return sensors_dicts

    def _sensor_callback(self, sensor_data: Any, sensor_type: str, sensor_queue: Queue):
        if isinstance(sensor_data, carla.Image):
            if sensor_type.split('.')[-1] == 'rgb':
                sensor_data.convert(cc.Raw)
                array: numpy.ndarray = numpy.frombuffer(sensor_data.raw_data, dtype=numpy.dtype("uint8"))
                array = numpy.reshape(array, (sensor_data.height, sensor_data.width, 4))
                try:
                    sensor_queue.put(SensorContainer(sensor_data.timestamp, sensor_data.frame, numpy.copy(array[:, :, :3])), block=True, timeout=1.)
                except Full:
                    pass
            elif sensor_type.split('.')[-1] == 'semantic_segmentation':
                sensor_data.convert(cc.Raw)
                array: numpy.ndarray = numpy.frombuffer(sensor_data.raw_data, dtype=numpy.dtype("uint8"))
                array = numpy.reshape(array, (sensor_data.height, sensor_data.width, 4))
                try:
                    sensor_queue.put(SensorContainer(sensor_data.timestamp, sensor_data.frame, array[:,:,2]), block=True, timeout=1.)
                except Full:
                    pass
            elif sensor_type.split('.')[-1] == 'depth':
                bgra_image: numpy.ndarray = numpy.ndarray(shape=(sensor_data.height, sensor_data.width, 4), dtype=numpy.uint8, buffer=sensor_data.raw_data)
                array: numpy.ndarray = (numpy.float32(bgra_image[:, :, 2]) + numpy.float32(bgra_image[:, :, 1]) * 256. + numpy.float32(bgra_image[:, :, 0]) * 256. * 256.) / (256. * 256. * 256. - 1.) * 1000.
                try:
                    sensor_queue.put(SensorContainer(sensor_data.timestamp, sensor_data.frame, array.astype(numpy.float32)), block=True, timeout=1.)
                except Full:
                    pass
        elif isinstance(sensor_data, carla.LidarMeasurement):
            points: numpy.ndarray = numpy.frombuffer(sensor_data.raw_data, dtype=numpy.dtype(numpy.float32))
            points = numpy.reshape(points, (-1, 4))[:, 0:3]
            po1nts = numpy.copy(points)
            po1nts[:, 1] *= -1.
            try:
                sensor_queue.put(SensorContainer(sensor_data.timestamp, sensor_data.frame, po1nts), block=True, timeout=1.)
            except Full:
                pass
        elif isinstance(sensor_data, carla.SemanticLidarMeasurement):
            raw_points: numpy.ndarray = numpy.frombuffer(
                sensor_data.raw_data, 
                dtype=numpy.dtype([('x', numpy.float32), ('y', numpy.float32), ('z', numpy.float32), ('CosAngle', numpy.float32), ('ObjIdx', numpy.uint32), ('ObjTag', numpy.uint32)])
            )
            points: numpy.ndarray = numpy.stack([raw_points['x'], raw_points['y'], raw_points['z']], axis=1)
            po1nts = numpy.copy(points)
            po1nts[:, 1] *= -1.
            semantic1d: numpy.ndarray = numpy.uint8(raw_points['ObjTag'])
            try:
                sensor_queue.put(SensorContainer(sensor_data.timestamp, sensor_data.frame, (po1nts, semantic1d)), block=True, timeout=1.)
            except Full:
                pass
        else:
            raise NotImplementedError
    
    def _spawn_npc_vehicle(self, settings: Dict[str, Union[int, float, str, bool]], spawn_points: Any) -> None:
        bps = self.world.get_blueprint_library().filter('vehicle.*')
        if settings['SAFE_SPAWN']:
            bps = [x for x in bps if int(x.get_attribute('number_of_wheels')) == 4]
            bps = [x for x in bps if not x.id.endswith('isetta')]
            bps = [x for x in bps if not x.id.endswith('carlacola')]
            bps = [x for x in bps if not x.id.endswith('cybertruck')]
            bps = [x for x in bps if not x.id.endswith('t2')]

        num_spawn_points: int = len(spawn_points)
        if settings['NUM_NPC_VEHICLES'] < num_spawn_points:
            random.shuffle(spawn_points)
        elif settings['NUM_NPC_VEHICLES'] > num_spawn_points:
            settings['NUM_NPC_VEHICLES'] = num_spawn_points

        SpawnActor = carla.command.SpawnActor
        SetAutopilot = carla.command.SetAutopilot
        SetVehicleLightState = carla.command.SetVehicleLightState
        FutureActor = carla.command.FutureActor

        batch: List[Any] = []
        for n, transform in enumerate(spawn_points):
            if n >= settings['NUM_NPC_VEHICLES']:
                break
            bp = random.choice(bps)
            if bp.has_attribute('color'):
                color = random.choice(bp.get_attribute('color').recommended_values)
                bp.set_attribute('color', color)
            if bp.has_attribute('driver_id'):
                driver_id = random.choice(bp.get_attribute('driver_id').recommended_values)
                bp.set_attribute('driver_id', driver_id)
            bp.set_attribute('role_name', 'npc_vehicles')
            light_state = vls.Position | vls.LowBeam | vls.LowBeam
            batch.append(SpawnActor(bp, transform)
                        .then(SetAutopilot(FutureActor, True, self.traffic_manager.get_port()))
                        .then(SetVehicleLightState(FutureActor, light_state)))
        for response in self.client.apply_batch_sync(batch):
            if response.error:
                pass
            else:
                self.npc_vehicle_list.append(response.actor_id)
        for _ in range(self.num_warmup_frames):
            self.world.tick()
        
    def _spawn_npc_walker(self, settings: Dict[str, Union[int, float, str, bool]]) -> None:
        SpawnActor = carla.command.SpawnActor
        bps = self.world.get_blueprint_library().filter('walker.pedestrian.*')
        spawn_points: List[Any] = []
        for i in range(settings['NUM_NPC_WALKERS']):
            spawn_point = carla.Transform()
            loc = self.world.get_random_location_from_navigation()
            if loc is not None:
                spawn_point.location = loc
                spawn_points.append(spawn_point)
        batch: List[Any] = []
        walker_speed: List[Any] = []
        for spawn_point in spawn_points:
            bp = random.choice(bps)
            if bp.has_attribute('is_invincible'):
                bp.set_attribute('is_invincible', 'false')
            if bp.has_attribute('speed'):
                if (random.random() > settings['RUNNING_WALKER_PCT']):
                    walker_speed.append(bp.get_attribute('speed').recommended_values[1])
                else:
                    walker_speed.append(bp.get_attribute('speed').recommended_values[2])
            else:
                walker_speed.append(0.0)
            batch.append(SpawnActor(bp, spawn_point))
        results = self.client.apply_batch_sync(batch, True)
        temp_walker_speed: List[Any] = []
        npc_walker_list: List[Any] = []
        for i, result in enumerate(results):
            if result.error: pass
            else:
                npc_walker_list.append({"id": result.actor_id})
                temp_walker_speed.append(walker_speed[i])
        walker_speed = temp_walker_speed
        batch = []
        bp = self.world.get_blueprint_library().find('controller.ai.walker')
        for npc_walker in npc_walker_list:
            batch.append(SpawnActor(bp, carla.Transform(), npc_walker["id"]))
        results = self.client.apply_batch_sync(batch, True)

        for i, result in enumerate(results):
            if result.error: pass
            else: npc_walker_list[i]["con"] = result.actor_id
        for npc_walker in npc_walker_list:
            self.npc_walker_controller_list.append(npc_walker["con"])
            self.npc_walker_controller_list.append(npc_walker["id"])
        self.all_walker_actors = self.world.get_actors(self.npc_walker_controller_list)
        self.world.tick()
        self.world.set_pedestrians_cross_factor(settings['CROSSING_WALKER_PCT'])
        for i in range(0, len(self.npc_walker_controller_list), 2):
            self.all_walker_actors[i].start()
            self.all_walker_actors[i].go_to_location(self.world.get_random_location_from_navigation())
            self.all_walker_actors[i].set_max_speed(float(walker_speed[i//2]))
        for _ in range(self.num_warmup_frames):
            self.world.tick()

class Processing(QThread):
    def __init__(self, parent: Optional[QObject]) -> None:
        super().__init__(parent=parent)
    
    def run(self) -> None:
        self.parent().game_loop()
    
    def stop(self) -> None:
        self.terminate()

class SensorContainer(NamedTuple):
    timestamp: float
    frame: int
    data: numpy.ndarray

def main() -> None:
    app = QApplication(sys.argv)
    c2h = Carla2HDF5(app)
    c2h.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()