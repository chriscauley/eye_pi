def angle180(a):
  a = a%360
  if a > 180: return a-360
  if a <= -180: return a+360
  return a

def in_range(a,target):
  delta = 10
  a = angle180(target - delta) < angle180(a) < angle180(target + delta)
  b = angle180(target - delta) + 180 < angle180(a) < angle180(target + delta) + 180
  c = angle180(target - delta) - 180 < angle180(a) < angle180(target + delta) - 180
  if a or b or c:
    return True

def in_range2(a,target,delta=20):
  if a > 180:
    a -= 180
  if a < 180:
    a += 180
  for gap in range(-540,540,180):
    #print target-delta+gap, ' ',a, ' ', target+delta+gap
    if target-delta+gap < a < target+delta+gap:
      return True

def test(target,debug=False):
  blarg = False
  c = 0
  for i in range(0,720):
    if in_range2(target,i):
      if debug:
        print i,
      blarg = True
    elif blarg:
      c += 1
      blarg = False
      if debug:
        print '\n',
  if blarg:
    c += 1
  if not debug:
    print target,'\t',c

for j in range(-180,180,10):
  test(j)

#test(-20)
test(170,True)

#test(-180)
#in_range2(-180,360)
