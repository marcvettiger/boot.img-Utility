#! /usr/bin/python
#
# Date:		7.01.2013
# Author: 	Marc Vettiger
#
# Image class for handling boot images


import os
import struct
from Image import *
########################################################3




class BootHandle:
	"""A class that handels boot images"""
	cwd = ''	#current work directory
	bwd = None	#bootimage work directory 
	img = None

	def __init__(self):
		self.cwd = os.getcwd() + '/'
		
	def info(self):
		if self.img is None:
			print "	No boot.img loaded yet	"
		else:
			print self.img.info_short()

		if self.bwd is not None:
			print
			print " extracted files: "
			print " " + self.bwd
			
		print
	

	def info_img(self):
		if self.img is None:
			print "	No boot.img loaded yet	"
			print
		else:	
			self.img.info()
		if self.bwd is not None:
			print " boot.img extracted files: "
			print " " + self.bwd
			print

	def set_img(self,name,path):
		if os.path.exists(path):
			xImg = Image(name,path)
			if xImg.isImg:
				self.img = xImg
				print
				print "New boot.img set"
				print
				self.info()
			else: 
				print " No boot.img set!"
			print
		else: 
			print " Error: Path to image file not valide!"
	
	def open_img(self):
		if self.img is None:
			print "	No boot.img loaded yet"
			print
		else:  
			print " Creating work directory: "
			print " " + self.cwd + 'boot.img-EXTRACTED'
			print 
			ans = ask_ok("Do you want to extract to this directory? ")
			if (ans == False):
				return 
			# Create work directory
			print
			self.bwd = self.cwd + 'boot.img-EXTRACTED'
			if not os.path.exists(self.bwd):
				print " Creating new directory" 
				os.makedirs(self.bwd)
			else: 
				os.system('rm -R ' + self.bwd + '/* 2> /dev/null')
			#Initiate extraction, pass directory 	
			self.img.open_img(self.bwd)

	def pack_img(self):
		if self.img is None:
			print "	No boot.img loaded yet"
			print
		elif self.bwd is None:
			print " No boot.img extracted yet"
			print
		else:
			self.img.pack_img(self.bwd)

		
########################################################
########################################################








#Ask if function
def ask_ok(prompt='Do you want to quit?', retries=2, compliant='yes or no, please!'):
	while True:
		ok = raw_input(prompt)
		if ok in ( 'y' ,'ye', 'yes'):
			return True
		if ok in ('n', 'no','nope'):
			return False
		retries -= 1
		if retries < 0 :
			print "Error: Refusinik user!"
			exit(1) #TODO: Go back to main menu
		print compliant

