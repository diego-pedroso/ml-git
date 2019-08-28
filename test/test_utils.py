"""
© Copyright 2020 HP Development Company, L.P.
SPDX-License-Identifier: GPL-2.0-only
"""

import shutil
import unittest
import tempfile
import os
from mlgit.utils import json_load, yaml_load, yaml_save

class UtilsTestCases(unittest.TestCase):
    def test_json_load(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            jsn = {}
            self.assertFalse(bool(jsn))
            jsn = json_load('./udata/data.json')
            self.assertEqual(jsn["dataset"]["categories"] ,"imgs")
            self.assertEqual(jsn["dataset"]["name"] ,"dataex")
            self.assertEqual(jsn["dataset"]["version"], 1)


            self.assertTrue(bool(jsn))

    def test_yaml_load(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            yal = {}
            self.assertFalse(bool(yal))
            yal = yaml_load('./udata/data.yaml')
            self.assertTrue(bool(yal))
            self.assertEqual(yal["store"]["s3"]["mlgit-datasets"]["region"], "us-east-1")

    def test_yaml_save(self):
        with tempfile.TemporaryDirectory() as tmpdir:

            # get new variable
            arr = tmpdir.split('\\')
            temp_var = arr.pop()

            yaml_path = os.path.join(tmpdir, "data.yaml")

            shutil.copy("udata/data.yaml", yaml_path)

            # load yaml
            yal = yaml_load(yaml_path)

            temp_arr = yal["dataset"]["git"].split(".")
            temp_arr.pop()
            temp_arr.pop()
            temp_arr.append(temp_var)
            temp_arr.append("git")
            # create new git variable
            new_git_var = '.'.join(temp_arr)

            self.assertFalse(yal["dataset"]["git"] == new_git_var)

            yal["dataset"]["git"] = new_git_var

            yaml_save(yal, yaml_path)
            self.assertTrue(yal["dataset"]["git"] == new_git_var)


if __name__ == "__main__":
	unittest.main()