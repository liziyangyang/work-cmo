#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import sys

url = "http://ip/api/v3/users"
private_token = 'JTj3jwSgxoYJHng36-ag'

file = open(sys.argv[1], 'r')
user_list = file.readlines()
user_infos = []
file.close()

for user in user_list:
    new_user = user.strip('\n')
    user_info = ('raisecom', new_user+'@raisecom.com', new_user, new_user, 'false', '0')
    user_infos.append(user_info)

payload = "password=%s&email=%s&username=%s&name=%s&can_create_group=%s&projects_limit=%s&"

for item in user_infos:
    req = (payload % item) + "private_token=" + private_token;
    response = requests.request("POST", url, data=req)
