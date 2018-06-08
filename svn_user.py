#!/usr/bin/python

# -*- coding: utf-8 -*-
import sys

auth_file = open(sys.argv[1], 'r')

user_list = auth_file.readlines()

new_file = open('user_mail.txt', 'w')

for user_name in user_list:
    user = user_name.strip('\n')
    user_mail = user + ' = ' + user + ' <' + user + '@raisaecom.com>\n'
    new_file.write(user_mail)

auth_file.close()
new_file.close()
