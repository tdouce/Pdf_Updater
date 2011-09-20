"""
script for a local organization to take each page from a large pdf
and save it as a seperate pdf with a file name as account number.

http://pybrary.net/pyPdf/
"""

import os, re
from pyPdf import PdfFileWriter, PdfFileReader


# path to the file you want to dice apart
pdfPath = r'C:\Path\to\sample.pdf'

# path to the directory you want to save the files to.
save_to_path = r"C:\some\directory"


def update_pdf( pdfPath, save_to_path ):

    # List to keep track of how many times each account number occured.
    # We will use this to name the files appropriately
    accnt_number_files = []

    page_numbers_not_extracted = []
    
    # instantiate
    input1 = PdfFileReader(file(pdfPath, "rb"))

    # Get number of pages in pdf
    number_of_pages = input1.getNumPages()
    print 'total pages: ', number_of_pages

    # Loop through each page
    for page in range(0,number_of_pages):

        print
        print '*'*20
        print
        print 'Extracting page #',page + 1

        # Get the current page
        page1 = input1.getPage(page)

        # extract the text
        text = page1.extractText().encode("ascii","ignore")

        # Regex to search for the account number
        accnt_number = re.search('\d{2}-\d{2}-[A-Z]{2}\d{3}-\d{3}', text )

        # number of characters an account number has
        length = len(str(accnt_number.group()))
        
        
        # If account number found and exactly 15 characters are in the account number
        if accnt_number and length == 15:

            # Replace some extraneious data
            accnt_number = accnt_number.group().replace(u"\xa0","")
            
            print 'Found account number: ', accnt_number

            #accnt_number_files.append( accnt_number )

            # instantiate the writer object
            output = PdfFileWriter()
        
            # Add page to as is
            output.addPage( input1.getPage( page ))

            if accnt_number in accnt_number_files:

                # create the path to where you want to save the pdf to, file by account number plush number of times accnt number appeared
                save_file = os.path.join( save_to_path, "%s_%s.pdf" % ( accnt_number, accnt_number_files.count(accnt_number)+1 ) )

            else:

                # create the path to where you want to save the pdf to, file by account number
                save_file = os.path.join( save_to_path, "%s.pdf" % accnt_number)

            # Add the the account number to the list
            accnt_number_files.append( accnt_number )

            print 'Saving page to file: ', save_file

            # output stream
            outputStream = file( save_file , "wb")

            # write stream to file
            output.write( outputStream )

            # close file
            outputStream.close()

        # if account number is not found
        else:
            
            print 'can not find account number'
            page_numbers_not_extracted.append( page )


    print '\n'*2
    print '^'*80
    print '\n'*2
    
    # If an account number was not extracted print out the problem page number
    for page in page_numbers_not_extracted:
        
        print 'pdf page NOT extracted: ', page

    # If all pages were successfull the print out a sucessfull message
    if len( page_numbers_not_extracted) == 0:
        
        print len( accnt_number_files ), 'of', number_of_pages, 'successfully written'
        print 'All pages successfully converted to files!'
        print '\n'



            


updatepdf( pdfPath, save_to_path )
