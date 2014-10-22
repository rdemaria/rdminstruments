# TODO: missing endian verification
# TODO: missing data type verification 8bit integer only
# TODO: not tested with version 1 and 2
# TODO: respect coffset

import struct
import numpy as n
import time
import os

def ctime(c):
  return time.asctime(time.gmtime(c))



staticheader="""
Byte order verification, H
Versioning number, 8s
Num digits in byte count, B
Number of bytes to the end of file, l
Number of bytes per point, B
Byte offset to beginning of curve buffer, l
Horizontal zoom scale factor, l
Horizontal zoom position, f
Vertical zoom scale factor, d
Vertical zoom position, f
Waveform label, 32s
N number of FastFrames minus one, L
Size of the waveform header, H
"""
waveheader3="""
SetType, i
WfmCnt, L
Acquisition Counter, Q
Transaction counter, Q
Slot ID, i
Is static flag, i
Wfm update specification count, L
Imp dim ref count, L
Exp dim ref count, L
Data type, i
Gen purpose counter, Q
Accumulated waveform count, L
Target accumulation count, L
Curve ref count, L
Number of requested fast frames, L
Number of acquired fast frames, L
Summary frame type, H
Pix map display format, i
Pix map max value, Q
Exp dim 1 Dim scale , d
Exp dim 1 Dim offset , d
Exp dim 1 Dim size , L
Exp dim 1 Units , 20s
Exp dim 1 Dim extent min , d
Exp dim 1 Dim extent max , d
Exp dim 1 Dim resolution , d
Exp dim 1 Dim ref point , d
Exp dim 1 Format , i
Exp dim 1 Storage type , i
Exp dim 1 N Value , 4s
Exp dim 1 Over range , 4s
Exp dim 1 Under range , 4s
Exp dim 1 High range , 4s
Exp dim 1 Low range , 4s
Exp dim 1 User scale , d
Exp dim 1 User units , 20s
Exp dim 1 User offset , d
Exp dim 1 Point density , d
Exp dim 1 HRef , d
Exp dim 1 TrigDelay , d
Exp dim 2 Dim scale , d
Exp dim 2 Dim offset , d
Exp dim 2 Dim size , L
Exp dim 2 Units , 20s
Exp dim 2 Dim extent min , d
Exp dim 2 Dim extent max , d
Exp dim 2 Dim resolution , d
Exp dim 2 Dim ref point , d
Exp dim 2 Format , i
Exp dim 2 Storage type , i
Exp dim 2 N Value , 4s
Exp dim 2 Over range , 4s
Exp dim 2 Under range , 4s
Exp dim 2 High range , 4s
Exp dim 2 Low range , 4s
Exp dim 2 User scale , d
Exp dim 2 User units , 20s
Exp dim 2 User offset , d
Exp dim 2 Point density , d
Exp dim 2 HRef , d
Exp dim 2 TrigDelay , d
Imp dim 1 Dim scale, d
Imp dim 1 Dim offset, d
Imp dim 1 Dim size, L
Imp dim 1 Units, 20s
Imp dim 1 Dim extent min, d
Imp dim 1 Dim extent max, d
Imp dim 1 Dim resolution, d
Imp dim 1 Dim ref point, d
Imp dim 1 Spacing, L
Imp dim 1 User scale , d
Imp dim 1 User units , 20s
Imp dim 1 User offset , d
Imp dim 1 Point density , d
Imp dim 1 HRef , d
Imp dim 1 TrigDelay , d
Imp dim 2 Dim scale, d
Imp dim 2 Dim offset, d
Imp dim 2 Dim size, L
Imp dim 2 Units, 20s
Imp dim 2 Dim extent min, d
Imp dim 2 Dim extent max, d
Imp dim 2 Dim resolution, d
Imp dim 2 Dim ref point, d
Imp dim 2 Spacing, L
Imp dim 2 User scale , d
Imp dim 2 User units , 20s
Imp dim 2 User offset , d
Imp dim 2 Point density , d
Imp dim 2 HRef , d
Imp dim 2 TrigDelay , d
Time Base 1 Real point spacing, L
Time Base 1 Sweep, i
Time Base 1 Type of base, i
Time Base 2 Real point spacing, L
Time Base 2 Sweep, i
Time Base 2 Type of base, i
"""

waveheader2="""
SetType, i
WfmCnt, L
Acquisition Counter, Q
Transaction counter, Q
Slot ID, i
Is static flag, i
Wfm update specification count, L
Imp dim ref count, L
Exp dim ref count, L
Data type, i
Gen purpose counter, Q
Accumulated waveform count, L
Target accumulation count, L
Curve ref count, L
Number of requested fast frames, L
Number of acquired fast frames, L
Summary frame type, H
Pix map display format, i
Pix map max value, Q
Exp dim 1 Dim scale , d
Exp dim 1 Dim offset , d
Exp dim 1 Dim size , L
Exp dim 1 Units , 20s
Exp dim 1 Dim extent min , d
Exp dim 1 Dim extent max , d
Exp dim 1 Dim resolution , d
Exp dim 1 Dim ref point , d
Exp dim 1 Format , i
Exp dim 1 Storage type , i
Exp dim 1 N Value , 4s
Exp dim 1 Over range , 4s
Exp dim 1 Under range , 4s
Exp dim 1 High range , 4s
Exp dim 1 Low range , 4s
Exp dim 1 User scale , d
Exp dim 1 User units , 20s
Exp dim 1 User offset , d
Exp dim 1 Point density , L
Exp dim 1 HRef , d
Exp dim 1 TrigDelay , d
Exp dim 2 Dim scale , d
Exp dim 2 Dim offset , d
Exp dim 2 Dim size , L
Exp dim 2 Units , 20s
Exp dim 2 Dim extent min , d
Exp dim 2 Dim extent max , d
Exp dim 2 Dim resolution , d
Exp dim 2 Dim ref point , d
Exp dim 2 Format , i
Exp dim 2 Storage type , i
Exp dim 2 N Value , 4s
Exp dim 2 Over range , 4s
Exp dim 2 Under range , 4s
Exp dim 2 High range , 4s
Exp dim 2 Low range , 4s
Exp dim 2 User scale , d
Exp dim 2 User units , 20s
Exp dim 2 User offset , d
Exp dim 2 Point density , L
Exp dim 2 HRef , d
Exp dim 2 TrigDelay , d
Imp dim 1 Dim scale, d
Imp dim 1 Dim offset, d
Imp dim 1 Dim size, L
Imp dim 1 Units, 20s
Imp dim 1 Dim extent min, d
Imp dim 1 Dim extent max, d
Imp dim 1 Dim resolution, d
Imp dim 1 Dim ref point, d
Imp dim 1 Spacing, L
Imp dim 1 User scale , d
Imp dim 1 User units , 20s
Imp dim 1 User offset , d
Imp dim 1 Point density , L
Imp dim 1 HRef , d
Imp dim 1 TrigDelay , d
Imp dim 2 Dim scale, d
Imp dim 2 Dim offset, d
Imp dim 2 Dim size, L
Imp dim 2 Units, 20s
Imp dim 2 Dim extent min, d
Imp dim 2 Dim extent max, d
Imp dim 2 Dim resolution, d
Imp dim 2 Dim ref point, d
Imp dim 2 Spacing, L
Imp dim 2 User scale , d
Imp dim 2 User units , 20s
Imp dim 2 User offset , d
Imp dim 2 Point density , L
Imp dim 2 HRef , d
Imp dim 2 TrigDelay , d
Time Base 1 Real point spacing, L
Time Base 1 Sweep, i
Time Base 1 Type of base, i
Time Base 2 Real point spacing, L
Time Base 2 Sweep, i
Time Base 2 Type of base, i
"""


waveheader1="""
SetType, i
WfmCnt, L
Acquisition Counter, Q
Transaction counter, Q
Slot ID, i
Is static flag, i
Wfm update specification count, L
Imp dim ref count, L
Exp dim ref count, L
Data type, i
Gen purpose counter, Q
Accumulated waveform count, L
Target accumulation count, L
Curve ref count, L
Number of requested fast frames, L
Number of acquired fast frames, L
Pix map display format, i
Pix map max value, Q
Exp dim 1 Dim scale , d
Exp dim 1 Dim offset , d
Exp dim 1 Dim size , L
Exp dim 1 Units , 20s
Exp dim 1 Dim extent min , d
Exp dim 1 Dim extent max , d
Exp dim 1 Dim resolution , d
Exp dim 1 Dim ref point , d
Exp dim 1 Format , i
Exp dim 1 Storage type , i
Exp dim 1 N Value , 4s
Exp dim 1 Over range , 4s
Exp dim 1 Under range , 4s
Exp dim 1 High range , 4s
Exp dim 1 Low range , 4s
Exp dim 1 User scale , d
Exp dim 1 User units , 20s
Exp dim 1 User offset , d
Exp dim 1 Point density , L
Exp dim 1 HRef , d
Exp dim 1 TrigDelay , d
Exp dim 2 Dim scale , d
Exp dim 2 Dim offset , d
Exp dim 2 Dim size , L
Exp dim 2 Units , 20s
Exp dim 2 Dim extent min , d
Exp dim 2 Dim extent max , d
Exp dim 2 Dim resolution , d
Exp dim 2 Dim ref point , d
Exp dim 2 Format , i
Exp dim 2 Storage type , i
Exp dim 2 N Value , 4s
Exp dim 2 Over range , 4s
Exp dim 2 Under range , 4s
Exp dim 2 High range , 4s
Exp dim 2 Low range , 4s
Exp dim 2 User scale , d
Exp dim 2 User units , 20s
Exp dim 2 User offset , d
Exp dim 2 Point density , L
Exp dim 2 HRef , d
Exp dim 2 TrigDelay , d
Imp dim 1 Dim scale, d
Imp dim 1 Dim offset, d
Imp dim 1 Dim size, L
Imp dim 1 Units, 20s
Imp dim 1 Dim extent min, d
Imp dim 1 Dim extent max, d
Imp dim 1 Dim resolution, d
Imp dim 1 Dim ref point, d
Imp dim 1 Spacing, L
Imp dim 1 User scale , d
Imp dim 1 User units , 20s
Imp dim 1 User offset , d
Imp dim 1 Point density , L
Imp dim 1 HRef , d
Imp dim 1 TrigDelay , d
Imp dim 2 Dim scale, d
Imp dim 2 Dim offset, d
Imp dim 2 Dim size, L
Imp dim 2 Units, 20s
Imp dim 2 Dim extent min, d
Imp dim 2 Dim extent max, d
Imp dim 2 Dim resolution, d
Imp dim 2 Dim ref point, d
Imp dim 2 Spacing, L
Imp dim 2 User scale , d
Imp dim 2 User units , 20s
Imp dim 2 User offset , d
Imp dim 2 Point density , L
Imp dim 2 HRef , d
Imp dim 2 TrigDelay , d
Time Base 1 Real point spacing, L
Time Base 1 Sweep, i
Time Base 1 Type of base, i
Time Base 2 Real point spacing, L
Time Base 2 Sweep, i
Time Base 2 Type of base, i
"""



updatespec="""
Real point offset, L
TT offset, d
Frac sec, d
Gmt sec, l
"""

curvespec="""
State flags, i
Type of check sum, i
Check sum, h
Precharge start offset, L
Data start offset, L
Postcharge start offset, L
Postcharge stop offset, L
End of curve buffer offset, L
"""


waveenums="""SetType
Single waveform set
FastFrame set

Data type
WFMDATA_SCALAR_MEAS
WFMDATA_SCALAR_CONST
WFMDATA_VECTOR
WFMDATA_PIXMAP
WFMDATA_INVALID
WFMDATA_WFMDB

Pix map display format
DSY_FORMAT_INVALID
DSY_FORMAT_YT
DSY_FORMAT_XY
DSY_FORMAT_XYZ

Format
EXPLICIT_INT16
EXPLICIT_INT32
EXPLICIT_UINT32
EXPLICIT_UINT64
EXPLICIT_FP32
EXPLICIT_FP64
EXPLICIT_UINT8 or INVALID_FORMAT
EXPLICIT_INT8
EXPLICIT_INVALID_FORMAT

Storage type
EXPLICIT_SAMPLE
EXPLICIT_MIN_MAX
EXPLICIT_VERT_HIST
EXPLICIT_HOR_HIST
EXPLICIT_ROW_ORDER
EXPLICIT_COLUMN_ORDER
EXPLICIT_INVALID_STORAGE

Sweep
SWEEP_ROLL
SWEEP_SAMPLE
SWEEP_ET
SWEEP_INVALID

Type of base
BASE_TIME
BASE_SPECTRAL_MAG
BASE_SPECTRAL_PHASE
BASE_INVALID

State flags
WFM_CURVEFLAG_YES
WFM_CURVEFLAG_NO
WFM_CURVEFLAG_MAYBE

Type of check sum
NO_CHECKSUM
CTYPE_CRC16
CTYPE_SUM16
CTYPE_CRC32
CTYPE_SUM32

Summary frame type
SUMMARY_FRAME_OFF
SUMMARY_FRAME_AVERAGE
SUMMARY_FRAME_ENVELOPE
"""

waveenums=dict([ [j.pop(0),j] for j in [i.split('\n') for i in waveenums.split('\n\n')] ])


def fmtlst(fmt):
  return [ tuple(map(str.strip,i.split(','))) for i in fmt.split('\n') if i]

def structread(data,offset,fmt):
  s=struct.calcsize(fmt)
  return struct.unpack(fmt,data[offset:offset+s])

def fullreads(data,offset,fmt,count=1):
  names,fmt=zip(*fmtlst(fmt))
  fmt='='+''.join(fmt)
  s=struct.calcsize(fmt)
  values=[]
  for i in range(count):
    values.append(struct.unpack(fmt,data[offset+s*i:offset+s+s*i]))
  values=zip(*values)
  return zip(names,values)

def fullread(data,offset,fmt):
  names,fmt=zip(*fmtlst(fmt))
  fmt='='+''.join(fmt)
  s=struct.calcsize(fmt)
  values=struct.unpack(fmt,data[offset:offset+s])
  return zip(names,values)


def debug(data,fmt,offset=0):
  for name,f in fmtlst(fmt):
    s=struct.calcsize(f)
    value,=struct.unpack(f,data[offset:offset+s])
    print '%4d %4d %-50s %-10s' % (offset,s,name,value)
    offset+=s

class wfm(object):
  def __init__(self,f):
    h=f.read(78)
    self.staticheader=dict(fullread(h,0,staticheader))
    version=self.staticheader['Versioning number']
    N=self.staticheader['N number of FastFrames minus one']
    coffset=self.staticheader['Size of the waveform header']
    h=f.read(coffset-54)
    if version[-1]=='3':
      self.waveheader=fullread(h,0,waveheader3)
    elif version[-1]=='2':
      self.waveheader=fullread(h,0,waveheader2)
    elif version[-1]=='1':
      self.waveheader=fullread(h,0,waveheader1)
    self.waveheader=dict(self.waveheader)
    self.rawwaveheader=h
    frame=n.fromfile(f,fmtlst(updatespec),count=1)
    curve=n.fromfile(f,fmtlst(curvespec),count=1)
    self.points=curve['End of curve buffer offset'][0]
    self.frames=N+1
    self.frame=n.hstack([frame,n.fromfile(f,fmtlst(updatespec),count=N)])
    self.curve=n.hstack([curve,n.fromfile(f,fmtlst(curvespec),count=N)])
    self.v=n.fromfile(f,'i1',count=self.points*self.frames).reshape((self.frames,self.points))
    self.checksum,=structread(f.read(),0,'Q')
    self.acqtime=int(frame[0][3])
    self.vscale =self.waveheader['Exp dim 1 Dim scale']
    self.voffset=self.waveheader['Exp dim 1 Dim offset']
    self.tscale =self.waveheader['Imp dim 1 Dim scale']
#    self.tsize=self.waveheader['Imp dim 1 Dim size'] #CHECK SPEC!!!
    self.tsize=self.points
    self.timeoffset=self.frame['TT offset']*self.tscale
  def check(self):
    a=n.sum(fromfile(f,'uint8')[:-8])
    if a==self.checksum:
      return True
    else:
      print 'Checksum error %d %d' % (a,self.checksum)
      return False
  def getvolt(self):
    return self.v*self.vscale+self.voffset
  def gettime(self):
    return n.arange(0,self.tsize,dtype=float)*self.tscale
  def getframetime(self):
    time=n.zeros((self.frames,self.points),dtype=float)
    time[:]=self.gettime()
    time+=self.timeoffset[:,n.newaxis]
    return time
  def getdate(self):
    return time.strftime('%y%m%d-%H%M%S',time.gmtime(self.frame['Gmt sec'][0]))
  def conv(self,tf):
    v1=n.empty(self.v.shape,dtype=float)
    for i in range(self.frames):
      v1[i]=n.fft.irfft(n.fft.rfft(self.v[i])*tf)
    return v1
  def __repr__(self):
    return '<Waveform %d Frames X %d Points>' % (self.frames,self.points)

# routines for writing matlab/octave code
filetypes=dict(c="char", b="schar", B="uchar", h="short", H="ushort",
i="int", I="uint", l="long", L="ulong", q="int64", Q="uint64",
f="float32", d="float64", s="char")

def mconv(fmt):
  names,fmt=zip(*fmtlst(fmt))
  names=[i.lower().replace(' ','_') for i in names]
  s,t=[],[]
  for i in fmt:
    if i.endswith('s'):
      s.append(int(i[:-1])); t.append('string')
    else:
      s.append(1); t.append(filetypes[i])
  return zip(*(names,s,t))


def mkread(fmt,prefix=''):
  for n,s,t in mconv(fmt):
   if t=='string':
     print '%s%s=char(fread(fid,%d,"char")\');' % (prefix,n,s)
   else:
     print '%s%s=fread(fid,%d,"%s");' % (prefix,n,s,t)


def load(fh):
  return wfm(fh).__dict__

def dump(fh,data):
  raise "Not implemented"

if __name__=='__main__':
  fn='/home/rdemaria/work/SPS/2008-06-10_measures/lowchrom14400ms5batch_long_no_clip001_Ch1.wfm'
  self=wfm(fn)
