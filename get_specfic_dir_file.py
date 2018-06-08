#!/usr/bin/python
#-*- coding: utf-8 -*-

import os

all_file = []
all_file_dir = []

def get_all_file(path, dir_depth, want_depth):
    global all_file
    if dir_depth == want_depth:
        all_file += os.listdir(path)
        for i in os.listdir(path):
            file_path = os.path.join(path, i)
            all_file_dir.append(file_path)
        return

    all_file_list = os.listdir(path)
    for file in all_file_list:
        sub_path = os.path.join(path, file)
        if os.path.isdir(sub_path):
            get_all_file(sub_path, dir_depth + 1, want_depth)

get_all_file("dir_path", 1, 3)
print "all_file=" ,all_file
print "all_file_dir=", all_file_dir
