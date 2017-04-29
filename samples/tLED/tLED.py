# Copyright 2017 Conexant Systems, LLC
 
 
# Permission is hereby granted by Conexant, free of charge, to any developer obtaining a copy
# of this software and associated documentation files (the "Software"), 
# to download, use, copy, modify, merge and distribute the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.  CONEXANT RESERVES THE RIGHT TO MAKE CHANGES TO THE SOFTWARE 
# WITHOUT NOTIFICATION.


import time
import colorControl as cc
import threading
import subprocess
import os

global led_count
led_count = 32	#place number of LEDs, not fixed on arduino yet

global threadToRun
threadToRun = None

global currentThread
currentThread = None 

global doacommand
doacommand = ["./host_demo.exe", "-u", "--4micDOA", "2"]

class StoppableThread(threading.Thread):
	"""Thread class with a stop() method. The thread itself has to check
	regularly for the stopped() condition."""

	def __init__(self):
		super(StoppableThread, self).__init__()
		print "Stoppable init"
		self._stop = threading.Event()
		self._resume = threading.Event()
		self._kill = threading.Event()

	def stop(self):
		self._stop.set()
		self.cControl.stop = True

	def stopped(self):
		return self._stop.isSet()

	def stopClear(self):
		self._stop.clear()

	def resume(self):
		self._resume.set()

	def resumeClear(self):
		self._resume.clear()

	def kill(self):
		self._kill.set()
		self.resume()
		self.cControl.stop = True


class LEDThread(StoppableThread):
	def __init__(self, cControl):
		super(LEDThread, self).__init__()
		self.cControl = cControl
		self.oldDOA = 0
		self.currentAnimation = "startup"
		self.nextAnimation = None
		self.volume = 50

	def setVolume(self, vol):
		self.volume = int(vol)

	def DOA(self):
		global doacommand
		#Read and set DOA
		with open(os.devnull, "w") as dnull:
			direction = subprocess.check_output(doacommand,stderr=dnull)
		#Type conversions are hell
		direction = float(direction)
		direction = int(direction)

		#No dominant speaker if it returns above 360 degrees, use old direction
		if direction < 360:
			self.oldDOA = direction

		self.cControl.DOA(self.oldDOA)

		time.sleep(0.03)

		return

	def cloudActivity(self):
		self.cControl.cloudActivity()

		return

	def volumeAnim(self):
		self.cControl.volumeChange(self.volume)
		self.stop()

		return

	def wifiSetup(self):
		self.cControl.wifiSetup()

		return

	def startup(self):		
		self.cControl.startUp()

		return

	def speaking(self):
		self.cControl.speech()

		return

	def finished(self):
		self.cControl.finished(self.oldDOA)
		self.stop()
		return

	def error(self):
		self.cControl.error()
		self.stop()
		return

	def alarm(self):
		self.cControl.alarm()
		return

	# def alarmStop(self):
	# 	#TOOD: Animation?
	# 	self.stop()
	# 	return

	# def noContent(self):
	# 	#TODO
	# 	self.stop()
	# 	return

	def run(self):
		while not self._kill.isSet():
			self.cControl.stop = False

			if self.currentAnimation == "DOA":
				self.DOA()
			elif self.currentAnimation == "cloudActivity":
				self.cloudActivity()
			elif self.currentAnimation == "speaking":
				self.speaking()
			elif self.currentAnimation == "finished":
				self.finished()
			elif self.currentAnimation == "volume":
				self.volumeAnim()
			elif self.currentAnimation == "alarm":
				self.alarm()
			elif self.currentAnimation == "error":
				self.error()
			elif self.currentAnimation == "startup":
				self.startup()
			elif self.currentAnimation == "wifiSetup":
				self.wifiSetup()

			if self.stopped():
				#Turn off LEDs
				self.cControl.clearColor()

				self.currentAnimation = None
				if self.nextAnimation:
					self.resume()
					self.currentAnimation = self.nextAnimation
					self.nextAnimation = None

				#wait until thread is resumed
				self._resume.wait()
				self.resumeClear()
				self.stopClear()
		self.cControl.clearColor()
		return

def doa(tck, cControl):
	direction = tck.readTCL()
	direction = float(direction)
	direction = int(direction)
	cControl.DOA(direction)

def main_loop(tck, cControl):
	recording = tck.readUBIRecording()
	type(recording)
	print recording