import pdfplumber
import re
from pdfminer.layout import LTTextContainer, LTText
from pdfminer.high_level import extract_pages

text = ''
fileName = "RVP_Part3_69_118.pdf"
pdf = pdfplumber.open(fileName)
totalpages = len(pdf.pages)
MAX_TEXT_SIZE = 9.01
MAX_INDENT = 61

#Reading in Shapes
shapeFileIn = "VaseShapesReference.txt"
shape_file = open(shapeFileIn, encoding = 'latin-1')
shape = shape_file.read()
ShapeList = shape.split('\n')
for i in range(len(ShapeList)):
    ShapeList[i] = ShapeList[i].replace('Ê', ' ')
    ShapeList[i] = ShapeList[i].replace('\n', '')
    ShapeList[i] = ShapeList[i].strip()
    ShapeList[i] = ShapeList[i].upper()
while "" in ShapeList:
    ShapeList.remove("")
shape_file.close()

artistFileIn = "PainterList.txt"
artist_file = open(artistFileIn, encoding = 'latin-1')
artist = artist_file.read()
ArtistList = artist.split('\n')
for i in range(len(ArtistList)):
    ArtistList[i] = ArtistList[i].replace('Ê', ' ')
    ArtistList[i] = ArtistList[i].replace('\n', '')
    ArtistList[i] = ArtistList[i].strip()
    ArtistList[i] = ArtistList[i].upper()
while "" in ArtistList:
    ArtistList.remove("")
artist_file.close()

def checkArtist( line ):
    for i in ArtistList:
        if i in line:
            print(line)


f = open("FOOTERrem.txt", "a")

previous_height = 0
current_height = 0
count = 0

for i in range(0, 30):
    write = True
    PageObj = pdf.pages[i]
    lines = ''
    
    for j in range(0, len(PageObj.chars)):
        if write:
            current_height = PageObj.chars[j].get("top")
            if PageObj.chars[j].get("size") < MAX_TEXT_SIZE:
                Text = PageObj.chars[j].get("text")
                size = str(PageObj.chars[j].get("size"))

                if current_height != previous_height:

                    Text = '\n'+Text

                    previous_height = current_height
                    
                    if PageObj.chars[j].get("x0") < MAX_INDENT:
                        text += '\n\n' + Text
                        
                        if 5.000 < PageObj.chars[j].get("size") < 6.000:
                            write = False
                        
                        if write:
                            f.writelines('\n'+Text)
                            text = ""
                    
                    else:
                        if write:
                            f.writelines(Text)
                        
                else:
                    if write:
                        f.writelines(Text)
                        
            else:
                if PageObj.chars[j].get("x0") < MAX_INDENT: #If an entire line has been read in
                    if lines.upper().strip() in ShapeList: #If the line is in the ShapeList
                        text += '\n\n' + lines.strip()
                        #f.writelines('\n\n' + lines.strip() + '\n')
                        print(lines)

                    else:
                        #checkArtist(lines)
                        for i in ArtistList:
                            if i in lines:
                                print(lines)

                        
                    lines = PageObj.chars[j].get("text")
                else:
                    lines += PageObj.chars[j].get("text")
        
        else:
            break

f.close()
    

#Getting Entries

regExp = '^(?!\d+|\*).*'
f = open("FOOTERrem.txt")
f_read = f.read()
RecordList = f_read.split('\n\n')

    
for i in range(len(RecordList)):
    if re.search(regExp, RecordList[i]):
        if RecordList[i].upper().strip() not in ShapeList:
            RecordList[i] = ""
            
        if RecordList[i].upper().strip() in ShapeList:
             RecordList[i] = "SHAPE: " + RecordList[i]

while("" in RecordList):
    RecordList.remove("")
    
f = open("entries.txt", "a")
for record in RecordList:
    f.writelines(record + '\n\n')