import logging
import os
import subprocess
import threading
import tkinter as tk
from tkinter import BOTH, TOP, filedialog, LEFT, X, Y, RIGHT, END
from playsound import playsound

from dadou_utils.utils.time_utils import TimeUtils
from dadou_utils.files.files_utils import FilesUtils
from dadou_utils.utils_static import NAME, PLAYLISTS, AUDIO, STOP, INPUT_KEY, KEY, PLAYLIST_PLAY, BASE_PATH, BORDEAUX, \
    PLAYLIST_PATH, CYAN, AUDIOS_DIRECTORY, FONT1, FONT2, ANIMATION
from dadou_utils.audios.sound_object import SoundObject

from dadoucontrol.control_factory import ControlFactory
from dadoucontrol.control_config import config



class PlaylistWindow(tk.Frame):
    def __init__(self, parent, *args, **kwargs):

        self.control_json = ControlFactory().control_json_manager
        self.deviceManager = ControlFactory().device_manager
        self.input_key_play = config[PLAYLIST_PLAY]

        self.current_pos = 0
        self.audio_process = None

        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.pack(fill=BOTH, expand=True, side=TOP)
        self.main = tk.Frame(self, width=600, bg=config[BORDEAUX])
        self.main.pack(fill=BOTH, expand=True, side=RIGHT)

        left_menu = tk.Frame(self, width=50, bg=config[CYAN])
        left_menu.pack(fill=BOTH, ipadx=20, side=LEFT)

        self.files = tk.StringVar()
        self.files.set(FilesUtils.get_folder_files_name(config[BASE_PATH] + config[PLAYLIST_PATH]))
        self.files_listbox = tk.Listbox(left_menu, listvariable=self.files, height=20, font=config[FONT2])
        self.files_listbox.bind('<<ListboxSelect>>', self.click_file)
        self.files_listbox.pack(fill=X, ipadx=20, side=TOP)

        self.playlist_data = None

        self.playlist_var = tk.StringVar()
        self.files.set(FilesUtils.get_folder_files_name(config[BASE_PATH] + config[PLAYLIST_PATH]))
        self.playlist_listbox = tk.Listbox(self.main, listvariable=self.playlist_var, selectbackground=config[BORDEAUX], height=16, width=40, font=config[FONT2])
        self.playlist_listbox.bind('<<ListboxSelect>>', self.click_audio)
        self.playlist_listbox.grid(row=0, column=0, rowspan=7, columnspan=3, sticky='new')

        #scrollbar = tk.Scrollbar(self.main)

        # Adding Scrollbar to the right
        # side of root window
        #scrollbar.grid(row=1, column=1, rowspan=5, sticky='new')

        # Insert elements into the listbox
        #for values in range(100):
        #    self.playlist_listbox.insert(END, values)

        # Attaching Listbox to Scrollbar
        # Since we need to have a vertical
        # scroll we use yscrollcommand
        #self.playlist_listbox.config(yscrollcommand=scrollbar.set)

        # setting scrollbar command parameter
        # to listbox.yview method its yview because
        # we need to have a vertical view
        #œscrollbar.config(command=listbox.yview)

        self.add_button = tk.Button(self.main, text='add', width=15, height=2, font=config[FONT1], command=self.click_add)
        self.add_button.grid(row=0, column=4, sticky='new')

        self.play_button = tk.Button(self.main, text='play', width=15, height=2, font=config[FONT1], command=self.click_play)
        self.play_button.grid(row=1, column=4, sticky='new')

        self.send_button = tk.Button(self.main, text='send', width=15, height=2, font=config[FONT1], command=self.click_send)
        self.send_button.grid(row=2, column=4, sticky='new')

        self.stop_button = tk.Button(self.main, text='stop', width=15, height=2, font=config[FONT1], command=self.click_stop)
        self.stop_button.grid(row=3, column=4, sticky='new')

        self.up_button = tk.Button(self.main, text='up', width=15, height=2, font=config[FONT1], command=self.OnEntryUp)
        self.up_button.grid(row=4, column=4, sticky='new')

        self.down_button = tk.Button(self.main, text='down', width=15, height=2, font=config[FONT1], command=self.OnEntryDown)
        self.down_button.grid(row=5, column=4, sticky='new')

        self.check_glove_input()
        self.last_glove_input_time = 0

    def OnEntryDown(self):
        self.playlist_listbox.yview_scroll(1, "units")

    def OnEntryUp(self):
        self.playlist_listbox.yview_scroll(-1, "units")

    def click_add(self):
        filepath = filedialog.askopenfilename(initialdir=config[BASE_PATH] + config[AUDIOS_DIRECTORY],title="Open a Text File",
                                              filetypes=(("text    files", "*"), ("all files", "*.*")))
        self.files.append(filepath)

    def click_play(self):
        #audio = SoundObject(config[BASE_PATH] + '/..' + config[AUDIOS_DIRECTORY], self.playlist_listbox.get(self.playlist_listbox.curselection()[0]))
        #audio.play()
        playlist_num = self.playlist_listbox.curselection()[0]
        audio_params = list(self.playlist_data.values())[playlist_num]
        audio_path = config[BASE_PATH] + '/..' + config[AUDIOS_DIRECTORY] + audio_params[AUDIO]
        if os.path.isfile(audio_path):
            #self.audio_thread = threading.Thread(target=playsound, args=(audio_path,), daemon=True).start()
            if self.audio_process:
                self.audio_process.terminate()
            self.audio_process = subprocess.Popen(['mpg123',  # The program to launch
                                  '-C',  # Commands can be sent
                                  '-q',  # Be quiet
                                  audio_path],
                                 stdin=subprocess.PIPE,  # Send commands here
                                 stdout=None,
                                stderr=None)

            #playsound(audio_path)
            #self.audio_segment = SoundObject(audio_path)
            #self.audio_segment.play()
            self.next()
        else:
            logging.error("{} not available".format(audio_path))

    def click_send(self):
        playlist_num = self.playlist_listbox.curselection()[0]
        #audio_name = self.playlist_listbox.get(playlist_num)
        audio_params = list(self.playlist_data.values())[playlist_num]
        #audio_params[AUDIO] = audio_name
        logging.info("send playlist number {} value {}".format(playlist_num, audio_params))
        self.next()
        ControlFactory().message.send_multi_ws(audio_params)


    def click_stop(self):
        ControlFactory().message.send_multi_ws({AUDIO: STOP, ANIMATION: False})
        self.audio_process.terminate()

    def click_audio(self, evt):
        w = evt.widget
        if len(w.curselection()):
            #index = int(w.curselection()[0])
            #value = w.get(index)
            self.current_pos = int(w.curselection()[0])
            self.playlist_listbox.select_set(self.current_pos)
            #self.playlist_var.set(value)
            #logging.info('You selected item %d: "%s"' % (index, value))

            self.playlist_listbox.selection_clear(0, 'end')
            self.playlist_listbox.select_set(self.current_pos)

    def next(self):
        self.playlist_listbox.selection_clear(0, 'end')
        self.current_pos = self.current_pos+1
        self.playlist_listbox.select_set(self.current_pos)

    def click_file(self, evt):
        w = evt.widget
        if len(w.curselection()):
            index = int(w.curselection()[0])
            value = w.get(index)
            #self.playlist_var.set(value)
            logging.info('You selected item %d: "%s"' % (index, value))

            self.playlist_listbox.delete(0, "end")
            self.playlist = value
            self.get_playlist(self.playlist)

    def get_playlist(self, file):
        items = []
        self.playlist_data = self.control_json.open_json(PLAYLISTS + '/' + file)
        for key in self.playlist_data:
            items.append(key)

        self.playlist_var.set(items)
        self.current_pos = 0
        self.playlist_listbox.select_set(self.current_pos)

    def check_glove_input(self):
        self.after(100, self.check_glove_input)
        devices = self.deviceManager.get_device_type(INPUT_KEY)
        for device in devices:
            msg = device.get_msg_separator()
            if msg:
                if msg in self.input_key_play:
                    if TimeUtils.is_time(self.last_glove_input_time, 2000):
                        self.click_send()
                        self.last_glove_input_time = TimeUtils.current_milli_time()
                else:
                    #TODO improve that ...
                    ControlFactory().message.send_multi_ws({KEY: msg})

