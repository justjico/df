#------------------------------------------------------------------------------
#           Name: df_client.py
#         Author: Isaac Chavez
#  Last Modified: 4/1/11
#    Description: This Python script demonstrates how to create a digital fountain,
#                 which sends out a UDP packet every 2 seconds.
#
#------------------------------------------------------------------------------

# TO-DO Implement a custom optimized random distribution rng

import socket
import random
from time import sleep,time
from numpy import frombuffer,bitwise_xor,byte,uint64
from sys import getsizeof

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

def encode_pack():
    """Encode a new digital fountain packet"""
    # TO-DO Read all packets from a source file
    snap = ['packetaa','packetab','packetac','packetad']
    size = len(snap) 
    key = int(time())
    random.seed(key)
    d = random.randint(1,size)
    count = 0
    blocko = "def"
    for i in range(d):
        # pick d random blocks
        if len(snap) > 0 :
            r = random.randint(0,len(snap)-1)
        else :
            r = 0

        #TO-DO Read dir as input or default
        f = open('/home/ichavez/python/Digital-Fountain/in/'+snap[r],'rb')
        del snap[r]
        blockn = f.read()
        if count > 0 :
            blocko = do_xor(blocko,blockn)
        else :
        blocko = blockn
        count += 1
        f.close()

    if count ==1 :
        print "sent d=1 packet " + repr(r)
    blocko = repr(size).zfill(3) + repr(key) + blocko
    return blocko
  
#TO-DO optimize!
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


while 1:
	#sock.sendto("test2", ("224.51.105.104", 4242))
	sock.sendto(encode_pack(), ("224.51.105.104", 4242))
	#TO-DO Control speed
	sleep( 5 )


