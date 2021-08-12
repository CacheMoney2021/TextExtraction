# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 12:10:43 2021

@author: aayes
"""

import pdfplumber
import re

text = ''
pdf = pdfplumber.open("RVP_56-62.pdf")
totalpages = len(pdf.pages)
#f = open("TrialWithRE.txt", "a")

#for loop to go through pages, extract text, delete the first line (page no. and header) and append to text variable
for i in range(0, totalpages):
        PageObj = pdf.pages[i]
        Text = PageObj.extract_text()
        Text = Text.split('\n')
        del Text[0]
        Text = '\n'.join(Text)
        text += Text + '\n'
        
rows = text.split('\n')
plate = []


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


               
           
                