# -*- coding: utf-8 -*-
"""
Created on Mon Aug 23 11:25:48 2021

@author: aayes
"""

import pandas as pd
import re
Text_file = open('Part1.txt')
Text = Text_file.read()

#attribute lists to append
referenceNo = []
Location = []
Provenance = []
Height = []
Diameter = []
Plate = []
Publications = []
Description = []

RecordList = Text.split('\n\n')
RecordList.pop()
#extracting reference number
for record in RecordList:
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
      breakPoints = [' from ', ' Ht.', ' ht.', ' Ht', ' Diam. c.', ' Diam', ' diam', ' PLATE']
      locationOnwards = record.split(sep=" ", maxsplit = 1)[1].strip()
      if re.search(startLine, locationOnwards):
          locationOnwards = locationOnwards.split(sep=" ", maxsplit = 1)[1].strip()
      if any(breakPoint in record for breakPoint in breakPoints):
            location = re.split(locRegex, locationOnwards)[0]
            Location.append(location)
      else:
            location = locationOnwards.split(sep = '\n', maxsplit = 1)[0].strip()
            Location.append(location)
            
for i in range(len(Location)):
    if " from " in Location[i]:
        Location[i] = Location[i].split(sep = " from ", maxsplit =1)[0]
Location.pop()
           
# #extracting Provenence
proRegex = r'Ht.|ht.|Ht|Diam. c.|Diam.|diam.|PLATE'

for record in RecordList:
    breakPoints = [' Ht.', ' ht.', ' Ht', ' Diam. c.', ' Diam', ' diam', ' PLATE']
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
       
       

#extracting height
for record in RecordList:
    if "Ht." in record:
        heightOnwards = record.split(sep="Ht.")[1]
        HeightOnwardsStrip = heightOnwards.strip()
        height = HeightOnwardsStrip.split(sep=" ", maxsplit = 1)[0]
        Height.append(height)
    elif "ht." in record:
        heightOnwards = record.split(sep="ht.")[1]
        HeightOnwardsStrip = heightOnwards.strip()
        height = HeightOnwardsStrip.split(sep=" ", maxsplit = 1)[0]
        Height.append(height)
    elif "Ht" in record:
        heightOnwards = record.split(sep="Ht")[1]
        HeightOnwardsStrip = heightOnwards.strip()
        height = HeightOnwardsStrip.split(sep=" ", maxsplit = 1)[0]
        Height.append(height)
    else:
        height = " "
        Height.append(height)

#extracting diameter
for record in RecordList:
    if "Diam. c. " in record:
        diamOnwards = record.split(sep="Diam. c. ")[1]
        diamOnwardsStrip = diamOnwards.strip()
        diameter = diamOnwardsStrip.split(sep=" ", maxsplit = 1)[0]
        Diameter.append(diameter)
    elif "Diam." in record:
        diamOnwards = record.split(sep="Diam.")[1]
        diamOnwardsStrip = diamOnwards.strip()
        diameter = diamOnwardsStrip.split(sep=" ", maxsplit = 1)[0]
        Diameter.append(diameter)
    elif "diam." in record:
        diamOnwards = record.split(sep="diam.")[1]
        diamOnwardsStrip = diamOnwards.strip()
        diameter = diamOnwardsStrip.split(sep=" ", maxsplit = 1)[0]
        Diameter.append(diameter)
    else:
        diameter = " "
        Diameter.append(diameter)

#extracting plate
for record in RecordList:
    if "PLATE" in record:
        plateOnwards = record.split(sep="PLATE")[1].strip()
        plate = plateOnwards.split('\n', 1)[0]
        Plate.append(plate)
    else:
        plate = " "
        Plate.append(plate)
        

#extracting publication
for record in RecordList:
    pubs = []
    checkPub = ' [0-9]+'
    removeList = ['above', '\\\\', ' \l.', ' r.', '(a)', '[a)']
    
    firstSplit = record.split(sep='\n', maxsplit = 1)[1]
    allPubs = re.split("\. \n", firstSplit)[0]

    if 'PLATE' in allPubs:
        allPubs = allPubs.split(sep='PLATE')[1]
        allPubs = (allPubs.split('\n')[1])

    if re.search(checkPub, allPubs):
        if allPubs[0] != "(":   #Potentially change this to an indent check for future Parts
            pubs = allPubs.split(";")

            for p in pubs:
                removeIndex = []
                for r in removeList:
                    if r in p:
                        removeIndex.append(pubs.index(p)) #record 1/99 has an r. and isn't being removed.

                removeIndex = list( dict.fromkeys(removeIndex) )
                if len(removeIndex) > 0:
                    for i in removeIndex:
                        pubs[i] = ''
                while '' in pubs:
                        pubs.remove('')
            
            publications = [p.replace("\n", "") for p in pubs] #removing \n from publications
            Publications.append(publications)

        else:
            publications = " "
            Publications.append(publications)

    else:
        publications = " "
        Publications.append(publications)
        
#extracting Desciption
for record in RecordList:
    if "(a)" in record :
        description = record.split(sep = "(a)", maxsplit = 1)[1]
        Description.append("(a) " + description)
    elif "[a)" in record:
        description = record.split(sep = "[a)", maxsplit = 1)[1]
        Description.append("[a) " + description)
    else:
        firstSplit = record.split(sep='\n', maxsplit = 1)[1]
        description = re.split("\. \n", firstSplit)
        #description = firstSplit.split(sep = '\. \n', maxsplit = 1)
        #description = firstSplit.partition("\. \n")[1]
        Description.append(description)
        

Location.append(" ")
Description.append(" ")
print(len(referenceNo))
print(len(Location))
print(len(Provenance))
print(len(Height))
print(len(Diameter))
print(len(Plate))
print(len(Publications))
print(len(Description))

        
#Writing DataFrames to a csv file
df = pd.DataFrame({'ReferenceNo': referenceNo,'Location': Location, 'Provenance': Provenance, 'Height': Height, 'Diameter': Diameter, 'Plate': Plate, 'Publications' : Publications, 'Description': Description})
df.to_csv('ExtractedAttributes.csv', index=False)
