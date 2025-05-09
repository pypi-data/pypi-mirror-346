import unittest
from unittest.mock import patch, MagicMock
import os
import shutil
import subprocess
import zlib
from file_dir_backup.core import BackupManager
from file_dir_backup.constants import FULL_BACKUP, INCREMENTAL_BACKUP, RSYNC_METHOD, SHUTIL_METHOD
from file_dir_backup import constants


class TestBackupManager(unittest.TestCase):
    def setUp(self):
        self.source = "/path/to/source"
        self.destination = "/path/to/destination"
        self.backup_type = FULL_BACKUP
        self.method = RSYNC_METHOD
        self.compress = False
        self.bandwidth_limit = None
        self.backup_manager = BackupManager(
            source=self.source,
            destination=self.destination,
            backup_type=self.backup_type,
            method=self.method,
            compress=self.compress,
            bandwidth_limit=self.bandwidth_limit
        )

    @patch('subprocess.run')
    def test_full_backup_rsync(self, mock_run):
        self.backup_manager.method = RSYNC_METHOD
        self.backup_manager.compress = False
        self.backup_manager.full_backup()
        expected_command = ['rsync', '-av', f'{self.source}/', f'{self.destination}/']
        mock_run.assert_called_once_with(expected_command, check=True)

    @patch('os.path.exists')
    @patch('shutil.rmtree')
    @patch('shutil.copytree')
    def test_full_backup_shutil(self, mock_copytree, mock_rmtree, mock_exists):
        mock_exists.return_value = True  # 模拟目标目录存在
        self.backup_manager.method = SHUTIL_METHOD
        self.backup_manager.compress = False
        self.backup_manager.full_backup()
        mock_rmtree.assert_called_once_with(self.destination)
        mock_copytree.assert_called_once_with(self.source, self.destination)

    @patch('subprocess.run')
    def test_incremental_backup_rsync(self, mock_run):
        self.backup_manager.method = RSYNC_METHOD
        self.backup_manager.compress = False
        self.backup_manager.incremental_backup()
        expected_command = ['rsync', '-avu', f'{self.source}/', f'{self.destination}/']
        mock_run.assert_called_once_with(expected_command, check=True)

    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('shutil.copy2')
    def test_incremental_backup_shutil(self, mock_copy2, mock_makedirs, mock_exists):
        mock_exists.return_value = False
        self.backup_manager.method = SHUTIL_METHOD
        self.backup_manager.compress = False
        with patch('os.walk') as mock_walk:
            mock_walk.return_value = [('/path/to/source', [], ['file.txt'])]
            self.backup_manager.incremental_backup()
            mock_makedirs.assert_called()
            mock_copy2.assert_called()


class TestConfigLoading(unittest.TestCase):
    @patch('os.path.exists')
    @patch('configparser.ConfigParser.read')
    def test_load_config_file(self, mock_read, mock_exists):
        mock_exists.return_value = True
        p = constants.load_config_file()
        mock_read.assert_called()


if __name__ == '__main__':
    unittest.main()
