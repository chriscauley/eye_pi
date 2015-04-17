from django.db import models

def filter_sph(qs,key,target):
  if target == 0:
    min_max = [-0.25, 0.25]
  elif target > 0:
    min_max = [target - 0.5, target]
  #target < 0                                                           
  elif target > -0.8:
    min_max = [target, target + 0.5]
  elif target > -1.8:
    min_max = [target - 0.25, target + 0.25]
  else: # target is less than -1.8
    min_max = [target - 0.5, target + 0.5]
  return qs.filter(**{key+"__gte":min_max[0],key+"__lte":min_max[1]})

def filter_cyl(qs,key,target):
  min_max = [-target,target]
  return qs.filter(**{key+"__gte":min_max[0],key+"__lte":min_max[1]})

def filter_axis(qs,key,target):
  axis_Q = models.Q()
  for gap in range(-540,540,180):
    axis_Q = axis_Q | models.Q(**{key+"__gte":target+gap-20,key+"__lte":target+gap+20})
  return qs.filter(axis_Q)

KEYS = ['r_sph','r_cyl','r_axis','l_sph','l_cyl','l_axis'] #for xlx file
DISPLAY_KEYS = ['l_sph','r_sph','l_cyl','r_cyl','l_axis','r_axis'] # for html 

class PairManager(models.Manager):
  def filter(self,*args,**kwargs):
    values = {}
    filters = {
      "r_sph": filter_sph,
      "r_cyl": filter_cyl,
      "r_axis": filter_axis,
      "l_sph": filter_sph,
      "l_cyl": filter_cyl,
      "l_axis": filter_axis,
    }
    for key in KEYS:
      values[key] = kwargs.pop(key,0)
    qs = super(PairManager,self).filter(*args,**kwargs)
    for key in KEYS:
      qs = filters[key](qs,key,values[key])
    return qs

class Pair(models.Model):
  number = models.IntegerField()
  r_sph = models.FloatField("Right Sphere",null=True,blank=True)
  r_cyl = models.FloatField("Right Cylinder",null=True,blank=True)
  r_axis = models.IntegerField("Right Axis",null=True,blank=True)
  l_sph = models.FloatField("Left Sphere",null=True,blank=True)
  l_cyl = models.FloatField("Left Cylinder",null=True,blank=True)
  l_axis = models.IntegerField("Left Axis",null=True,blank=True)
  lens = models.CharField(max_length=32,null=True,blank=True)
  frame = models.CharField(max_length=32,null=True,blank=True)

  selected = models.BooleanField(default=False)

  objects = PairManager()
  def __unicode__(self):
    s = "%s + %s x %s \n \n%s + %s x %s"%(self.l_sph,self.l_cyl,self.l_axis,self.r_sph,self.r_cyl,self.r_axis)
    if self.frame:
      s += " (%s)"%self.frame
    return s

  def get_values(self):
    """ Return a tuple of values for template. d_ attributes are from self.cache_differences."""
    return [getattr(self,"cached_"+key) for key in DISPLAY_KEYS]
  def cache_differences(self,query):
    """ Calculate the differences between a query and a pair. """
    for key in KEYS:
      value = getattr(self,key)
      target = float(query[key])
      difference = getattr(self,key) - target
      math = "%s %s %s"%(target,"+" if difference < 0 else "-",abs(difference))

      # klass tells how far off difference is (to color square)
      # sph and cyl uses 0.25 while axis uses 10 degrees
      if 'axis' in key:
        klass = int(min(abs(difference/10),5))
      else:
        klass = int(min(abs(difference/0.25),5))
      t = (key,value,math,klass)
      setattr(self,"cached_"+key,t)

def parse_row(row):
  output = {'number': row[0]}
  for i,value in enumerate(row[1:]):
    try:
      float(value)
    except ValueError:
      print value,' is not a float'                                                                      
      return
    output[values[i][0]] = value
  return output

def from_xlx(fname):
  f = open(fname,'r')
  xlrd.open_workbook(file_choice)
  worksheet = workbook.sheet_by_name('Database')
  glasses = []
  total = 0
  for i_r in range(1,worksheet.nrows):
    row = [c.value for c in worksheet.row(i_r)]
    if not row[1]:
      continue
      
    pair = parse_row(row[:7])
    total += 1
    if pair:
      glasses.append(pair)
  print len(glasses)
