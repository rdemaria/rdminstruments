from datalib.wfm import wfm
import os
from pydspro import t2f
from numpy import pi, exp, newaxis, sign
from numpy.fft import irfft, rfft
from matplotlib.pyplot import *

class tekdpo7254(object):
  def __init__(self,fn):
    self.a=os.path.exists(fn+'_Ch1.wfm') and wfm(open(fn+'_Ch1.wfm')) or None
    self.b=os.path.exists(fn+'_Ch2.wfm') and wfm(open(fn+'_Ch2.wfm')) or None
    self.c=os.path.exists(fn+'_Ch3.wfm') and wfm(open(fn+'_Ch3.wfm')) or None
    self.d=os.path.exists(fn+'_Ch4.wfm') and wfm(open(fn+'_Ch4.wfm')) or None
    self.all=[self.a,self.b,self.c,self.d]
    self.t=self.a.gettime()
    self.tscale=self.a.tscale
    self.offset=self.a.frame['TT offset']
    self.frames=self.a.frames
    self.f=t2f(self.t)
    self.triggerinterpolated=False
    self.label=dict(a='Ch1',b='Ch2',c='Ch3',d='Ch4')
    self.name=fn
  def trigger_interpolation(self):
    if not self.triggerinterpolated:
      offset=self.offset*self.a.tscale
      voffset=exp(2j*pi*self.f*offset[:,newaxis])
      for n in 'abcd':
        a=getattr(self,n)
        if a:
          a.v=irfft(rfft(a.v,axis=1)*voffset)
      self.triggerinterpolated=True
    else:
      print "Data already trigger interpolated"
  def plotframe(self,frame=0,trange=None,traces='abcd'):
    return frameWin(self,frame=frame,trange=trange,traces=traces,title=self.name)
  def __repr__(self):
    return str(self.all)


class frameWin(object):
  def __init__(self,tek,frame=0,trange=None,traces='abcd',title='frame'):
    self.interactive(False) # always first
    self.tek=tek
    self.frame=frame
    self.trange=trange
    self.traces=traces
    self.title=title
    self.fig=None
    self.color=dict(a='k',b='b',c='r',d='g')
    self.update()
    self.interactive(True)#always last
  def update(self):
    oldint=self._interactive
    self.interactive(False)
    tscale=self.tek.tscale
    t=self.tek.t
    data={}
    for n in self.traces:
      data[n]=getattr(self.tek,n)
    if self.trange:
      self.slice=slice(int(self.trange[0]/tscale),self.trange[1]/tscale)
    else:
      self.slice=slice(self.trange)
    t=t[self.slice]
    self.frame=self.frame%self.tek.frames
    if not self.fig or not hasattr(self.fig.figure.canvas,'mpl_connect'):
      self.fig=subplot(111)
      oldpint=rcParams['interactive']
      self.trace_plot={}
      for n,d in data.items():
        if d:
          v=d.getvolt()[self.frame][self.slice]
          p=plot(t,v,label=self.tek.label[n],color=self.color[n])[0]
        else:
          p=None
        self.trace_plot[n]=p
      xlabel('time [sec]')
      ylabel('trace [Volt]')
      grid(True)
      legend()
      self.fig.figure.canvas.mpl_connect('scroll_event',self.onscroll)
      self.fig.figure.canvas.mpl_connect('key_press_event',self.onkeypress)
    else:
      oldpint=rcParams['interactive']
      ioff()
      for n,d in data.items():
        if d:
          v=d.getvolt()[self.frame][self.slice]
          self.trace_plot[n].set_xdata(t)
          self.trace_plot[n].set_ydata(v)
    self.fig.set_title(self.title+':%s' % self.frame)
    rcParams['interactive']=oldpint
    draw()
    self.interactive(oldint) #always last
  def interactive(self,v=True):
    object.__setattr__(self,'_interactive',v)
  def __setattr__(self,k,v):
    object.__setattr__(self,k,v)
    if self._interactive:
      self.update()
  def onscroll(self,event):
    self.frame+=int(sign(event.step))
    return True
  def onkeypress(self,event):
    print event.button
    return True



