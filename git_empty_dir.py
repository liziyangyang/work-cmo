#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

def find_empty(rootDir):
    dir_list = os.listdir(rootDir)
    if len(dir_list) == 0:
        print(rootDir + ' is empty dir')
        file = os.path.join(rootDir, '.gitkeep')
        os.mknod(file, 0664)
        print file
    else:
        for dir_name in dir_list:
            path = os.path.join(rootDir, dir_name)
            #print path
            if os.path.isdir(path):
                find_empty(path)

rootDir = sys.argv[1]

find_empty(rootDir)
