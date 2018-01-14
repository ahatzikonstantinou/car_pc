#!/usr/bin/python
# -*- coding: utf-8 -*-

# ATsend.py
#  
# Turn the phone bluetooth off and on each time you
# send the At commands to free up the DUN port
#
# Requires Pybluez from Google
# http://pybluez.googlecode.com
# PyBluez works on GNU/Linux and Windows XP (Microsoft and Widcomm Bluetooth stacks)
#
# Send At commands to mobile device via DUN
#
# Some code to show how to dial a number with
# AT commands also shown below
# 
# November 5, 2008
 
import sys
import bluetooth  #Pybluez http://pybluez.googlecode.com
 
deviceName = []
deviceAddress = None
foundDevices = bluetooth.discover_devices()
 
count = 0
while count == 0:
    print ""
    print ""
    for bdaddr in foundDevices:
        deviceName.append(bluetooth.lookup_name( bdaddr ))
        deviceAddress = bdaddr
        print "%2d  %-16s Address: %s" % (count +1, deviceName[count], deviceAddress) 
        count += 1  
    choice = raw_input("Choose Device or 0 to repeat scan")
 
    # Repeat scan to get more device names
    if (choice.isdigit() and int(choice) <= len(foundDevices)):
        count = int(choice) 
        if choice > "0": 
             
            print "\n-- Select device, 0 to repeat scan or q to quit --"
            print ""
            selected = deviceName[count -1]
            deviceAddress = foundDevices[count -1]
          
            if deviceAddress is not None:
                print ""
            else:
                print "Could not find a Bluetooth device"
                
    elif choice == 0: 
        count = choice  # Repeat the while loop and device scan again
    elif choice == "q" or choice == "Q":
        exit(0)
        
services = bluetooth.find_service(address=deviceAddress)
devicename = bluetooth.lookup_name(deviceAddress, timeout=10)
showProfiles = None
 
if len(services) > 0:
    print "Found %d services on %s\n" % (len(services), deviceAddress)
# 
else:
    print "No device found at address: %s" % deviceAddress
    print
    print "Did you turn on bluetooth?"
    print "Did you accept/authorize the connection?"
    print
    sys.exit(3)
 
dunPort = 0 # Not found yet   
# Get Service Details
# global showProfiles
showProfiles = raw_input("Show Bluetooth Profiles supported? y|n")
for svc in services:
     # Look for DUN port
    if  svc["name"] == "QC Dial-up Networking":
        dunPort = svc["port"]
    if  showProfiles == "y":
        print "BT Profile: %s"    % svc["name"]
        print "    Host:        %s" % svc["host"]
        print "    Description: %s" % svc["description"]
        print "    Provided By: %s" % svc["provider"]
        print "    Protocol:    %s" % svc["protocol"]
        print "    channel/PSM: %s" % svc["port"]
        print "    svc classes: %s "% svc["service-classes"]
        print "    profiles:    %s "% svc["profiles"]
        print "    service id:  %s "% svc["service-id"]
        print
                   
if False :#dunPort != 0:
    print "Found Dial-Up Networking port = %d\n" % (dunPort)
        
    s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
 
    conn = s.connect((deviceAddress, dunPort))
 
    # A semicolon ";" at the of the number dialed
    # is necessary to make a voice call
    # with out the ";" this  command will try to
    # make a data call
 
    # Example to Dial a number using AT command
    
    #s.send('ATD +1650xxxxxxx;\r'),
    #print s.recv(1024),
    
 
# This next section has to expect the correct number of returns
# The first command "ATE1" gets a single "OK" response with a carrage return
# The next commands expects 2 lines returned.
# Each line return ends with \r
# The correct send/expect sequence must be followedd or you will get
# a hang or no response.
 
    #s.send("ATE1\r")
    #print s.recv(1024),
    s.send("AT\r")
    print s.recv(1024)

    s.send("AT+CMGF=1\r")
    print s.recv(1024)
    #print s.recv(1024)

    s.send('AT+CMGS="0784XXXXXXX"\r')
    print s.recv(1024)
    s.send("This is freds test!"+chr(26))
    print s.recv(1024)
    print s.recv(1024)
    
    #s.send("AT+GMI\r")
    #print s.recv(1024),
    #print s.recv(1024),
 
    #s.send("AT+CGMI\r")
    #print s.recv(1024),
    #print s.recv(1024),
 
    #s.send("AT+GMM\r")
    #print s.recv(1024),
    #print s.recv(1024),
 
    #s.send("AT+CGMM\r")
    #print s.recv(1024),
    #print s.recv(1024),
 
    s.close
    sys.exit(0)                 
    
else :
    print "Could not find Dial Up Networking port."
    print "Or DUN port is busy."
    print "Switch the target's Bluetooth off then on and retry"
    sys.exit(4)
