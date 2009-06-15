#!/usr/bin/env python

#Your API Key is eda6d854f8f3d5a03da8fa4960f687fe and your secret is c2099b3b7500d1a9fd8dace8b89b76fe
import pylast
import getpass
import os
import urllib
import hashlib
import sys

def hcf(a,b):
	while b != 0:
		remainder = a % b
		a = b
		b = remainder
	return a

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "run like\npython valkyrie.py your_screen_width your_screen_height"
		quit()
	else: #all good
		screen_width = int(sys.argv[1])
		screen_height = int(sys.argv[2])

	API_KEY = 'eda6d854f8f3d5a03da8fa4960f687fe'
	API_SECRET = 'c2099b3b7500d1a9fd8dace8b89b76fe'
	username = raw_input("Please enter your username: ")
	#username = 'timskinner1' #FIXME
	md5_password = pylast.md5(getpass.getpass())
	session_key = pylast.SessionKeyGenerator(API_KEY, API_SECRET).get_session_key(username, md5_password)

	user = pylast.User(username, API_KEY, API_SECRET, session_key)
	print("connection established, looking for album art")

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

	size = hcf(screen_width,screen_height)
	while size >= 160:
		size = size/2 #FIXME fails if not divisible by 2, but that never happens
	#now 80 <= size < 160

	jpg_count = 0
	while jpg_count < (screen_width/size)*(screen_height/size): #so loops around if less than necessary number of albums
		for key in fetched_albums:
			alb = fetched_albums[key]
			if jpg_count < (screen_width/size)*(screen_height/size):
				try :
					url = alb.get_image_url()
					if url != None:
						urllib.urlretrieve(url, hashlib.md5(alb.get_title()+str(jpg_count)).hexdigest() + '.jpg')#insert jpg_count so filename changes on each while for same album
						jpg_count += 1
					else:		
						print(alb.get_name() + ": artwork not found")
				except:
					None

	os.system('montage -mode Concatenate -resize '+str(size)+'x'+str(size)+'! -tile '+str(screen_width/size)+'x'+str(screen_height/size)+' *.jpg ~/test.jpg')

