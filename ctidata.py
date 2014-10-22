"""Agilent Network Analyzer format"""


from numpy import *
from view import *
from pydspro import f2t

class cti(view):
  def __init__(self,fh):
    self._data=self.__dict__
    self._proto=[]
    self.version=fh.readline()
    self.comment=[]
    self.dataname=[]
    freqbegin=-1
    databegin=-1
    dataindex=-1
    for l in fh:
      l=l.strip()
      if l.startswith('!'):
        self.comment.append(l)
      elif l.startswith('NAME'):
        self.name=l
      elif l.startswith('VAR '):
        noop,varname,noop,val=l.split()
        self.npoints=int(val)
      elif l.startswith('DATA '):
        noop,name,noop=l.split()
        self.dataname.append(name)
      elif l.startswith('VAR_LIST_BEGIN'):
        self.f=empty(self.npoints,dtype=float)
        freqbegin=0
      elif l.startswith('VAR_LIST_END'):
        self.f=array(self.f)
        freqbegin=-1
      elif l.startswith('BEGIN'):
        databegin=0
        dataindex+=1
        name=self.dataname[dataindex]
        data=empty(self.npoints,dtype=complex)
        setattr(self,name,data)
      elif l.startswith('END'):
        databegin=-1
      elif freqbegin>-1:
        self.f[freqbegin]=float(l)
        freqbegin+=1
      elif databegin>-1:
        l=l.split(',')
        data[databegin]=complex(float(l[0]),float(l[1]))
        databegin+=1
  def mktime(self,points=32768):
    nfreq=linspace(0,self.f[-1],points)
    for name in self.dataname:
      data=getattr(self,name)
      newdata=array(interp(nfreq,self.f,real(data),0),dtype=complex)
      newdata+=1j*interp(nfreq,self.f,imag(data),0)
      setattr(self,name,newdata)
    self.f=nfreq
    self.t=f2t(self.f)
    return self
  def leftpad(self):
    deltaf=self.f[2]-self.f[1]
    missing=arange(self.f[0],0,-deltaf)[::-1]
    nfreq=r_[missing,self.f]
    missing=missing*0j+1
    for name in self.dataname:
      data=getattr(self,name)
      newdata=r_[missing,data]
      setattr(self,name,newdata)
    self.f=nfreq
    self.f-=self.f[0]  #BAD
    self.t=f2t(self.f)
    return self



