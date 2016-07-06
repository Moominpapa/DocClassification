#!/usr/bin/env python
#-*-coding:cp936-*-
"""convert to exe"""
__author__ = 'moominpapa'

from distutils.core import setup
import py2exe

# bundle_files  1-wrap all, 2- wrap but python compiler, 3-not wrap
options = {"py2exe":{"compressed":1,"optimize":2,"bundle_files":1}}
setup(windows=['doctreeframe.py'],options=options,zipfile=None)
