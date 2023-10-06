import copy
import logging
import os
import socket

from dadou_utils.misc import Misc

from dadou_utils.utils_static import AUDIOS_DIRECTORY, BUTTON_GRID, EYES, RPI_TYPE, LAPTOP_TYPE, NAME, SERIAL_ID, \
    MSG_SIZE, TYPE, PATH, SEQUENCES, \
    MOUTH, VISUALS, VISUALS, LAPTOP_TYPE, RPI_TYPE, BASE_PATH, WS_CLIENT, JSON_EXPRESSIONS, JSON_LIGHTS, JSON_DIRECTORY, \
    SEQUENCES_DIRECTORY, AUDIO_NAME, AUDIO_PATH, DEVICES, PATHS, LOGGING_CONFIG_FILE, JSON_CONFIG, JSON_LIGHTS_BASE, \
    JSON_SPEECHS, PLAYLIST_PATH, GLOVE_LEFT, GLOVE_RIGHT, PROJECT_LIGHTS_DIRECTORY, \
    PLAYLIST_PLAY, PLAYLIST_STOP, PURPLE, BORDEAUX, YELLOW, ORANGE, CYAN, FONT1, FONT2, FONT3, SYSTEM, \
    RPI_LOGGING_CONFIG_FILE, LAPTOP_LOGGING_CONFIG_FILE, JSON_LIGHTS_METHODS, WS_CLIENTS, WS_PORT, LOGGING_FILE_NAME, \
    BAUD_RATE, ICONS, CONFIG, LOG_FILE, HOST_NAME, UP, WHEELS, FORWARD, DOWN, BACKWARD, LEFT, RIGHT, ANIMATION, A, B, X, \
    Y, BUTTON, MSG, BL, BR, START, SELECT, ALL, LEFT_ARM, RIGHT_ARM, NECK, RIGHT_EYE, LEFT_EYE

config = {}

DUAL_GLOVE_9DOF_LEFT, DUAL_GLOVE_9DOF_RIGHT, DUAL_GLOVE_LEFT, DUAL_GLOVE_RIGHT, SINGLE_GLOVE_9DOF, SINGLE_GLOVE, DUAL_GLOVE, CONFIG = \
    "2 GL 9", "2 GR 9", "2 GL", "2 GR", "1 G 9", "1 G", "2 G", CONFIG
IHL, IML, IBL, MHL, MML, MBL, AHL, AML, ABL, OHL, OML, OBL, IHR, IMR, IBR, MHR, MMR, MBR, AHR, AMR, ABR, OHR, OMR, OBR =1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24
#IH, IM, IB, MH, MM, MB, AH, AM, AB, OH, OM, OB = 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12

config[BASE_PATH] = os.getcwd()
config[HOST_NAME] = socket.gethostname()

config[WS_PORT] = 4421
#config[WS_CLIENTS] = {'robot': '192.168.1.200', 'sceno': '192.168.1.220', 'harddrive': '192.168.1.230'}
config[WS_CLIENTS] = {ALL: {'robot': 'didier.local', 'sceno': 'sceno.local', 'harddrive': 'disk.local'}, "gamepad": {'robot': 'didier.local'}}
#config[WS_CLIENT] = {'sceno': 'ws://192.168.1.220:4421', 'sceno': 'ws://192.168.1.220:4421'}
############## JSON FILES ##############

config[LOGGING_FILE_NAME] = "logs/control.log"

config[JSON_CONFIG] = 'control_config.json'
config[JSON_EXPRESSIONS] = 'expressions.json'
config[JSON_LIGHTS] = 'lights_base.json'
config[JSON_LIGHTS_BASE] = 'lights_base.json'
config[JSON_LIGHTS_METHODS] = 'lights_methods.json'
config[JSON_SPEECHS] = 'speechs.json'

############### PATHS ###############

config[BASE_PATH] = os.path.dirname(__file__)
config[AUDIOS_DIRECTORY] = '/audios/'
config[RPI_LOGGING_CONFIG_FILE] = '/../conf/logging-pi.conf'
config[LAPTOP_LOGGING_CONFIG_FILE] = '/../conf/logging-laptop.conf'
config[JSON_DIRECTORY] = '/../json/'
config[PLAYLIST_PATH] = '/../json/playlists/'
config[SEQUENCES_DIRECTORY] = '/sequences/'
config[PROJECT_LIGHTS_DIRECTORY] = '/projects_lights/'
############# COLORS ###############
#https://coolors.co/palettes/trending

config[PURPLE] = '#5f0f40'
config[BORDEAUX] = '#9a031e'
config[YELLOW] = '#fb8b24'
config[ORANGE] = '#e36414'
config[CYAN] = '#0f4c5c'

############ FONTS #################

config[FONT1] = "Helvetica 30 italic bold" #None tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
config[FONT2] = "Helvetica 17 italic bold" #None tkfont.Font(family='Helvetica', size=15, weight="bold", slant="italic")
config[FONT3] = "Helvetica 15 italic bold" #None tkfont.Font(family='Helvetica', size=12, weight="bold", slant="italic")

FONT_DROPDOWN = "Helvetica 30 italic bold"
FONT_BUTTON = "Helvetica 34 italic bold"

config[BUTTON_GRID] = "Helvetica 31 italic bold" #None tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

########### GAMEPAD ###############
HE, AR, EY, AN = "HE", "AR", "EY", "AN"
SELECT_MODE = [HE, AR, EY, AN]


BUTTONS_MAPPING = {HE: {UP: {RIGHT_ARM: UP}, DOWN: {RIGHT_ARM: DOWN}, LEFT: {NECK: UP}, RIGHT: {NECK: DOWN},
                        A: {RIGHT_EYE: UP}, B: {RIGHT_EYE: DOWN}, X: {LEFT_EYE: UP},
                        Y: {LEFT_EYE: DOWN}, BL: {}, BR: {},
                        'by': {WHEELS: FORWARD}, 'bw': {WHEELS: LEFT}, 'br': {WHEELS: RIGHT}, 'bg': {WHEELS: BACKWARD},
                        'bb': {ANIMATION: 'random button'}, START: {}, SELECT: {}}}
BUTTONS_MAPPING[AR] = copy.copy(BUTTONS_MAPPING[HE])
#BUTTONS_MAPPING[AR][A] = {LEFT_ARM: UP}
#BUTTONS_MAPPING[AR][B] = {LEFT_ARM: DOWN}

BUTTONS_MAPPING[EY] = copy.copy(BUTTONS_MAPPING[HE])
BUTTONS_MAPPING[AN] = copy.copy(BUTTONS_MAPPING[HE])

config[PLAYLIST_PLAY] = ['c', 'D']
config[PLAYLIST_STOP] = ['j', 'H']
RESTART_APP = ['I']

################## USB DEVICES ################
config[DEVICES] = [
        {
            NAME: 'bouton rouge',
            SERIAL_ID: 'usb-Raspberry_Pi_Pico_E66250758B6A3721-if00',
            MSG: "br",
            MSG_SIZE: 0,
            TYPE: BUTTON,
            BAUD_RATE: 115200
        },
        {
            NAME: 'bouton blanc',
            SERIAL_ID: 'usb-Raspberry_Pi_Pico_E4683818DF310B23-if00',
            MSG: "bw",
            MSG_SIZE: 0,
            TYPE: BUTTON,
            BAUD_RATE: 115200
        },
        {
            NAME: 'bouton blue',
            SERIAL_ID: 'usb-Raspberry_Pi_Pico_E66250758B474521-if00',
            MSG: "bb",
            MSG_SIZE: 0,
            TYPE: BUTTON,
            BAUD_RATE: 115200
        },
        {
            NAME: 'bouton jaune',
            SERIAL_ID: 'usb-Raspberry_Pi_Pico_DE61B868C74A4E36-if00',
            MSG: "by",
            MSG_SIZE: 0,
            TYPE: BUTTON,
            BAUD_RATE: 115200
        },
        {
            NAME: 'bouton vert',
            SERIAL_ID: 'usb-Raspberry_Pi_Pico_E66250758B90892A-if00',
            MSG: "bg",
            MSG_SIZE: 0,
            TYPE: BUTTON,
            BAUD_RATE: 115200
        },
        {
            NAME: 'buttons',
            SERIAL_ID: 'usb-1a86_USB_Serial-if00-port0',
            MSG_SIZE: 0,
            TYPE: "input_key",
            BAUD_RATE: 115200
        },
        {
            NAME: GLOVE_LEFT,
            SERIAL_ID: 'usb-Raspberry_Pi_Pico_E6611CB69753BB25-if00',
            MSG_SIZE: 0,
            TYPE: "input_key",
            BAUD_RATE: 115200
        },
        {
            NAME: "glove_right",
            SERIAL_ID: "usb-Raspberry_Pi_Pico_E4627CB0E7171B30-if00",
            "msg_size": 0,
            TYPE: "input_key",
            BAUD_RATE: 115200
        },
        {
            NAME: "joy",
            SERIAL_ID: "usb-FTDI_FT232R_USB_UART_AD0KBT1R-if00-port0",
            "msg_size": 6,
            TYPE: "joy",
            BAUD_RATE: 115200
        },
        {
            NAME: "sliders",
            SERIAL_ID: "usb-Raspberry_Pi_Pico_E66138935F269628-if00",
            "msg_size": 6,
            TYPE: "sliders",
            BAUD_RATE: 9600
        }
    ]

config[PATHS] = {
        VISUALS: "/../visuals/",
        EYES: "/../visuals/eye/",
        MOUTH: "/../visuals/mouth/",
        SEQUENCES: "/../json/sequences/",
        ICONS: "/../visuals/icons/"
    }

config[SYSTEM] = Misc.get_system_type()

if Misc.is_raspberrypi():
    config[LOGGING_CONFIG_FILE] = config[BASE_PATH] + config[RPI_LOGGING_CONFIG_FILE]
else:
    config[LOGGING_CONFIG_FILE] = config[BASE_PATH] + config[LAPTOP_LOGGING_CONFIG_FILE]
#else:
#    logging.error("can't find system type {}".format(config[SYSTEM]))

