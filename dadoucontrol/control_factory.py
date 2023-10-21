import logging
import logging.config
import time
import platform

from dadou_utils.com.message import Message
from dadou_utils.com.serial_devices_manager import SerialDeviceManager
from dadou_utils.logging_conf import LoggingConf
from dadou_utils.misc import Misc
from dadou_utils.utils_static import BASE_PATH, LOGGING_CONFIG_FILE, DEVICES, JSON_DIRECTORY, WS_CLIENT, \
    LOGGING_FILE_NAME, INPUT_KEY, SLIDERS, NAME, LOG_FILE, BUTTON, MSG, ALL, JOYSTICK

from dadou_utils.com.ws_client import WsClient
from dadou_utils.singleton import SingletonMeta

from dadoucontrol.audio.audio_navigation import AudioNav
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
        #logging.config.dictConfig(LoggingConf.get(config[LOGGING_FILE_NAME], "main"))
        logging.config.fileConfig(config[LOGGING_CONFIG_FILE], disable_existing_loggers=False)

        self.control_json_manager = ControlJsonManager() 

        self.audio_nav = AudioNav()
        self.sequence_management = SequencesManagement(self.control_json_manager)
        self.devices_manager = SerialDeviceManager(config[DEVICES])

        #wait for network
        if not Misc.internet_connected():
            logging.error("no network waiting")
            time.sleep(1)

        ws_devices_conf = config[WS_CLIENTS][ALL]
        device = platform.uname()[1]
        if device in config[WS_CLIENTS]:
            logging.info("ws devices conf {}".format(device))
            ws_devices_conf = config[WS_CLIENTS][device]

        self.ws_clients = []
        for key, value in ws_devices_conf.items():
            self.ws_clients.append(WsClient(value, config[WS_PORT], key))

        self.message = Message(self.ws_clients, self.devices_manager)

    def ws_device_connected(self, device):
        connected = False
        for ws_client in self.ws_clients:
            if ws_client.name == device and ws_client.activ:
                connected = True
        return connected
