#! /usr/bin/python
#
# Date:		7.01.2013
# Author: 	Marc Vettiger
#
# Image class for handling boot images

import os
import struct
from BootHandle import *
########################################################3

H = BootHandle()

def showMenu(menuOptions=["option a","option b","option c","exit"]):
	for i,v in enumerate(menuOptions):
		print ' ('+ str(i) +') - '+v

def askSelectionPrompt(options = [0,1,2,3,4,5,6,7,8,9], prompt="Enter selection: ",compliant="Please enter valid option:"):
	while True:
		selection= raw_input(prompt)
		try:
			selection=int(selection)
			if selection in range(len(options)):
				return selection
			print "No valid option given" 
		except:	
			print "No integer value given"
		print compliant

def askForFile(cwd,prompt="Enter file path: ",compliant="Error: File not available, please enter correct path to file: "):
	while True:
		fpwd= cwd + raw_input(prompt)		
		if os.path.exists(fpwd):	#TODO: Check if no directory!!
			return fpwd

		print compliant
		


########################################################
# Start application
########################################################

menuPoints = [	'load new boot.img',
		'show boot.img info',
		'show boot.img details',
		'extract boot.img',
		'pack boot.img',
		'exit']


while True:
	os.system('clear')
	print "============================================================"
	print " Android boot.img Utility v1.1 - by Marc Vettiger "
	print "============================================================"
	print
	print "Current work directory: " 
	print " " + H.cwd 
	print
	showMenu(menuPoints)
	print
	ans = askSelectionPrompt(menuPoints)
	print

	if ans is 0:
		print "Current work directory: "
		print " " + H.cwd
		fpwd= askForFile(H.cwd)
		name= raw_input("Enter a name for the boot.img: ")
		H.set_img(name,fpwd)
		raw_input("Press enter to continue") 
	elif ans is 1:
		H.info()
		raw_input("Press enter to continue") 
	elif ans is 2:
		H.info_img()
		raw_input("Press enter to continue") 
	elif ans is 3:
		H.open_img()
		raw_input("Press enter to continue") 
	elif ans is 4:
		H.pack_img()
		raw_input("Press enter to continue") 
	elif ans is 5:
		print "Leaving application..."
		break;
			 

