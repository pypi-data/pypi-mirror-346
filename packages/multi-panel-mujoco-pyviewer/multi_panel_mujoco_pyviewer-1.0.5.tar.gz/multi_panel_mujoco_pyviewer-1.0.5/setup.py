#!/usr/bin/env python3
import os
from setuptools import find_packages, setup

VERSION = '1.0.5'

INSTALL_REQUIRES = (
    ['mujoco >= 2.1.5',
     'glfw >= 2.5.0',
     'imageio',
     'pyyaml']
)

setup(
    name='mujoco-python-viewer',
    version=VERSION,
    author='Longsen Gao',
    author_email='longsengao@gmail.com',
    url='https://github.com/gaolongsen/multi-panel_mujoco-pyviewer',
    description='Multi-panels render viewer for MuJoCo Python',
    long_description='Multi-panels render viewer for MuJoCo Python',
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(),
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3 :: Only',
    ],
    zip_safe=False,
)
