def parse(file):

    params = dict()

    with open(file) as f:
        
        line = f.readline()
        while line:
            name, val = line.strip().split(',')
            params[name] = val
            line = f.readline()
    
    return params
