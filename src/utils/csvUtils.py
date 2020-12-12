import csv

def readCsv(filename, delimiter=","):
    inputFile = open(filename, encoding="utf8")
    rows = list(csv.DictReader(inputFile, delimiter=delimiter))
    return rows

def saveAsCsv(filename, headers, rows):
    outputFile = open(filename, "w", newline="", encoding="utf8")
    dictWriter = csv.DictWriter(outputFile, headers)
    dictWriter.writeheader()
    dictWriter.writerows(rows)
