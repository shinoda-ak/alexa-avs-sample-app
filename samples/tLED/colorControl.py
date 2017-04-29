# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time
#import math
from neopixel import *

import math

# LED strip configuration:
LED_COUNT      = 32      # Number of LED pixels.
LED_PIN        = 12      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

controlColors = {
	"DOAMain" : Color(40,0,20),
	"DOASecondary" : Color(20,0,10),
	"Volume" : Color(40,0,20),
	"Speech" : Color(40,0,20),
	"Finished" : Color(40,0,20),
	"Error" : Color(0,40,0),
	"Cloud" : Color(40,0,20),
	"Alarm" : [Color(255, 0, 0), Color(255, 255, 0), Color(0, 255, 0), Color(0, 255, 255), Color(0, 0, 255), Color(255, 0, 255)]
}

class colorControl:
	def __init__(self):
		# Create NeoPixel object with appropriate configuration.
		self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
		# Intialize the library (must be called once before other functions).
		self.strip.begin()
		self.stop = False


	# Define functions which animate LEDs in various ways.
	def DOA(self, doa):
		"""Point towards the dominant speaker"""
		if doa > 359:
			#If DOA is over 360 degrees, there is no dominant speaker
			self.clearColor()
		else:
			#Turn every LED off
			for i in range(self.strip.numPixels()):
				self.strip.setPixelColor(i,Color(0,0,0))
			##Get the relative pixel value for DOA and fraction
			frac, pixelDOA = math.modf(doa * 32 / 360 ) 
			#Round to next integer
			if frac >= 0.5:
				pixelDOA = pixelDOA+1
			#Reverse the order of LEDs and shift to account for correct first pixel
			pixelDOA = (50 - int(pixelDOA)) % 32
			
			#Set the color of the surrounding pixels to half value of the main pixel
			self.strip.setPixelColor((pixelDOA+31)%32, controlColors["DOASecondary"])
			self.strip.setPixelColor(pixelDOA, controlColors["DOAMain"])
			self.strip.setPixelColor((pixelDOA+1)%32, controlColors["DOASecondary"])

			self.strip.show()

	def volumeChange(self, volume, wait_ms=64):
		"""Animation for volume change"""
		numLEDs = int(volume * 32 / 100)
		#print "volumeChange", numLEDs, volume

		for i in range(numLEDs):
			if self.stop:
				self.stop = False
				return
			self.strip.setPixelColor(i, controlColors["Volume"])
			self.strip.show()
			time.sleep(wait_ms/1000.0)
			wait_ms = wait_ms - 2
		for x in range(100):
			if self.stop:
				self.stop = False
				return
			time.sleep(0.02)
		for i in range(10):
			if self.stop:
				self.stop = False
				return
			fadedCol = self.fadeColor(controlColors["Volume"],i*10)
			for i in range(numLEDs):
				self.strip.setPixelColor(i,fadedCol)
			self.strip.show()
			time.sleep(30/1000.0)
		self.clearColor()

	def fadeColor(self, color, percentage):
		"""Fades a Color(x,x,x) by percentage amount"""
		if percentage < 0 or percentage > 100:
			print "Invalid percentage"
			return Color(0,0,0)
		r = ((color >> 16) & 255) * (100-percentage)/100
		g = ((color >> 8) & 255) * (100-percentage)/100
		b = ((color) & 255) * (100-percentage)/100
		return Color(r,g,b)

	def cloudActivity(self):
		"""Animation showing that the device is accessing the cloud"""
		#Let's just use theaterChaseRainbow for now
		self.theaterChaseNew(controlColors["Cloud"],60,1)

	def startUp(self):
		self.rainbow(10)

	def wifiSetup(self):
		self.colorWipeDeluxe(Color(0,0,60))

	def speech(self, wait_ms=60):
		colors = [
			0,
			self.fadeColor(controlColors["Speech"],90),
			self.fadeColor(controlColors["Speech"],80),
			self.fadeColor(controlColors["Speech"],70),
			self.fadeColor(controlColors["Speech"],60),
			self.fadeColor(controlColors["Speech"],50),
			self.fadeColor(controlColors["Speech"],40),
			self.fadeColor(controlColors["Speech"],30),
			self.fadeColor(controlColors["Speech"],20),
			self.fadeColor(controlColors["Speech"],10),
			controlColors["Speech"],
			controlColors["Speech"],
			controlColors["Speech"],
			controlColors["Speech"],
			controlColors["Speech"],
			controlColors["Speech"]
		]

		for x in colors:
			if self.stop:
				self.stop = False
				return
			for i in range(self.strip.numPixels()):
				self.strip.setPixelColor(i,x)
			self.strip.show()
			time.sleep(wait_ms/1000.0)
		for x in reversed(colors):
			if self.stop:
				self.stop = False
				return
			for i in range(self.strip.numPixels()):
				self.strip.setPixelColor(i,x)
			self.strip.show()
			time.sleep(wait_ms/1000.0)

	def finished(self,DOA, wait_ms=40):
		##Get the relative pixel value for DOA and fraction
		frac, pixelDOA = math.modf(DOA * 32 / 360 ) 
		#Round to next integer
		if frac >= 0.5:
			pixelDOA = pixelDOA+1
		#Reverse the order of LEDs and shift to account for correct first pixel
		pixelDOA = (50 - int(pixelDOA)) % 32
		pixelDOA1 = (pixelDOA + 8) % 32
		pixelDOA2 = (pixelDOA + 16) % 32
		pixelDOA3 = (pixelDOA + 24) % 32

		for x in range(8):
			if self.stop:
				self.stop = False
				return
			self.strip.setPixelColor((pixelDOA+x)%32,controlColors["Finished"])
			self.strip.setPixelColor((pixelDOA1+x)%32,controlColors["Finished"])
			self.strip.setPixelColor((pixelDOA2+x)%32,controlColors["Finished"])
			self.strip.setPixelColor((pixelDOA3+x)%32,controlColors["Finished"])
			self.strip.show()
			time.sleep(wait_ms/1000.0)
		for x in range(8):
			if self.stop:
				self.stop = False
				return
			self.strip.setPixelColor((pixelDOA+x)%32,0)
			self.strip.setPixelColor((pixelDOA1+x)%32,0)
			self.strip.setPixelColor((pixelDOA2+x)%32,0)
			self.strip.setPixelColor((pixelDOA3+x)%32,0)
			self.strip.show()
			time.sleep(wait_ms/1000.0)
		return

	def error(self):
		self.colorFlash(controlColors["Error"])

	def alarm(self):
		for x in (controlColors["Alarm"]):
			if self.colorFlash(x):
				return
			

	def colorFlash(self, flashColor,wait_ms=60):
		colors = [
			0,
			self.fadeColor(flashColor,90),
			self.fadeColor(flashColor,80),
			self.fadeColor(flashColor,70),
			self.fadeColor(flashColor,60),
			self.fadeColor(flashColor,50),
			self.fadeColor(flashColor,40),
			self.fadeColor(flashColor,30),
			self.fadeColor(flashColor,20),
			self.fadeColor(flashColor,10),
			flashColor,
			flashColor,
			flashColor
			#controlColors["Error"],
			#controlColors["Error"],
			#controlColors["Error"]
		]

		for x in colors:
			if self.stop:
				self.stop = False
				return True
			for i in range(self.strip.numPixels()):
				self.strip.setPixelColor(i,x)
			self.strip.show()
			time.sleep(wait_ms/1000.0)
		for x in reversed(colors):
			if self.stop:
				self.stop = False
				return True
			for i in range(self.strip.numPixels()):
				self.strip.setPixelColor(i,x)
			self.strip.show()
			time.sleep(wait_ms/1000.0)
		return False




	def colorWipeDeluxe(self, color, wait_ms=50):
		"""Wipe color across display a pixel at a time."""
		color2 = self.fadeColor(color,25)
		color3 = self.fadeColor(color,50)
		color4 = self.fadeColor(color,75)
		color5 = self.fadeColor(color,90)
		for i in range(self.strip.numPixels()):
			if self.stop:
				self.stop = False
				return
			self.strip.setPixelColor(i, color)
			self.strip.setPixelColor((i+31)%32, color2)
			self.strip.setPixelColor((i+30)%32, color3)
			self.strip.setPixelColor((i+29)%32, color4)
			self.strip.setPixelColor((i+29)%32, color5)

			self.strip.show()
			time.sleep(wait_ms/1000.0)

	def colorWipe(self, color, wait_ms=50):
		"""Wipe color across display a pixel at a time."""
		for i in range(self.strip.numPixels()):
			if self.stop:
				self.stop = False
				return
			self.strip.setPixelColor(i, color)
			self.strip.show()
			time.sleep(wait_ms/1000.0)

	def theaterChase(self, color, wait_ms=50, iterations=10):
		"""Movie theater light style chaser animation."""
		for j in range(iterations):
			for q in range(3):
				if self.stop:
					self.stop = False
					return
				for i in range(0, self.strip.numPixels(), 3):
					self.strip.setPixelColor(i+q, color)
				self.strip.show()
				time.sleep(wait_ms/1000.0)
				for i in range(0, self.strip.numPixels(), 3):
					self.strip.setPixelColor(i+q, 0)

	def theaterChaseNew(self, color, wait_ms=50, iterations=10):
		"""Movie theater light style chaser animation."""
		color2 = self.fadeColor(color,90)
		color3 = self.fadeColor(color,75)
		color4 = self.fadeColor(color,60)
		for j in range(iterations):
			for q in range(4):
				if self.stop:
					self.stop = False
					return
				for i in range(0, self.strip.numPixels(),4):
					self.strip.setPixelColor((i+q)%32, color)
					self.strip.setPixelColor((i+q+1)%32, color2)
					self.strip.setPixelColor((i+q+2)%32, color3)
					self.strip.setPixelColor((i+q+3)%32, color4)
				self.strip.show()
				time.sleep(wait_ms/1000.0)
				#for i in range(0, self.strip.numPixels(), 3):
				#	self.strip.setPixelColor(i+q, 0)

	def wheel(self, pos):
		"""Generate rainbow colors across 0-255 positions."""
		if pos < 85:
			return Color(pos, 85 - pos, 0)
		elif pos < 170:
			pos -= 85
			return Color(85 - pos, 0, pos)
		else:
			pos -= 170
			return Color(0, pos, 85 - pos)

	def rainbow(self, wait_ms=20, iterations=1):
		"""Draw rainbow that fades across all pixels at once."""
		for j in range(256*iterations):
			if self.stop:
				self.stop = False
				return
			for i in range(self.strip.numPixels()):
				self.strip.setPixelColor(i, self.wheel((i+j) & 255))
			self.strip.show()
			time.sleep(wait_ms/1000.0)

	def rainbowCycle(self, wait_ms=20, iterations=5):
		"""Draw rainbow that uniformly distributes itself across all pixels."""
		for j in range(256*iterations):
			if self.stop:
				self.stop = False
				return
			for i in range(self.strip.numPixels()):
				self.strip.setPixelColor(i, self.wheel(((i * 256 / self.strip.numPixels()) + j) & 255))
			self.strip.show()
			time.sleep(wait_ms/1000.0)

	def theaterChaseRainbow(self, wait_ms=50):
		"""Rainbow movie theater light style chaser animation."""
		for j in range(256):
			for q in range(3):
				if self.stop:
					self.stop = False
					return
				for i in range(0, self.strip.numPixels(), 3):
					self.strip.setPixelColor(i+q, self.wheel((i+j) % 255))
				self.strip.show()
				time.sleep(wait_ms/1000.0)
				for i in range(0, self.strip.numPixels(), 3):
					self.strip.setPixelColor(i+q, 0)

	def clearColor(self):
		"""Set all pixels to off."""
		for i in range(self.strip.numPixels()):
			self.strip.setPixelColor(i,Color(0,0,0))
		self.strip.show()

# Main program logic follows:
# if __name__ == '__main__':
# 	# Create NeoPixel object with appropriate configuration.
# 	self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
# 	# Intialize the library (must be called once before other functions).
# 	self.strip.begin()

# 	print ('Press Ctrl-C to quit.')
# 	while True:
# 		# Color wipe animations.
# 		colorWipe(self.strip, Color(255, 0, 0))  # Red wipe
# 		colorWipe(self.strip, Color(0, 255, 0))  # Blue wipe
# 		colorWipe(self.strip, Color(0, 0, 255))  # Green wipe
# 		# Theater chase animations.
# 		theaterChase(self.strip, Color(127, 127, 127))  # White theater chase
# 		theaterChase(self.strip, Color(127,   0,   0))  # Red theater chase
# 		theaterChase(self.strip, Color(  0,   0, 127))  # Blue theater chase
# 		# Rainbow animations.
# 		rainbow(self.strip)
# 		rainbowCycle(self.strip)
# 		theaterChaseRainbow(self.strip)
