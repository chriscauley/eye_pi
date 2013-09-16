import sys, os
import xlrd
import math

def select_file():
    pwd = os.path.dirname(os.path.realpath(__file__))
    files = [f for f in os.listdir(pwd) if f.lower().endswith('xls')]
    if len(files) == 1:
        return files[0]
    if len(files) == 0:
        print "No file could be found. Is it in the same directory as the program?"
        exit()
    print "The following excel files are available:"
    for i,fname in enumerate(files):
        print i,": ",fname
    try:
        return os.path.join(pwd,files[int(raw_input("Select a file: "))])
    except (ValueError,IndexError):
        print "Invalid choice, try again..."
        return select_file()

def number_input(s):
    while True:
        value = raw_input(s)
        try:
            return float(value)
        except ValueError:
            print "Please enter a number."

values = [
    ("r_sph","right sphere"),
    ("r_cyl","right cylinder"),
    ("r_axis","right axis"),
    ("l_sph","left sphere"),
    ("l_cyl","left cylinder"),
    ("l_axis","left axis"),
    ]

def get_input():
    output = {}
    for key,name in values:
        output[key] = number_input("What is the %s? "%name)

def parse_row(row):
    output = {'number': row[0]}
    for i,value in enumerate(row[1:]):
        try:
            float(value)
        except ValueError:
            #print value,' is not a float'
            return
        output[values[i][0]] = value
    return output

def filter_sph(lr_sph,target,glasses,debug=False):
    if target == 0:
        out = [g for g in glasses if abs(g[lr_sph]) <= 0.25]
    elif target > 0:
        out = [g for g in glasses if target - 0.5 <= g[lr_sph] <= target]
    #target < 0
    elif target > -0.8:
        out = [g for g in glasses if target <= g[lr_sph] <= target + 0.5]
    elif target > -1.8:
        out = [g for g in glasses if target - 0.25 <= g[lr_sph] <= target + 0.25]
    else:
        out = [g for g in glasses if target - 0.5 <= g[lr_sph] <= target + 0.5]
    rejects = []
    if debug:
        rejects = [g for g in glasses if not g in out]
    return out,rejects

def filter_cyl(lr_cyl,target,glasses,debug=False):
    out = [g for g in glasses if abs(target) >= abs(g[lr_cyl])]
    rejects = []
    if debug:
        rejects = [g for g in glasses if abs(target) < abs(g[lr_cyl])]
    return out,rejects

def in_range(a,target,delta=20):
    if a > 180:
        a -= 180
    if a < 180:
        a += 180
    for gap in range(-540,540,180):
        if target-delta+gap <= a <= target+delta+gap:
            return True

def filter_axis(lr_axis,target,glasses,debug=False):
    out = []
    rejects = []
    for g in glasses:
        if in_range(g[lr_axis],target):
            out.append(g)
        else:
            if debug:
                rejects.append(g)
    return out,rejects

functions = (
    ("r_sph", filter_sph),
    ("r_cyl", filter_cyl),
    ("r_axis", filter_axis),
    ("l_sph", filter_sph),
    ("l_cyl", filter_cyl),
    ("l_axis", filter_axis),
    )

def eval_rejects(key,target,rejects):
    values = [r[key] for r in rejects]
    upper = sorted([v for v in values if v > target]) or [None,None]
    lower = sorted([v for v in values if v < target]) or [None,None]
    print key," target value: ",target
    print key," lower values: %s,%s"%(lower[0],lower[-1])
    print key," upper values: %s,%s"%(upper[0],upper[-1])
    print ""

if __name__ == "__main__":
    debug = False
    if len(sys.argv) > 1 and sys.argv[1] == "debug":
        debug = True
    file_choice = select_file()
    workbook = xlrd.open_workbook(file_choice)
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
    print "%s/%s glasses successfully read from excel file"%(len(glasses),total)
    if debug:
        target_glasses = {
            'r_sph':-2,
            'r_cyl':-10,
            'r_axis':170,
            'l_sph':-2,
            'l_cyl':-10,
            'l_axis':170
            }
    else:
        target_glasses = get_input()
    filter_axis('r_axis',50,glasses)
    for key,func in functions:
        new_glasses,rejects = func(key,target_glasses[key],glasses,debug)
        if debug:
            print key, " matched out %s glasses"%len(new_glasses)
            eval_rejects(key,target_glasses[key],rejects)
        else:
            glasses = new_glasses
            print len(glasses)," glasses left after ",key
    if not debug:
        print "Found %s matching pairs!"%len(glasses)
        all_keys = ["number"]+[i[0] for i in functions]
        print "\t".join(all_keys)
        print "TARGET\t","\t".join([str(target_glasses[key]) for key in all_keys[1:]])
        for g in glasses:
            print "\t".join([str(g[key]) for key in all_keys])
