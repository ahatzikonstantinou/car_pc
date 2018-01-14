#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Python SMS Download

SMS Python helps you download phone text messages via bluetooth (or possibly some other kind of serial port). It's written for Mac OS X but parts of it should work on other systems, if you can create a tty for the serial port.
To Use:

    Download the file into a directory in yor python path (or the working directory)
    Pair your phone with your computer. See your computer's instructions for details of this.
    Create bluetooth serial port on the device. On OS X Tiger you do this from System Prefs > Bluetooth > Devices > Edit Serial Ports. Select RS-232 as the port type, and note down the port name.
    Change MY_NAME and MY_NUMBER in the file, and port_name to "tty.[name-of-port]"
    Make sure you have the python serial package in your python path ($PYTHONPATH) (the package is available from Fink)
    Run the program: python sms.py
    You messages will be printed to standard output, with any messages to stderr. The format is designed to be easy to parse automatically. 

You can also import the package in python and play with some facilities there (like the phonebook). If I have time I'll make the whole thing more friendly, add some docstrings, maybe make a .app version, and check whether it works with other phones. 
From http://astro.ic.ac.uk/~jaz/code/
'''

import serial,exceptions,re
from time import sleep
from math import *
import sys
from pprint import *

MY_NAME='Joe Zuntz'
MY_NUMBER='07746367297'

#port_name="/dev/tty.K700i-SerialPort1-1"
port_name="/dev/rfcomm0"
#port_name="/dev/rfcomm1"
#port_name="/dev/rfcomm2"

AT={
    'pb_select':"AT+CPBS=\"%s\"\r\n",
    'pb_number':"AT+CPBR=?\r\n",
    'pb_read':"AT+CPBR=%s\r\n",
    'pb_readn':"AT+CPBR=%s,%s\r\n",
    'sms_read':'AT+CMGR=%s\r\n',
    'sms_mem':'AT+CPMS=%s\r\n',
    'sms_list':'AT+CMGL=%s\r\n'
   }
okay='OK\r\n'

REPLIES={
          'error':re.compile('ERROR')
         }
RE={
    'pb_entry':re.compile(r'\+CPBR: (\d+),"(\S+)",(\d+),"([a-zA-Z0-9]*\s*[a-zA-Z0-9]*)/(.)"'),
    'pb_number':re.compile(r'\+CPBR: \((\d+)\-(\d+)\),(\d+),(\d+)')
   }

NUMBER_TYPES={
    'Home':('H','h','Home','HOME','home'),
    'Work':('W','w','Work','WORK','work'),
    'Mobile':('M','m','Mobile','mobile','MOBILE','MOB','mob','Mob'),
    'Other':('O','o','Other','other','OTHER')
    }

def connect(name):
    return serial.Serial(name,timeout=2)

class err(exceptions.Exception):
    pass

class PhoneError(err):
    pass

class ATError(err):
    pass

class LookupFailure(err):
    pass

class UnkownSMSError(err):
    pass

class PhoneBook:
    def __init__(self,name):
        self.name=name
        self.book=[]
        self.entries=0
        self.entry=0
    def __getitem__(self,n):
        return self.book[n]
    def __str__(self):
        return "Phonebook: "+self.name+"\n"+str(self.book)
    def __repr__(self):
        return "Phonebook: "+str(self.name)
    def addEntry(self,name,number,type):
        self.book.append(PhoneBookEntry(name,number,type="H"))
        self.entries+=1
    def lookupName(self,name):
        result=[]
        for entry in self.book:
            if entry.name.upper()==name.upper():
                result.append(entry.number)
        if len(result)==0:
            raise LookupFailure("Entry not found")
        if len(result)>1:
            return result
        return result[0]
    def lookupNumber(self,number):
        result=[]
        for entry in self.book:
            if pn_match(entry.number,number):
                result.append(entry.name)
        if len(result)==0:
            raise LookupFailure("Entry not found")
        if len(result)>1:
            sys.stderr.write("More than one name found for number:"+number)
        return result[0]

class SMSset(list):
    def __init__(self,name="Set 1"):
        self.name=name
    def __repr__(self):
        return "SMS Collection"+self.name


class SMS:
    def __init__(self,D,user=MY_NAME,usernumber=MY_NUMBER):
        if D['kind']=='R':
            self.kind='R'
            self.sender_number=D['number']
            self.recipient_name=user
            self.recipient_number=usernumber
            try:
                self.sender_name=D['name']
            except KeyError:
                self.sender_name=''
            self.message=D['text']
            self.date=D['date']
            self.time=D['time']
        elif D['kind']=='S':
            self.kind='S'
            self.sender_number=usernumber
            self.sender_name=user
            self.recipient_number=D['number']
            try:
                self.recipient_name=D['name']
            except KeyError:
                self.recipient_name=''
            self.time=''
            self.date=''
            self.message=D['text']
        else :
            raise UnknownSMSType
    def __repr__(self):
        if self.kind=='R':
            if self.sender_name != '':
                return "SMS from "+str(self.sender_name)+" on "+self.date
            else:
                return "SMS from "+str(self.sender_number)+" on "+self.date
        else:
            if self.recipient_name != '':
                return "SMS to "+str(self.recipient_name)
            else:
                return "SMS from "+str(self.recipient_number)
    def __str__(self):
        return 'STARTSMS\nTO:'+self.recipient_name+'\nTO NUMBER:'+self.recipient_number+'\nFROM:'+self.sender_name+'\nFROM NUMBER:'+self.sender_number+'\nON:'+self.date+'\nAT:'+self.time+'\nTEXT:'+self.message+'\nENDSMS\n'

    
class PhoneBookEntry:
    def __init__(self,name,number,type='H'):
        self.name=name
        self.number=number
        self.type=type
        for t in NUMBER_TYPES.keys():
            if type in NUMBER_TYPES[t]:
                self.type=t                
    def __str__(self):
        return str(self.name)+": "+str(self.number)+"("+self.type+")"
    def __repr__(self):
        return str(self.name)+": "+str(self.number)+"("+self.type+")"
  
class phone:
    def __init__(self,name):
        self.port=connect(name)
        self.phonebook=None
        
    def runCommand(self,at_command, *at_args):
        print( 'Executing {}'.format( AT[at_command]%at_args ) )
        self.port.write(AT[at_command]%at_args)
        sleep(1)
        response=self.port.readlines()
        pprint( response )
        if REPLIES['error'].match(response[-2]):
            raise ATError(''.join(response))
        return response[1:-1]
        
    def loadSMS(self):
        self.runCommand('sms_mem','"ME"')
        messages=self.runCommand('sms_list',4)
        print( 'messages:' )
        pprint( messages )
        messages=[line for line in messages if not ( line.startswith('AT') or line.startswith('+') or line.startswith('\r\n')) ]
        messages=[decode_pdu(pdu) for pdu in messages]
        book=self.getPhonebook()
        messages_out=[]
        for message in messages:
            try:
                message['name']=self.phonebook.lookupNumber(message['number'])
            except:
                LookupFailure
            messages_out.append(SMS(message))
        return messages_out
            
    def loadPhonebook(self,simcard=False):
        pb=PhoneBook('K700i Phone Book')
        if simcard:
            location='SM'
        else:
            location='ME'
        self.runCommand('pb_select',location)
        report=RE['pb_number'].match(self.runCommand('pb_number')[0]).groups()
        start,end=report[0],report[1]
        self.port.write(AT['pb_readn']%(start,end))
        sleep(1)
        lines=self.port.readlines()
        for line in lines:
            parsed_line=RE['pb_entry'].match(line)
            if parsed_line:
                group=parsed_line.groups()
                name,number,type=group[3],group[1],group[4]
                pb.addEntry(name,number,type)
        self.phonebook=pb
        
    def getPhonebook(self):
        if self.phonebook is None:
            self.loadPhonebook()
        return self.phonebook

def pn_match(a,b):
    a1=a.lstrip('+')
    b1=b.lstrip('+')
    a1=a1.lstrip('44')
    b1=b1.lstrip('44')
    a1=a1.lstrip('0')
    b1=b1.lstrip('0')
    return a1==b1

def fullsplit(m):
    """Split a list by commas and whitespace"""
    return flatten([a.split() for a in m.split(",")])


def pairswitch(message):
    if len(message)%2==1: message=message+"F"
    return ''.join(flatten([[message[2*i+1],message[2*i]] for i in range(len(message)/2) ]))


def flatten(L):
    if type(L) != type([]): return [L]
    if L == []: return L
    return flatten(L[0]) + flatten(L[1:])

def encode_pdu(number,message):
    init_code="001100"
    l=len(number)
    len_code=l[l.index('x')+1:].zfill(2)

def decode_number(number):
    n=[ [number[2*i+1],number[2*i]] for i in range(len(number)/2)]
    n=flatten(n)
    n=[c for c in n if ( c!="F" and c!="f")]
    return ''.join(n)

def decode_pdu(m2):
    m=m2.strip('\n').strip('\r')
    pdu={}
    start=0
    smsc_length=int(m[start:start+2],16)
    smsc_num='0'
    start+=2
    if smsc_length != 0:
        smsc_type=int(m[start:start+2],16)
        start+=2
        smsc_num=m[start:start+smsc_length*2-2]
        start+=(smsc_length-1)*2
        if smsc_type == 145:
            smsc_num='+'+smsc_num
    deliver_code=int(m[start:start+2],16)
    start+=2
    if deliver_code & 1 == 1:
        sent=True
        #This is a message sent from the phone
        message_ref=int(m[start:start+2],16)
        start+=2
    else:
        sent=False
    address_length=int(m[start:start+2],16)
    start+=2
    if address_length%2==1:
        address_length+=1
    address_type=int(m[start:start+2],16)
    start+=2
    number=decode_number(m[start:start+address_length])
    start+=address_length
    if address_type == 145:
        number='+'+number
    pid=m[start:start+2]
    start+=2
    dcs=m[start:start+2]
    start+=2
    if sent:
        valid_period=int(m[start:start+2],16)
        start+=2
    else:
        time_sent=decode_number(m[start:start+14])
        date=time_sent[0:2]+"/"+time_sent[2:4]+"/"+time_sent[4:6]
        time=time_sent[6:8]+"."+time_sent[8:10]+"."+time_sent[10:12]
        start+=14
    message_length=int(m[start:start+2],16)
    start+=2
    text=decode_octet(m[start:start+message_length*2])
    start+=message_length
    if sent:
        return {
            'kind':"S",
            'number':number,
            'text':text,
            'ref':message_ref,
            'validity':valid_period,
            'dcs':dcs,
            'pid':pid,
            'code':deliver_code,
            'smsc':smsc_num
            }
    else:
        return {
            'kind':"R",
            'number':number,
            'text':text,
            'date':date,
            'time':time,
            'dcs':dcs,
            'pid':pid,
            'code':deliver_code,
            'smsc':smsc_num,
            }

            

def decode_octet(s):
    s2=[int(pair,16) for pair in [s[2*i:2*i+2] for i in range(len(s)/2)] ]
    for i in reversed(range(1,len(s2))):
        n=i%7
        if n!=0:
            m=(s2[i-1]>>(8-n))<<(8-n)
            s2[i-1]=s2[i-1]-m
            s2[i]=(s2[i]<<n)+(m>>(8-n))
    s3=[]
    for i in range(len(s2)):
        if s2[i]<256:
            s3.append(chr(s2[i]))
        else:
            s3.append(chr(s2[i]%128))
            s3.append(chr(s2[i]>>7))
    return ''.join(s3)
        
def encode_octet(s):
    s2=[ord(char) for char in s]
    for i in range(len(s2)-1):
        n=(i+1)%8
        m=s2[i+1]%(2**n)
        s2[i]+=m<<(8-n)
        s2[i+1]=(s2[i+1]-m)>>n
    return ''.join([hex(item)[2:].zfill(2).upper() for item in s2 if item != 0])


if __name__=="__main__":
    p=phone(port_name)
    messages=p.loadSMS()
    for message in messages:
        print message

