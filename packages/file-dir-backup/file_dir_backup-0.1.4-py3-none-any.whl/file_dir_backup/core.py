#!/usr/bin/env python
# -*- coding: utf-8 -*-
import shutil
import subprocess
import os
import zlib
from .logger import get_logger
from .constants import RSYNC_METHOD, SHUTIL_METHOD, FULL_BACKUP, INCREMENTAL_BACKUP


class BackupManager:
    def __init__(self, source=None, destination=None, backup_type=FULL_BACKUP,
                 method=RSYNC_METHOD, compress=False, bandwidth_limit=None):
        self.source = source
        self.destination = destination
        self.backup_type = backup_type
        self.method = method
        self.compress = compress
        self.bandwidth_limit = bandwidth_limit
        self.logger = get_logger()

    def full_backup(self):
        try:
            if self.method == RSYNC_METHOD:
                command = ['rsync', '-avz'] if self.compress else ['rsync', '-av']
                if self.bandwidth_limit:
                    command.extend(['--bwlimit', str(self.bandwidth_limit)])
                command.extend([f'{self.source}/', f'{self.destination}/'])
                subprocess.run(command, check=True)
                self.logger.info(f'Full backup completed using rsync from {self.source} to {self.destination}')
            elif self.method == SHUTIL_METHOD:
                if os.path.exists(self.destination):
                    shutil.rmtree(self.destination)
                if self.compress:
                    for root, dirs, files in os.walk(self.source):
                        relative_path = os.path.relpath(root, self.source)
                        dest_dir = os.path.join(self.destination, relative_path)
                        if not os.path.exists(dest_dir):
                            os.makedirs(dest_dir)
                        for file in files:
                            src_file = os.path.join(root, file)
                            dest_file = os.path.join(dest_dir, file)
                            with open(src_file, 'rb') as f_in:
                                data = f_in.read()
                                compressed_data = zlib.compress(data)
                            with open(dest_file, 'wb') as f_out:
                                f_out.write(compressed_data)
                else:
                    shutil.copytree(self.source, self.destination)
                self.logger.info(f'Full backup completed using shutil from {self.source} to {self.destination}')
        except Exception as e:
            self.logger.error(f'Full backup failed: {e}')

    def incremental_backup(self):
        try:
            if self.method == RSYNC_METHOD:
                command = ['rsync', '-avzu'] if self.compress else ['rsync', '-avu']
                if self.bandwidth_limit:
                    command.extend(['--bwlimit', str(self.bandwidth_limit)])
                command.extend([f'{self.source}/', f'{self.destination}/'])
                subprocess.run(command, check=True)
                self.logger.info(f'Incremental backup completed using rsync from {self.source} to {self.destination}')
            elif self.method == SHUTIL_METHOD:
                for root, dirs, files in os.walk(self.source):
                    relative_path = os.path.relpath(root, self.source)
                    dest_dir = os.path.join(self.destination, relative_path)
                    if not os.path.exists(dest_dir):
                        os.makedirs(dest_dir)
                    for file in files:
                        src_file = os.path.join(root, file)
                        dest_file = os.path.join(dest_dir, file)
                        if not os.path.exists(dest_file) or os.path.getmtime(src_file) > os.path.getmtime(dest_file):
                            if self.compress:
                                with open(src_file, 'rb') as f_in:
                                    data = f_in.read()
                                    compressed_data = zlib.compress(data)
                                with open(dest_file, 'wb') as f_out:
                                    f_out.write(compressed_data)
                            else:
                                shutil.copy2(src_file, dest_file)
                self.logger.info(f'Incremental backup completed using shutil from {self.source} to {self.destination}')
        except Exception as e:
            self.logger.error(f'Incremental backup failed: {e}')

    def backup(self):
        if self.backup_type == FULL_BACKUP:
            self.full_backup()
        elif self.backup_type == INCREMENTAL_BACKUP:
            self.incremental_backup()
