# -*- coding: utf-8 -*-
"""
Created on Wed Sep  1 17:23:43 2021

@author: aayes
"""
import re


shape_file = open("Shapes.txt")
shape = shape_file.read()
ShapeList = shape.split('\n')
for i in range(len(ShapeList)):
    ShapeList[i] = ShapeList[i].strip()
    #print(shape)
ShapeList.pop()

regExp = '^(?!\d+|\*).*'
f = open("FOOTERrem.txt")
f_read = f.read()
RecordList = f_read.split('\n\n')

    
for i in range(len(RecordList)):
    if re.search(regExp, RecordList[i]):
        if RecordList[i].upper().strip() not in ShapeList:
        #print(i)
            RecordList[i] = ""

while("" in RecordList):
    RecordList.remove("")