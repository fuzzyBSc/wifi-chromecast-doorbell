#!/usr/bin/env python

import sys, getopt
import time
import pychromecast

device='Jason'
mediaformat='video/mp4'
repeat=1

myopts, args = getopt.getopt(sys.argv[1:], "d:m:r:");

for o, a in myopts:
	if o == '-d':
		device = a
	elif o == '-m':
		mediaformat = a
	elif o == '-r':
		repeat = int(a)
	else:
		media = a

print device
print mediaformat

cast = None
sleep = 0
while cast == None:
	if sleep > 0:
		time.sleep(sleep)
		print("Retrying...");
	cast = pychromecast.get_chromecast(friendly_name=device)
	sleep = 1
cast.wait()
print(cast.device)

mc = cast.media_controller
mc.stop();

for ii in xrange(repeat):
	if repeat != 1:
		print ii
	for media in args:
		mc.play_media(media, mediaformat);
		while mc.status.player_state in [u'UNKNOWN', u'IDLE']:
			time.sleep(1)
		print(mc.status)
		while mc.status.player_state in [u'PLAYING', u'BUFFERING']:
			time.sleep(1)
		print(mc.status)

