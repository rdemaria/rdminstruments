from numpy import fromfile
from utils import myopen
# hdtl_froz2.c:   fprintf(headtail_pr, "%13.8e  %13.8e  %13.8e  %13.8e  %13.8e  %13.8e  %13.8e  %13.8e\n",zs[jmain], npr1*xoff, npr1*yoff, npr1*xpoff, npr1*ypoff, npr1*sx, npr1*sy, npr1);

class hdtldata(object):
  def __init__(self,fn,turns=None):
    slices=0
    cols=0
    for i in myopen(fn):
      if cols==0:
        cols=len(i.split())
      if i=='\n':
        break
      slices+=1
    if turns:
      t=fromfile(fn,sep='\n',count=turns)
    else:
      t=fromfile(fn,sep='\n')
      turns=len(t)/slices/cols
      if turns*slices*cols!=len(t):
        print 'FormatError:', \
              '%d uncomplete data' % (len(t)-turns*slices*cols)
        t=t[:turns*slices*cols]
    t=t.reshape(turns,slices,cols)
    self.turns,self.slices,self.cols=t.shape
    self.npr1  =t[:,:,7]
    self.zs    =t[:,:,0]
    self.xoff  =t[:,:,1]/self.npr1
    self.yoff  =t[:,:,2]/self.npr1
    self.xpoff =t[:,:,3]/self.npr1
    self.ypoff =t[:,:,4]/self.npr1
    self.sx    =t[:,:,5]/self.npr1
    self.sy    =t[:,:,6]/self.npr1
    self.t=t

if __name__=='__main__':
  print 'tfstable.py:  test OK'
