from vicp import WavePro
from lecroywf import LecroyWF



o=WavePro('lecroyscrub.cern.ch')


def readstring(fh,size):
  s=fh.read(size)
  print fh.tell()
  return s.split('\x00')[0]

def readsingle(fh,fmt):
  s=struct.calcsize(fmt)
  ret=struct.unpack(fmt,fh.read(s))[0]
  print fh.tell()
  return ret

def readenum(fh,data):
  i=struct.unpack('H',fh.read(2))[0]
  print fh.tell()
  return data[i]

def readtime(fh):
  fmt='dBBBBHH'
  out=struct.unpack(fmt,fh.read(struct.calcsize(fmt)))
  print fh.tell()
  return dict(zip('sec min hour day month year noop'.split(),out))

def readall(fh,fmt):
  s=struct.calcsize(fmt)
  ret=struct.unpack(fmt,fh.read(s))
  print fh.tell()
  return ret

def readarray(fh,fmt,count):
  fmt=dtype(fmt)
  s=fmt.itemsize*count
  ret=frombuffer(fh.read(s),dtype=fmt,count=count)
  print fh.tell()
  return ret



fh=open('test.trc')


DESCRIPTOR_NAME          =findstart(fh)
TEMPLATE_NAME            =readstring(fh,16)
COMM_TYPE                =readenum(fh,['byte','word'])
COMM_ORDER               =readenum(fh,['HIFIRST','LOFIRST'])
# block sizes
WAVE_DESCRIPTOR          =readsingle(fh,'L')
USER_TEXT                =readsingle(fh,'L')
RES_DESC1                =readsingle(fh,'L')
# block arrays
TRIGTIME_ARRAY           =readsingle(fh,'L')
RIS_TIME_ARRAY           =readsingle(fh,'L')
RES_ARRAY1               =readsingle(fh,'L')
WAVE_ARRAY_1             =readsingle(fh,'L')
WAVE_ARRAY_3             =readsingle(fh,'L')
RES_ARRAY2               =readsingle(fh,'L')
RES_ARRAY3               =readsingle(fh,'L')
INSTRUMENT_NAME          =readstring(fh,16)
INSTRUMENT_NUMBER        =readsingle(fh,'L')
TRACE_LABEL              =readstring(fh,16)
RESERVED1                =readsingle(fh,'H')
RESERVED2                =readsingle(fh,'H')
# waveform
WAVE_ARRAY_COUNT         =readsingle(fh,'L')
PNTS_PER_SCREEN          =readsingle(fh,'L')
FIRST_VALID_PNT          =readsingle(fh,'L')
LAST_VALID_PNT           =readsingle(fh,'L')
FIRST_POINT              =readsingle(fh,'L')
SPARSING_FACTOR          =readsingle(fh,'L')
SEGMENT_INDEX            =readsingle(fh,'L')
SUBARRAY_COUNT           =readsingle(fh,'L')
SWEEPS_PER_ACQ           =readsingle(fh,'L')
POINTS_PER_PAIR          =readsingle(fh,'H')
PAIR_OFFSET              =readsingle(fh,'H')
VERTICAL_GAIN            =readsingle(fh,'f')
VERTICAL_OFFSET          =readsingle(fh,'f')
MAX_VALUE                =readsingle(fh,'f')
MIN_VALUE                =readsingle(fh,'f')
NOMINAL_BITS             =readsingle(fh,'H')
NOM_SUBARRAY_COUNT       =readsingle(fh,'H')
HORIZ_INTERVAL           =readsingle(fh,'f')
HORIZ_OFFSET             =readsingle(fh,'d')
PIXEL_OFFSET             =readsingle(fh,'d')
VERTUNIT                 =readstring(fh,48)
HORUNIT                  =readstring(fh,48)
HORIZ_UNCERTAINTY        =readsingle(fh,'f')
TRIGGER_TIME             =readtime(fh)
ACQ_DURATION             =readsingle(fh,'f')
RECORD_TYPE              =readenum(fh,RECORD_TYPE_enum)
PROCESSING_DONE          =readenum(fh,PROCESSING_DONE_enum)
RESERVED5                =readsingle(fh,'H')
RIS_SWEEPS               =readsingle(fh,'H')
TIMEBASE                 =readenum(fh,TIMEBASE_enum)
VERT_COUPLING            =readenum(fh,VERT_COUPLING_enum)
PROBE_ATT                =readsingle(fh,'f')
FIXED_VERT_GAIN          =readenum(fh,FIXED_VERT_GAIN_enum)
BANDWIDTH_LIMIT          =readenum(fh,'off on'.split())
VERTICAL_VERNIER         =readsingle(fh,'f')
ACQ_VERT_OFFSET          =readsingle(fh,'f')
WAVE_SOURCE              =readenum(fh,WAVE_SOURCE_enum)
assert self.params.USER_TEXT==0         #not tested
assert self.params.RIS_SWEEPS==1        #not tested




