#!/usr/bin/env python

#Your API Key is eda6d854f8f3d5a03da8fa4960f687fe and your secret is c2099b3b7500d1a9fd8dace8b89b76fe
import pylast
import getpass
import os
import urllib

API_KEY = 'eda6d854f8f3d5a03da8fa4960f687fe'
API_SECRET = 'c2099b3b7500d1a9fd8dace8b89b76fe'
username = raw_input("Please enter your username: ")
#username = 'timskinner1' #FIXME
md5_password = pylast.md5(getpass.getpass())
session_key = pylast.SessionKeyGenerator(API_KEY, API_SECRET).get_session_key(username, md5_password)

user = pylast.User(username, API_KEY, API_SECRET, session_key)
fetched_albums = user.get_top_albums()

albums = []
for alb in fetched_albums:
	albums += [alb.get_item()]

homedir = os.path.expanduser('~')
os.chdir(homedir + '/.cache/valkyrie')

for alb in albums:
	url = alb.get_image_url()
	if str(url).strip() != 'None': #FIXME Ugly Exception
		urllib.urlretrieve(url, alb.get_title() + '.jpg')

os.system('montage -mode Concatenate -resize 120x120! -tile 5x10 *.jpg ~/test.jpg')

