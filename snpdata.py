from utils import myopen
from numpy import fromfile,loadtxt,r_
from pydspro import f2t,t2f,db2c,a2c

class s1p:
  def __init__(self,fn):
    """read file with freq, abs, angle columns"""
    acc=0
    fh=open(fn)
    while not fh.readline()[0].isdigit():
      acc+=1
    data=loadtxt(fn,skiprows=acc)
    freq,m,a= data.T
    self.t=f2t(freq)
    self.f=t2f(self.t)
    self.s=r_[[1.]*(len(self.f)-len(freq)),db2c(m)*a2c(a)]

class s4p:
  def __init__(self,fn):
    """read s4p 4 ports network analyzer ascii data file"""
    data=fromfile(fn,sep='\n')
    data=data.reshape((len(data)/33,33)).T
    names=[ 'S%d%d' % (i,j) for i in range(1,5) for j in range(1,5)]
    self.f=data[0]
    self.t=f2t(self.f)
    self.f=t2f(self.t)
    self.names=names
    for i,n in enumerate(names):
      v=zeros(len(self.f),dtype=complex)
      v[1:]=db2c(data[i*2+1])*a2c(data[i*2+2])
      v[0]=1
      setattr(self,n,v)
    self.fn=fn[:-4]


