#! /usr/bin/python
#
# Date:		7.01.2013
# Author: 	Marc Vettiger
#
# Image class for handling boot images


import os
import struct


########################################################3

class Image:
	"""An android Image object"""

	name = ""
	path = ""
	isImg = True
	
	bwd = ""		# boot image work directory
	ramdiskdir = ""		# ramdisk directory 	

	size = 0
	img = []
	header = {}
		

	def __init__(self,name,path):
		self.path = path
		self.name = name

		with open(self.path,'rb') as fimg:
			self.img = fimg.read()
		fimg.close()		  
		self.size = len(self.img)	# Check size
		self.__check_ANDROID()	# Check if it is an Android image
		self.__loadHeader()		# Load header of image

	def info_short(self):
		return " " + self.name + "		" + self.path

	def info(self):
		print "Name:	",self.name
		print "Path:	",self.path
		print "Size:	",self.size
		print
		print "Header attributes: "
		print 
		print '{0:15} : {1:1}'.format("MAGIC" , self.header["MAGIC"])
		print
		print '{0:15} : {1:1}'.format("KERNEL_SIZE" , str(self.header["KERNEL_SIZE"]) + ' bytes')
		print '{0:15} : {1:1}'.format("KERNEL_ADDR" , hex(self.header["KERNEL_ADDR"]))
		print
		print '{0:15} : {1:1}'.format("RAMDISK_SIZE" , str(self.header["RAMDISK_SIZE"])+' bytes')
		print '{0:15} : {1:1}'.format("RAMDISK_ADDR" , hex(self.header["RAMDISK_ADDR"]))
		print
		print '{0:15} : {1:1}'.format("SECOND_SIZE" , str(self.header["SECOND_SIZE"])+' bytes')
		print '{0:15} : {1:1}'.format("SECOND_ADDR" , hex(self.header["SECOND_ADDR"]))
		print
		print '{0:15} : {1:1}'.format("TAGS_ADDR" , hex(self.header["TAGS_ADDR"]))
		print '{0:15} : {1:1}'.format("PAGE_SIZE" , str(self.header["PAGE_SIZE"]))
		print
		print '{0:15} : {1:1}'.format("CMD_LINE" , self.header["CMD_LINE"])
		print
		print

#		for item in self.header:
#			if ( item[-4:] == 'ADDR'):
#				print '{0:15}	:	{1:1}'.format( item, hex(self.header[item]))  
#			elif(item[-4:] == 'SIZE'):
#				print  '{0:15}	:	{1:1}'.format( item, str(self.header[item]) + ' bytes')  
#			else:
#				print  '{0:15}	:	{1:1}'.format( item, self.header[item])  
#		print

	
	def __check_size(self):
		if self.size <= 3*2048:
			print " Error:	", self.name
			print " File is too small for being an android image (size exception)!"
			self.isImg = False
			


	def __check_ANDROID(self):
		magic = self.img[0:8]
		m = "".join(struct.unpack('8s',magic))	
		if m != "ANDROID!" :
			print " Error:	", self.name
			print " File is no ANDROID! image"
			self.isImg = False

	def __loadHeader(self):
		headerPart = self.img[0:608]
		headerV = struct.unpack('8sIIIIIIIIII16s512sIIIIIIII',headerPart)	
		headerE = [
		"MAGIC", "KERNEL_SIZE","KERNEL_ADDR","RAMDISK_SIZE", "RAMDISK_ADDR","SECOND_SIZE",
		"SECOND_ADDR","TAGS_ADDR","PAGE_SIZE","UNUSED01","UNUSED02","NAME","CMD_LINE",
		"ID01","ID02","ID03","ID04","ID05","ID06","ID07","ID08"]
		self.header ={}
		for i in range(len(headerE)):
			self.header[headerE[i]] = headerV[i]

	def open_img(self,bwd):
		### Set work directory ###############
		self.bwd = bwd
		
		### EXTRACT KERNL ##########
		print " Extracting boot.img-kernel..."
		kpages = (self.header["KERNEL_SIZE"]+self.header["PAGE_SIZE"]-1)/ self.header["PAGE_SIZE"] 	
		kStartByte = self.header["PAGE_SIZE"]
		kEndByte = self.header["PAGE_SIZE"] + self.header["KERNEL_SIZE"]
		ktmp = self.img[kStartByte:kEndByte]
		fimgK = open(self.bwd + '/boot.img-kernel','wb')
		fimgK.write(ktmp)
		fimgK.close()
		del ktmp

		### EXTRACT RAMDISK GZ ##########
		print " Extracting boot.img-ramdisk.gz..."
		rpages = (self.header["RAMDISK_SIZE"]+self.header["PAGE_SIZE"]-1)/ self.header["PAGE_SIZE"]
		rStartByte = self.header["PAGE_SIZE"] + kpages*self.header["PAGE_SIZE"]
		rEndByte = rStartByte + self.header["RAMDISK_SIZE"] 
		rtmp = self.img[rStartByte:rEndByte]		
		fimgR=open(self.bwd+'/boot.img-ramdisk.gz','wb')
		fimgR.write(rtmp)
		fimgR.close()

#		#TODO: Implement extraction!!!
#	
		## create boot.img-ramdisk directory 
		self.ramdiskdir = self.bwd + '/boot.img-ramdisk'
		if not os.path.exists(self.ramdiskdir):
			os.makedirs(self.ramdiskdir)
		else: os.system('rm -R ' + self.ramdiskdir + '/* 2> /dev/null')

		err1 = os.system('gzip -dc ' + self.bwd + '/boot.img-ramdisk.gz  > ' + self.ramdiskdir + '/boot.img-ramdisk.cpio')	
		if err1:
			print " Error: Failed to extract gzip from boot.img-ramdisk"
			return False
		err2 = os.system('rm ' + self.bwd + '/boot.img-ramdisk.gz')
		if err2:
			print " Error: Failed to remove boot.img-ramdisk.gz"
			return False
		err3 = os.system('cd ' + self.ramdiskdir + ' &&  cpio -id < ' + self.ramdiskdir + '/boot.img-ramdisk.cpio')
		if err3:
			print "Error: Failed to extract boot.img-ramdisk.cpio"
			return False
		err4 = os.system('rm ' + self.ramdiskdir + '/boot.img-ramdisk.cpio')
		if err4:
			print "Error: Failed to remove boot.img-ramdisk.cpio"
			return False 


		#################################################


	def pack_img(self,bwd):
		print "Start packing boot.img..."		

		err0 = os.system('chmod a+x resources/mk*')
		if err0:
			print "Error: Failed to change mkbootfs and mkbootimg to executable"
			return False

		err1 = os.system('resources/mkbootfs ' + self.ramdiskdir + ' | gzip > ' + self.ramdiskdir + '.gz')
		if err1:
			print "Error: Failed to create ramdiskdir.gz"
			return False

		vkernel= self.bwd + '/boot.img-kernel'
		#print vkernel
		vramdisk= self.ramdiskdir + '.gz'
		#print vramdisk

		cmdl=self.header["CMD_LINE"]
		cmdl=cmdl.strip("\x00")
		cmdl=repr(cmdl)
		print
		print "Kernel command line:"
		print cmdl

		vbase=hex(self.header["KERNEL_ADDR"])
		vbase=vbase[0:-1]
		print
		print "Kernel address:"
		print vbase
	
		vpagesz=str(self.header["PAGE_SIZE"])
		print
		print "Page Size:"
		print vpagesz
	
		vramdiskaddr=hex(self.header["RAMDISK_ADDR"])
		vramdiskaddr = vramdiskaddr[0:-1]
		print
		print "Ramdisk addr: "
		print vramdiskaddr

		out=self.bwd + '/newboot.img'
		print
		print "Output: "
		print out		

		print " mkbootimg Command line: "
		print 
		print  'resources/mkbootimg --kernel ' + vkernel + ' --ramdisk ' + vramdisk + ' --cmdline ' + cmdl + ' --base ' + vbase + ' --pagesize ' + vpagesz + ' --ramdiskaddr ' + vramdiskaddr + ' -o ' + out
		print
		print 

		err2 = os.system('resources/mkbootimg --kernel ' + vkernel  + ' --ramdisk ' + vramdisk + ' --cmdline ' + cmdl + ' --base ' + vbase + ' --pagesize ' + vpagesz + ' --ramdiskaddr ' + vramdiskaddr + ' -o ' + out)


		if err2:
			print "Error: Failed to create new boot.img"

		os.system('rm ' + vramdisk)

			
		#TODO: Implement packing algorithm
		print "End of packing boot.img"
	
		
########################################################






