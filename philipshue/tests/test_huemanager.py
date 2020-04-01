from unittest import mock, TestCase
from philipshue.huemanager import HueManager

groups_url = "http://192.168.1.23/api/your_whitelist_entry_here/groups/"
scenes_url = "http://192.168.1.23/api/your_whitelist_entry_here/scenes/"

groups_string = """{
    "1": {
        "name": "Living room",
        "lights": ["1", "2", "3"],
        "sensors": [],
        "type": "Room"
    },
    "2": {
        "name": "Dining",
        "lights": ["4", "5"],
        "sensors": [],
        "type": "Room"
    },
    "3": {
        "name": "Kitchen",
        "lights": ["6"],
        "sensors": [],
        "type": "Room"
    }
}
"""
scenes_string = """{
"hxkBm5btcft17RE": {
    "name": "Savanna sunset",
    "type": "GroupScene",
    "group": "1",
    "lights": ["1", "2", "3"]
},
"-dd2XUCmuJUipeO": {
    "name": "Tropical twilight",
    "type": "GroupScene",
    "group": "1",
    "lights": ["4", "5"]
},
"L41Hjg64T-Ey4PT": {
    "name": "Arctic aurora",
    "type": "GroupScene",
    "group": "2",
    "lights": ["6"]
}
}
"""


def mocked_requests_get(*args):
    class MockResponse:
        def __init__(self, content):
            self._content = content

        @property
        def content(self):
            return self._content

    if args[0] == scenes_url:
        return MockResponse(scenes_string)
    elif args[0] == groups_url:
        return MockResponse(groups_string)


class TestHueManager(TestCase):

    @mock.patch("philipshue.huemanager.requests.get", side_effect=mocked_requests_get)
    def test_get_groups(self, mock_get):
        hue = HueManager()
        mock_get.called_with(groups_url)
        self.assertEqual(3, len(hue.groups))

    @mock.patch("philipshue.huemanager.requests.get", side_effect=mocked_requests_get)
    def test_get_scenes(self, mock_get):
        hue = HueManager()
        mock_get.called_with(scenes_url)
        self.assertEqual(3, len(hue.scenes))

    @mock.patch("philipshue.huemanager.requests.get", side_effect=mocked_requests_get)
    @mock.patch("requests.put")
    def test_activate_scene(self, mock_put, mock_get):
        hue = HueManager()
        hue.activate_scene_in_group("Tropical twilight", "1")

        expected_url = 'http://192.168.1.23/api/your_whitelist_entry_here/groups/1/action'
        self.assertIn(mock.call(expected_url, '{"scene": "-dd2XUCmuJUipeO"}'), mock_put.call_args_list)

    @mock.patch("philipshue.huemanager.requests.get", side_effect=mocked_requests_get)
    def test_get_group_by_name(self, mock_get):
        hue = HueManager()
        group = hue.get_group_by_name("Kitchen")
        self.assertEqual("3", group.group_id)
