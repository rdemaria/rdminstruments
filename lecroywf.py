""" module to read LECROY waveform format '.trc' extension
    see WM-RCM-E_Rev_D-2.pdf for information

"""



import struct
from numpy import array,frombuffer,dtype

import time

def readstring(fh,size):
  s=fh.read(size)
  return s.split('\x00')[0]

def readsingle(fh,fmt):
  s=struct.calcsize(fmt)
  return struct.unpack(fmt,fh.read(s))[0]

def readenum(fh,data):
  i=struct.unpack('H',fh.read(2))[0]
  return data[i]

def readtime(fh):
  fmt='dBBBBHH'
  out=struct.unpack(fmt,fh.read(struct.calcsize(fmt)))
  return dict(zip('sec min hour day month year noop'.split(),out))

def readall(fh,fmt):
  s=struct.calcsize(fmt)
  return struct.unpack(fmt,fh.read(s))

def readarray(fh,fmt,count):
  fmt=dtype(fmt)
  s=fmt.itemsize*count
  return frombuffer(fh.read(s),dtype=fmt,count=count)


RECORD_TYPE_enum="""
single_sweep interleaved histogram graph
filter_coefficient complex extrema sequence_obsolete
centered_RIS peak_detect""".split()

PROCESSING_DONE_enum="""\
no_processing fir_filter interpolated sparsed
autoscaled no_result rolling cumulative""".split()

TIMEBASE_enum={ 0  :'1_ps/div',
1  :'2_ps/div',
2  :'5_ps/div',
3  :'10_ps/div',
4  :'20_ps/div',
5  :'50_ps/div',
6  :'100_ps/div',
7  :'200_ps/div',
8  :'500_ps/div',
9  :'1_ns/div',
10 :'2_ns/div',
11 :'5_ns/div',
12 :'10_ns/div',
13 :'20_ns/div',
14 :'50_ns/div',
15 :'100_ns/div',
16 :'200_ns/div',
17 :'500_ns/div',
18 :'1_us/div',
19 :'2_us/div',
20 :'5_us/div',
21 :'10_us/div',
22 :'20_us/div',
23 :'50_us/div',
24 :'100_us/div',
25 :'200_us/div',
26 :'500_us/div',
27 :'1_ms/div',
28 :'2_ms/div',
29 :'5_ms/div',
30 :'10_ms/div',
31 :'20_ms/div',
32 :'50_ms/div',
33 :'100_ms/div',
34 :'200_ms/div',
35 :'500_ms/div',
36 :'1_s/div',
37 :'2_s/div',
38 :'5_s/div',
39 :'10_s/div',
40 :'20_s/div',
41 :'50_s/div',
42 :'100_s/div',
43 :'200_s/div',
44 :'500_s/div',
45 :'1_ks/div',
46 :'2_ks/div',
47 :'5_ks/div',
100:'EXTERNAL', }


VERT_COUPLING_enum="DC_50_Ohms ground DC_1MOhm ground AC,_1MOhm".split()
FIXED_VERT_GAIN_enum="""\
1_uV/div
2_uV/div
5_uV/div
10_uV/div
20_uV/div
50_uV/div
100_uV/div
200_uV/div
500_uV/div
1_mV/div
2_mV/div
5_mV/div
10_mV/div
20_mV/div
50_mV/div
100_mV/div
200_mV/div
500_mV/div
1_V/div
2_V/div
5_V/div
10_V/div
20_V/div
50_V/div
100_V/div
200_V/div
500_V/div
1_kV/div""".split()


WAVE_SOURCE_enum={0:'CHANNEL_1',1:'CHANNEL_2',2:'CHANNEL_3',3:'CHANNEL_4',4:'UNKOWN'}

class Params(object):
  pass


def findstart(fh):
  buff=''
  while not buff.endswith('WAVEDESC'):
    buff+=fh.read(1)
    if len(buff)>1024:
      raise ValueError
  fh.read(8)
  return len(buff)


class LecroyWF(object):
  def mktimestamp(self):
    t=self.params.TRIGGER_TIME
    sec=t['sec']
    frac,sec=int(sec-int(sec)),int(sec)
    tpl=(t["year"],t["month"],t["day"],t["hour"],t["min"],sec,0,0,0)
    self.timestamp=time.mktime(tpl)
    self.timestamp_frac=frac
  def __init__(self,fh,mode='full'):
    self.params=Params()
    self.params.DESCRIPTOR_NAME          =findstart(fh)
    self.params.TEMPLATE_NAME            =readstring(fh,16)
    self.params.COMM_TYPE                =readenum(fh,['byte','word'])
    self.params.COMM_ORDER               =readenum(fh,['HIFIRST','LOFIRST'])
    # block sizes
    self.params.WAVE_DESCRIPTOR          =readsingle(fh,'I')
    self.params.USER_TEXT                =readsingle(fh,'I')
    self.params.RES_DESC1                =readsingle(fh,'I')
    # block arrays
    self.params.TRIGTIME_ARRAY           =readsingle(fh,'I')
    self.params.RIS_TIME_ARRAY           =readsingle(fh,'I')
    self.params.RES_ARRAY1               =readsingle(fh,'I')
    self.params.WAVE_ARRAY_1             =readsingle(fh,'I')
    self.params.WAVE_ARRAY_3             =readsingle(fh,'I')
    self.params.RES_ARRAY2               =readsingle(fh,'I')
    self.params.RES_ARRAY3               =readsingle(fh,'I')
    self.params.INSTRUMENT_NAME          =readstring(fh,16)
    self.params.INSTRUMENT_NUMBER        =readsingle(fh,'I')
    self.params.TRACE_LABEL              =readstring(fh,16)
    self.params.RESERVED1                =readsingle(fh,'H')
    self.params.RESERVED2                =readsingle(fh,'H')
    # waveform
    self.params.WAVE_ARRAY_COUNT         =readsingle(fh,'I')
    self.params.PNTS_PER_SCREEN          =readsingle(fh,'I')
    self.params.FIRST_VALID_PNT          =readsingle(fh,'I')
    self.params.LAST_VALID_PNT           =readsingle(fh,'I')
    self.params.FIRST_POINT              =readsingle(fh,'I')
    self.params.SPARSING_FACTOR          =readsingle(fh,'I')
    self.params.SEGMENT_INDEX            =readsingle(fh,'I')
    self.params.SUBARRAY_COUNT           =readsingle(fh,'I')
    self.params.SWEEPS_PER_ACQ           =readsingle(fh,'I')
    self.params.POINTS_PER_PAIR          =readsingle(fh,'H')
    self.params.PAIR_OFFSET              =readsingle(fh,'H')
    self.params.VERTICAL_GAIN            =readsingle(fh,'f')
    self.params.VERTICAL_OFFSET          =readsingle(fh,'f')
    self.params.MAX_VALUE                =readsingle(fh,'f')
    self.params.MIN_VALUE                =readsingle(fh,'f')
    self.params.NOMINAL_BITS             =readsingle(fh,'H')
    self.params.NOM_SUBARRAY_COUNT       =readsingle(fh,'H')
    self.params.HORIZ_INTERVAL           =readsingle(fh,'f')
    self.params.HORIZ_OFFSET             =readsingle(fh,'d')
    self.params.PIXEL_OFFSET             =readsingle(fh,'d')
    self.params.VERTUNIT                 =readstring(fh,48)
    self.params.HORUNIT                  =readstring(fh,48)
    self.params.HORIZ_UNCERTAINTY        =readsingle(fh,'f')
    self.params.TRIGGER_TIME             =readtime(fh)
    self.params.ACQ_DURATION             =readsingle(fh,'f')
    self.params.RECORD_TYPE              =readenum(fh,RECORD_TYPE_enum)
    self.params.PROCESSING_DONE          =readenum(fh,PROCESSING_DONE_enum)
    self.params.RESERVED5                =readsingle(fh,'H')
    self.params.RIS_SWEEPS               =readsingle(fh,'H')
    self.params.TIMEBASE                 =readenum(fh,TIMEBASE_enum)
    self.params.VERT_COUPLING            =readenum(fh,VERT_COUPLING_enum)
    self.params.PROBE_ATT                =readsingle(fh,'f')
    self.params.FIXED_VERT_GAIN          =readenum(fh,FIXED_VERT_GAIN_enum)
    self.params.BANDWIDTH_LIMIT          =readenum(fh,'off on'.split())
    self.params.VERTICAL_VERNIER         =readsingle(fh,'f')
    self.params.ACQ_VERT_OFFSET          =readsingle(fh,'f')
    self.params.WAVE_SOURCE              =readenum(fh,WAVE_SOURCE_enum)
    assert self.params.USER_TEXT==0         #not tested
    assert self.params.RIS_SWEEPS==1        #not tested
#    if self.USER_TEXT:
#      self.usertext=readstring(fh,self.USER_TEXT)
#    if self.params.RIS_SWEEPS==1:
#       self.trigger_time=readarray(fh,'d',self.params.RIS_SWEEPS)

#    trigtime=readall(fh,'%dd'% self.SUBARRAY_COUNT*2)
#    data=readall(fh,'%db' % self.WAVE_ARRAY_1)
    self.segments=self.params.SUBARRAY_COUNT
    self.points=self.params.WAVE_ARRAY_COUNT/self.segments
    self.mktimestamp()
    self.fs=1/self.params.HORIZ_INTERVAL
    self.delay=self.params.HORIZ_OFFSET
    self.scale=self.params.VERTICAL_GAIN
    self.offset=self.params.VERTICAL_OFFSET
    self.label=self.params.WAVE_SOURCE
    self.vmax=self.params.MAX_VALUE
    self.vmin=self.params.MIN_VALUE
    if mode=='full':
      assert self.segments*self.points==self.params.WAVE_ARRAY_COUNT
      if self.params.SUBARRAY_COUNT>1:
        trigtime=readarray(fh,'d',self.segments*2)
      else:
        trigtime=array([0,0])
      if self.params.COMM_TYPE=='word':
        datatype='int16'
        assert self.params.WAVE_ARRAY_COUNT*2==self.params.WAVE_ARRAY_1
      elif self.params.COMM_TYPE=='byte':
        datatype='int8'
        assert self.params.WAVE_ARRAY_COUNT==self.params.WAVE_ARRAY_1
      data=readarray(fh,datatype,self.segments*self.points)

      self.trigger_time=trigtime[0::2]
      self.trigger_offset=trigtime[1::2]
      self.data=data.reshape(self.segments,self.points)

      last=fh.read(1)
      try:
        assert last=='' or last=='\n' or last==';' or last=='#'
      except:
        print 'Last byte is:%s' % last

