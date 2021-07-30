import PyPDF2 as pdf
import pandas as pd
import numpy as np

testFile = './LOP10page.pdf'
with open(testFile, mode='rb') as f:
    reader = pdf.PdfFileReader(f)
    wordList = []
    

    def listToString(s):
        str1 = " "
        return str1.join(s)
    
    def cleanNumber(s):
        numeric_filter = filter(str.isdigit, s)
        numeric_string = "".join(numeric_filter)
        return numeric_string

    def extractText(pageNumber):
        page = reader.getPage(pageNumber)
        text = page.extractText()
        listOfLines = text.split("\n")
        
        unwantedCharacters = ["\t", ""]
        tempWordsList = []
        for line in listOfLines:
            if line.strip() not in unwantedCharacters:
                wordsInTheLine = line.split(" ")
                tempWordsList += wordsInTheLine
        
            return tempWordsList


    for pn in range(reader.numPages):        
        tempWordList = extractText(pn)
        wordList += tempWordList
    
txt = listToString(wordList)
import re

#Remove Intro and Parts text
txtTest = txt.split("Part 1.")
txtTest.pop(0)
txt1 = listToString(txtTest)
txtTest = re.split("Part 2. ", txt1)
txt2 = listToString(txtTest)
txtTest = re.split("Part 3. ", txt2)
txtTest.pop(1)
txt3 = listToString(txtTest)

#getting Plate number (not letters!)
#8 has , rather than . 6's f is read as / 7.a is read as l.a Weird cross symbol is read as \,f. II read as U.
# 12. (cross symbol)a-b read as I2.fa-b
txt4 = re.split('( (?:[0-9]|l|I|U|S|\\\\)(?:[0-9]|\^)?(?:[0-9]|\^)?(?:\.|,)[^0-9])', txt3)
txt4.pop(0)
#Getting final plate number in document
n = txt4[len(txt4) -2]
numberOfPlates = int(cleanNumber(n))

labelPlateNumber = txt4[0::2]
everythingElse = txt4[1::2]
print(range(len(everythingElse)))

tablePlateNumbers = pd.DataFrame({
    'PlateNumber' : labelPlateNumber,
    'EverythingElse' : everythingElse
})

#tablePlateNumbers.to_csv('table1.txt', header=True, index=False, sep='\t', mode='a')

txt5 = listToString( everythingElse )
txt6 = txt5.replace("*", "")
txt7 = re.split('((\s|\*)\\\\?t?«?Ł?\^?(?:[a-h]|/){1,2}-?/?[a-g]?\s)', txt6)
while (" " in txt7):
        txt7.remove(" ")
txt8 = listToString(txt7)
#labelPlateLetter = [sub.replace('/', 'f') for sub in txt7]
#print(labelPlateLetter)
tableNumEE = []
for pn in range(len(everythingElse)):
    plateNumber = pn
    ee = everythingElse[pn]
    entry = [pn+1, ee]
    tableNumEE.append(entry)

tablePNVL = []
for vl in range(len(tableNumEE)):
    #print(tableNumEE[vl])
    eeStr = tableNumEE[vl][1]
    eeList = re.split('((\s|\*)\\\\?t?«?Ł?\^?(?:[a-h]|/){1,2}-?/?[a-g]?\s)', eeStr)

    while ("*" in eeList):
        eeList.remove("*")
    while (" " in eeList):
        eeList.remove(" ")
        
    letterList = eeList[1::2]
    labelPlateLetter = [sub.replace('/', 'f') for sub in letterList]
    desc = eeList[2::2]
    entry = [tableNumEE[vl][0], letterList, desc]
    tablePNVL.append(entry)

tableVaseID = []
titles = ["Plate Number", "Plate Letters", "Vase IDs", "Rest of text"]
tableVaseID.append(titles)

for vID in range(len(tablePNVL)):
    idStr = listToString(tablePNVL[vID][2])
    idSplit = re.split('([1-3]/[0-9]+)', idStr)
    idList = idSplit[1::2]
    word = idSplit[0::2]
    
    entry = [tablePNVL[vID][0], tablePNVL[vID][1], idList, word]
    tableVaseID.append(entry)
    

print(tableVaseID)
textfile = open('vaseTable.txt', 'w')
for element in tableVaseID:
    textfile.write(str(element) + '\n')
textfile.close()
