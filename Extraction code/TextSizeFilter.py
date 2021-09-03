import pdfplumber
import re
from pdfminer.layout import LTTextContainer, LTText
from pdfminer.high_level import extract_pages

text = ''
fileName = "RVP.pdf"
pdf = pdfplumber.open(fileName)
totalpages = len(pdf.pages)
f = open("letter.txt", "a")

MAX_TEXT_SIZE = 9.01
MAX_INDENT = 61



for i in range(55, 82):
        PageObj = pdf.pages[i]

        for j in range(0, len(PageObj.chars)):
            if PageObj.chars[j].get("size") < MAX_TEXT_SIZE:
                    Text = PageObj.chars[j].get("text")
                    count = 0
                    if PageObj.chars[j].get("x0") < MAX_INDENT:
                        text += '\n\n' + Text
                        f.writelines('\n' + '\n' + Text)
                    else:
                        text += Text + '\n'
                        f.writelines(Text)
                        
f.close()       

newF = open('paragraphRemoved.txt', 'a')
f = open("letter.txt")
F = f.read()
lines = F.split('\n')

while("" in lines):
    lines.remove("")
    
for i in range(0,len(lines)):
    if len(lines[i])==1:
        lines[i] = lines[i] + lines[i+1]
        lines[i+1] = lines[i+1].replace(lines[i+1], "")

while("" in lines):
    lines.remove("")


for line in lines:
    newF.writelines(line+'\n\n')
    
newF.close()
f.close()


