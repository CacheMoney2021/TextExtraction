# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 17:23:43 2021

@author: aayes
"""
import re
import pandas as pd

#Creating list of Shapes to check against
shape_file = open("VaseShapesReference.txt")
shape = shape_file.read()
ShapeList = shape.split('\n')
for i in range(len(ShapeList)):
    ShapeList[i] = ShapeList[i].strip()
ShapeList.pop()

regExp = '^(?!\d+|\*|\•).*'
f = open("Part1.txt")
f_read = f.read()
RecordList = f_read.split('\n\n')

#Labelling Shape in RecordList    
for i in range(len(RecordList)):
    if re.search(regExp, RecordList[i]):
        if RecordList[i].upper().strip() in ShapeList:
            RecordList[i] = "SHAPE: " + RecordList[i]

        else:
            RecordList[i] = ""


while("" in RecordList):
    RecordList.remove("")

#Attribute extraction    
regFrom = r' from [A-Z]'
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
pastLocation = []
Provenance = []
Height = []
Diameter = []
Plate = []
Publications = []
Description = []
Shape= []
Fabric = []
Technique = []

regShape = '^(?!SHAPE: ).*'

#extracting shape:
for record in RecordList:
    if 'SHAPE: ' in record:
        shape = record.split(':')[1].strip()
        continue
    Shape.append(shape)

#Removing Shape from RecordList:
for i in range(len(RecordList)):
    if "SHAPE: " in RecordList[i]:
        RecordList[i] = ""

while("" in RecordList):
    RecordList.remove("")

#Removing THE RED-FIGURED VASES OF PAESTUM from records 
for i in range(len(RecordList)):
    RecordList[i] = RecordList[i].replace("THE RED-FIGURED VASES OF PAESTUM", "").strip()
    

#extracting reference number
for record in RecordList:
    if re.search(regShape, record):
        refNo = record.split(sep=" ", maxsplit = 1)[0]
        if refNo == '*':
            refNo = record.split(sep=" ", maxsplit = 2)[1]
            referenceNo.append('1/*' + refNo)
        else:
            referenceNo.append('1/'+ refNo)

            
#extractiing location:
locRegex = r'Ht.|ht.|Ht|Diam. c.|Diam.|diam.|PLATE'
startLine = '^\d+'

for record in RecordList:
      #pastLocation code needs to be added
      breakPoints = [' from ', ' Ht.', ' ht.', ' Ht', ' Diam. c.', ' Diam', ' diam', ' PLATE']
      locationOnwards = record.split(sep=" ", maxsplit = 1)[1].strip()
        
      #split on any Unicode decimal digit (Reference number)
      if re.search(startLine, locationOnwards): 
          locationOnwards = locationOnwards.split(sep=" ", maxsplit = 1)[1].strip()
      
    #Break when any later attribute starts
      if any(breakPoint in record for breakPoint in breakPoints):
            location = re.split(locRegex, locationOnwards)[0]
            Location.append(location)
      else:
            location = locationOnwards.split(sep = '\n', maxsplit = 1)[0].strip()
            Location.append(location)
 
#Is this a double up?
for i in range(len(Location)):
    if " from " in Location[i]:
        Location[i] = Location[i].split(sep = " from ", maxsplit =1)[0]


#extracting Provenance
proRegex = r'Ht.|ht.|Ht|Diam. c.|Diam.|diam.|PLATE'

for record in RecordList:
    breakPoints = [' Ht.', ' ht.', ' Ht', ' Diam. c.', ' Diam', ' diam', ' PLATE']
    firstLine = record.split(sep = '\n', maxsplit = 1)[0]
    
    #Check if Provenance (preceeded by 'from') followed by other attributes
    if "from" in firstLine and any(breakPoint in record for breakPoint in breakPoints):
        provenanceOnwards = record.split(sep="from", maxsplit = 1)[1].strip()
        provenance = re.split(proRegex, provenanceOnwards)[0]
        Provenance.append(provenance)
    #Check if Provenance
    elif "from" in firstLine:
        provenanceOnwards = firstLine.split(sep="from")[1].strip()
        provenance = provenanceOnwards.split('\n', 1)[0]
        Provenance.append(provenance)
    else:
        provenance = ""
        Provenance.append(provenance)


#extracting height
heights = r'Ht.|ht.|Ht'
for record in RecordList:
    breakPoints = [' Ht.', ' ht.', ' Ht']
    
    #Check if Height attribute
    if any(breakPoint in record for breakPoint in breakPoints):
        HeightOnwards = re.split(heights, record)[1].strip()
        if HeightOnwards.startswith("("):
            HeightOnwards = HeightOnwards.split(sep = ")", maxsplit = 1)[1].strip()
        if HeightOnwards.startswith("and"):
            HeightOnwards = HeightOnwards.split(sep = " ", maxsplit = 2)[2].strip()
        height = HeightOnwards.split(sep=" ", maxsplit = 1)[0]
        Height.append(height)
    else:
        height = ""
        Height.append(height)


# #extracting diameter
diams = r'diam. of base|Diam. c.|diam. c.|Diam.|diam.'
for record in RecordList:
    breakPoints = [' diam. of base', ' Diam. c.', ' Diam.', ' diam.']
    
    #Check if Diameter attribute
    if any(breakPoint in record for breakPoint in breakPoints):
        DiamOnwards = re.split(diams, record)[1].strip()
        diameter = DiamOnwards.split(sep=" ", maxsplit = 1)[0]
        Diameter.append(diameter)
    else:
        diameter = ""
        Diameter.append(diameter)
        

#extracting plate
plates = r'PLATES|PLATE'
for record in RecordList:
    breakPoints = ['PLATES', 'PLATE']
    
    #Check if Plate
    if any(breakPoint in record for breakPoint in breakPoints):
        plateOnwards = re.split(plates, record)[1].strip()
        plate = plateOnwards.split('\n', 1)[0]
        Plate.append(plate)
    else:
        plate = " "
        Plate.append(plate)

    

#extracting publication
for record in RecordList:
    pubs = []
    checkPub = ' [0-9]+'
    removeList = ['above', '\\\\', ' \l.',' 1.', ' r.', '(a)', '[a)']
    
    #Publication never starts on first line. If no second line, no publications.
    if '\n' in record:
        firstSplit = record.split(sep='\n', maxsplit = 1)[1]
        allPubs = re.split("\. \n", firstSplit)[0]
        #If Plate info is on second line, remove Plate. 
        if 'PLATE' in allPubs:
            allPubs = allPubs.split(sep='PLATE')[1]
            allPubs = (allPubs.split('\n')[1])
            
        #If there are no numbers, there will be no publication.
        if re.search(checkPub, allPubs):
            if allPubs[0] != "(":   #Potentially change this to an indent check for future Parts
                pubs = allPubs.split(";")
                
                addPub = pubs[len(pubs)-1].split('\n')
                pubs.pop(len(pubs)-1)
                pubs.append(addPub[0])
    
                for p in pubs:
                    removeIndex = []
                    
                    #removeList is words found ONLY in description
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

       
#extracting Desciption
breakPoints = [' Ht.', ' ht.', ' Ht', ' Diam. c.', ' Diam', ' diam', ' PLATE']
regBreakPoint = r'Ht.|ht.|Ht|Diam. c.|Diam|diam|PLATES|PLATE'
regDesc = r'PP|PAdd|PPSupp|pp. | pi. \d+| p. \d+'
for record in RecordList:
    if "(a)" in record :
        description = record.split(sep = "(a)", maxsplit = 1)[1]
        Description.append("(a) " + description)
    elif "[a)" in record:
        description = record.split(sep = "[a)", maxsplit = 1)[1]
        Description.append("[a) " + description)
        
    elif '\n' in record:
        description = record.split(sep='\n', maxsplit = 1)[1].strip()
        if re.search(regDesc,description):
            description = description.split(sep = '. \n', maxsplit=1)[1].strip()
            if re.search(regDesc,description):
                description = description.split(sep = '. \n', maxsplit=1)[1].strip()
        if re.search(regBreakPoint,description):
            description = description.split(sep='\n', maxsplit =1 )[1]
        Description.append(description)
    else:
        description = ""
        Description.append(description)
        

for i in range(len(RecordList)):
    Fabric.append("Paestan")

for i in range(len(RecordList)):
    Technique.append("Red-Figure")

#Writing DataFrames to a csv file
df = pd.DataFrame({'ReferenceNo': referenceNo,'Location': Location, 'Provenance': Provenance, 'Height': Height, 'Diameter': Diameter, 'Plate': Plate, 'Publications': Publications, 'Description': Description, 'Shape': Shape, 'Fabric': Fabric, 'Technique': Technique})
df.to_csv('AttributeExtraction_p1.csv', index=False)
