# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 11:50:40 2021

@author: Mariyam Mohammed
"""
import re
import pandas as pd

shape_file = open("VaseShapesReference.txt")
shape = shape_file.read()
ShapeList = shape.split('\n')
for i in range(len(ShapeList)):
    ShapeList[i] = ShapeList[i].strip()
    #print(shape)
ShapeList.pop()

regExp = '^(?!\d+|\*|\•).*'
f = open("FilterFontSizePart3.txt")
f_read = f.read()
RecordList = f_read.split('\n\n')

   
for i in range(len(RecordList)):
    if re.search(regExp, RecordList[i]):
        if RecordList[i].upper().strip() in ShapeList:
            RecordList[i] = "SHAPE: " + RecordList[i]
        #print(i)
        else:
            RecordList[i] = ""
            

while("" in RecordList):
    RecordList.remove("")
   
regFrom = r', from | from [A-Z]'
for i in range(len(RecordList)):
    breakPoints = [' Ht.', ' ht.', ' Ht', ' Diam. c.', ' Diam', ' diam', ' PLATE', '(a)', '[a)', 'SHAPE: ']
    if not any(breakPoint in RecordList[i] for breakPoint in breakPoints):
        if re.search(regFrom, RecordList[i]):
            RecordList[i] = RecordList[i]
        else:
            RecordList[i] = ""


while("" in RecordList):
    RecordList.remove("")

#attribute lists to append
referenceNo = []
Location = []
Provenance = []
Height = []
Diameter = []
Plate = []
Publications = []
Description = []
Shape= []
Fabric = []
Technique = []
previousLocation = []

regShape = '^(?!SHAPE: ).*'

#extracting shape:
for record in RecordList:
    if 'SHAPE: ' in record:
        shape = record.split(':')[1].strip()
        continue
    Shape.append(shape)

for i in range(len(RecordList)):
    if "SHAPE: " in RecordList[i]:
        RecordList[i] = ""

while("" in RecordList):
    RecordList.remove("")
    
#replacing text
for i in range (len(RecordList)):
    RecordList[i] = RecordList[i].replace("THE RED-FIGURED VASES OF PAESTUM", "").strip()

#extracting reference number
for record in RecordList:
    if re.search(regShape, record):
        refNo = record.split(sep=" ", maxsplit = 1)[0]
        if refNo == '*':
            refNo = record.split(sep=" ", maxsplit = 2)[1]
            referenceNo.append('3-' + refNo)
        else:
            referenceNo.append('3-' + refNo)
            
for i in range(len(referenceNo)):
    referenceNo[i] = referenceNo[i].replace('*', "")
    referenceNo[i] = referenceNo[i].replace('•', "")
    referenceNo[i] = referenceNo[i].replace('/', "-")
            
# #extractiing location:
locRegex = r'Broken|broken|Max|max|Actual|actual|Ht.|ht.|Ht|Diam. c.|Diam.|diam.|PLATE'
startLine = '^\d+'

for record in RecordList:
      breakPoints = [' Broken',' broken',' Max ',' max ',' Actual ',' actual ',' Ht.', ' ht.', ' Ht', ' Diam. c.', ' Diam', ' diam', ' PLATE']
      locationOnwards = record.split(sep=" ", maxsplit = 1)[1].strip()
      if re.search(startLine, locationOnwards):
          locationOnwards = locationOnwards.split(sep=" ", maxsplit = 1)[1].strip()
      if any(breakPoint in record for breakPoint in breakPoints):
            location = re.split(locRegex, locationOnwards)[0]
            Location.append(location)
            previousLocation.append("")
      else:
            location = locationOnwards.split(sep = '\n', maxsplit = 1)[0].strip()
            Location.append(location)
            previousLocation.append("")
           
for i in range(len(Location)):
    if " from " in Location[i]:
        Location[i] = Location[i].split(sep = " from ", maxsplit =1)[0]
 
#Removing \n from final Location list
for i in range(len(Location)):
    Location[i] = Location[i].replace('\n', ' ')        
 
# Extracting previous Location
regPrev = r'\(ex |ex '
for i in range(len(Location)):
    if Location[i].startswith('(a)'):
        Location[i] = Location[i].replace('(a)', "").strip()
    if Location[i].startswith('Once '):
        prev = Location[i]
        Location[i] = ""
        prev = prev.replace("Once ", "")
        previousLocation[i] = prev
    if 'ex ' in Location[i]:
        previousLocation[i] = re.split(regPrev, Location[i])[1].strip()
        Location[i] = re.split(regPrev, Location[i])[0].strip()
       
for i in range(len(previousLocation)):
    if "(" in previousLocation[i]:
        previousLocation[i] = previousLocation[i]
    else:
        previousLocation[i] = previousLocation[i].replace(').',"")

#Removing \n from final previousLocation list
for i in range(len(previousLocation)):
    previousLocation[i] = previousLocation[i].replace('\n', ' ')

# #extracting Provenence
proRegex = r'Broken|broken|Fragments|fragments|Max|max|Actual|actual|Ht.|ht.|Ht|Diam. c.|Diam.|diam.|PLATE'

for record in RecordList:
    breakPoints = [' Broken',' broken',' Fragments',' fragments',' Max ',' max ',' Actual ',' actual ',' Ht.', ' ht.', ' Ht', ' Diam. c.', ' Diam', ' diam', ' PLATE']
    firstLine = record.split(sep = '\n', maxsplit = 1)[0]
    if "from" in firstLine and any(breakPoint in record for breakPoint in breakPoints):
        provenanceOnwards = record.split(sep="from", maxsplit = 1)[1].strip()
        provenance = re.split(proRegex, provenanceOnwards)[0]
        Provenance.append(provenance)
    elif "from" in firstLine:
        provenanceOnwards = firstLine.split(sep="from")[1].strip()
        provenance = provenanceOnwards.split('\n', 1)[0]
        Provenance.append(provenance)
    else:
        provenance = " "
        Provenance.append(provenance)
        
#Removing \n from final provenance list
for i in range(len(Provenance)):
    Provenance[i] = Provenance[i].replace('\n', ' ')

# #extracting height
heights = r'Ht.|ht.|Ht'
for record in RecordList:
    breakPoints = [' Ht.', ' ht.', ' Ht']
    if any(breakPoint in record for breakPoint in breakPoints):
        HeightOnwards = re.split(heights, record)[1].strip()
        if HeightOnwards.startswith("("): 
            HeightOnwards = HeightOnwards.split(sep = ")", maxsplit = 1)[1].strip()
        height = HeightOnwards.split(sep=" ", maxsplit = 1)[0]
        Height.append(height)
    else:
        height = " "
        Height.append(height)
        


# #extracting diameter
diams = r'diam. of base|Diam. c.|diam. c.|Diam.|diam.'
for record in RecordList:
    breakPoints = [' diam. of base', ' Diam. c.', ' diam. c.', ' Diam.', ' diam.']
    if any(breakPoint in record for breakPoint in breakPoints):
        DiamOnwards = re.split(diams, record)[1].strip()
        diameter = DiamOnwards.split(sep = " ", maxsplit = 1)[0]
        Diameter.append(diameter)
    else:
        diameter = " "
        Diameter.append(diameter)


#extracting plate
plates = r'PLATES|PLATE'
for record in RecordList:
    breakPoints = ['PLATES', 'PLATE']
    if any(breakPoint in record for breakPoint in breakPoints):
        plateOnwards = re.split(plates, record)[1].strip()
        plate = plateOnwards.split('\n', 1)[0]
        Plate.append(plate)
    else:
        plate = " "
        Plate.append(plate)

#Converting plate into number format
NewPlate = []
Text = ""

for i in range(len(Plate)): 
    plate = Plate[i].replace(" ", "-")
    plate = Plate[i].lower()
    for char in plate:
        if char.islower():
            charNum = ord(char) - 96
            Text = Text + " " + str(charNum)
        else:
            Text = Text + str(char)
    NewPlate.append(Text)
    Text = ""
    
regSpace = re.compile(r"\s+") #r'\s+'
for i in range(len(NewPlate)):
    NewPlate[i] = NewPlate[i].strip()
    NewPlate[i] = NewPlate[i].replace(",", " ")
    NewPlate[i] = regSpace.sub(" ", NewPlate[i])    
    NewPlate[i] = NewPlate[i].replace(" ", "-")
    NewPlate[i] = NewPlate[i].replace("--", "-")

imagePlate = []
refImage = []
for i in range(len(NewPlate)):
    count = NewPlate[i].count('-',0,len(NewPlate[i]))
    if count < 2:
        imagePlate.append(NewPlate[i])
        refImage.append(referenceNo[i])
    else:
        imageID = NewPlate[i].split(sep = '-', maxsplit = count)[0]
        plateList = NewPlate[i].split(sep = '-', maxsplit = count)
        for j in range(1,len(plateList)):
           imagePlate.append(imageID + '-' + plateList[j]) 
           refImage.append(referenceNo[i])

for i in range(len(imagePlate)):
    if imagePlate[i] == "":
        refImage[i] = refImage[i].replace(refImage[i], "")
        
while("" in imagePlate):
    imagePlate.remove("")
    
while("" in refImage):
    refImage.remove("")
    

# #extracting publication
for record in RecordList:
    pubs = []
    checkPub = ' [0-9]+'
    removeList = ['above', '\\\\', ' \l.',' 1.', ' r.', '(a)', '[a)']
    if '\n' in record:
        firstSplit = record.split(sep='\n', maxsplit = 1)[1]
        #if not firstSplit =="":
        allPubs = re.split("\. \n", firstSplit)[0]
        if 'PLATE' in allPubs:
            if '\n' in allPubs:
                allPubs = allPubs.split(sep='PLATE')[1]
                allPubs = (allPubs.split('\n')[1])

        if re.search(checkPub, allPubs):
            if allPubs[0] != "(":   #Potentially change this to an indent check for future Parts
                pubs = allPubs.split(";")
               
                addPub = pubs[len(pubs)-1].split('. \n')
                pubs.pop(len(pubs)-1)
                pubs.append(addPub[0])
   
                for p in pubs:
                    removeIndex = []
                    for r in removeList:
                        if r in p:
                            removeIndex.append(pubs.index(p)) #record 1/99 has an r. and isn't being removed.
   
                    removeIndex = list( dict.fromkeys(removeIndex) )
                    if len(removeIndex) > 0:
                        n = len(pubs)
                        for i in range(0, n - removeIndex[0]):
                            pubs.pop()
                        # for i in removeIndex:
                        #     pubs[i] = ''
                    while '' in pubs:
                            pubs.remove('')
   
                publications = [p.replace("\n", "") for p in pubs] #removing \n from publications
                Publications.append(publications)
                
            else:
                publications = ""
                Publications.append(publications)
   
        else:
            publications = ""
            Publications.append(publications)
    else:
        publications = ""
        Publications.append(publications)         

for i in range(len(Publications)):
    if len(Publications[i]) == 0:
        Publications[i] = ""

#Extracting description
regDesc = r'PP|PAdd|PPSupp|pp. | pi. \d+| p. \d+'
regBreakPoint = r'Ht.|ht.|Ht|Diam. c.|Diam.|diam.|PLATES|PLATE'
for record in RecordList:
    if "(a)" in record :
        description = record.split(sep = "(a)", maxsplit = 1)[1]
        Description.append("(a) " + description)
    elif "[a)" in record:
        description = record.split(sep = "[a)", maxsplit = 1)[1]
        Description.append("[a) " + description)
    elif "{a)" in record:
        description = record.split(sep = "{a)", maxsplit = 1)[1]
        Description.append("{a) " + description)       
    elif '\n' in record:
        description = record.split(sep='\n', maxsplit = 1)[1].strip()
        if re.search(regDesc,description):
            if '. \n' in description:                
                description = description.split(sep = '. \n', maxsplit=1)[1].strip()
                if re.search(regDesc,description):
                    description = description.split(sep = '. \n', maxsplit=1)[1].strip()
        if re.search(regBreakPoint, description):
            if '\n' in description:
                description = description.split(sep = '\n', maxsplit = 1)[1].strip()
        Description.append(description)   
    else:
        description = ""
        Description.append(description)
        
for i in range(len(Description)):
    if not '\n' in Description[i]:
        if 'PAdd' in Description[i]:
            Description[i] = ""
            
#Removing \n from final description list
for i in range(len(Description)):
    Description[i] = Description[i].replace('\n', ' ')

#List of Fabric and Technique
for i in range(len(RecordList)):
    Fabric.append("Paestan")

for i in range(len(RecordList)):
    Technique.append("Red-Figure")    
            
#removing punctuations from the end of elements in list to prevent it (e.g ",") to interfere with the database
puncCheck = r'[^\w\s]' #match for word, number, or space
for i in range(len(RecordList)):
    Location[i] = Location[i].strip()
    previousLocation[i] = previousLocation[i].strip()   
    Provenance[i] = Provenance[i].strip()
    Height[i] = Height[i].strip()
    Diameter[i] = Diameter[i].strip()
    Description[i] = Description[i].strip()
    if not len(Location[i]) == 0:
        if re.search(puncCheck,Location[i][-1]):
            Location[i] = Location[i][:-1]
    if not len(previousLocation[i]) == 0:
        if re.search(puncCheck,previousLocation[i][-1]):
            previousLocation[i] = previousLocation[i][:-1]            
    if not len(Provenance[i]) == 0:
        if re.search(puncCheck,Provenance[i][-1]):
            Provenance[i] = Provenance[i][:-1]
    if not len(Height[i]) == 0:
        if re.search(puncCheck,Height[i][-1]):
            Height[i] = Height[i][:-1]
    if not len(Diameter[i]) == 0:
        if re.search(puncCheck,Diameter[i][-1]):
            Diameter[i] = Diameter[i][:-1]  
    if not len(Description[i]) == 0:
        if re.search(puncCheck,Description[i][-1]):
            Description[i] = Description[i][:-1]
        
        
#Writing DataFrames to a csv file
df = pd.DataFrame({'ReferenceNo': referenceNo,'Location': Location, 'Previous Location': previousLocation, 'Provenance': Provenance, 'Height': Height, 'Diameter': Diameter, 'Publications': Publications, 'Description': Description, 'Shape': Shape, 'Fabric': Fabric, 'Technique': Technique})
df.to_csv('AttributeExtraction_p3.csv', index=False)

#writing refImage and Images plate to a csv file 
df1 = pd.DataFrame({'ReferenceNo': refImage, 'Plate': imagePlate })
df1.to_csv('PlateAttribute_p3.csv', index = False)