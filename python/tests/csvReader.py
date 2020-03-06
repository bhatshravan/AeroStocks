import csv


##### VARIABLES AND FILE NAMES #####

# DOCUMENT to read
fileName = 'sample.csv'

# DOCUMENT to create
newFileName = 'newFileName.csv'

# Header for new file
header = ['col1', 'col2', 'col3', 'col4', 'col5', 'col6', 'col7']


##### OPEN FILE TO READ #####

# Open csv file
myCSVFile = open(fileName, 'rb')

# OPTIONAL: Skip first line (header):
next(myCSVFile)

myFile = csv.reader(myCSVFile)


##### CREATE FILE TO WRITE  ####

# Create new csv file and make it appendable
# other options: w = overwrite, r = read, a = append, ab = append binary.
csvFile = open(newFileName, 'ab')

newFile = csv.writer(csvFile)

# write header to new file
newFile.writerow(header)


##### LOOP OVER DOCUMENT ####

# Alternative way to skip first line--pt1
#firstLine= True

# Loop over csv rows
for row in myFile:

    # Alternative way to skip first line--pt2
    # if firstLine:
                # firstLine=False
                # continue

    ## DO STUFF WITH EACH ROW OR VALUE ##

    # Print value in particular column
    print(row[2])

    # Print entire row
    print(row)

    # append a new value to end of row
    row.append("MyNewValue")

    # Write entire row to another document
    newFile.writerow(row)


#####CLOSE THE DOCUMENTS####

myCSVFile.close()
csvFile.close()
