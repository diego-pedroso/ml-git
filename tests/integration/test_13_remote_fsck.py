"""
© Copyright 2020 HP Development Company, L.P.
SPDX-License-Identifier: GPL-2.0-only
"""

import os
import unittest

import pytest

from ml_git.ml_git_message import output_messages
from tests.integration.commands import MLGIT_REMOTE_FSCK, MLGIT_PUSH, MLGIT_COMMIT
from tests.integration.helper import ML_GIT_DIR, ERROR_MESSAGE, MLGIT_ADD
from tests.integration.helper import check_output, init_repository, MINIO_BUCKET_PATH


@pytest.mark.usefixtures('tmp_dir', 'aws_session')
class RemoteFsckAcceptanceTests(unittest.TestCase):
    file = 'zdj7WWzF6t7MVbteB97N39oFQjP9TTYdHKgS2wetdFWuj1ZP1'

    def setup_remote_fsck(self, entity='dataset'):
        init_repository(entity, self)

        with open(os.path.join(entity, entity+'-ex', 'remote'), 'wt') as z:
            z.write(str('0' * 10011))

        self.assertNotIn(ERROR_MESSAGE, check_output(MLGIT_ADD % (entity, entity+'-ex', '--bumpversion')))
        self.assertIn(output_messages['INFO_COMMIT_REPO'] % (os.path.join(self.tmp_dir, ML_GIT_DIR, entity, 'metadata'),
                                                             os.path.join('computer-vision', 'images', entity+'-ex')),
                      check_output(MLGIT_COMMIT % (entity, entity+'-ex', '')))

        HEAD = os.path.join(ML_GIT_DIR, entity, 'refs', 'dataset-ex', 'HEAD')
        self.assertTrue(os.path.exists(HEAD))
        self.assertNotIn(ERROR_MESSAGE, check_output(MLGIT_PUSH % (entity, entity+'-ex')))

    @pytest.mark.usefixtures('switch_to_tmp_dir', 'start_local_git_server')
    def test_01_remote_fsck(self):
        self.setup_remote_fsck()
        os.unlink(os.path.join(MINIO_BUCKET_PATH, 'zdj7Wi996ViPiddvDGvzjBBACZzw6YfPujBCaPHunVoyiTUCj'))
        self.assertIn(output_messages['INFO_REMOTE_FSCK'] % (0, 1), check_output(MLGIT_REMOTE_FSCK % ('dataset', 'dataset-ex')))
        self.assertTrue(os.path.exists(os.path.join(MINIO_BUCKET_PATH, 'zdj7Wi996ViPiddvDGvzjBBACZzw6YfPujBCaPHunVoyiTUCj')))

    def _get_file_path(self):
        hash_path = os.path.join(self.tmp_dir, ML_GIT_DIR, 'dataset', 'objects', 'hashfs')
        file_path = ''

        for root, _, files in os.walk(hash_path):
            for f in files:
                if f == self.file:
                    file_path = os.path.join(root, f)

        self.assertTrue(os.path.exists(file_path))
        return file_path

    @pytest.mark.usefixtures('switch_to_tmp_dir', 'start_local_git_server')
    def test_02_remote_fsck_thorough(self):
        self.setup_remote_fsck()
        file_path = self._get_file_path()

        os.remove(file_path)

        self.assertIn(output_messages['INFO_CONSIDER_USING_THOROUGH_OPTION'] % '1',
                      check_output(MLGIT_REMOTE_FSCK % ('dataset', 'dataset-ex')))

        self.assertFalse(os.path.exists(file_path))

        self.assertIn(output_messages['INFO_MISSING_DESCRIPTOR_WITH_THOROUGH'] % '1',
                      check_output(MLGIT_REMOTE_FSCK % ('dataset', 'dataset-ex') + ' --thorough'))

        self.assertTrue(os.path.exists(file_path))

    @pytest.mark.usefixtures('switch_to_tmp_dir', 'start_local_git_server')
    def test_03_remote_fsck_paranoid(self):
        self.setup_remote_fsck()
        self._get_file_path()

        os.unlink(os.path.join(MINIO_BUCKET_PATH, self.file))

        with open(os.path.join(MINIO_BUCKET_PATH, self.file), 'wt') as z:
            z.write(str('1' * 10011))

        output = check_output(MLGIT_REMOTE_FSCK % ('dataset', 'dataset-ex') + ' --paranoid')

        self.assertIn(output_messages['ERROR_CHUNCK_CORRUPTION_DETECTED'] % (self.file, "zdj7WZMTS5ZPFmD1j1PKtxoqevRsyxT3Gy2TDY2cvNMmhT3E6"), output)
        self.assertIn(output_messages['INFO_REMOTE_FSCK'] % (1, 0), output)

        self.assertNotIn(output_messages['ERROR_CHUNCK_CORRUPTION_DETECTED'] % (self.file, "zdj7WZMTS5ZPFmD1j1PKtxoqevRsyxT3Gy2TDY2cvNMmhT3E6"),
                         check_output(MLGIT_REMOTE_FSCK % ('dataset', 'dataset-ex') + ' --paranoid'))
        self.assertTrue(os.path.exists(os.path.join(MINIO_BUCKET_PATH, self.file)))
