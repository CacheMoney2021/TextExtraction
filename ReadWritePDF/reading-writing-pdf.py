# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 16:21:59 2021

@author: aayes
"""

import pdfplumber 
import re
pdf = pdfplumber.open("RVP_56-62.pdf")

    
f = open("myfile5.txt", "w")
totalpages = len(pdf.pages)

# for i in range(0, totalpages):
#         PageObj = pdf.pages[i]
#         Text = PageObj.extract_text()
#         f.write(Text)


    
for i in range(0, totalpages):
        PageObj = pdf.pages[i]
        Text = PageObj.extract_text()
        store = re.split("((?<=\n)\*|(?<=\n)[0-9]+(?=[ ]{2,}))",Text)
        #look behind an "*" for a \n OR look behind a number for \n and look ahead for 2 or more spaces 
        #((?=[*])|(?=[1-9]+[ ]{2,}))
        #for record in store:
        for j in range(1,len(store)):
            f.write("\n" + store[j])
        
f.close()

# for record in store:
#     f.write(record + "\n")
        
        # if re.search("\n\d | \n\*", Text):
        #     #print("YES")
        #     yes = re.search("\n\d | \n\*", Text)
        #     print(yes)
        #     stored = Text.split("\n",1)
        #     #f.write(stored)
            


            
        

        