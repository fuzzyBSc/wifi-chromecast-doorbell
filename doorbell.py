from mod_python import apache
import ring

def handler(req):
	if ring.ring(None, ['http://192.168.2.50/audio/salamisound-2555311-ding-dong-bell-doorbell.mp3'], 'audio/mp3', 3):
		return apache.OK
	else:
		return apache.HTTP_INTERNAL_SERVER_ERROR

