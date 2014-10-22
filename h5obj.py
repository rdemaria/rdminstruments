import h5py
import numpy
import time
import os
import user

def warning(msg):
  print "Warning:",msg

def h5addclass(cls):
  globals()[cls.__name__]=cls

def h5listclass():
  return [i for i in globals() if hasattr(i,'__name__') ]

class h5meta(dict):
  def __init__(self,*l,**d):
    self.__dict__=self
    dict.__init__(self,*l,**d)

def _dicttoh5(v,g,k):
  gg=g.create_group(k)
  gg.attrs['class']='dict'
  for kk,vv in v.items():
    gg.attrs[repr(kk)]=repr(vv)
  return gg


def _dictfromh5(v):
  noobj={}
  for kk,vv in v.attrs.iteritems():
    if kk!='class':
      try:
        noobj[eval(kk)]=eval(vv)
      except:
        warning('%s or %s could not be evaluated') % (kk,vv)
        noobj[eval(kk)]=eval(vv)
  return noobj


class h5obj(object):
  """ Class that serialize in hdf5 objects"""
  _version='1.0'
  _desc=h5meta() #contains additional information on dataset
  def __init__(self,*args,**attrs):
    """ Initialize h5obj:
        h5obj()                      empty object
        h5obj(filename,load=load)    load from hdf5 file
        h5obj(oldobj)                copy from another object
        h5obj(key=value,...)         set attributes
    """
    self._setfilename('unnamed')
    self.timestamp='not available'
    load='full'
    if 'load' in attrs:
      load=attrs['load']
      del attrs['load']
    if len(args)==1:
      s=args[0]
      if isinstance(s,h5obj):
        self.merge(s)
      else:
        self.load(s,load=load)
    elif len(args)>1:
      msg="h5obj objects accept only one unnamed argument"
      raise "Wrong number of arguments",msg
    self.__dict__.update(attrs)
  def merge(self,a):
    """ Copy attribute from a to self"""
    self.__dict__.update(a.__dict__)
  def dump(self,fn=None):
    """ Save on filename, optionally a new fn can be provided"""
    self.timestamp=time.time()
    fh=self._h5(fn=fn,mode='w')
    self._toh5(fh)
    self._h5close()
  def load(self,fn=None,deep=False,load='full'):
    """Load from a filename, optionally a new fn can be provided"""
    fh=self._h5(fn=fn,mode='r')
    self._fromh5(fh,deep=deep,load=load)
    if  load!='demand':
      self._h5close()
  def update(self):
    """Virtual method: Update the class using cpu"""
    return self
  def _setfilename(self,fn):
    if not fn.endswith('.h5'):
      fn+='.h5'
    if fn.startswith(user.home):
      fn=fn.replace(user.home,'~')
    self.filename=fn
  def _h5(self,fn=None,mode='a'):
    if fn:
      self._setfilename(fn)
    fh=h5py.File(os.path.expanduser(self.filename),mode=mode)
    self._tempfh=fh
    return fh
  def _h5close(self):
    self._tempfh.close()
    del self._tempfh
  def _toh5(self,g):
    for k,v in self.__dict__.items():
      if not k.startswith('_'):
        if isinstance(v,numpy.ndarray):
          ds=g.create_dataset(k,data=v,compression='gzip')
          if k in self._desc:
            ds.attrs['desc']=self._desc[k]
        elif isinstance(v,int) or isinstance(v,float) \
            or isinstance(v,complex) or isinstance(v,str) \
            or isinstance(v,long) or isinstance(v,numpy.number):
          g.attrs[k]=v
        elif type(v) in [list,tuple]:
          g.attrs[k]=repr(v)
        elif isinstance(v,dict):
          _dicttoh5(v,g,k)
        elif hasattr(v,'_toh5'):
          v._toh5(g.create_group(k))
        g.attrs['class']=self.__class__.__name__
        g.attrs['classversion']=self._version
    return g
  def _fromh5(self,g,deep=False,load='full'):
    attr=dict(g.attrs.iteritems())
    clsname=attr.pop('class')
    gbl=globals()
    gbl[self.__class__.__name__]=self.__class__
    if clsname in gbl:
      cls=gbl[clsname]
    else:
      warning('class %s not found, falling back on h5obj' % clsname)
      cls=h5obj
    clsv=attr.pop('classversion')
    self.__class__=cls
    if clsv!=cls._version:
      msg="version mismatch, class %s v%s opened with v%s"
      warning(msg %(cls,clsv,cls._version))
    for k,v in attr.items():
      setattr(self,k,v)
    for k,v in g.iteritems():
      if isinstance(v,h5py.Group):
        if v.attrs['class']=='dict':
          nobj=_dictfromh5(v)
        else:
          if deep==False:
            nobj=h5obj()._fromh5(v,load='no',deep=False)
          elif  deep==True:
            nobj=h5obj()._fromh5(v,load=load,deep=True)
      elif isinstance(v,h5py.Dataset):
        if load=='full':
          nobj=v[:]
        elif load=='demand':
          nobj=v
        else:
          nobj='not loaded'
        if 'desc' in v.attrs:
          self._desc[k]=v.attrs['desc']
      setattr(self,k,nobj)
    return self
  def __repr__(self):
    cls=self.__class__.__name__
    l=len(cls)+2
    out=[]
    for k,v in sorted(self.__dict__.items()):
      if hasattr(v,'_toh5'):
        v=str(v)
      elif isinstance(v,numpy.ndarray):
        v='array %s%s' % (v.dtype.name,list(v.shape))
      out.append(' '*l+'%-15s= %s,' % (k,v))
    out[0]='%s( '%cls+out[0][l:]
    out[-1]=out[-1][:-1]+' )'
    return '\n'.join(out)
  def __str__(self):
    name=hasattr(self,'filename') and self.filename or '...'
    return '%s("%s")' %(self.__class__.__name__,name)

if __name__=='__main__':
  o=h5obj()
  o.at=1
  o.ar=[1,2,3]
  o.dump('o.h5')
  o2=h5obj(source=o)
  o2.dump('o2.h5')
  o3=h5obj('o2.h5')
  class ncls(h5obj):
    pass
  o4=ncls('o2.h5')
  o4.dump('o4.h5')

