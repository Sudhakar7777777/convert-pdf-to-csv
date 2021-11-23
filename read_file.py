from PyPDF2 import PdfFileReader


def extract_information(pdf_path: str):
    with open(pdf_path, 'rb') as f:
        pdf = PdfFileReader(f)
        information = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()

    txt = f"""
    Information about {pdf_path}: 

    Author: {information.author}
    Creator: {information.creator}
    Producer: {information.producer}
    Subject: {information.subject}
    Title: {information.title}
    Number of pages: {number_of_pages}
    """

    print(txt)
    return information


def extract_content(pdf_path: str, page_number: int):
    with open(pdf_path, 'rb') as f:
        pdf = PdfFileReader(f)

        # get the first page
        page = pdf.getPage(page_number)
        print(page)
        print('Page type: {}'.format(str(type(page))))

        text = page.extractText()
        print(text)


if __name__ == '__main__':
    path = 'ratings.pdf'
    extract_information(path)
    extract_content(path, 3)
