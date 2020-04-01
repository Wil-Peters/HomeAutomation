import configparser
import json
import os

from typing import List

import requests


class GroupDoesntExistException(Exception):
    pass


class Group(object):
    def __init__(self, name, group_id):
        self._name = name
        self._group_id = group_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def group_id(self) -> str:
        return self._group_id


class Scene(object):
    def __init__(self, name, scene_id, group):
        self._name = name
        self._scene_id = scene_id
        self._group = group

    @property
    def name(self) -> str:
        return self._name

    @property
    def scene_id(self) -> str:
        return self._scene_id

    @property
    def group(self) -> str:
        return self._group


class HueManager(object):
    _groups: List[Group] = []
    _scenes: List[Scene] = []

    def __init__(self):
        config = configparser.ConfigParser()
        config_file = os.path.dirname(os.path.abspath(__file__)) + "/config.ini"
        config.read(config_file)
        base_url = config["Hue"]["Url"]
        self._groups_url = base_url + "/groups/"
        self._scenes_url = base_url + "/scenes/"
        self._group_action_url = base_url + "/groups/{}/action"
        self._load_groups()
        self._load_scenes()

    @property
    def groups(self) -> List[Group]:
        return self._groups

    def get_group_by_name(self, group_name) -> Group:
        for group in self.groups:
            if group.name.lower() == group_name.lower():
                return group
        raise GroupDoesntExistException("{} doesn't exist".format(group_name))

    @property
    def scenes(self) -> List[Scene]:
        return self._scenes

    def _load_groups(self):
        groups_string = requests.get(self._groups_url).content
        self._groups = []
        for key, group_dict in json.loads(groups_string).items():
            if group_dict["type"] == "Room":
                group = Group(group_dict["name"], key)
                self._groups.append(group)

    def _load_scenes(self):
        scenes_string = requests.get(self._scenes_url).content
        self._scenes = []
        for key, scene_dict in json.loads(scenes_string).items():
            if "group" in scene_dict.keys():
                scene = Scene(scene_dict["name"], key, scene_dict["group"])
                self._scenes.append(scene)

    def activate_scene_in_group(self, scene_name, group):
        for scene in self.scenes:
            if scene.name == scene_name and scene.group == group:
                uri = self._group_action_url.format(group)
                payload = {"scene": scene.scene_id}
                requests.put(uri, json.dumps(payload))

    def send_room_command_to_bridge(self, room_name: str, payload_json: str):
        group = self.get_group_by_name(room_name)
        uri = self._group_action_url.format(group.group_id)
        requests.put(uri, payload_json)
