""" Prologix gpib interface"""

import os
import serial
import time

class Prologixgpib(object):
  def __init__(self,port='/dev/ttyUSB0'):
    self.ser=serial.Serial('/dev/ttyUSB0',rtscts=0,timeout=1)
    self.name=self.get_version()
    self.init()
  def init(self):
    self.ser.write("++mode 1\r")
    time.sleep(0.1)
    self.ser.write("++ifc\r")
    time.sleep(0.1)
    self.ser.write("++auto 0\r")
    time.sleep(0.1)
    self.ser.write("++eoi 0\r")
    time.sleep(0.1)
  def get_version(self):
    self.ser.write("++ver\r")
    return self.ser.readline().rstrip()
  def read(self,addr):
    self.ser.write("++addr " + str(addr) + "\r")
    time.sleep(0.1)
    self.ser.write("++read eoi\r")
    return self.ser.read()
  def write(self,addr,s):
    self.ser.write("++addr " + str(addr) + "\r")
    time.sleep(0.1)
    self.ser.write(s + "\r")
  def __repr__(self):
    return '<%s>' % self.name

