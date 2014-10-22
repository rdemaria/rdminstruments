import os
import gzip
import time

import matplotlib.pyplot as _p
import numpy as _n
import pydspro as _m
import yaml

from datalib import view
from datalib import LecroyWF


baddata=[3,4,5,6,7,8,17,79]


def resample_peak(data,nv=None,nh=None):
  segments,points=data.shape
  if nh is not None:
    nd=_n.zeros( (segments,nh),dtype=data.dtype)
    chunk=points/nh
    for i in xrange(chunk):
      test=nd > data[:,i:chunk*nh:chunk]
      nd[:]=  _n.where(test,nd,data[:,i:chunk*nh:chunk])
    data=nd
    segments,points=data.shape
  if nv is not None:
    nd=_n.zeros( (nv,points),dtype=data.dtype)
    chunk=segments/nv
    for i in xrange(chunk):
      test=nd > data[i:chunk*nv:chunk,:]
      nd[:]=  _n.where(test,nd,data[i:chunk*nv:chunk,:])
    data=nd
  return data


def asctime(timestamp):
  t=time.localtime(timestamp)



class Channel(view):
  """
  Vertical data
  name      :  Channel identifier
  data      :  Sampled data array[segments,points]
  scale     :  Scaling factor
  offset    :  Offset term
  params    :  Dictionary of acquisition parameters
  segments  :  Number of segments
  points    :  Number of points
  values    :  data*scale + offset

  Horizontal channel
  timestamp       : seconds from epoch
  timestamp_frac  : fraction of a second from trigger_unixtime
  trigger_time    : seconds from timestamp array[segments]
  trigger_offset  : first sample time from trigger_time
  fs        : sample frequency
  delay     : trigger delay parameter
  """
  def __init__(self,trace):
    view.__init__(self)
    self._data=trace.__dict__
    self.segments,self.points=self.data.shape
  def mktime(self):
    "Make time vector"
    return _n.arange(0,self.points/self.fs,1/self.fs)
  def mkfreq(self):
    "Make freq vector"
    l=self.points/2+1
    return _n.arange(0,self.fs/2,self.fs/l/2)
  def plotOverview(self,lines=1024):
    nv=self.segments>lines*2 and lines or None
    nh=self.points>lines*2 and lines or None
    nd=resample_peak(self.data,nv,nh)
    tmax=self.points/self.fs*1e6
    ex=(0,tmax,self.trigger_time[0],self.trigger_time[-1])
    _p.imshow(nd,aspect='auto',origin='lower',extent=ex,cmap=_p.cm.spectral)
    _p.colorbar()
    _p.clim(0,128)
    _p.title(self.label)
    _p.xlabel('time [us]')
    _p.ylabel('time [s]')
  def plotWindow(self,ta=None,tb=None,sa=None,sb=None):
    if ta is None: ta=0
    if sa is None: sa=0
    if tb is None: tb=self.points-1
    if sb is None: sb=self.segments-1
    nd=self.data[sa:sb,ta:tb]
    ex=(ta/self.fs*1e6,tb/self.fs*1e6,self.trigger_time[sa],self.trigger_time[sb])
    _p.imshow(nd,aspect='auto',origin='lower',extent=ex,cmap=_p.cm.spectral)
    _p.colorbar()
    cmin= nd.min()
    cmax= nd.max()
    _p.clim(cmin,cmax)
    _p.title(self.label)
    _p.xlabel('time [us]')
    _p.ylabel('time [s]')
  def bunchdetect(self,turn=1,thrs=15):
    squarewave=_m.movavg2(abs(_m.movavg2(self.data[1],thrs))>15,thrs)>=.1
  def plot2DbyIdx(self,tidx1=0,tidx2=None):
    if tidx2 is None:
      tidx2=self.points
    nd=self.data[:,tidx1:tidx2]
    ex=(tidx1/self.fs*1e6,tidx2/self.fs*1e6,self.trigger_time[0],self.trigger_time[-1])
    _p.imshow(nd,aspect='auto',origin='lower',extent=ex,cmap=_p.cm.spectral)
    _p.colorbar()
    cmin= nd.min()
    cmax= nd.max()
    _p.clim(cmin,cmax)
    _p.title(self.label)
    _p.xlabel('time [us]')
    _p.ylabel('time [s]')
  def integrate(self,highpass=1e7):
    self.data=_n.asarray(self.data,dtype='int16')
    hp=int(self.fs/highpass)
    for i in range(self.segments):
      v=self.data[i]
      self.data[i]=-_n.cumsum(v - _m.movavg2(v,hp))




class Rawdata(view):
  """Load buttonbpm data saved in the control dirs"""
  basedir='/operations/app_store/RunData/run_fy10/fullRun/RHIC/Instrumentation/buttonBPM/'
  def __init__(self,n):
    view.__init__(self)
    if type(n) is str:
      fn=n
    else:
      fn='CXTrace%05d.trc' % n
    fn=os.path.join(self.basedir,fn)
    if fn.endswith('.gz'):
      fh=gzip.open(fn)
    elif os.path.exists(fn+'.gz'):
      fh=gzip.open(fn+'.gz')
    else:
      fh=open(fn)
    self.a=Channel(LecroyWF(fh))
    self.b=Channel(LecroyWF(fh))
    self.c=Channel(LecroyWF(fh))
    self.d=Channel(LecroyWF(fh))
    fh.close()
    metafn=os.path.join(self.basedir,'CXTrace%05d.txt' % n)
    self.a.label='Channel 1'
    self.b.label='Channel 2'
    self.c.label='Channel 3'
    self.d.label='Channel 4'
    if os.path.exists(metafn):
      metadata=yaml.load(open(metafn))
      self.a.label=metadata['ch1']
      self.b.label=metadata['ch2']
      self.c.label=metadata['ch3']
      self.d.label=metadata['ch4']
    self.points=self.a.points
    self.segments=self.a.segments
    self.fs=self.a.fs
    self.trigger_time=self.a.trigger_time
    self.trigger_offset=self.a.trigger_offset
    self.t=self.a.mktime()
    self.f=_m.t2f(self.t)
    self.timestamp=self.a.timestamp
  def asctime(self):
    t=time.localtime(self.timestamp)
    return time.strftime('%a, %d %b %Y %H:%M:%S -0500',t)
  def plotOverview(self):
    _p.subplot(221)
    self.a.plotOverview(lines=512)
    _p.subplot(222)
    self.b.plotOverview(lines=512)
    _p.subplot(223)
    self.c.plotOverview(lines=512)
    _p.subplot(224)
    self.d.plotOverview(lines=512)
    timestamp=time.ctime(self.timestamp)
    _p.suptitle('buttonBPM: peak overview' + self.asctime())
    return self
  def plotWindow(self):
    _p.subplot(221)
    self.a.plotWindow(0,5000)
    _p.subplot(222)
    self.b.plotWindow(0,5000)
    _p.subplot(223)
    self.c.plotWindow(0,5000)
    _p.subplot(224)
    self.d.plotWindow(0,5000)
    timestamp=time.ctime(self.timestamp)
    _p.suptitle('buttonBPM: zoom overview' + self.asctime())
    return self
  def integrate(self,highpass=1e7):
    self.a.integrate(highpass)
    self.b.integrate(highpass)
    self.c.integrate(highpass)
    self.d.integrate(highpass)

class RawdataLocal(Rawdata):
  """Load buttonbpm data saved in the control dirs"""
  basedir='/home/rdemaria/work/RHIC/buttonbpm/prod4'
