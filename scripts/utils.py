def output(filename,d,limit):
    import csv
    import sys
    import os

    csv.field_size_limit(sys.maxsize)

    #pipe sout into the log file
    log_file = open("out/message.log", "w")
    sys.stdout = log_file
    print("Line Number\t ItemID skipped")

    result = 0

    with open(filename) as inputfile:
        inputData = csv.reader(inputfile, dialect=d)
        dataHeaders = next(inputData)

        with open("out/" + os.path.basename(filename), 'w') as outfile:
            outputData = csv.writer(outfile, dialect=d)
            outputData.writerow(dataHeaders)
            print(dataHeaders)
            i = 0
            try:
                for row_string in inputData:
                    if (result < limit) or (limit == 0):
                            if ("NULL" not in row_string) and (len(row_string) == len(dataHeaders)):
                                    result += 1
                                    outputData.writerow(row_string)
                            else: print(str(result + 2) + "\t" + str(row_string[0]))  # headers and what row is it
                    else: outputData.close()
                    i += 1
            except Exception as e:
                print('error at line number %i' % i)
                print(e)




def cleanData(datafile,limit):
    userData = output(datafile,'excel-tab', limit)
    return userData
