#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 12 22:58:50 2021

@author: HannahStudy
"""
import re

#TESTS
#Reference Number test
def refNumberTest(input, expectedOutput):
    refNo = input.split(sep=" ", maxsplit = 1)[0]
    if refNo == '*':
        refNo = input.split(sep=" ", maxsplit = 2)[1]
    
    print( "Reference Number: " + refNo + " Expected Output: " + expectedOutput + " Test is: " + str(refNo == expectedOutput))

#Height test
def heightTest(input, expectedOutput):
    height = ""
    if "Ht." in input:
        heightOnwards = input.split(sep="Ht.")[1]
        HeightOnwardsStrip = heightOnwards.strip()
        testHeight = HeightOnwardsStrip.split(sep=" ", maxsplit = 1)[0]
        height = testHeight
    elif " ht." in input:
        heightOnwards = input.split(sep="ht.")[1]
        HeightOnwardsStrip = heightOnwards.strip()
        testHeight = HeightOnwardsStrip.split(sep=" ", maxsplit = 1)[0]
        height = testHeight
    elif "Ht" in input:
        heightOnwards = input.split(sep="Ht")[1]
        HeightOnwardsStrip = heightOnwards.strip()
        testHeight = HeightOnwardsStrip.split(sep=" ", maxsplit = 1)[0]
        height = testHeight
    else:
        height = " "

    print( "Height: " + height + " Expected Output: " + expectedOutput + " Test is: " + str(height == expectedOutput))

#Diameter test
def diameterTest(input, expectedOutput):
    diameter = ""
    if "Diam. c. " in input:
        diamOnwards = input.split(sep="Diam. c. ")[1]
        diamOnwardsStrip = diamOnwards.strip()
        diameter = diamOnwardsStrip.split(sep=" ", maxsplit = 1)[0]
    elif "Diam." in input:
        diamOnwards = input.split(sep="Diam.")[1]
        diamOnwardsStrip = diamOnwards.strip()
        diameter = diamOnwardsStrip.split(sep=" ", maxsplit = 1)[0]
    elif "diam." in input:
        diamOnwards = input.split(sep="diam.")[1]
        diamOnwardsStrip = diamOnwards.strip()
        diameter = diamOnwardsStrip.split(sep=" ", maxsplit = 1)[0]
    else:
        diameter = " "
    
        print( "Diameter: " + diameter + " Expected Output: " + expectedOutput + " Test is: " + str(diameter == expectedOutput))

#Collection test
def collectionTest(input, expectedOutput):
    location =""
    locRegex = r'Ht.| ht.|Ht|Diam. c.|Diam.|diam.|PLATE'
    startLine = '^\d+'
    
    breakPoints = [' from ', ' Ht.', ' ht.', ' Ht', ' Diam. c.', ' Diam', ' diam', ' PLATE']
    locationOnwards = input.split(sep=" ", maxsplit = 1)[1].strip()
    if re.search(startLine, locationOnwards):
        locationOnwards = locationOnwards.split(sep=" ", maxsplit = 1)[1].strip()
    
    if any(breakPoint in input for breakPoint in breakPoints):
        location = re.split(locRegex, locationOnwards)[0]
    else:
        location = locationOnwards.split(sep = '\n', maxsplit = 1)[0].strip()
                
    if " from " in location:
        location = location.split(sep = " from ", maxsplit =1)[0]

    print( "Collection: " + location + " Expected Output: " + expectedOutput + " Test is: " + str(location == expectedOutput))

#Provenance test
def provenanceTest(input, expectedOutput):
    provenance = ""
    proRegex = r'Ht.|ht.|Ht|Diam. c.|Diam.|diam.|PLATE'

    breakPoints = [' Ht.', ' ht.', ' Ht', ' Diam. c.', ' Diam', ' diam', ' PLATE']
    firstLine = input.split(sep = '\n', maxsplit = 1)[0]
    if "from" in firstLine and any(breakPoint in input for breakPoint in breakPoints):
        provenanceOnwards = input.split(sep="from", maxsplit = 1)[1].strip()
        provenance = re.split(proRegex, provenanceOnwards)[0]

    elif "from" in firstLine:
        provenanceOnwards = firstLine.split(sep="from")[1].strip()
        provenance = provenanceOnwards.split('\n', 1)[0]

    else:
        provenance = " "
    
    print( "Provenance: " + provenance + " Expected Output: " + expectedOutput + " Test is: " + str(provenance == expectedOutput))

#Plate test
def plateTest(input, expectedOutput):
    plate = ""
    if "PLATE" in input:
        plateOnwards = input.split(sep="PLATE")[1].strip()
        plate = plateOnwards.split('\n', 1)[0]

    else:
        plate = " "
    
    print( "Plate: " + plate + " Expected Output: " + expectedOutput + " Test is: " + str(plate == expectedOutput))

#Publication test
def publicationTest(input, expectedOutput):
    publications = ""
    pubs = []
    checkPub = ' [0-9]+'
    removeList = ['above', '\\\\', ' \l.', ' r.', '(a)', '[a)']
    
    firstSplit = input.split(sep='\n', maxsplit = 1)[1]
    allPubs = re.split("\. \n", firstSplit)[0]
    
    if 'PLATE' in allPubs:
        allPubs = allPubs.split(sep='PLATE')[1]
        allPubs = (allPubs.split('\n')[1])

    if re.search(checkPub, allPubs):
        if allPubs[0] != "(":   #Potentially change this to an indent check for future Parts
            pubs = allPubs.split(";")

            for p in pubs:
                removeIndex = []
                for r in removeList:
                    if r in p:
                        removeIndex.append(pubs.index(p)) #record 1/99 has an r. and isn't being removed.

                removeIndex = list( dict.fromkeys(removeIndex) )
                if len(removeIndex) > 0:
                    for i in removeIndex:
                        pubs[i] = ''
                while '' in pubs:
                        pubs.remove('')
            
            publications = [p.replace("\n", "") for p in pubs] #removing \n from publications

        else:
            publications = []

    else:
        publications = []
    
    print( "Publications: " + str(publications) + " Expected Output: " + str(expectedOutput) + " Test is: " + str(publications == expectedOutput))

#Description test    
def descriptionTest(input, expectedOutput):
    description = ""
    if "(a)" in input :
        description = input.split(sep = "(a)", maxsplit = 1)[1]

    elif "[a)" in input:
        description = input.split(sep = "[a)", maxsplit = 1)[1]

    else:
        description = input.split(sep='\n', maxsplit = 1)[1]

        #description = re.split("\. \n", firstSplit)

    print( "Description: " + str(description) + " Expected Output: " + expectedOutput + " Test is: " + str(description == expectedOutput))
        
    
# def shapeTest()
#def artistTest()

#TEST CASES
test_01 = "*1  Syracuse 36334, from the Fusco necropolis. Ht. 42-5.  PLATE 1 a\nPP, no. 1, pi. 1 a; PPSupp, no. 1; LCS, p. 203, no. 26; Suppl. Ill, p. 99, no. 48; IGD III. 1, \n3; Gogos, OJh 55, 1984, p. 45, fig. 13; A.J. N. W. Prag, The Oresteia, pi. 35 d. \n[a) Orestes, Electra and Pylades at the tomb of Agamemnon, [b) young satyr and \nmaenad. \nFor a different interpretation [Iphigenia in Tauris) of the obverse, see Carlo Anti, Dioniso \n10, 1947, pp. 124-36; the problem is discussed in PPSupp, pp. 25-6; see also Kossatz-\nDiessmann, Dramen des Aischylos, pp. 94 and 96. \nTHE SICILIAN FORERUNNERS "
test_01_OutputRefNo = "*1"
test_01_OutputHeight = "42-5."
test_01_OutputDiameter = " "
test_01_OutputCollection = "Syracuse 36334,"
test_01_OutputProvenance = "the Fusco necropolis. "
test_01_OutputPlate = "1 a"
test_01_OutputPublications = ['PP, no. 1, pi. 1 a', ' PPSupp, no. 1', ' LCS, p. 203, no. 26', ' Suppl. Ill, p. 99, no. 48', ' IGD III. 1, 3', ' Gogos, OJh 55, 1984, p. 45, fig. 13', ' A.J. N. W. Prag, The Oresteia, pi. 35 d']
test_01_OutputDescription = " Orestes, Electra and Pylades at the tomb of Agamemnon, [b) young satyr and \nmaenad. \nFor a different interpretation [Iphigenia in Tauris) of the obverse, see Carlo Anti, Dioniso \n10, 1947, pp. 124-36; the problem is discussed in PPSupp, pp. 25-6; see also Kossatz-\nDiessmann, Dramen des Aischylos, pp. 94 and 96. \nTHE SICILIAN FORERUNNERS "

test_02 = "2  West Berlin F 3296, from Palazzuolo. Ht. 52, diam. 51. \nPP, no. 2, pis. 2 a and 3 a; PPSupp, no. 2; LCS, p. 203, no. 27; Suppl. Ill, p. 99, no. 49; van \nder Meer, BABesch 52-3, 1977-8, fig. 40; Trendall, Festschrift Hemelrijk, p. 159, fig. 2. \n[a) Punishment of Dirce and Lykos, [b) maenad between two satyrs. "
test_02_OutputRefNo = "2"
test_02_OutputHeight = "52,"
test_02_OutputDiameter = "51."
test_02_OutputCollection = "West Berlin F 3296,"
test_02_OutputProvenance = "Palazzuolo. "
test_02_OutputPlate = " "
test_02_OutputPublications = ['PP, no. 2, pis. 2 a and 3 a', ' PPSupp, no. 2', ' LCS, p. 203, no. 27', ' Suppl. Ill, p. 99, no. 49', ' van der Meer, BABesch 52-3, 1977-8, fig. 40', ' Trendall, Festschrift Hemelrijk, p. 159, fig. 2']
test_02_OutputDescription = " Punishment of Dirce and Lykos, [b) maenad between two satyrs. "

test_03 = "*3  Palermo 2198 (old no. 3480), from Gela. Rim broken off; actual ht. 32-5.  PLATE 1 b,c \nLCS, p. 203, no. 28a, pi. 80,1 (reverse); Suppl. Ill, p. 99, no. 51. \n[a) Standing draped woman, resting r. arm on pillar, Eros beside seated woman looking \ninto mirror, half-draped youth; bust of silen, above, [b) draped woman with fillet in r. hand, \nyoung satyr bending forward with phiale in r. hand. "
test_03_OutputRefNo = "*3"
test_03_OutputHeight = "32-5."
test_03_OutputDiameter = " "
test_03_OutputCollection = "Palermo 2198 (old no. 3480),"
test_03_OutputProvenance = "Gela. Rim broken off; actual "
test_03_OutputPlate = "1 b,c "
test_03_OutputPublications = ['LCS, p. 203, no. 28a, pi. 80,1 (reverse)', ' Suppl. Ill, p. 99, no. 51']
test_03_OutputDescription = " Standing draped woman, resting r. arm on pillar, Eros beside seated woman looking \ninto mirror, half-draped youth; bust of silen, above, [b) draped woman with fillet in r. hand, \nyoung satyr bending forward with phiale in r. hand. "

test_04 = "*5  Vienna 986. Ht. 37-5.  PLATE 1 e,f \nPP, no. 4, pi. 3 d; PPSupp, no. 4; LCS, p. 204, no. 29; Suppl. Ill, p. 99, no. 52; LIMC  III, \np. 923, Eros 872, pi. 658, 6. \n[a) Maenad, with Eros, seated between two silens, [b) two draped women, 1. with \nthyrsus, r. with pomegranate and fillet. \nFor the open box below the seated maenad to r., cf. no. 3. "
test_04_OutputRefNo = "*5"
test_04_OutputHeight = "37-5."
test_04_OutputDiameter = " "
test_04_OutputCollection = "Vienna 986. "
test_04_OutputProvenance = " "
test_04_OutputPlate = "1 e,f "
test_04_OutputPublications = ['PP, no. 4, pi. 3 d', ' PPSupp, no. 4', ' LCS, p. 204, no. 29', ' Suppl. Ill, p. 99, no. 52', ' LIMC  III, p. 923, Eros 872, pi. 658, 6']
test_04_OutputDescription = " Maenad, with Eros, seated between two silens, [b) two draped women, 1. with \nthyrsus, r. with pomegranate and fillet. \nFor the open box below the seated maenad to r., cf. no. 3. "

test_05 = "*14  Copenhagen, N.M. 9183. Ht. 35, diam. 33.  PLATE2a> \nPP, no. 13; PPSupp, no. 12; LCS, p. 205, no. 37; Suppl. Ill, p. 101, no. 63. \n(a) Satyr bending forward in front of seated half-draped women, holding mirror, \nstanding draped woman with egg and thyrsus, [b) young satyr with thyrsus, and draped \nwoman with fillet. "
test_05_OutputRefNo = "*14"
test_05_OutputHeight = "35,"
test_05_OutputDiameter = "33."
test_05_OutputCollection = "Copenhagen, N.M. 9183. "
test_05_OutputProvenance = " "
test_05_OutputPlate = "2a> "
test_05_OutputPublications = ['PP, no. 13', ' PPSupp, no. 12', ' LCS, p. 205, no. 37', ' Suppl. Ill, p. 101, no. 63']
test_05_OutputDescription = " Satyr bending forward in front of seated half-draped women, holding mirror, \nstanding draped woman with egg and thyrsus, [b) young satyr with thyrsus, and draped \nwoman with fillet. "

test_06 = "*15  Los Angeles, Dechter coll., ex London Market, Christie's, Sale Cat. 12 Dec. 1984, no. 128, ill. \non p. 25. Ht. 30, diam. 30-5  PLATE 2/ \nEx Erbach 30; PPSupp, no. 13; LCS, p. 205, no. 38; Suppl. Ill, p. 101, no. 64. \n[a) Centaur with tree-trunk attacking warrior holding spear and shield; abovebust of \nsatyr, looking down from behind raised ground, [b) two draped women, 1. with wreath and \nthyrsus, r. holding up mirror. \nThe two following calyx-kraters have been extensively repainted but should \nbelong here: "
test_06_OutputRefNo = "*15"
test_06_OutputHeight = "30,"
test_06_OutputDiameter = "30-5 "
test_06_OutputCollection = "Los Angeles, Dechter coll., ex London Market, Christie's, Sale Cat. 12 Dec. 1984, no. 128, ill. \non p. 25. "
test_06_OutputProvenance = " "
test_06_OutputPlate = "2/ "
test_06_OutputPublications = ['Ex Erbach 30', ' PPSupp, no. 13', ' LCS, p. 205, no. 38', ' Suppl. Ill, p. 101, no. 64']
test_06_OutputDescription = " Centaur with tree-trunk attacking warrior holding spear and shield; abovebust of \nsatyr, looking down from behind raised ground, [b) two draped women, 1. with wreath and \nthyrsus, r. holding up mirror. \nThe two following calyx-kraters have been extensively repainted but should \nbelong here: "

test_07 = "*27  Paestum, from S. Venera (11 May 1976). Diam. c. 22.  PLATE 3e. \nSeated woman, holding phiale in r. hand; part of a young satyr, bending forward behind \nher. \nPelikai "
test_07_OutputRefNo = "*27"
test_07_OutputHeight = " "
test_07_OutputDiameter = "22."
test_07_OutputCollection = "Paestum,"
test_07_OutputProvenance = "S. Venera (11 May 1976). "
test_07_OutputPlate = "3e. "
test_07_OutputPublications = [] 
test_07_OutputDescription = "Seated woman, holding phiale in r. hand; part of a young satyr, bending forward behind \nher. \nPelikai " 

test_08 = "28  Rome, private coll. Ht. 22. \ndell' Osso, ArchCl 27, 1975, p. 346, no. 1, pis. 88 and 89,1 (where it is classed as Apulian); \nLCS, Suppl. Ill, p. 102, no. 74. \n(a) Young satyr with wine-skin in r. hand and torch in 1., [b) draped woman with \nthyrsus. "
test_08_OutputRefNo = "28"
test_08_OutputHeight = "22."
test_08_OutputDiameter = " "
test_08_OutputCollection = "Rome, private coll. "
test_08_OutputProvenance = " "
test_08_OutputPlate = " "
test_08_OutputPublications = ["dell' Osso, ArchCl 27, 1975, p. 346, no. 1, pis. 88 and 89,1 (where it is classed as Apulian)", " LCS, Suppl. Ill, p. 102, no. 74"] 
test_08_OutputDescription = " Young satyr with wine-skin in r. hand and torch in 1., [b) draped woman with \nthyrsus. "

test_09 = "35  Basel, private coll. Diam. 18. \nLCS, Suppl. Ill, p. 102, no. 75. \nSeated woman with outstretched arms; silen seated beside rock; seated Eros with \noutspread wings. "
test_09_OutputRefNo = "35"
test_09_OutputHeight =" "
test_09_OutputDiameter = "18."
test_09_OutputCollection = "Basel, private coll. "
test_09_OutputProvenance = " "
test_09_OutputPlate = " "
test_09_OutputPublications = ['LCS, Suppl. Ill, p. 102, no. 75'] 
test_09_OutputDescription = "Seated woman with outstretched arms; silen seated beside rock; seated Eros with \noutspread wings. "

test_10 = "*79  Dublin, University College 1468 (formerly on loan to the National Museum, 960.1; ex Hope \ncoll. 266). Ht. 34-6, diam. 35-6.  PLATE 9 a, b \nPP, no. 19, fig. 9; PPSupp, no. 23; LCS, p. 214, no. 74, pi. 84,6 (reverse); Suppl. Ill, p. \n106, no. 113; Johnston, Gr. V. in Ireland, p. 391, no. 501. \n(a) Nude woman with phiale standing by laver, facing draped woman bending forward \nwith mirror in r. hand and spray in 1., bearded silen holding branch in r. hand and facing \nstanding draped woman, [b) nude youth between two draped women, each holding a \npomegranate in her concealed hand. "
test_10_OutputRefNo = "*79"
test_10_OutputHeight = "34-6,"
test_10_OutputDiameter = "35-6."
test_10_OutputCollection = "Dublin, University College 1468 (formerly on loan to the National Museum, 960.1; ex Hope \ncoll. 266). "
test_10_OutputProvenance = " "
test_10_OutputPlate = "9 a, b "
test_10_OutputPublications = ['PP, no. 19, fig. 9', ' PPSupp, no. 23', ' LCS, p. 214, no. 74, pi. 84,6 (reverse)', ' Suppl. Ill, p. 106, no. 113', ' Johnston, Gr. V. in Ireland, p. 391, no. 501']
test_10_OutputDescription = " Nude woman with phiale standing by laver, facing draped woman bending forward \nwith mirror in r. hand and spray in 1., bearded silen holding branch in r. hand and facing \nstanding draped woman, [b) nude youth between two draped women, each holding a \npomegranate in her concealed hand. "


#OUTPUTS
#Reference Number tests
#refNumberTest(test_01, test_01_OutputRefNo)
#refNumberTest(test_02, test_02_OutputRefNo)
#refNumberTest(test_03, test_03_OutputRefNo)
#refNumberTest(test_04, test_04_OutputRefNo)
#refNumberTest(test_05, test_05_OutputRefNo)
#refNumberTest(test_06, test_06_OutputRefNo)
#refNumberTest(test_07, test_07_OutputRefNo)
#refNumberTest(test_08, test_08_OutputRefNo)
#refNumberTest(test_09, test_09_OutputRefNo)
#refNumberTest(test_10, test_10_OutputRefNo)


#Height tests 
#heightTest(test_01, test_01_OutputHeight)
#heightTest(test_02, test_02_OutputHeight)
#heightTest(test_03, test_03_OutputHeight)
#heightTest(test_04, test_04_OutputHeight)
#heightTest(test_05, test_05_OutputHeight)
#heightTest(test_06, test_06_OutputHeight) # ht in Dechter being caught as break point in Collection (Location). Resolved by breaking on ' ht' instead. To be added to main code. 
#heightTest(test_07, test_07_OutputHeight)
#heightTest(test_08, test_08_OutputHeight)
#heightTest(test_09, test_09_OutputHeight)
#heightTest(test_10, test_10_OutputHeight)


#Diameter test
#diameterTest(test_01, test_01_OutputDiameter)
#diameterTest(test_02, test_02_OutputDiameter)
#diameterTest(test_03, test_03_OutputDiameter)
#diameterTest(test_04, test_04_OutputDiameter)
#diameterTest(test_05, test_05_OutputDiameter)
#diameterTest(test_06, test_06_OutputDiameter)
#diameterTest(test_07, test_07_OutputDiameter)
#diameterTest(test_08, test_08_OutputDiameter)
#diameterTest(test_09, test_09_OutputDiameter)
#diameterTest(test_10, test_10_OutputDiameter)

#Provenance tests
#provenanceTest(test_01, test_01_OutputProvenance)
#provenanceTest(test_02, test_02_OutputProvenance)
#provenanceTest(test_03, test_03_OutputProvenance)
#provenanceTest(test_04, test_04_OutputProvenance)
#provenanceTest(test_05, test_05_OutputProvenance)
#provenanceTest(test_06, test_06_OutputProvenance)
#provenanceTest(test_07, test_07_OutputProvenance)
#provenanceTest(test_08, test_08_OutputProvenance)
#provenanceTest(test_09, test_09_OutputProvenance)
#provenanceTest(test_10, test_10_OutputProvenance)

#Plate tests
#plateTest(test_01, test_01_OutputPlate)
#plateTest(test_02, test_02_OutputPlate)
#plateTest(test_03, test_03_OutputPlate)
#plateTest(test_04, test_04_OutputPlate)
#plateTest(test_05, test_05_OutputPlate)
#plateTest(test_06, test_06_OutputPlate)
#plateTest(test_07, test_07_OutputPlate)
#plateTest(test_08, test_08_OutputPlate)
#plateTest(test_09, test_09_OutputPlate)
#plateTest(test_10, test_10_OutputPlate)

#Collection tests
#collectionTest(test_01, test_01_OutputCollection)
#collectionTest(test_02, test_02_OutputCollection)
#collectionTest(test_03, test_03_OutputCollection)
#collectionTest(test_04, test_04_OutputCollection)
#collectionTest(test_05, test_05_OutputCollection)
#collectionTest(test_06, test_06_OutputCollection)
#collectionTest(test_07, test_07_OutputCollection)
#collectionTest(test_08, test_08_OutputCollection)
#collectionTest(test_09, test_09_OutputCollection)
#collectionTest(test_10, test_10_OutputCollection)

#Publication tests
#publicationTest(test_01, test_01_OutputPublications)
#publicationTest(test_02, test_02_OutputPublications)
#publicationTest(test_03, test_03_OutputPublications)
#publicationTest(test_04, test_04_OutputPublications)
#publicationTest(test_05, test_05_OutputPublications)
#publicationTest(test_06, test_06_OutputPublications)
#publicationTest(test_07, test_07_OutputPublications)
#publicationTest(test_08, test_08_OutputPublications)
#publicationTest(test_09, test_09_OutputPublications)
#publicationTest(test_10, test_10_OutputPublications) #Failing to pick up \n for final line. Error unresolved (15/10/2021).

#Description tests
#descriptionTest(test_01, test_01_OutputDescription)
#descriptionTest(test_02, test_02_OutputDescription)
#descriptionTest(test_03, test_03_OutputDescription)
#descriptionTest(test_04, test_04_OutputDescription)
#descriptionTest(test_05, test_05_OutputDescription)
#descriptionTest(test_06, test_06_OutputDescription)
#descriptionTest(test_07, test_07_OutputDescription)
#descriptionTest(test_08, test_08_OutputDescription)
#descriptionTest(test_09, test_09_OutputDescription) #Publication included as part of description. Error unresolved (15/10/2021.
#descriptionTest(test_10, test_10_OutputDescription)


print("\n\nEnd of tests")
