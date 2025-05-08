import glob

def first(suffix = ''):
    for path in glob.iglob(f'./*/.git{suffix}'):
        return path
    
    for path in glob.iglob(f'./*/*/.git{suffix}'):
        return path