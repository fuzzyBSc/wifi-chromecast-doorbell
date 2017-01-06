#!/usr/bin/env python

import sys, getopt
import time
import pychromecast
import threading

device=None
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

devices = None
if device == None:
	# All available devices
	devices = pychromecast.get_chromecasts_as_dict().values()
else:
	cast = None;
	sleep = 0
	while cast == None:
		if sleep > 0:
			time.sleep(sleep)
			print("Retrying " + device + "...");
		cast = pychromecast.get_chromecast(friendly_name=device)
		sleep = 1

lock = threading.Lock();

def playAudio(cast):
	try:
		cast.wait()
		mc = cast.media_controller;
		mc.stop();
		lock.acquire();
		print(cast.device)
		lock.release();
		for ii in xrange(repeat):
			if repeat != 1:
				lock.acquire();
				print ii
				lock.release();
			for media in args:
				mc.play_media(media, mediaformat);
				while mc.status.player_state in [u'UNKNOWN', u'IDLE']:
					lock.acquire();
					print(mc.status)
					lock.release();
					time.sleep(1)
				while mc.status.player_state in [u'PLAYING', u'BUFFERING']:
					lock.acquire();
					print(mc.status)
					lock.release();
					time.sleep(1)
	except KeyboardInterrupt:
		thread.interrupt_main();

def runThreads(threads):
	for thread in threads:
		thread.start();
	for thread in threads:
		thread.join();

print devices
print mediaformat

threads = map((lambda cast: threading.Thread(target = playAudio, args = [cast])), devices);
runThreads(threads);

