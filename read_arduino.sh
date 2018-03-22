#!/system/bin/sh

#This file must be placed in /data/local in nexus 7 2013, and add execute permission
#The script will  read /dev/ttyUSB0 which is supposed to be an arduino with the code to detect reverse lights on/off
#This script should be executed by tasker in nexus 7  when the intent "android.hardware.usb.action.USB_DEVICE_ATTACHED" is caught
#The script broadcasts an intent with the state that it read from arduino
#This intent should be caught by tasker and processed accordingly to start the usb camera app etc.

while read c; do am broadcast -a com.rev_lights.intent --es state "$c"; done < /dev/ttyUSB0
