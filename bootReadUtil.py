#!/usr/bin/python
#
# Date:		20.11.2012
# Author: 	Marc Vettiger
#
# bootParser for loading android boot.img


#TODO: Create boot.img class !! 

import struct 
import os

def ask_ok(prompt='Do you want to quit?', retries=2, compliant='yes or no, please!'):
	while True:
		ok = raw_input(prompt)
		if ok in ( 'y' ,'ye', 'yes'):
			return True
		if ok in ('n', 'no','nope'):
			return False
		retries = retries -1;
		if retries < 0 :
			print "Error: Refusinik user!"
			exit(1)
		print compliant




def bootOpen(imgPath):
	"""Usage:	bootOpen(path/to/boot.img)
	Loads a android boot.img and parses it into its appropriate structure.
	Return object is the structure containing the boot.
	"""

	fimg = open(imgPath,'rb')	#TODO: CHECK IF FILE EXISTS else QUIT
	print "Unpack boot.img:	" + imgPath
	img = fimg.read()
	fimg.close()
	
	# Size exception
	if (len(img) <= 3*2048):
		print "Error: " + imgPath + " is too small for being an android image (size exception)!"
		exit(1)


	#READ BOOT HEADER AND PARSE IT 
	bHeaderPart = img[0:608]	
	# Extract struct to a Tuple 
	# Read /system/core/mkbootimg/bootimg.h from official android source
	bHeaderV = struct.unpack('8sIIIIIIIIII16s512sIIIIIIII',bHeaderPart)	
	
	# Define Header Elements List:
	bHeaderE = [
		"MAGIC",
		"KERNEL_SIZE",
		"KERNEL_ADDR",
		"RAMDISK_SIZE", 
		"RAMDISK_ADDR",
		"SECOND_SIZE",
		"SECOND_ADDR",
		"TAGS_ADDR",
		"PAGE_SIZE",
		"UNUSED01",
		"UNUSED02",
		"NAME",
		"CMD_LINE",
		"ID01",
		"ID02",
		"ID03",
		"ID04",
		"ID05",
		"ID06",
		"ID07",
		"ID08"]

	#Parse values from Tuple and List into bheader Dictionary
	bHeader ={}
	for i in range(len(bHeaderE)):
		bHeader[bHeaderE[i]] = bHeaderV[i] 




	if (bHeader['MAGIC'] != "ANDROID!"):
		print  "Error: " + imgPath + " is no android image ('MAGIC' exception)!"
		exit(1)

	#TODO: Check SHA1 checksum field
	#TODO: Collect garbage


	
	#Print all elements and coresponding values
	print "All boot.img attributes: "
	for item in bHeaderE:
		if ( item[-4:] == 'ADDR'):
			print '{0:15}	:	{1:1}'.format( item, hex(bHeader[item]))  
		elif(item[-4:] == 'SIZE'):
			print  '{0:15}	:	{1:1}'.format( item, str(bHeader[item]) + ' bytes')  
		else:
			print  '{0:15}	:	{1:1}'.format( item, bHeader[item])  
	print



	ans = ask_ok("Do you want to extract this image? ")
	if (ans == False):
		print "Leaving boot.img-Utility..."
		exit(1)
	

	################ Start of extraction #########################	
	dirpath = os.getcwd()
	dirpath = dirpath + '/boot.img-EXTRACTED'
	if not os.path.exists(dirpath):
		os.makedirs(dirpath)
	else: os.system('rm -R ' + dirpath + '/*')
	
	print "Created work directory: " + dirpath
	# create boot.img-ramdisk directory 
	bdir = dirpath + '/boot.img-ramdisk'
	if not os.path.exists(bdir):
		os.makedirs(bdir)
	else: os.system('rm -R ' + bdir + '/*')
 


	
	print "Extracting boot.img-kernel..."
	kpages = (bHeader["KERNEL_SIZE"]+bHeader["PAGE_SIZE"]-1)/ bHeader["PAGE_SIZE"] 	
	kStartByte = bHeader["PAGE_SIZE"]
	kEndByte = bHeader["PAGE_SIZE"] + bHeader["KERNEL_SIZE"]
	ktmp = img[kStartByte:kEndByte]
	fimgK = open(dirpath + '/boot.img-kernel','wb')
	fimgK.write(ktmp)
	fimgK.close()
	del ktmp
	 
	print "Extracting boot.img-ramdisk.gz"
	rpages = (bHeader["RAMDISK_SIZE"]+bHeader["PAGE_SIZE"]-1)/ bHeader["PAGE_SIZE"]
	rStartByte = bHeader["PAGE_SIZE"] + kpages*bHeader["PAGE_SIZE"]
	rEndByte = rStartByte + bHeader["RAMDISK_SIZE"] 
	rtmp = img[rStartByte:rEndByte]
	fimgR = open( bdir +'/boot.img-ramdisk.gz','wb')
	fimgR.write(rtmp)
	fimgR.close()


	#TODO: Use python libraries to unpack
	print "Unpacking boot.img-ramdisk"
	os.chdir(bdir)	
	os.system('gzip -dv ./boot.img-ramdisk.gz')
	os.system('cpio -id < ./boot.img-ramdisk')
	os.system('rm ./boot.img-ramdisk')


	ans = ask_ok("Do you want to clean up boot.img-EXTRACTED ? ")
	if (ans == True):
		os.system('rm -R ' + dirpath)
		print "Removing boot.img-EXTRACTED..."

	

	# For testing 
	#f = open('./tmp','wb')
	#f.write(HeaderPart)
	#f.close()







