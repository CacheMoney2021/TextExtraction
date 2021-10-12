# TextExtraction

Developed for La Trobe’s CSE3PRA/PRB 2021. The Arthur Trendall Research Centre is a research centre for the study of ancient Mediterranean 
artefacts, much of their resources are paper based. They asked us to develop a tool they could use to extract artefact information from pdf 
scans of Trendall’s works, in order to make the artefacts accessible online.

CacheMoney2021/TextExtraction is a Python library for reading in journal pdfs and extracting vase information. 
Filter code removes non-artefact information, such as paragraphs. The resulting text file is then run through Extraction code, to identify 
the attributes for each artefact entry and produce a file that can be uploaded to a database. 

This code was developed by Aayesha Mohammed, Mariyam Mohammed and Rogue Lyons.

# Installation
This project can be downloaded from Github. 

## Clone the repo:
```
git clone https://github.com/CacheMoney2021/TextExtraction.git
```


## Install the requirements:
It requires the following languages/libraries:
python (3.8.8)
pandas (1.2.4)
pdfplumber (0.5.28)

```
python -m pip install -r requirements.txt
```

# Usage
This code is designed specifically for the RVP.pdf file supplied to the project. This file is not uploaded onto Github, as it is too large. 
The following usage assumes that the user has the required PDF.

The PDF should be saved into the Read_In_RVP folder, otherwise the pathname to the folder will need to be amended in 
ReadIn_RVP_FilterByFontSize.py.

## Running the code
### Step 1: Read_In_RVP folder
Open the Read_In_RVP folder first. Run ReadIn_RVP_FilterByFontSize.py. This will result in three .txt files- Part1.txt, Part2.txt, Part3.txt.

### Step 2: Attribute_Extraction folder
Open the Attribute_Extraction folder and run Attribute_Extraction.py. This should result in six .csv files-AttributeExtraction_p1.csv, 
AttributeExtraction_p2.csv, AttributeExtraction_p3.csv, plates_p1.csv, plates_p2.csv , plates_p3.csv.

The AttributeExtraction.csv files contain vase data, while the plates.csv files contain plate references and their corresponding vase 
reference. These files are intended to be used for populating the database.

# Known Bugs
### 12/10/2021
- Some shapes not extracted as text is too large and not caught by the current filter. This results in some vases being 
incorrectly categorised.
- If attempting to read in empty pages as part of a pdf, the program crashes.

# Authors and acknowledgment
The developers of this project acknowledge the Wurundjeri people, Traditional Custodians of the land on which we live and work. We recognise their continued connection to the land and waters of this beautiful place, and acknowledge that they never ceded sovereignty. We pay our respects to their Elders past, present and emerging. 

We would like to thank Scott Mann and Alex Nguyen for their work running this project and advising our team, and Dr Gillian Shepherd for her time and expertise in Arthur Trendall's work. 

# License


# Project status


