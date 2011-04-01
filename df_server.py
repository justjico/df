#------------------------------------------------------------------------------
#           Name: df_server.py
#         Author: Isaac Chavez
#  Last Modified: 4/1/11
#    Description: This Python script demonstrates how to create a digital fountain,
#                 it reads UDP packets to decode a file.
#
#------------------------------------------------------------------------------

import socket
import struct
import random
import os
import sys
from sys import getsizeof
from numpy import frombuffer,bitwise_xor,byte,uint64


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('',4242 ))
mreq = struct.pack("=4sl", socket.inet_aton("224.51.105.104"), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

def do_xor(aa,bb):
    """Perform xor operation between aa and bb """
    size = min(getsizeof(aa), getsizeof(bb)) - 24
    print "xoring size " + repr(size)
    a=frombuffer(aa,dtype=byte)
    b=frombuffer(bb,dtype=byte)
    for x in xrange(size):
        c=bitwise_xor(a,b);
    r=c.tostring()
    return r

def decode(n,pckcount):
    """Decode packet"""
    if decoded.count(n) == 0:
      os.rename('/home/ichavez/python/Digital-Fountain/out/packet'+repr(pckcount),'/home/ichavez/python/Digital-Fountain/out/decoded'+repr(n))
      decoded.append(n)
      decoded.sort()
      if len(decoded) > 3:
          print "Im done exit now !" 
          sys.exit(0)

      #print "decoded is of size " + repr(len(decoded))
      for i in decoded:
           print repr(i)

      decode_match()

def decode_match():
    """Decode new packet and match with packet queue"""
    q = queue[:]
    for l in q:
        print "decoding packet : " + repr(l[0])
        for l2 in l[1]:
            print"   with encoded packet : " + repr(l2)
    for l in q:
        pckcount = l[0]
        cf = open('/home/ichavez/python/Digital-Fountain/out/packet'+repr(pckcount),'rb')
        curr = cf.read()
        cf.close()
        ilist = l[1][:]

        for i in ilist:
            print " looking for " + repr(i) + " in decoded" 
            if decoded.count(i) > 0:
                df = open('/home/ichavez/python/Digital-Fountain/out/decoded'+repr(i),'rb')
                ds = df.read()
                curr = do_xor(ds,curr)
                df.close()
                cf = open('/home/ichavez/python/Digital-Fountain/out/packet'+repr(pckcount),'wb')
                cf.write(curr)
                cf.close()
                l[1].remove(i)

        if len(l[1]) == 1:
            queue.remove(l)  
            decode(l[1][0],l[0])

def decode_list(d,ilist,pckcount):
    """Decode packet list"""
    if d == 1:
        decode(ilist[0],pckcount)
        return
    ilist.sort()
    #print "degree to decode is :" + repr(d)
    cf = open('/home/ichavez/python/Digital-Fountain/out/packet'+repr(pckcount),'rb')
    curr = cf.read()
    cf.close()
    listc = ilist[:]
    mod = 0
    for i in listc:
        if decoded.count(i) > 0:
            f = open('/home/ichavez/python/Digital-Fountain/out/decoded'+repr(i),'rb')
            dec = f.read()
            f.close()
            curr = do_xor(dec,curr)
            ilist.remove(i)
            mod += 1
    if mod > 0 :
        print "reduced packet by " + repr(mod)
        cf = open('/home/ichavez/python/Digital-Fountain/out/packet'+repr(pckcount),'wb')
        cf.write(curr)
        cf.close()
    if len(ilist) == 1 :
        decode(ilist[0],pckcount)
    else :
        queue.append([pckcount,ilist]) 

pckcount = 0
pcklist = []
decoded = []
queue = []
while 1:
    f = open('/home/ichavez/python/Digital-Fountain/out/packet'+repr(pckcount),'wb')
    packet = sock.recv(10240)
    size = int(packet[:3])
    key = packet[3:13]
    packet = packet[13:]
    #print "size is " + repr(size) + "and key  is " + key
    random.seed(int(key))
    d = random.randint(1,size)
    tmprng = range(size)
    f.write(packet)
    f.close()

    #print "degree was : " + repr(d) 
    count = 0
    ilist = []
    for i in range(d) :
        idx = random.randint(0,len(tmprng)-1)
        print "packet " + repr(count) + " is ->" + repr(tmprng[idx])
        ilist.append(tmprng[idx])
        del tmprng[idx]
        count += 1
    decode_list(d,ilist,pckcount)

    #print "wrote packet : " + repr(pckcount)
    pckcount += 1

