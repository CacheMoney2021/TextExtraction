"""
Authors: Aayesha Mohammed, Mariyam Mohammed, Rogue Lyons
"""

import re
import pandas as pd

#Creating reference list to check Shapes against
shape_file = open("VaseShapesReference.txt")
shape = shape_file.read()
ShapeList = shape.split('\n')
for i in range(len(ShapeList)):
    ShapeList[i] = ShapeList[i].strip()
ShapeList.pop()


def create_RecordList(filename):
    RecordList = []
    f = open(str(filename))
    f_read = f.read()
    RecordList = f_read.split('\n\n')
    return RecordList

#removing paragraph lines
#if the entry DOESN'T start with a number, asterisk or bullet, check if it's a Shape entry otherwise remove.
def clean_RecordList(RecordList): 
    regExp = '^(?!\d+|\*|\•).*'
    for i in range(len(RecordList)):
        if re.search(regExp, RecordList[i]):
            if RecordList[i].upper().strip() in ShapeList:
                RecordList[i] = "SHAPE: " + RecordList[i]
            else:
                RecordList[i] = ""
    
    while("" in RecordList):
        RecordList.remove("")
     
    #removing paragraph lines that start with a number
    #if it doesn't contain any entry terms, remove.
    regFrom = r', from | from [A-Z]'
    for i in range(len(RecordList)):
        breakPoints = [' Ht.', ' ht.', ' Ht', ' Diam. c.', ' Diam', ' diam', ' PLATE', '(a)', '[a)', 'SHAPE: ']
        if not any(breakPoint in RecordList[i] for breakPoint in breakPoints):
            if re.search(regFrom, RecordList[i]):
                RecordList[i] = RecordList[i]
            else:
                RecordList[i] = ""
    
    while("" in RecordList):
        RecordList.remove("")
    return RecordList

        
#extracting shape:
def Extract_Shape(RecordList):
    Shape = []
    for record in RecordList:
        if 'SHAPE: ' in record:
            shape = record.split(':')[1].strip()
            continue
        Shape.append(shape)
    return Shape


#Removing Shape from RecordList:
def remove_Shape(RecordList):
    for i in range(len(RecordList)):
        if "SHAPE: " in RecordList[i]:
            RecordList[i] = ""
    
    while("" in RecordList):
        RecordList.remove("")
    return RecordList


#Removing THE RED-FIGURED VASES OF PAESTUM from records 
def header_remove(RecordList):
    for i in range(len(RecordList)):
        RecordList[i] = RecordList[i].replace("THE RED-FIGURED VASES OF PAESTUM", "").strip()
    return RecordList
    

#extracting reference number
def Extract_RefNo(RecordList, part):
    referenceNo = []
    for record in RecordList:
        refNo = record.split(sep=" ", maxsplit = 1)[0]
        if refNo == '*':
            refNo = record.split(sep=" ", maxsplit = 2)[1]
            referenceNo.append(part + '-' + refNo)
        else:
            referenceNo.append(part + '-' + refNo)
                
    for i in range(len(referenceNo)):
        referenceNo[i] = referenceNo[i].replace('*', "")   
        referenceNo[i] = referenceNo[i].replace('•', "") 
    return referenceNo

                
#extractiing location:
def Extract_Location(RecordList):
    Location = []
    locRegex = r'Broken|broken|Max|max|Actual|actual|Ht.|ht.|Ht|Diam. c.|Diam.|diam.|PLATE'
    startLine = '^\d+'
    
    for record in RecordList:
          breakPoints = [' Broken',' broken',' Max ',' max ',' Actual ',' actual ',' Ht.', ' ht.', ' Ht', ' Diam. c.', ' Diam', ' diam', ' PLATE']
          locationOnwards = record.split(sep=" ", maxsplit = 1)[1].strip()
          
          #removing vase number from entry. Location, if exists, is next attribute.
          if re.search(startLine, locationOnwards):
              locationOnwards = locationOnwards.split(sep=" ", maxsplit = 1)[1].strip()
          if any(breakPoint in record for breakPoint in breakPoints):
                location = re.split(locRegex, locationOnwards)[0]
                Location.append(location)
          else:
                location = locationOnwards.split(sep = '\n', maxsplit = 1)[0].strip()
                Location.append(location)
    
    #removing 'from' in Location
    for i in range(len(Location)):
        if " from " in Location[i]:
            Location[i] = Location[i].split(sep = " from ", maxsplit =1)[0]
    
    #removing /n from final Location List
    for i in range(len(Location)):
        Location[i] = Location[i].replace('\n', ' ')
    return Location

    
#excracting previousLocation
def Extract_previousLocation(Location):
    previousLocation = []
    regPrev = r'\(ex |ex '
    for i in range(len(Location)):
        if Location[i].startswith('(a)'):            
            Location[i] = ""
            
        #If current location is unknown and previous location is known, location starts with 'Once '    
        if Location[i].startswith('Once '):
            prev = Location[i]
            Location[i] = ""
            prev = prev.replace("Once ", "")
            previousLocation.append(prev)
            
        #If current location known and previous location known, location contains 'ex '.    
        elif 'ex ' in Location[i]:
            prev = re.split(regPrev, Location[i])[1].strip()
            Location[i] = re.split(regPrev, Location[i])[0].strip()
            previousLocation.append(prev)
        else:
            previousLocation.append("")
            
    for i in range(len(previousLocation)):
        if "(" in previousLocation[i]:
            previousLocation[i] = previousLocation[i]
        else:
            previousLocation[i] = previousLocation[i].replace(').',"")
    
    #removing /n from final previousLocation List
    for i in range(len(previousLocation)):
        previousLocation[i] = previousLocation[i].replace('\n', ' ')
    return previousLocation


#extracting Provenence
#Provenance always preceeded by 'from '
def Extract_Provenance(RecordList):
    Provenance = []
    proRegex = r'Broken|broken|Fragments|fragments|Max|max|Actual|actual|Ht.|ht.|Ht|Diam. c.|Diam.|diam.|PLATE'
    
    for record in RecordList:
        breakPoints = [' Broken',' broken',' Fragments',' fragments',' Max ',' max ',' Actual ',' actual ',' Ht.', ' ht.', ' Ht', ' Diam. c.', ' Diam', ' diam', ' PLATE']
        firstLine = record.split(sep = '\n', maxsplit = 1)[0]
        
        #If Provenance is between 'from' and breakpoints in firstLine 
        if "from" in firstLine and any(breakPoint in record for breakPoint in breakPoints):
            provenanceOnwards = record.split(sep="from", maxsplit = 1)[1].strip()
            provenance = re.split(proRegex, provenanceOnwards)[0]
            Provenance.append(provenance)
            
        # if Provenance is the last attribute in the firstLine.    
        elif "from" in firstLine:
            provenanceOnwards = firstLine.split(sep="from")[1].strip()
            provenance = provenanceOnwards.split('\n', 1)[0]
            Provenance.append(provenance)
        else:
            provenance = ""
            Provenance.append(provenance)
            
    #removing /n from final Provenance List
    for i in range(len(Provenance)):
        Provenance[i] = Provenance[i].replace('\n', ' ')
    return Provenance

#extracting height
def Extract_Height(RecordList):
    Height = []
    heights = r'Ht.|ht.|Ht'
    for record in RecordList:
        breakPoints = [' Ht.', ' ht.', ' Ht']
        if any(breakPoint in record for breakPoint in breakPoints):
            HeightOnwards = re.split(heights, record)[1].strip()
            if HeightOnwards.startswith("("):
                HeightOnwards = HeightOnwards.split(sep = ")", maxsplit = 1)[1].strip()
            if HeightOnwards.startswith("and"):
                HeightOnwards = HeightOnwards.split(sep = " ", maxsplit = 2)[2].strip()
            height = HeightOnwards.split(sep=" ", maxsplit = 1)[0]
            Height.append(height)
        else:
            height = ""
            Height.append(height)
    return Height


#extracting diameter
def Extract_Diameter(RecordList):
    Diameter = []
    diams = r'diam. of base|Diam. c.|diam. c.|Diam.|diam.'
    for record in RecordList:
        breakPoints = [' diam. of base', ' Diam. c.',' diam. c.', ' Diam.', ' diam.']
        if any(breakPoint in record for breakPoint in breakPoints):
            DiamOnwards = re.split(diams, record)[1].strip()
            diameter = DiamOnwards.split(sep=" ", maxsplit = 1)[0]
            Diameter.append(diameter)
        else:
            diameter = ""
            Diameter.append(diameter)
    return Diameter
        

#extracting plate
def Extract_Plate(RecordList):
    Plate = []
    plates = r'PLATES|PLATE'
    for record in RecordList:
        breakPoints = ['PLATES', 'PLATE']
        if any(breakPoint in record for breakPoint in breakPoints):
            plateOnwards = re.split(plates, record)[1].strip()
            plate = plateOnwards.split('\n', 1)[0]
            Plate.append(plate)
        else:
            plate = " "
            Plate.append(plate)
    return Plate
        
#Converting Plate into number format for database image reference 
def Convert_Plate(Plate, referenceNo, imagePlate, refImage):
    NewPlate = []
    Text = ""
    
    for i in range(len(Plate)):
        plate = Plate[i].replace(" ", "-")
        plate = Plate[i].lower()
        for char in plate:
            if char.islower():
                charNum = ord(char) - 96
                Text = Text + " " + str(charNum)
            else:
                Text = Text + str(char)
        NewPlate.append(Text)
        Text = ""
       
    regSpace = re.compile(r"\s+")
    for i in range(len(NewPlate)):
        NewPlate[i] = NewPlate[i].strip()
        NewPlate[i] = NewPlate[i].replace(",", " ")
        NewPlate[i] = regSpace.sub(" ", NewPlate[i])    
        NewPlate[i] = NewPlate[i].replace(" ", "-")
        NewPlate[i] = NewPlate[i].replace("--", "-")
    

    for i in range(len(NewPlate)):
        count = NewPlate[i].count('-',0,len(NewPlate[i]))
        if count < 2:
            imagePlate.append(NewPlate[i])
            refImage.append(referenceNo[i])
        else:
            imageID = NewPlate[i].split(sep = '-', maxsplit = count)[0]
            plateList = NewPlate[i].split(sep = '-', maxsplit = count)
            for j in range(1,len(plateList)):
                imagePlate.append(imageID + '-' + plateList[j])
                refImage.append(referenceNo[i])
    
    for i in range(len(imagePlate)):
        if imagePlate[i] == "":
            refImage[i] = refImage[i].replace(refImage[i], "")
    
    while("" in imagePlate):
        imagePlate.remove("")
    
    while("" in refImage):
        refImage.remove("")

        
#extracting publication
def Extract_Publications(RecordList):
    Publications = []
    for record in RecordList:
        pubs = []
        checkPub = ' [0-9]+'
        
        #tokens that appear in most descriptions, but never in publications
        removeList = ['above', '\\\\', ' \l.',' 1.', ' r.', '(a)', '[a)']
        
        #removing first line of entry- never contains publication info
        if '\n' in record:
            firstSplit = record.split(sep='\n', maxsplit = 1)[1]
            allPubs = re.split("\. \n", firstSplit)[0]
            if 'PLATE' in allPubs:
                if '\n' in allPubs:
                    allPubs = allPubs.split(sep='PLATE')[1]
                    allPubs = (allPubs.split('\n')[1])
            
            #where first line of vase info requires a second line, it always contains a plate as final attribute
            #removing any second lines that end in PLATE            
            if re.search(checkPub, allPubs):
                if allPubs[0] != "(":
                    pubs = allPubs.split(";")                    
                    addPub = pubs[len(pubs)-1].split('. \n')
                    pubs.pop(len(pubs)-1)
                    pubs.append(addPub[0])
                    
                    #Removing description lines
                    for p in pubs:
                        removeIndex = []
                        for r in removeList:
                            if r in p:
                                removeIndex.append(pubs.index(p)) #record 1/99 has an r. and isn't being removed.
        
                        removeIndex = list( dict.fromkeys(removeIndex) )
                        if len(removeIndex) > 0:
                            n = len(pubs)
                            for i in range(0, n - removeIndex[0]):
                                pubs.pop()
                            # for i in removeIndex:
                            #     pubs[i] = ''
                        while '' in pubs:
                                pubs.remove('')        
                    publications = [p.replace("\n", "") for p in pubs] #removing \n from publications
                    Publications.append(publications)        
                else:
                    publications = ""
                    Publications.append(publications)        
            else:
                publications = ""
                Publications.append(publications)
        else:
            publications = ""
            Publications.append(publications) 
    
    #replacing empty array [] in Publications with ""
    for i in range(len(Publications)):
        if len(Publications[i]) == 0:
            Publications[i] = ""
    return Publications

        
# #extracting Desciption
def Extract_Description(RecordList):
    Description = []
    regDesc = r'PP|PAdd|PPSupp|pp. | pi. \d+| p. \d+'
    regBreakPoint = r'Ht.|ht.|Ht|Diam. c.|Diam|diam|PLATES|PLATE'
    for record in RecordList:
        if "(a)" in record :
            description = record.split(sep = "(a)", maxsplit = 1)[1]
            Description.append("(a) " + description)
            
        elif "[a)" in record:
            description = record.split(sep = "[a)", maxsplit = 1)[1]
            Description.append("[a) " + description)
            
        elif '\n' in record: #marks end of Publications
            description = record.split(sep='\n', maxsplit = 1)[1].strip()
            if re.search(regDesc,description):
                if '. \n' in description:
                    description = description.split(sep = '. \n', maxsplit=1)[1].strip()
                    if re.search(regDesc,description):
                        description = description.split(sep = '. \n', maxsplit=1)[1].strip()
            if re.search(regBreakPoint,description):
                if '\n' in description:
                    description = description.split(sep='\n', maxsplit =1 )[1]
            Description.append(description)
        else:
            description = ''
            Description.append(description)
            
    #Removing Publications not being caught        
    regPub = r'PAdd|PP'
    for i in range(len(Description)):
        if not '\n' in Description[i]:
            if re.search(regPub, Description[i]):
                Description[i] = ''
                
    #removing /n from final description List
    for i in range(len(Description)):
        Description[i] = Description[i].replace('\n', ' ')
    return Description


#List of fabric and Technique
def FabricList(RecordList):
    Fabric = []            
    for i in range(len(RecordList)):
        Fabric.append("Paestan")
    return Fabric


def TechniqueList(RecordList):
    Technique = []
    for i in range(len(RecordList)):
        Technique.append("Red-Figure")
    return Technique


#removing punctuations from the end of elements in list (e.g ",") to prevent it from interfering with the database
def Remove_Last_Punctuation(List):
    puncCheck = r'[^\w\s]'
    for i in range(len(List)):
        List[i] = List[i].strip()
        if not len(List[i]) == 0:
            if re.search(puncCheck,List[i][-1]):
                List[i] = List[i][:-1]
    return List

def Remove_Last_Punctuation_from_all_lists (Location, previousLocation, Provenance, Height, Diameter, Description):
    Location = Remove_Last_Punctuation(Location)
    previousLocation = Remove_Last_Punctuation(previousLocation)
    Provenance = Remove_Last_Punctuation(Provenance)
    Height = Remove_Last_Punctuation(Height)
    Diameter = Remove_Last_Punctuation(Diameter)
    Description = Remove_Last_Punctuation(Description)


#Function that calls all other functions in order
def Concatenate_Attribute_Extraction(filename, part):
    RecordList = create_RecordList(filename)
    CleanedRecordList = clean_RecordList(RecordList)
    Shape = Extract_Shape(CleanedRecordList)
    CleanedRecordList = remove_Shape(CleanedRecordList)
    CleanedRecordList = header_remove(CleanedRecordList)
    referenceNo = Extract_RefNo(CleanedRecordList, part)
    Location = Extract_Location(CleanedRecordList)
    previousLocation = Extract_previousLocation(Location)
    Provenance = Extract_Provenance(CleanedRecordList)
    Height = Extract_Height(CleanedRecordList)
    Diameter = Extract_Diameter(CleanedRecordList) 
    Plate = Extract_Plate(CleanedRecordList)
    imagePlate = []
    refImage = []
    Convert_Plate(Plate, referenceNo, imagePlate, refImage)
    Publications = Extract_Publications(CleanedRecordList)
    Description = Extract_Description(CleanedRecordList)
    Fabric = FabricList(CleanedRecordList)
    Technique = TechniqueList(CleanedRecordList)
    Remove_Last_Punctuation_from_all_lists (Location, previousLocation,
                                            Provenance, Height, Diameter, Description)
    
    All_lists = [Shape,referenceNo, Location, previousLocation, Provenance, Height, 
                 Diameter, Publications, Description, Fabric, Technique, refImage, imagePlate] 
    return All_lists
    

#Writing DataFrames to a csv file
def Write_to_CSV(filename, part, output_CSV_file, output_CSV_Plate_file):
    Shape,referenceNo, Location, previousLocation, Provenance, Height, Diameter, Publications,\
    Description, Fabric, Technique, refImage, imagePlate = Concatenate_Attribute_Extraction(filename, part)
    
    #Writing Attribute lists to a csv file
    df = pd.DataFrame({'ReferenceNo': referenceNo,'Location': Location,
                       'Previous Location': previousLocation, 'Provenance': Provenance,
                       'Height': Height, 'Diameter': Diameter, 'Publications': Publications, 
                       'Description': Description, 'Shape': Shape, 'Fabric': Fabric, 'Technique': Technique})
    df.to_csv(output_CSV_file, index=False)
    
    #Writing Plates and its corresponding reference number to a csv file database images
    df1 = pd.DataFrame({'ReferenceNo': refImage, 'Plate': imagePlate})
    df1.to_csv(output_CSV_Plate_file, index=False)
    
#Writing all parts 1, 2 and 3
Write_to_CSV("../Read_In_RVP/Part1.txt", "1", "AttributeExtraction_p1.csv", "plates_p1.csv")
Write_to_CSV("../Read_In_RVP/Part2.txt", "2", "AttributeExtraction_p2.csv", "plates_p2.csv")
Write_to_CSV("../Read_In_RVP/Part3.txt", "3", "AttributeExtraction_p3.csv", "plates_p3.csv")
