# -*- coding: utf-8 -*-
"""
Created on Sat Jul 24 16:40:49 2021

@author: aayes
"""

from PyPDF2 import PdfFileReader
import re 

f = open("TextPDF.pdf", "rb")
pdf = PdfFileReader(f)
wordsList = []
unwantedCharacters = ["", ",", ".", "-", "("]

page = pdf.getPage(0)
text = page.extractText()
#listOfLines = text.split("\n")

x = re.split("\s", text)
y = re.split(r"\.", text)
z = re.findall("PLATE", text)
a = re.split("PLATE", text)
b = re.split("\*\d",text)
page2 = pdf.getPage(1)
text2 = page2.extractText()
z2 = re.findall("PLATE", text2)

#function to count instances of "\*\d
def countoverlappingdistinct(pattern, thestring):
  total = 0
  start = 0
  there = re.compile(pattern)
  while True:
    mo = there.search(thestring, start)
    if mo is None: return total
    total += 1
    start = 1 + mo.start()
    
regexp = re.compile("\*\d")
if regexp.search(text):
  print("matched")


wordsList = []
unwantedCharacters = ["", ",", ".", "-"]

#for line in listOfLines:
    #if line.strip() not in unwantedCharacters: 
        # wordsInTheLine = line.split(" ")
        # wordsList += wordsInTheLine
        # print(line)
        
#print(wordsList)

def extractText(pageNumber):
    page = pdf.getPage(pageNumber)
    text = page.extractText()
    listOfLines = text.split("\n")
    
    unwantedCharacters = ["", ",", ".", "-", "("]
    tempWordsList = []
    for line in listOfLines:
        if line.strip() not in unwantedCharacters: 
            wordsInTheLine = line.split(" ")
            tempWordsList += wordsInTheLine
            
        print(line) #this displayes the entire pdf as it is
            
           # return line
#    print(wordsList)

    return tempWordsList

for pageNumber in range(pdf.numPages):
    tempWordsList = extractText(pageNumber)
    wordsList += tempWordsList
    
print(wordsList)

#print(tempWordsList) #this is a list/array of all words in the pdf 

#def extractText(pageNumber):
#    page = pdf.getPage(pageNumber)
#    text = page.extractText()
#    listOfLines = text.split("\n")
#    
#    
#    
#    for line in listOfLines:
#        if line.strip() not in unwantedCharacters: 
#            wordsInTheLine = line.split(" ")
#            wordsList += wordsInTheLine
#            print(line)
#            
