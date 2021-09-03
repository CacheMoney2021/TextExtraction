import pdfplumber
import re
from pdfminer.layout import LTTextContainer, LTText
from pdfminer.high_level import extract_pages

text = ''
fileName = "RVP.pdf"
pdf = pdfplumber.open(fileName)
totalpages = len(pdf.pages)
# f = open("letter.txt", "a")
MAX_TEXT_SIZE = 9.01
MAX_INDENT = 61

f = open("FOOTERrem.txt", "a")

previous_height = 0
current_height = 0
count = 0

for i in range(95,96):
    write = True
    PageObj = pdf.pages[i]
    for j in range(0, len(PageObj.chars)):
        if write:
            current_height = PageObj.chars[j].get("top")
            if PageObj.chars[j].get("size") < MAX_TEXT_SIZE:
                Text = PageObj.chars[j].get("text")
                size = str(PageObj.chars[j].get("size"))
               # f2.writelines(Text + " " + size + '\n') 
                if current_height != previous_height:
                    #Text = PageObj.chars[j].get("text")
                    Text = '\n'+Text
                    #f.writelines(Text)
                    previous_height = current_height
                    if PageObj.chars[j].get("x0") < MAX_INDENT:
                        text += '\n\n' + Text
                        if 5.000 < PageObj.chars[j].get("size") < 6.000:
                            write = False
                            #print(PageObj.chars[j].get("size") , " " , PageObj.chars[j].get("text"))
                        if write:
                            f.writelines('\n'+Text)
                            text = ""
                    else:
                        if write:
                            f.writelines(Text)
                        #text += Text + '\n'
                        
                else:
                    if write:
                        f.writelines(Text)
        else:
            break
f.close()
