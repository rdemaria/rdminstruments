from prologixgpib import Prologixgpib


class HP8753(object):
  def __init__(self,addr=16):
    self.comm=Prologixgpib()
    self.addr=16
    self.name=self.get_version()
  def query(self,s):
    self.comm.write(self.addr,s)
    return self.comm.read(self.addr).rstrip()
  def get_version(self):
    return self.query('IDN?')
  def __repr__(self):
    return '<%s>' % self.name



