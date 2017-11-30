def output(filename,d,limit,err_dirname):
    import csv
    import sys,os
    import errno


    #pipe sout into the log file
    try:
        os.makedirs(err_dirname)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    log_filename = os.path.splitext(os.path.basename(filename))[0]
    log_file = open(err_dirname + "/" + log_filename + ".log", "w")
    sys.stdout = log_file
    print("Line Number\t ItemID skipped")

    result = 0


    with open(filename) as inputfile:
        inputData = csv.reader(inputfile, dialect=d)
        dataHeaders = next(inputData)

        with open("out/" + os.path.basename(filename), 'w') as outfile:
            outputData = csv.writer(outfile, dialect=d)
            outputData.writerow(dataHeaders)

            for row_string in inputData:
                if (result < limit) or (limit == 0):
                        if ("NULL" not in row_string) and (len(row_string) == len(dataHeaders)):
                                result += 1
                                outputData.writerow(row_string)
                        else: print(str(result + 2) + "\t" + str(row_string[0]))  # headers and what row is it
                else: outputData.close()


def cleanData(datafile,limit):
    userData = output(datafile,'excel-tab', limit)
    return userData


import os, sys
sampleData_file = 'sample3.tsv'


print("Usage: " + os.path.basename(__file__) + " <# data lines>")
cutoff = 0 # the entire file, default value
if len(sys.argv) > 1:
    cutoff = int(sys.argv[1])

userData = cleanData(sampleData_file,cutoff,"err")
