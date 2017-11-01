def parseRange(range_s):
    low_s, high_s = range_s.split('-')
    low = float(low_s)
    high = float(high_s)
    return low, high
