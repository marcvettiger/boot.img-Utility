Marc Vettiger - 12.03.2013

Purpose:
+ boot.img-Utility is able to extract, modify and repack Android boot images.


Log:
It is finally possible to repack your extracted boot.img. The repacking option is not implemented well, since the two C binary files are needed. Also a lot of security checks before repacking are not implemented yet in the application. 

+ Better "show info" design implemented of option 2.  


Outview:
+ Implement checks before repacking boot.img 


HOWTO: 
Make sure the two binaries mkbootfs and mkbootimg are executable. Otherwise:
# chmod a+x mkbootfs mkbootimg


