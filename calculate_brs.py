

def calculate(fname):
    brs = {}
    with open(fname, "r") as ins:
        for line in ins:
            br = line.split(',')[0].split(';')[0]
            if br is not None:
                if br not in brs:
                    brs[br] = 1
                else:
                    brs[br] += 1
    for key, value in brs.iteritems():
        print key + ", " + str(value)
    return brs

# calculate("../items.csv")

