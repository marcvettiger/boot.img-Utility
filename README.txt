###############################################
#
#	boot.img-Utility
#
#	Author: 	Marc Vettiger
#	Latest update:	18.04.2013
#
###############################################

About:

boot.img-Utility is able to extract, modify and repack Android boot images.
boot images containe a kernel and a ramdisk file system


Log:
+It is finally possible to repack your extracted boot.img. The repacking option is not implemented well, since the two C binary files are needed. Also a lot of security checks before repacking are not implemented yet in the application. 
+ Better "show info" design implemented of option 2.  

18.04.2013 - log
+ mkbootimg and mkbootfs are automatically changed to executables by os.system("chmod a+x resources/mk*")
+ boot.img-ramdisk.gz is deleted after repacking
+ pyclean is executed to clean up at exit()


TODO:
+ move Image.py and BootHandle.py to resource folder 



