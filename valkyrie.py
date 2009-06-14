#!/usr/bin/env python

#Your API Key is eda6d854f8f3d5a03da8fa4960f687fe and your secret is c2099b3b7500d1a9fd8dace8b89b76fe
import pylast
import getpass
import os
import urllib
import glob


API_KEY = 'eda6d854f8f3d5a03da8fa4960f687fe'
API_SECRET = 'c2099b3b7500d1a9fd8dace8b89b76fe'
username = raw_input("Please enter your username: ")
#username = 'timskinner1' #FIXME
md5_password = pylast.md5(getpass.getpass())
session_key = pylast.SessionKeyGenerator(API_KEY, API_SECRET).get_session_key(username, md5_password)

user = pylast.User(username, API_KEY, API_SECRET, session_key)
fetched_albums = {}
periods = ['6month', '3month', '12month', 'overall']
for period in periods:
	new_albums = user.get_top_albums(period)
	for alb in new_albums:
		if alb.get_item().get_title() not in fetched_albums:
			fetched_albums[alb.get_item().get_title()] = alb.get_item()

homedir = os.path.expanduser('~')
if not os.path.exists(homedir + '/.cache/valkyrie'):
	os.mkdir(homedir + '/.cache/valkyrie')
os.chdir(homedir + '/.cache/valkyrie')
os.system('rm -- *.jpg')

jpg_count = 0
for key in fetched_albums:
	alb = fetched_albums[key]
	if jpg_count < 80:
		try :
			url = alb.get_image_url()
			if url != None:
				urllib.urlretrieve(url, str(hash(alb.get_title())) + '.jpg')
				jpg_list = glob.glob("*.jpg")
				jpg_count = len(jpg_list)
			else:		
				print(alb.get_name() + ": artwork not found")
		except:
			None

os.system('montage -mode Concatenate -resize 128x128! -tile 10x8 *.jpg ~/test.jpg')

