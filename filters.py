from utils import parseRange

def matchColumnValue(data, column, value):
    value = str(value).lower()
    columnFilter = lambda item: item.lower().startswith(value)
    return data[data[column].apply(columnFilter)]

def filterColumnRange(data, column, range_s):
    low, high = parseRange(range_s)
    data = data[(data[column] >= low)]
    data = data[(data[column] <= high)]
    return data

# TODO: add more filters if we have more columns to filter by
filterBank = {
    'latitude' : lambda data, rangeV: filterColumnRange(data, 'latitude', rangeV),
    'longitude': lambda data, rangeV: filterColumnRange(data, 'longitude', rangeV),
    'years'    : lambda data, rangeV: filterColumnRange(data, 'year', rangeV),
    'title'    : lambda data, value: matchColumnValue(data, 'title', value)
}

def filterData(filters, data):
    for key,value in filters.iteritems():
        print 'Applying filter: ', key
        if key in filterBank:
            data = filterBank[key](data, value)
    return data
