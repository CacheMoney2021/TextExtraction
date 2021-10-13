"""
Authors: Aayesha Mohammed, Mariyam Mohammed, Rogue Lyons
"""

import pdfplumber


fileName = "RVP.pdf"
pdf = pdfplumber.open(fileName)
totalpages = len(pdf.pages)
MAX_TEXT_SIZE = 9.01 #max font size of all records 
MAX_INDENT = 61 #Starting of all records are indented

def FilterFontSize(startPage, endPage, outputFile):
    f = open(outputFile, "a")
    for i in range(startPage,endPage):
        previous_height = 0
        write = True
        PageObj = pdf.pages[i]
        for j in range(0, len(PageObj.chars)):
            if write:
                current_height = PageObj.chars[j].get("top")
                if PageObj.chars[j].get("size") < MAX_TEXT_SIZE: #check character size is within 'MAX_TEXT_SIZE'
                    Text = PageObj.chars[j].get("text")
                    if current_height > previous_height: #Indicating start of a new line
                        Text = '\n' + Text
                        previous_height = current_height
                        if 5.000 < PageObj.chars[j].get("size") < 6.00: ##Page footers have a smaller Font Size
                            write = False
                        if write:
                            if PageObj.chars[j].get("x0") < MAX_INDENT: #Indicating start of a new record
                                f.writelines('\n' + Text)
                            else:
                                f.writelines(Text)
                    else:
                        if write:
                            f.writelines(Text)
            else:
                break
    f.close()  
    

#Calling FilterFontSize function 3 times, for the 3 parts in the RVP with the specified startPage and endPage for each part 
FilterFontSize(55, 82, "Part1.txt")
FilterFontSize(88, 293, "Part2.txt")
FilterFontSize(301, 394, "Part3.txt") 
