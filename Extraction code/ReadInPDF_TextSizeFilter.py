# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 12:10:43 2021
@author: aayes
"""
#Testing text height in pdfplumber!!!!


import pdfplumber
import re
from pdfminer.layout import LTTextContainer, LTText
from pdfminer.high_level import extract_pages

text = ''
fileName = "RVP_Part3_69_118.pdf"
pdf = pdfplumber.open(fileName)
totalpages = len(pdf.pages)
f = open("letter.txt", "a")

MAX_TEXT_SIZE = 9.01
MAX_INDENT = 61

shapeFileIn = "VaseShapesReference.txt"
Shapes = []
SHAPE_MARKER = "SHAPE: "
f2 = open(shapeFileIn, encoding = 'latin-1')

for line in f2:
    shape = line.replace('Ê', ' ')
    shape = shape.replace('\n', '')
    Shapes.append(shape.upper())
    
f2.close()

while("" in Shapes) :
    Shapes.remove("")
while("\n" in Shapes) :
    Shapes.remove("\n")


#for loop to go through pages, extract text, delete the first line (page no. and header) and append to text variable
for i in range(0, totalpages):
        PageObj = pdf.pages[i]
        print(len(PageObj.chars))

        for j in range(0, len(PageObj.chars)):
            if PageObj.chars[j].get("size") < MAX_TEXT_SIZE:
                    Text = PageObj.chars[j].get("text")
                    count = 0
                    if PageObj.chars[j].get("x0") < MAX_INDENT:
                        text += '\n\n' + Text
                        f.writelines('\n' + '\n' + Text)
                    else:
                        text += Text #+ '\n'
                        f.writelines(Text)



f.close()       
rows = text.split('\n')
plate = []

#for loop to append all sinle character lines to their sentence
for k in range(0, len(rows)):
    if len(rows[k]) == 1:
        rows[k] = rows[k] + rows[k+2]
        rows[k+2] = rows[k+2].replace(rows[k+2], "")


#regular expression to search for each row starting with '*' or number with 1 or more space character 
regexp = '^\*|^\d+(?=[ ]{1,})'

#for loop to go through each row if regex expression satisfied append to list plate and write to text file
for j in range(0, len(rows)):
    shapeCheck = rows[j].replace('\n', '')
    shapeCheck = shapeCheck.strip()
    shapeCheck = shapeCheck.upper()   
        
    if re.search(regexp, rows[j]):
        for p_rows in range(j, len(rows)-1):
            plate.append(rows[p_rows])
            if re.search(regexp, rows[p_rows+1]):
                fplate = '\n'.join(plate)
                f = open("TrialWithRE.txt", "a")
                f.writelines(fplate + '\n' + '\n')
                f.close()
                plate = []
                break

    elif shapeCheck in Shapes:
        f = open("TrialWithRE.txt", "a")
        f.writelines('\n' + SHAPE_MARKER + shapeCheck + '\n' + '\n')
        f.close()
        
    else:
        pass
