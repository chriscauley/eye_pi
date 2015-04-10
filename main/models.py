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
  axis_Q = Q()
  for gap in range(-540,540,180):
    axis_Q = axis_Q | Q(key+"__gte":target+gap-20,key+"__lte":target+gap+20)
  return qs.filter(axis_Q)

class PairManager(models.Manager):
  def filter(self,*args,**kwargs):
    values = {}
    keys = ['r_sph','r_cyl','r_axis','l_sph','l_cyl','l_axis']
    filters = (
      ("r_sph", filter_sph),
      ("r_cyl", filter_cyl),
      ("r_axis", filter_axis),
      ("l_sph", filter_sph),
      ("l_cyl", filter_cyl),
      ("l_axis", filter_axis),
    )
    for key in keys:
      values[key] = kwargs.pop(key,0)
    qs = super(PairManager,self).filter(*args,**kwargs)
    for key in keys:
      qs = filters[key](qs,key,values[key])
    return qs

class Pair(models.Model):
  r_sph = models.FloatField("Right Sphere")
  r_cyl = models.FloatField("Right Cylinder")
  r_axis = models.IntegerField("Right Axis")
  l_sph = models.FloatField("Left Sphere")
  l_cyl = models.FloatField("Left Cylinder")
  l_axis = models.IntegerField("Left Axis")
  lens = models.CharField(max_length=32,null=True,blank=True)
  frame = models.CharField(max_length=32,null=True,blank=True)

  objects = PairManager()
  def __unicode__(self):
    s = "%s + %s x %s \n \n%s + %s x %s"%(self.l_sph,self.l_cyl,self.l_axis,self.r_sph,self.r_cyl,self.r_axis)
    if self.frame:
      s += " (%s)"%self.frame
    return s
