def matchColumnValue(data, column, value):
    value = str(value).lower()
    columnFilter = lambda item: value in item
    return data[data[column].apply(columnFilter)]

def filterColumnRange(data, column, range_s):
    low = min(range_s)
    high = max(range_s)
    data = data[(data[column] >= low)]
    data = data[(data[column] <= high)]
    return data

# TODO: add more filters if we have more columns to filter by
filterBank = {
    'latitude' : lambda data, rangeV: filterColumnRange(data, 'latitude', rangeV),
    'longitude': lambda data, rangeV: filterColumnRange(data, 'longitude', rangeV),
    'years'    : lambda data, rangeV: filterColumnRange(data, 'year', rangeV),
    'title'    : lambda data, value: matchColumnValue(data, 'title', value),
    'author'   : lambda data, value: matchColumnValue(data, 'author', value)
}

def filterData(filters, data):
    for key,value in filters.items():
        print('Applying filter: ', key)
        if key in filterBank:
            data = filterBank[key](data, value)
    return data
