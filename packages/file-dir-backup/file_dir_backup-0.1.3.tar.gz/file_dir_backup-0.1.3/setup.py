from setuptools import find_packages
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

__author__ = 'hjl'
__description__ = 'A simple backup tool'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2023 hjl'
__email__ = '1878324764@qq.com'


def get_version(version_tuple):
    if not isinstance(version_tuple[-1], int):
        return '.'.join(map(str, version_tuple[:-1])) + version_tuple[-1]
    return '.'.join(map(str, version_tuple))


init = os.path.join(os.path.dirname(__file__), "file_dir_backup", "__init__.py")
version_line = list(filter(lambda l: l.startswith("VERSION"), open(init)))[0]
VERSION = get_version(eval(version_line.split('=')[-1]))

README = os.path.join(os.path.dirname(__file__), 'README.md')


def read_md(f):
    with open(f, 'r', encoding='utf-8') as f:
        long_description = f.read()
    return long_description


def strip_comments(l):
    return l.split('#', 1)[0].strip()


def reqs(*f):
    return list(
        filter(None, [strip_comments(l) for l in open(os.path.join(os.getcwd(), *f)).readlines()]))


setup(
    name='file_dir_backup',
    version=VERSION,
    description='A file and directory backup tool',
    # 读取README.md文件作为项目描述
    long_description=read_md(README),
    long_description_content_type='text/markdown',
    license=__license__,
    author=__author__,
    author_email=__email__,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'file_dir_backup = file_dir_backup.cli:main'
        ]
    },
    install_requires=reqs('requirements.txt'),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: System :: Archiving :: Backup',
        'Topic :: Utilities',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
    ],
    python_requires='>=3.6',
    # 安装过程中，需要安装的静态文件，如配置文件、service文件、图片等
    data_files=[
        ('/etc/', ['file_dir_backup/etc/file_dir_backup.cfg']),
    ],
)
