#!/usr/bin/python
#
# Analyse playlist and extract streams it points to
#
# The library relies heavily on correct mimetype of the playlist.
#
# Author: Arie Skliarouk <skliarie@gmail.com>
#

import os,sys,re

def get_pltype_by_mimetype(mimetype):
  if mimetype in ["video/x-ms-asf-plugin","audio/x-ms-wax","audio/x-ms-asx","audio/x-ms-wma",
    "video/x-ms-wmv","video/x-ms-asx","video/x-ms-wvx","application/asx","video/x-ms-wmx",
    "application/mplayer2","application/vnd.ms-asf","asf","audio/asx","audio/x-ms-asf","video/x-ms-asf",
    "Video/x-ms-asf","audio/x-ms-wax-object"]:
    return "asx"
    
  #Real playlist
  if mimetype in ["application/vnd.rn-realmedia","audio/x-pn-realaudio","audio/vnd.rn-realaudio"]:
    return "realplayer"
    
  if mimetype=="application/x-shockwave-flash":
    print "Debug this"
    sys.exit(1)
    return "flash"
    
  #ShoutCast Playlist
  if mimetype in ["audio/x-scpls","audio/scpls","application/pls","application/x-scpls","application/pls+xml"]:
    return "pls"
    
  #SMIL playlist
  if mimetype in ["application/smil","application/smil+xml"]:
    return "smil"
  
  # M3U playlist
  if mimetype in ["audio/mpegurl","audio/x-mpegurl","audio/x-aac"]:
    return "m3u"

  if mimetype in ["text/plain","text/html","application/octet-stream","audio/mpeg","application/ogg"]:
    raise

  #Most likely direct audio streams
  if mimetype in ["audio/mpeg","audio/aacp"]:
    raise

  print "Error: Unrecognized mime type [%s]"%mimetype
  raise

def get_pltype_by_extension(extension):
  # The detection by extension is very unreliable, it is here for easing tests with disk-based files
  
  # There are two types of "asx" playlist, "asx" (which is XML based) and asf (which is simply list of links).
  if extension=="asx":
    return "asx"

  if extension=="pls":
    return "pls"

  if extension=="m3u":
    return "m3u"
    
  if extension=="smil":
    return "smil"

  print "Error: Unrecognized file extension [%s]" % extension

def get_single_line(body):
  return body.replace("\r\n"," ").replace("\r"," ").replace("\n"," ")

def search_asx_header(body):
  global asx_header_pattern
  if 'asx_header_pattern' not in globals():
    asx_header_pattern=re.compile(r'<asx',re.IGNORECASE)
  return asx_header_pattern.findall(body)

def search_asf_links(body):
  global asf_links_pattern
  if 'asf_links_pattern' not in globals():
    #asf_links_pattern=re.compile(r'^Ref\d*=(.*?)$',re.IGNORECASE)
    asf_links_pattern=re.compile(r'^Ref\d*=(.*?)$',re.MULTILINE|re.IGNORECASE)
  return asf_links_pattern.findall(body)

def get_pltype_by_body(body):
  # This is unreliable, used when mimetype is not provided or incorrect
  if len(body)>50000:
    print "Info: playlist can not be this long"
    sys.exit(0)
    return None
  
  # Detecting shoutcat playlist
  # [playlist] NumberOfEntries=1
  body=get_single_line(body)
  
  global shoutcast_header_pattern
  if 'shoutcast_header_pattern' not in globals():
    shoutcast_header_pattern=re.compile(r'\[playlist\] NumberOfEntries',re.IGNORECASE)
  shoutcast_header=shoutcast_header_pattern.findall(body)
  if len(shoutcast_header)!=0:
    return "pls"

  asx_header=search_asx_header(body)
  if len(asx_header)!=0:
    return "asx"

  print body
  return None

def get_streams_from_file(filename,pl_type):
  body=open(filename).read()
  if len(body)==0:
    return None
  return get_streams_body_pl_type(body,pl_type)

def get_streams_body_mimetype(body,mimetype):
  try:
    pl_type=get_pltype_by_mimetype(mimetype)
  except:
    try:
      pl_type=get_pltype_by_body(body)
    except:
      print "Warning: could not recognize the playlist"
      raise

  try:
    streams=get_streams_body_pl_type(body,pl_type)
  except:
    print "Warning: could not detect playlist type by body scan"
    raise

  return streams

def get_streams_body_pl_type(body,pl_type):
  if len(body)>200000:
    print "playlists_analyser.py: Info: too long file, must be audio data"
    raise

  try:
    if pl_type=="asx":
      streams=get_streams_asx(body)
    elif pl_type=="pls":
      streams=get_streams_pls(body)
    elif pl_type=="m3u":
      streams=get_streams_m3u(body)
    elif pl_type=="smil":
      streams=get_streams_smil(body)
    else:
      print "Fatal: Unsupported playlist type [%s]" % pl_type
      sys.exit(1)
  except:
    print "Error: no streams were detected"
    raise Exception("no_stream_detected")

  # Verify that detected streams are legitimate
  for stream_raw in streams:
    stream=stream_raw.lower()
    if (("http://" in stream) or ("rtsp://" in stream) or ("mms://" in stream) or ("mmst://" in stream) or ("mmsu://" in stream)):
      pass
    else:
      print "Error: unrecognized stream [%s]"%stream
      raise Exception("unrecognized_stream")

  return streams

def get_streams_asx(body):
  # There are ASX (XML-based) and ASF playlists that have the same mime-type
  # Luckily, we can easily discern these by first line 
  body=body.replace('\r','')

  lines=body.split("\n")
  firstline=lines[0].rstrip()
  # From the end as elements get shifted to compensate deleted element
  #for i in range(len(lines)-1,0,-1):
  #  if len(lines[i])==0:
  #    del lines[i]
  if firstline=="[Reference]":
    links=search_asf_links(body)
    if len(links)==0:
      print body
    return links

  body=get_single_line(body)

  asx_header=search_asx_header(body)
  if len(asx_header)!=0:
    #<REF HREF="http://www.granderioam.com.br/aovivo/gram.asx" />
    global asx_stream_urls_pattern1
    if 'asx_stream_urls_pattern1' not in globals():
      #asx_stream_urls_pattern1=re.compile(r'<ref href = "(.*)" />',re.IGNORECASE)
      asx_stream_urls_pattern1=re.compile(r'<ref href\ *=\ *"(.*?)"\ */*>',re.IGNORECASE)
    stream_urls=asx_stream_urls_pattern1.findall(body)

    #if len(stream_urls)==0:
    #  # Some playlists use different syntax

    #  global asx_stream_urls_pattern2
    #  if 'asx_stream_urls_pattern2' not in globals():
    #    #asx_stream_urls_pattern1=re.compile(r'<ref href = "(.*)" />',re.IGNORECASE)
    #    asx_stream_urls_pattern2=re.compile(r'<ref href\ *=\ *"(.*?)"\ *><\/ref>',re.IGNORECASE)
    #  stream_urls=asx_stream_urls_pattern2.findall(body)

    if len(stream_urls)==0:
      print "Error: no streams were found!"
      raise Exception("asx_no_streams")

    return stream_urls

  # Sometimes URLs appear as they are, without [Reference] tag and Ref1= prefix
  stream_urls=[]
  for line in lines:
    if len(line)>0:
      #print "["+line+"]"
      #print len(line)
      stream_urls.append(line)

  assert(len(stream_urls)>0)
  return stream_urls

def get_streams_pls(body):
  #[playlist] NumberOfEntries=1
  #File1=http://thehost.com/file1.ogg

  body=body.replace('\r','')

  #body=get_single_line(body)

  global stream_urls_pattern
  if 'stream_urls_pattern' not in globals():
    stream_urls_pattern=re.compile(r'^File\d+=(.*)$',re.MULTILINE)
  stream_urls=stream_urls_pattern.findall(body)

  if len(stream_urls)==0:
    print "Error: the stream is shoutcast RT playlist but no URLs??"
    raise Exception("ShoutcastNoUrls")

  assert(len(stream_urls)>0)
  return stream_urls

def get_streams_m3u(body):
  ##EXTM3U
  ##EXTINF:arl
  #http://mp3.live.tv-radio.com/arl/all/arl.mp3
  body=body.replace("\r","")

  stream_urls=[] 
  lines=body.split("\n")
  for line in body.split("\n"):
    if len(line)==0: continue
    if line.startswith('#EXTM3U'): continue
    if line.startswith('#EXTINF'): continue
    if line.startswith('#EXT-X-TARGETDURATION'): continue
    if line.startswith('#EXT-X-ENDLIST'): continue

    #print "["+line+"]"
    #print len(line)
    stream_urls.append(line.rstrip())

  assert(len(stream_urls)>0)
  return stream_urls

def get_streams_smil(body):
  print "Error: not implemented yet"
  raise

if __name__ == '__main__':
  pl_file=sys.argv[1]

  if (len(sys.argv)==2):
    #playlist type was not specified, try to detect from file extension
    fileName, dot_file_extension = os.path.splitext(pl_file)
    file_extension=dot_file_extension[1:]
    try:
      pl_type=get_pltype_by_extension(file_extension)
    except:
      raise
  else:
    try:
      pl_type=get_pltype_by_mimetype(sys.argv[2])
    except:
      pass

  print "mimetype: [%s]" % pl_type
  try:
    streams=get_streams_from_file(pl_file,pl_type)
    print "streams detected:"
    print streams
  except:
    raise
