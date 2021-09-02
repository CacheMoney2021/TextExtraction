#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 16:29:59 2021

@author: HannahStudy
"""

import pandas as pd
import csv
import re
Text_file = open('TrialWithRE.txt', encoding="ISO-8859-1")
Text = Text_file.read()

#attribute lists to append
referenceNo = []
Provenence = []
Height = []
Diameter = []
Plate = []
Publications = []
Shape = []

SHAPE_MARKER = "SHAPE:"
SHAPE = ""

RecordList = Text.split('\n\n')
RecordList.pop()

#assigning Shape
for record in RecordList:
    if ' ' in record:
        if record.split()[0] == SHAPE_MARKER:
            shape = SHAPE.replace(SHAPE, record.split(':', 1)[1])
            SHAPE = SHAPE.replace(SHAPE, shape)
        else:
            Shape.append(SHAPE)
    
        #extracting reference number
        #for record in RecordList:
            refNo = record.split(sep=" ", maxsplit = 1)[0]
            if refNo == '*':
                refNo = record.split(sep=" ", maxsplit = 2)[1]
                referenceNo.append('*' + refNo)
            else:
                referenceNo.append(refNo)
        
        #May need to check for Shape (and Artist if we get that far) before doing anything else
        #as if Shape is being assigned, none of the other attributes will be present
        
        
        
        #extracting Provenence
        #for record in RecordList:
            provNo = " "
            breakPointsHt = ["Ht", "Ht.", "ht"]
            breakPointsDiam = ["Diam. c. ", "Diam.", "diam."]
            breakPointsPlate = ["PLATE", " P L A T E"]
            numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            fuckinTrendall = "from T. "
            if len(record) == 0:
                pass
            elif record[0] == '*' or record[0] in numbers:
                vaseWithProvList = record.split('\n', 1)
                a = vaseWithProvList[0]
                if "from" in a: #checks that Provenance is included in entry
                    if fuckinTrendall not in a:
                        d = "from "
                        v = [d+e for e in a.split(d) if e]
                        v.pop(0) 
        
                        if "Ht" in v[0]:
                            w = v[0].split("Ht")
                            Provenence.append(w[0])
                            continue
                        elif "Ht." in v[0]:
                            w = v[0].split("Ht.")
                            Provenence.append(w[0])
                            continue
                        elif "ht" in v[0]:
                            w = v[0].split("ht")
                            Provenence.append(w[0])
                            continue
                        
                        if "Diam. c. " in v[0]:
                            w = v[0].split("Diam. c. ")
                            Provenence.append(w[0])
                            continue
                        elif "Diam." in v[0]:
                            w = v[0].split("Diam.")
                            Provenence.append(w[0])
                            continue
                        elif "diam." in v[0]:
                            w = v[0].split("diam.")
                            Provenence.append(w[0])
                            continue
                            
                        if "PLATE" in v[0]:
                            w = v[0].split("PLATE")
                            Provenence.append(w[0])
                            continue
                        elif "P L A T E" in v[0]: 
                            w = v[0].split("P L A T E")
                            Provenence.append(w[0])
                            continue
                        Provenence.append(v[0])
                    else:
                        Provenence.append(provNo)
                else:
                    Provenence.append(provNo)
        
        #ectracting height
        #for record in RecordList:
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
        #for record in RecordList:
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
        #for record in RecordList:
            if "PLATE" in record:
                plateOnwards = record.split(sep="PLATE")[1].strip()
                plate = plateOnwards.split('\n', 1)[0]
                Plate.append(plate)
            else:
                plate = " "
                Plate.append(plate)
        
        
        #for record in RecordList:
            pubs = []
            if '\n' in record:
                firstSplit = record.split(sep='\n', maxsplit = 1)[1]
                allPubs = re.split("\. \n", firstSplit)[0] #(, instead of .)
                if allPubs[0] != "(":   #Potentially change this to an indent check for future Parts
                    pubs = allPubs.split(";")
                    publications = [p.replace("\n", "") for p in pubs] #removing \n from publications
                    Publications.append(publications)
                    #print(publications)
                
                else:
                    publications = " "
                    Publications.append(publications)
    

for a in range(len(Shape)):
    print(referenceNo[a])
    print(Shape[a])        
# print(Shape)
print(len(Shape))
print(len(referenceNo))    
# #Writing DataFrames to a csv file 
# df = pd.DataFrame({'ReferenceNo': referenceNo, 'Shape': Shape, 'Provenence': Provenence, 'Height': Height, 'Diameter': Diameter, 'Plate': Plate, 'Publications': Publications})
# df.to_csv('AttributesPart1.csv', index=False) 
