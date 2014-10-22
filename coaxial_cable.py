def model(f,c1,c2,c3):
  """Frequency response of a coaxial cable
     c1 : skin depth term effect sqrt(f)
     c2 : loss term   f
     c3 : corrugation term f**3
  """
  return exp(-a1*sqrt(2j*f)-a2*f)


class CoaxialCable(object):
  def __init__(self,length,speed=0.9):
    self.length=100
    self.speed=0.9


