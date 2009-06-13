#!/usr/bin/env python

#Your API Key is eda6d854f8f3d5a03da8fa4960f687fe and your secret is c2099b3b7500d1a9fd8dace8b89b76fe
import pylast
import getpass
import os

API_KEY = 'eda6d854f8f3d5a03da8fa4960f687fe'
API_SECRET = 'c2099b3b7500d1a9fd8dace8b89b76fe'
#username = raw_input("Please enter your username: ")
username = 'timskinner1' #FIXME
md5_password = pylast.md5(getpass.getpass())
session_key = pylast.SessionKeyGenerator(API_KEY, API_SECRET).get_session_key(username, md5_password)

user = pylast.User(username, API_KEY, API_SECRET, session_key)
os.system('montage -mode Concatenate -resize 120x120! -tile 5x2 *.jpg ~/test.jpg')

