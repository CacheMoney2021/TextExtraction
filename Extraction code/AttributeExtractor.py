#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 19:42:47 2021

@author: HannahStudy
"""

#Attribute extraction: Provenance
#Notes:
         #If adding in code that pulls previous attriutes in string, 
         #alter/remove v.pop[0]
         

import re

f = open('TrialWithRE.txt', 'r')
text = f.read()

numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
fuckinTrendall = "from T"
textList = text.split('\n\n')
textList.pop(len(textList)-1)

#
#to split entries into:
#    firstLine(ID, Location ,Provenance, Height/Diam, Plate No)
#    publicationLine (publications, separated by ;. May capture first line of descriptions)
#    everythingElse (should contain descriptions)
#

firstLines = []
publicationLines = []
everythingElse = []


def listToString(s):
    str1 = " "
    return str1.join(s)


for txt in textList:
    a = txt.split('\n', 1)
    firstLines += [a[0]]
    a = re.split('(\n)', txt)
    a.pop(0)
    a.pop(0)
    pl = a[0]
    publicationLines += [pl]
    a.pop(0)
    if len(a) > 1:
        a.pop(0)
    print(a)
    if a:
        everythingElse += [a]
        
print(everythingElse)

#
#End of creating lists
#


def getProvenance( text ):
    for vase in text:
        if vase[0] == "":
            pass
        elif vase[0] == '*' or vase[0] in numbers:
            vaseWithProvList = vase.split('\n', 1)
            a = vaseWithProvList[0]
            if "from" in a: #checks that Provenance is included in entry
                if fuckinTrendall not in a:
                    d = "from "
                    v = [d+e for e in a.split(d) if e]
                    v.pop(0) #removes what is before Provenance. 
                    #print(v)
                    #From here, call getHt?
                
                
getProvenance(firstLines)
print('end')