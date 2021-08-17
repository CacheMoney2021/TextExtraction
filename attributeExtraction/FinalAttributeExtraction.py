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
df = pd.DataFrame({'ReferenceNo': referenceNo, 'Height': Height, 'Diameter': Diameter, 'Plate': Plate})
df.to_csv('AttributesPart1.csv', index=False) 