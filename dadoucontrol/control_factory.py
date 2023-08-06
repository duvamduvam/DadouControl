import logging
import logging.config
import time

from dadou_utils.logging_conf import LoggingConf
from dadou_utils.misc import Misc
from dadou_utils.utils_static import BASE_PATH, LOGGING_CONFIG_FILE, DEVICES, JSON_DIRECTORY, WS_CLIENT, \
    LOGGING_FILE_NAME, INPUT_KEY, SLIDERS, NAME, LOG_FILE

from dadou_utils.com.serial_devices_manager import SerialDeviceManager
from dadou_utils.com.ws_client import WsClient
from dadou_utils.singleton import SingletonMeta

from dadoucontrol.audio.audio_navigation import AudioNav
from dadoucontrol.com.robot_message import RobotMessage
from dadoucontrol.control_config import config
from dadoucontrol.files.control_json_manager import ControlJsonManager
from dadoucontrol.logic.sequences.sequences_manager import SequencesManagement

from dadou_utils.utils_static import WS_CLIENTS, WS_PORT


class ControlFactory(metaclass=SingletonMeta):

    def __init__(self):
        self.VisualMouth = None
        self.VisualEye = None

        print("config file {}".format(config[LOGGING_CONFIG_FILE]))
        #TODO improve process file name
        logging.config.dictConfig(LoggingConf.get(config[LOGGING_FILE_NAME], "main"))
        #logging.config.fileConfig(config[LOGGING_CONFIG_FILE], disable_existing_loggers=False)

        self.control_json_manager = ControlJsonManager()
        self.device_manager = SerialDeviceManager(config[DEVICES])
        self.input_key_devices = self.device_manager.get_device_type(INPUT_KEY)
        self.sliders = self.device_manager.get_device_type(SLIDERS)

        self.audio_nav = AudioNav()
        self.sequence_management = SequencesManagement(self.control_json_manager)

        #wait for network
        if not Misc.internet_connected():
            logging.error("no network waiting")
            time.sleep(1)

        self.ws_clients = []
        for key, value in config[WS_CLIENTS].items():
            self.ws_clients.append(WsClient(value, config[WS_PORT], key))

        self.message = RobotMessage(self.ws_clients, self.device_manager)

    def input_connected(self, type, name):
        connected = False
        for input_device in type:
            if name in input_device.name:
                connected = True
        return connected

    def device_connected(self, device):
        connected = False
        for ws_client in self.ws_clients:
            if ws_client.name == device and ws_client.activ:
                connected = True
        return connected

