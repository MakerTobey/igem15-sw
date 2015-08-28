import os
import threading
import subprocess
import picamera
import time, datetime
import traceback
import re
import uuid

class MjpgStreamer:
    @staticmethod
    def touch(fname, times=None):
        with open(fname, 'a'):
            os.utime(fname, times)

    @staticmethod
    def is_running(process):
        s = subprocess.Popen(["ps", "axw"], stdout=subprocess.PIPE, universal_newlines=True)
        for x in s.stdout:
            if re.search(process, x):
                return True
        return False

    @staticmethod
    def _start():
        os.chdir("/home/pi/igem15-sw/contrib/mjpg-streamer/mjpg-streamer-experimental/")
        subprocess.call('/home/pi/igem15-sw/contrib/mjpg-streamer/mjpg-streamer-experimental/run.sh', shell=True)

    @staticmethod
    def start():
        # start mjpg-streamer
        if not MjpgStreamer.is_running("mjpg_streamer") and not os.path.isfile("/tmp/igemcam-lock"):
            threading.Thread(target=MjpgStreamer._start).start()

    @staticmethod
    def stop():
        # stop mjpg-streamer
        subprocess.call(["killall", "mjpg_streamer"])

    @staticmethod
    def captureImg():
        MjpgStreamer.touch("/tmp/igemcam-lock")
        MjpgStreamer.stop()
        os.chdir("/home/pi/igem15-sw/captured")
        fname = str(datetime.datetime.now())
        uid = str(uuid.uuid4())
        with picamera.PiCamera() as camera:
            camera.resolution = (1024, 768)
            camera.start_preview()
            time.sleep(0.1)
            camera.capture('%s.%s.jpg' % (fname, uid))
        os.remove("/tmp/igemcam-lock")
        MjpgStreamer.start()
        return '/captured/%s.%s.jpg' % (fname, uid)

