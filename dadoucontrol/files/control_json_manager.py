import distutils
import json
import logging

import jsonpath_rw_ext
from dadou_utils.misc import Misc

from dadoucontrol.control_static import JSON_LIGHTS_BASE, SEQUENCES_DIRECTORY, JSON_EXPRESSIONS, \
    JSON_LIGHTS, JSON_SPEECHS
from dadou_utils.files.abstract_json_manager import AbstractJsonManager

from utils_static import AUDIOS


class ControlJsonManager(AbstractJsonManager):

    def __init__(self, base_folder, json_folder, config_file):
        super().__init__(base_folder, json_folder, config_file)
        self.lights_base = self.open_json(JSON_LIGHTS_BASE, 'r')
        #self.lights = self.open_json(LIGHTS_FILE, 'r')
        #self.expressions = self.open_json(EXPRESSIONS_FILE, 'r')

    #def get_config(self):
    #    return self.config

    def get_folder_path_from_type(self, folder_type):
        result = jsonpath_rw_ext.match('$.paths[?name~' + folder_type + ']', self.config)
        return self.base_folder+self.standard_return(result, True, self.PATH)

    def get_sequence(self, name):
        return self.open_json(SEQUENCES_DIRECTORY+name)

    def get_expressions(self):
        return self.open_json(JSON_EXPRESSIONS, 'r')

    def get_expressions_names(self):
        expressions_names = []
        for e in self.get_expressions():
            expressions_names.append(e['name'])
        return expressions_names

    def get_lights(self):
        return self.open_json(JSON_LIGHTS, 'r')

    def get_lights_base(self):
        #bases = self.lights['base']
        #return_values = []
        #for base in bases:
        #    return_values.append(base['name'])
        return self.lights_base

    def get_expressions_name(self, name):
        for result in self.open_json(JSON_EXPRESSIONS, 'r'):
            if result['name'] == name:
                return result

    def delete_expression(self, name):
        expressions = self.open_json(JSON_EXPRESSIONS, 'r')
        self.delete_item(expressions, name)
        with open(self.json_folder+JSON_EXPRESSIONS, 'w') as outfile:
            json.dump(expressions, outfile, indent=4)

    def save_expressions(self, name, duration, loop, keys, left_eyes, right_eyes, mouths):
        expressions = self.open_json(JSON_EXPRESSIONS, 'r')
        self.delete_item(expressions, name)
        expressions.append({"name": name, "duration": duration, "loop": Misc.to_bool(loop), "keys": Misc.convert_to_array(keys),
                            "left_eyes": left_eyes, "right_eyes": right_eyes, "mouths": mouths})
        with open(self.json_folder+JSON_EXPRESSIONS, 'w') as outfile:
            json.dump(expressions, outfile, indent=4)
        #expressions_w = self.open_json(EXPRESSIONS_FILE, 'w')
        #expressions_w.write(expressions)

    def save_lights(self, lights):
        #lights = self.open_json(LIGHTS_FILE, 'r')
        with open(self.json_folder+JSON_LIGHTS, 'w') as outfile:
            json.dump(lights, outfile, indent=4)

    def get_speechs(self):
        return self.open_json(JSON_SPEECHS, 'r')
