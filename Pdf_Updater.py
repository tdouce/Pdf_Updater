"""
script for organization to take each page from a large pdf
and save it as a seperate pdf with a file name as account number.

http://pybrary.net/pyPdf/
"""

import os, re, pdb
from pyPdf import PdfFileWriter, PdfFileReader


# path to the file you want to dice apart
pdfPath = r'C:\Path\To\Pdf\mypdf.pdf'

# path to the directory you want to save the files to.
save_to_path = r"C:\Path\To\Save\Pdfs"


def update_pdf():

    # List to keep track of how many times each account number occured.
    # We will use this to name the files appropriately
    accnt_number_files = []

    accnt_page_tracker = {}

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
            accnt_number = str( accnt_number.group().replace(u"\xa0","") )
            
            # if accnt number has already been encountered
            if accnt_page_tracker.has_key( accnt_number ):

                # Add the page object to the list, with is the dictionary value for the account
                # number (the dictionary key)
                accnt_page_tracker[ accnt_number ] =  accnt_page_tracker[ accnt_number ] + [ page1 ]  

            # if the account number has NOT been encountered
            else:

                # Add it to the dictionary in a list
                accnt_page_tracker[ accnt_number ] =  [ page1 ]

            # append accnt number to the list
            accnt_number_files.append( accnt_number )
   
        # if account number is not found
        else:
            
            print 'can not find account number'
            page_numbers_not_extracted.append( page )

    print
    print '*'*20
    print
    

    # Iterate over each account number in the dictionary
    for accnt_number in accnt_page_tracker.iteritems():

        # Instantiate object
        pdf = PdfFileWriter()

        # for each page object. This will get every page associated with the account number
        for page in accnt_number[1]:

            # Add to object
            pdf.addPage( page )

        # Create the pdf file
        save_file = os.path.join( save_to_path, "%s.pdf" % ( accnt_number[0] ) ) 
        
        # output the stream
        outputStream = file( save_file , "wb")

        # write stream to file
        pdf.write( outputStream )

        # close file
        outputStream.close()


        


    print '\n'*2
    print '^'*80
    print '\n'*2
    
    # If an account number was not extracted print out the problem page number
    for page in page_numbers_not_extracted:
        
        print 'pdf page NOT extracted: ', page

    # If all pages were successfull the print out a sucessfull message
    if len( page_numbers_not_extracted) == 0:
        
        print len( accnt_number_files ), 'of', number_of_pages, 'successfully written'
        print 'All pages successfully extracted and saved to pdf!'
        print '\n'


update_pdf()



