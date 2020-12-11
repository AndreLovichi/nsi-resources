import csv

def saveAsCsv(filename, headers, rows):
    outputFile = open(filename, "w", newline="")
    dictWriter = csv.DictWriter(outputFile, headers)
    dictWriter.writeheader()
    dictWriter.writerows(rows)
