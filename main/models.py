from django.db import models

def range_sph(qs,key,targets):
  target = targets[key]
  lr = key[0] # l or r
  lr_cyl = lr + "_cyl"
  if target == 0:
    return [-0.25, 0.25]
  elif target > 0:
    return [target - 0.5, target]

  #target < 0 requires looking at lr_cyl
  elif targets[lr_cyl] > -0.8:
    return [target, target + 0.5]
  elif targets[lr_cyl] > -1.8:
    return [target - 0.25, target + 0.25]
  else: # target is less than -1.8
    return [target - 0.5, target + 0.5]

def filter_sph(qs,key,targets):
  min_max = range_sph(qs,key,targets)
  return qs.filter(**{key+"__gte":min_max[0],key+"__lte":min_max[1]})

def range_cyl(qs,key,targets):
  target = targets[key]
  if target > 0:
    return [0,target]
  else:
    return [target,0]

def filter_cyl(qs,key,targets):
  min_max = range_cyl(qs,key,targets)
  return qs.filter(**{key+"__gte":min_max[0],key+"__lte":min_max[1]})

def filter_axis(qs,key,targets):
  target = targets[key]
  axis_Q = models.Q(**{key:0})
  for gap in range(-540,540,180):
    axis_Q = axis_Q | models.Q(**{key+"__gte":target+gap-20,key+"__lte":target+gap+20})
  return qs.filter(axis_Q)

KEYS = ['r_sph','r_cyl','r_axis','l_sph','l_cyl','l_axis'] #for xlx file
DISPLAY_KEYS = KEYS # ['l_sph','r_sph','l_cyl','r_cyl','l_axis','r_axis'] # for html 

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
    number = kwargs.pop('number',0)
    for key in KEYS:
      values[key] = kwargs.pop(key,0)
    qs = super(PairManager,self).filter(*args,**kwargs)
    if number:
      qs = qs.filter(number=number)
    for key in KEYS:
      qs = filters[key](qs,key,values)
    return qs

class Pair(models.Model):
  number = models.IntegerField()
  r_sph = models.FloatField("Right Sphere",null=True,blank=True)
  r_cyl = models.FloatField("Right Cyl",null=True,blank=True)
  r_axis = models.IntegerField("Right Axis",null=True,blank=True)
  l_sph = models.FloatField("Left Sphere",null=True,blank=True)
  l_cyl = models.FloatField("Left Cyl",null=True,blank=True)
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
    distance = 0
    for key in KEYS:
      value = getattr(self,key)
      target = float(query[key])
      if value == None: #value is unknown
        t = (key,"?","unknown","unknown")
        setattr(self,"cached_"+key,t)
        continue

      difference = getattr(self,key) - target
      if (abs(difference) > 20): #adjust phase!
        difference = 180 - abs(difference)

      math = "%s %s %s"%(target,"+" if difference < 0 else "-",abs(difference))
      if difference == 0:
        math = target

      # klass tells how far off difference is (to color square)
      # sph and cyl uses 0.25 while axis uses 10 degrees
      if 'axis' in key:
        klass = int(min(abs(difference/4),5))
      else:
        klass = int(min(abs(difference/0.25),5))
      t = (key,value,math,klass)
      distance += klass
      setattr(self,"cached_"+key,t)
    self.cached_distance = distance

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
