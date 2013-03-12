#! /usr/bin/python
#
#
#
#####################################
import sys
import bootReadUtil

#Check for arguments
if (len(sys.argv) < 2):
	print "Error: Please specify boot.img path!"
	exit(1)
elif (len(sys.argv) > 2):
	print "Error: Too many arguments!"
	exit(1)

bootReadUtil.bootOpen(sys.argv[1])



#print bootReadUtil.bootOpen.__doc__

