#!/usr/bin/python
# © 2017 Conexant Systems, LLC
 
 
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


from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import cgi
import tLED
#Check if another instance is running, closes if it is
from tendo import singleton
me = singleton.SingleInstance()

PORT_NUMBER = 4000

cControl = tLED.cc.colorControl()

LEDThread = tLED.LEDThread(cControl)
LEDThread.start()

class myHandler(BaseHTTPRequestHandler):
	#Handler for the GET requests
	def do_GET(self):
		#Split path and variables
		splitpath = self.path.split("?")

		if splitpath[0] =="/Ready":
			#print "Ready"
			if LEDThread.currentAnimation:
				LEDThread.stop()
			self.send_response(204)
			return

		if splitpath[0] =="/Volume":
			if len(splitpath) != 1:
				valid = False
				variables = splitpath[1].split("&")
				for i in variables:
					var = i.split("=")
					if var[0] == "volume":
						LEDThread.setVolume(var[1])

						if not LEDThread.currentAnimation:
							LEDThread.currentAnimation = "volume"
							LEDThread.resume()
						else:
							LEDThread.nextAnimation = "volume"
							LEDThread.stop()
						valid = True
						break
				if valid:
					self.send_response(204)
				else:
					self.send_response(400)
			else:
				self.send_response(400)
			return

		if splitpath[0] =="/RecordingStarted":
			if not LEDThread.currentAnimation:
				LEDThread.currentAnimation = "DOA"
				LEDThread.resume()
			else:
				LEDThread.nextAnimation = "DOA"
				LEDThread.stop()
			self.send_response(204)
			return

		if splitpath[0] =="/CloudActivityStarted":
			if not LEDThread.currentAnimation:
				LEDThread.currentAnimation = "cloudActivity"
				LEDThread.resume()
			else:
				LEDThread.nextAnimation = "cloudActivity"
				LEDThread.stop()
			self.send_response(204)
			return

		if splitpath[0] =="/CloudActivityStopped":
			if not LEDThread.currentAnimation:
				LEDThread.currentAnimation = "finished"
				LEDThread.resume()
			else:
				if LEDThread.currentAnimation == "cloudActivity":
					if not LEDThread.nextAnimation:
						LEDThread.nextAnimation = "finished"
					LEDThread.stop()
			self.send_response(204)
			return

		if splitpath[0] =="/WifiSetup":
			#Should only happen after startup, and only stopped by ready, but no checks needed
			if not LEDThread.currentAnimation:
				LEDThread.currentAnimation = "wifiSetup"
				LEDThread.resume()
			else:
				LEDThread.nextAnimation = "wifiSetup"
				LEDThread.stop()
			self.send_response(204)
			return

		if splitpath[0] =="/SpeakingStarted":
			if not LEDThread.currentAnimation:
				LEDThread.currentAnimation = "speaking"
				LEDThread.resume()
			else:
				LEDThread.nextAnimation = "speaking"
				LEDThread.stop()
			self.send_response(204)
			return


		if splitpath[0] =="/MusicPlay":
			# Currently no special animation for music
			if not LEDThread.currentAnimation:
				LEDThread.currentAnimation = "finished"
				LEDThread.resume()
			else:
				LEDThread.nextAnimation = "finished"
				LEDThread.stop()
			self.send_response(204)
			return

		if splitpath[0] =="/Finished":
			if not LEDThread.currentAnimation:
				LEDThread.currentAnimation = "finished"
				LEDThread.resume()
			else:
				LEDThread.nextAnimation = "finished"
				LEDThread.stop()
			self.send_response(204)
			return

		if splitpath[0] =="/Error":
			if not LEDThread.currentAnimation:
				LEDThread.currentAnimation = "error"
				LEDThread.resume()
			else:
				LEDThread.nextAnimation = "error"
				LEDThread.stop()
			self.send_response(204)
			return

		if splitpath[0] =="/AlarmStart":
 			if not LEDThread.currentAnimation:
				LEDThread.currentAnimation = "alarm"
				LEDThread.resume()
			else:
				LEDThread.nextAnimation = "alarm"
				LEDThread.stop()
			self.send_response(204)
			return

		if splitpath[0] =="/AlarmStop":
			if LEDThread.currentAnimation == "alarm":
				LEDThread.currentAnimation = LEDThread.nextAnimation
				LEDThread.stop()
			if LEDThread.nextAnimation == "alarm":
				LEDThread.nextAnimation = None
			return

		self.send_response(204)
		print splitpath[0] + " is not implemented"


	def do_HEAD(self):
		#Not sure if this is necessary
		print "do_HEAD"
		return

			
try:
	#Create a web server and define the handler to manage the incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming http requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	LEDThread.kill()

	server.socket.close()