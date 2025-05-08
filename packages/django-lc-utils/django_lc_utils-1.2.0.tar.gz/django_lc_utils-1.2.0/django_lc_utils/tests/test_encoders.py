import json
import unittest

import semantic_version

from ..encoders import VersionCompatibleEncoder


class TestVersionCompatibleEncoder(unittest.TestCase):
    def test_version_compatible_encoder_pass(self):
        data = {"version": semantic_version.Version("1.2.3")}
        encoded_data = json.dumps(data, cls=VersionCompatibleEncoder)
        decoded_data = json.loads(encoded_data)
        self.assertEqual(decoded_data["version"], "1.2.3")

    def test_version_compatible_encoder_fail(self):
        data = {"version": semantic_version.Version("1.2.3")}
        encoded_data = json.dumps(data, cls=VersionCompatibleEncoder)
        decoded_data = json.loads(encoded_data)
        self.assertNotEqual(decoded_data["version"], semantic_version.Version("1.2.3"))

    def test_version_compatible_encoder_type_str_pass(self):
        data = {"version": semantic_version.Version("1.2.3")}
        encoded_data = json.dumps(data, cls=VersionCompatibleEncoder)
        decoded_data = json.loads(encoded_data)
        self.assertIsInstance(decoded_data["version"], str)

    def test_version_compatible_encoder_version_instance_fail(self):
        data = {"version": semantic_version.Version("1.2.3")}
        encoded_data = json.dumps(data, cls=VersionCompatibleEncoder)
        decoded_data = json.loads(encoded_data)
        self.assertNotIsInstance(decoded_data["version"], semantic_version.Version)
