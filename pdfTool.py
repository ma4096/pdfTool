from PyPDF4 import PdfFileReader, PdfFileWriter

header = """PDF Tool based on PyPDF4
"""
safePath = ""
basePdfPath = ""

def overwriteAt(writer):
    print("Overwrite mode selected")
    newPdfPath = input("Path of PDF to be inserted: ").replace("\\","/")
    nPage = int(input("Page on which insertion should start: "))
       
    baseReader = PdfFileReader(basePdfPath)
    newReader = PdfFileReader(newPdfPath)
    if nPage > baseReader.getNumPages():
        print("Error: Call wants to overwrite pages after ending of base")
    else:
        nrp = newReader.getNumPages()
        
        for page in range(nPage):
            writer.addPage(baseReader.getPage(page))
        for newPage in range(nrp):
            writer.addPage(newReader.getPage(newPage))
        for page in range(nPage+nrp, baseReader.getNumPages()):
            writer.addPage(baseReader.getPage(page))
            
        with open(safePath, 'wb') as out:
            writer.write(out)
        print(f"Successfully overwritten pages {nPage}-{nPage+nrp}")
        
def appendEnd(writer):
    print("Append mode selected")
    seconPdfPath = input("Second pdf path: ").replace("\\","/")
    
    firstReader = PdfFileReader(basePdfPath)
    seconReader = PdfFileReader(seconPdfPath)
    for page in range(firstReader.getNumPages()):
        writer.addPage(firstReader.getPage(page))
    for page in range(seconReader.getNumPages()):
        writer.addPage(seconReader.getPage(page))
    with open(safePath, 'wb') as out:
        writer.write(out)
    print("Successfully appended")
    
def extract(writer):
    print("Extraction mode selected")
    firstPage = int(input("Page number of starting page: ")) - 1 #-1 because index
    lastPage = int(input("Page number of the last page: ")) # no -1 because range func
    
    reader = PdfFileReader(basePdfPath)
    if ((firstPage <= lastPage) and (lastPage <= reader.getNumPages())):
        for page in range(firstPage, lastPage):
            writer.addPage(reader.getPage(page))
        with open(safePath, 'wb') as out:
            writer.write(out)
        print("Successfully extracted")
    else:
        print("Error: Most likely faulty page numbers")
        
if __name__ == "__main__":    
    print(header)
    modes = {
        "o": ["overwrite pages from one pdf with another pdf", overwriteAt],
        "a": ["append one pdf to another", appendEnd],
        "e": ["extract pages from one pdf", extract],
        "x": ["exit the program"]
        }
    while True:
        print("mode\tdescription")
        for mode in modes:
            print(mode + "\t\t" + modes[mode][0])
        selected_mode = input("Select mode: ")
        if selected_mode == "x":
            break
        writerPdf = PdfFileWriter()
        basePdfPath = input("Path of the base PDF: ").replace("\\","/")
        safePath = input("Path to which the result will be saved: ").replace("\\","/")
        try:
            modes[selected_mode][1](writerPdf)
        except OSError as err:
            print("OS error: {0}".format(err))
        except:
            print("\nAN ERROR OCURRED. Returning to selection.\n")
        
    print("Program closed")
    
