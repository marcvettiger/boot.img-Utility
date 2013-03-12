#! /bin/sh


KERNEL='boot.img-kernel'
BOOTDIR='boot.img-ramdisk'
RAMDISK=$BOOTDIR'.gz'

###	SGS3 SGH-I747 BOOT.IMG Attributes	### 
#CMDLINE="console=null androidboot.hardware=qcom user_debug=31"
#BASE="0x80200000"
#PAGESZ="2048"
#RAMDISKADDR="0x81500000"
###################################

### HTC Sen4G BOOT.IMG Attributes		###
CMDLINE="console=ttyHSL0 androidboot.hardware=pyramid no_console_suspend=1"
BASE="0x40400000"
PAGESZ="2048"
RAMDISKADDR="0x41400000"
###################################


OUT="newboot.img"


if [ ! -f $KERNEL ]; then 
	echo "Error: No $KERNEL found!"
	return 0
fi

if [ ! -d $BOOTDIR ] ; then
	echo "Error: No $BOOTDIR directory found!"
	return 0
fi
	
echo "Create gpio archive from boot.img-ramdisk"
`./mkboot_src/mkbootfs ./$BOOTDIR/ | gzip  > $RAMDISK` 


echo "Create newboot.img"
`./mkboot_src/mkbootimg --kernel $KERNEL --ramdisk $RAMDISK --cmdline "$CMDLINE" --base $BASE --pagesize $PAGESZ --ramdiskaddr $RAMDISKADDR -o $OUT`


echo "Delete obsolete files? [yes/no]: " 
read yn

if [ $yn = 'yes' ] || [ $yn = 'y' ] ; then
	 echo "Cleaning up..." 
	`rm $RAMDISK`
	`rm $KERNEL`
	`rm -R $BOOTDIR`
fi

echo "End of script" 




