#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 12 22:58:50 2021

@author: HannahStudy
"""

testInput = "*1  Syracuse 36334, from the Fusco necropolis. Ht. 42-5.  PLATE 1 a"
testOutputHeight = "42-5."


#def refNumberTest()

def heightTest(input, expectedOutput):
    height = ""
    if "Ht." in input:
        heightOnwards = input.split(sep="Ht.")[1]
        HeightOnwardsStrip = heightOnwards.strip()
        testHeight = HeightOnwardsStrip.split(sep=" ", maxsplit = 1)[0]
        height = testHeight
    elif "ht." in input:
        heightOnwards = input.split(sep="ht.")[1]
        HeightOnwardsStrip = heightOnwards.strip()
        testHeight = HeightOnwardsStrip.split(sep=" ", maxsplit = 1)[0]
        height = testHeight
    elif "Ht" in record:
        heightOnwards = record.split(sep="Ht")[1]
        HeightOnwardsStrip = heightOnwards.strip()
        testHeight = HeightOnwardsStrip.split(sep=" ", maxsplit = 1)[0]
        height = testHeight
    else:
        height = " "

    return height == expectedOutput

# def diameterTest()

# def collectionTest()

# def plateTest()

# def provenanceTest()

# def publicationTest()

# def descriptionTest()


# def shapeTest()

print(heightTest(testInput, testOutputHeight))