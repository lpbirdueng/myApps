import csv
#with open("test.csv")
with open('countries.csv', 'r', newline='') as f:
    dialect = csv.Sniffer().sniff(f.read())
    dialect.delimiter = ' '
    #print("dialect = ", dialect.delimiter,dialect.doublequote,dialect.escapechar,dialect.lineterminator,dialect.quotechar,dialect.quoting,dialect.skipinitialspace)
    rows = csv.reader(f,dialect)
    for row in rows:
        print(row)
          
"""
# Set up input and output variables for the script
gpsTrack = open("C:\\Users\\luale\\Documents\\alex\\software\\py\\myApps\\gps_track.txt", "r")
 
# Set up CSV reader and process the header
csvReader = csv.reader(gpsTrack)
header = next(csvReader)
latIndex = header.index("lat")
lonIndex = header.index("long")
 
# Make an empty list
coordList = []
 
# Loop through the lines in the file and get each coordinate
for row in csvReader:
    lat = row[latIndex]
    lon = row[lonIndex]
    coordList.append([lat,lon])
    print(row)
""" 



'''
with open('names.csv', 'a') as csvfile:
    fieldnames = ['first_name', 'last_name']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow({'first_name': 'Lu', 'last_name': 'Alex'})
    writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
    writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})
'''