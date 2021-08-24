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
fileName = "RVP_Part11_69_78.pdf"
pdf = pdfplumber.open(fileName)
totalpages = len(pdf.pages)
f = open("letter.txt", "a")

MAX_TEXT_SIZE = 9.01
MAX_INDENT = 59
#f = open("TrialWithRE.txt", "a")

#for loop to go through pages, extract text, delete the first line (page no. and header) and append to text variable
for i in range(0, totalpages):
        PageObj = pdf.pages[i]
        print(len(PageObj.chars))
        for j in range(0, len(PageObj.chars)):
            if PageObj.chars[j].get("size") < MAX_TEXT_SIZE:
                Text = PageObj.chars[j].get("text")
                
                if PageObj.chars[j].get("x0") < MAX_INDENT:
                    text += '\n\n' + Text
                    f.writelines('\n' + '\n' + Text)

                else:
                    text += Text #+ '\n'
                    f.writelines(Text)


f.close()       
rows = text.split('\n')
plate = []

print(rows)

#regular expression to search for each row starting with '*' or number with 1 or more space character 
regexp = '^\*|^\d+(?=[ ]{1,})'

#for loop to go through each row if regex expression satisfied append to list plate and write to text file
for j in range(0, len(rows)):
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
