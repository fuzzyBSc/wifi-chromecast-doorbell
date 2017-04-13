#!/usr/bin/env python

import sys, getopt
import time
import pychromecast
import threading

def playAudio(cast, mediaList, mediaformat, repeat):
	try:
		cast.wait()
		mc = cast.media_controller;
		mc.stop();
		print(cast.device)
		for ii in xrange(repeat):
			if repeat != 1:
				print ii
			for media in mediaList:
				mc.play_media(media, mediaformat);
				attempts = 10
				while attempts > 0 and mc.status.player_state in [u'UNKNOWN', u'IDLE']:
					print(mc.status)
					--attempts
					time.sleep(1)
				attempts = 30
				while attempts > 0 and mc.status.player_state in [u'PLAYING', u'BUFFERING']:
					print(mc.status)
					time.sleep(1)
	except KeyboardInterrupt:
		thread.interrupt_main();

def runThreads(threads):
	for thread in threads:
		thread.start();
	for thread in threads:
		thread.join();

def ring(device, mediaList, mediaformat, repeat):
	if device == None:
		# All available devices
		devices = pychromecast.get_chromecasts_as_dict().values()
	else:
		cast = None;
		sleep = 0
		attempts = 10
		while attempts > 0 and cast == None:
			if sleep > 0:
				time.sleep(sleep)
				print("Retrying " + device + "...");
			cast = pychromecast.get_chromecast(friendly_name=device)
			sleep = 1
			--attempts

	threads = map((lambda cast: threading.Thread(target = playAudio, args = [cast, mediaList, mediaformat, repeat])), devices);
	runThreads(threads);
		

if __name__ == "__main__":
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

	devices = None

	ring(device, args, mediaformat, repeat);

