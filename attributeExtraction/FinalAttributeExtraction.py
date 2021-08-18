# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 14:31:15 2021

@author: Mariyam Mohammed
"""

import pandas as pd
import csv
import re
Text_file = open('Part1.txt')
Text = Text_file.read()

#attribute lists to append
referenceNo = []
Provenence = []
Height = []
Diameter = []
Plate = []

RecordList = Text.split('\n\n')

#extracting reference number
for record in RecordList:
    refNo = record.split(sep=" ", maxsplit = 1)[0]
    if refNo == '*':
        refNo = record.split(sep=" ", maxsplit = 2)[1]
        referenceNo.append('*' + refNo)
    else:
        referenceNo.append(refNo)    
#extracting Provenence
for record in RecordList:
    provNo = " "
    breakPointsHt = ["Ht", "Ht.", "ht"]
    breakPointsDiam = ["Diam. c. ", "Diam.", "diam."]
    breakPointsPlate = ["PLATE", " P L A T E"]
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    fuckinTrendall = "from T. "
    if record[0] == "":
        pass#Provenence.append(provNo)
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
        
#Writing DataFrames to a csv file 
df = pd.DataFrame({'ReferenceNo': referenceNo, 'Provenance': Provenence, 'Height': Height, 'Diameter': Diameter, 'Plate': Plate})
df.to_csv('AttributesPart1.csv', index=False) 
