from main.models import Pair, KEYS
import xlrd

def parse_row(row):
  output = {'number': row[0]}
  for i,value in enumerate(row[1:]):
    try:
      float(value)
    except ValueError:
      print '%s is not a float... %s'%(value,KEYS[i])
      value = None
    output[KEYS[i]] = value
  return output

def from_xlx(f):
  workbook = xlrd.open_workbook(f)
  worksheet = workbook.sheet_by_name('Database')
  glasses = []
  for i_r in range(1,worksheet.nrows):
    row = [c.value for c in worksheet.row(i_r)]
    if not row[1]:
      continue

    pair = parse_row(row[:7])
    if pair:
      glasses.append(pair)
  total = 0
  dups = 0
  for glass in glasses:
    print glass
    pair,new = Pair.objects.get_or_create(**glass)
    if new:
      total += 1
    else:
      dups += 1
  return total,dups

def cached_method(target,name=None):
  target.__name__ = name or target.__name__
  if target.__name__ == "<lambda>":
    raise ValueError("Using lambda functions in cached_methods causes __name__ collisions.")
  def wrapper(*args, **kwargs):
    obj = args[0]
    name = '___' + target.__name__

    if not hasattr(obj, name):
      value = target(*args, **kwargs)
      setattr(obj, name, value)

    return getattr(obj, name)
  
  return wrapper

def cached_property(target,name=None):
  return property(cached_method(target,name=name))
