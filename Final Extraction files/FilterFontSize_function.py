# -*- coding: utf-8 -*-
"""
Created on Sun Sep 19 11:36:56 2021

@author: aayes
"""

import pdfplumber


fileName = "RVP.pdf"
pdf = pdfplumber.open(fileName)
totalpages = len(pdf.pages)
MAX_TEXT_SIZE = 9.01
MAX_INDENT = 61

def FilterFontSize(startPage, endPage, outputFile):
    f = open(outputFile, "a")
    for i in range(startPage,endPage): #88-293 part 2
        previous_height = 0
        write = True
        PageObj = pdf.pages[i]
        for j in range(0, len(PageObj.chars)):
            if write:
                current_height = PageObj.chars[j].get("top")
                if PageObj.chars[j].get("size") < MAX_TEXT_SIZE:
                    Text = PageObj.chars[j].get("text")
                    if current_height > previous_height:
                        Text = '\n' + Text
                        previous_height = current_height
                        if 5.000 < PageObj.chars[j].get("size") < 6.00:
                            write = False
                        if write:
                            if PageObj.chars[j].get("x0") < MAX_INDENT:
                                f.writelines('\n' + Text)
                            else:
                                f.writelines(Text)
                    else:
                        if write:
                            f.writelines(Text)
            else:
                break
    f.close()  
    

FilterFontSize(55, 82, "Part1.txt")
FilterFontSize(88, 293, "Part2.txt")
FilterFontSize(301, 394, "Part3.txt") 
