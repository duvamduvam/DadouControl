import logging
import tkinter as tk

from dadoucontrol.control_factory import ControlFactory
from dadoucontrol.gui.expression_duration import ExpressionDuration
from dadoucontrol.gui.windows.frames.abstract.rectangle_frame import RectangleFrame
from dadoucontrol.gui.windows.frames.abstract.rectangle_frame_text import RectangleFrameText
from dadoucontrol.gui.windows.frames.music_frame import MusicFrame
from dadoucontrol.gui.windows.frames.widgets.navigation_widget import NavigationWidget
from dadoucontrol.gui.windows.frames.neck_frame import NeckFrame
from dadoucontrol.gui.windows.frames.wheels_frame import WheelsFrame

from dadoucontrol.gui.windows.frames.widgets.sequences_manager_widget import SequencesManagerWidget


class SequenceFrame(tk.Frame):

    current_position = 0

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, bg='grey')
        self.pack(fill='both', expand=True, side='top')

        self.left_menu = tk.Frame(self, bg='blue', width=100)
        self.left_menu.pack(fill='y', side='left')

        music_frame = MusicFrame(self, 'red')

        NavigationWidget(self.left_menu, width=100)
        sequence_widget = SequencesManagerWidget(self, self.left_menu, music_frame)

        expressions = ControlFactory().control_json_manager.get_expressions_names()
        self.faces_frame = RectangleFrameText(self, 'face', 'green', expressions)
        lights = ControlFactory().control_json_manager.get_lights()
        self.lights_frame = RectangleFrameText(self, 'lights', 'yellow', lights)
        self.neck_frame = NeckFrame(self, 'orange')
        self.wheels_frame = WheelsFrame(self, 'violet')

        sequence_widget.load_first_sequence()

    def open_popup(self, parent):
        top = tk.Toplevel(parent)
        top.geometry("500x250")
        top.title("Child Window")
        tk.Label(top, text="Hello World!", font=('Mistral 18 bold')).place(x=150, y=80)

    def load(self):
        name = self.current_expression_name.get()
        expression = ControlFactory().control_json_manager.get_expressions_name(name)
        ExpressionDuration.value= expression['duration']
        self.expression_duration.set(ExpressionDuration.value)
        self.right_eye_frame.load(expression['left_eyes'])
        self.left_eye_frame.load(expression['right_eyes'])
        self.mouth_frame.load(expression['mouths'])
