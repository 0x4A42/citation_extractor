from citation_mining.citation_obj import CitationObj
from citation_mining.citation_loader_base import CitationLoaderBase
import io
import json
import re
from pdfminer3.layout import LAParams
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter


class CitationLoaderPDF(CitationLoaderBase):

    def __init__(self, file_path, regex_path):
        """This class is the loader for PDF files, extracting data from the
        text of academic papers

        Args:
            file_path (string): path to the PDF file you are looking to
            extract citations from
            regex_path (string): path to the regex

        Attributes:
            analyzed_files (list): Array containing the data of files that
            have already been analyzed
        """
        self.file_path = file_path
        self.regex_path = regex_path
        self.analyzed_files = []

    def return_citation_array(self):
        """Goes through the parsed text and extracts citations
            returns the results in a list

        Returns:
            citation_list (list): A list containing the extracted citations
        """
        if not self.__has_file_been_read__():
            list_of_citation_objects = []
            pdf_text = self.__get_pdf_text__()
            citation_regex = self.__get_citation_regex__()
            citation_data = re.findall(citation_regex, pdf_text)
            for citation in citation_data:
                list_of_citation_objects.append(CitationObj(
                    citation[1], citation[0], citation[2], self.file_path))
            self.analyzed_files.append(self.file_path)
            return list_of_citation_objects
        else:
            print("File already analyzed")

    def return_citation_dictionary(self):
        """Goes through the parsed text and extracts citations
            returns the results in a dictionary

        Returns:
            citation_dict (dictionary): A dictionary containing the
            extracted citations
        """
        if not self.__has_file_been_read__():
            list_of_citation_objects = []
            pdf_text = self.__get_pdf_text__()
            citation_regex = self.__get_citation_regex__()
            citation_data = re.findall(citation_regex, pdf_text)
            for citation in citation_data:
                list_of_citation_objects.append(CitationObj(
                    citation[1], citation[0], citation[2], self.file_path))
            citation_dict = {"IEEE": list_of_citation_objects}
            self.analyzed_files.append(self.file_path)
            return citation_dict
        else:
            print("File already analyzed")

    def return_complete_dict(self):
        """Returns a dictionary of all terms defined in the config file

        Returns:
            citation_dict (dictionary): A dictionary of all terms defined in
            the config file
        """
        list_of_citation_objects = []
        pdf_text = self.__get_pdf_text__()
        citation_regex = self.__get_citation_regex__()
        url_regex = self.__get_url_regex__()
        doi_regex = self.__get_doi_regex__()
        citation_data = re.findall(citation_regex, pdf_text)
        list_of_urls = re.findall(url_regex, pdf_text)
        list_of_dois = re.findall(doi_regex, pdf_text)
        for citation in citation_data:
            list_of_citation_objects.append(CitationObj(
                citation[1], citation[0], citation[2]))
        citation_dict = {"IEEE": list_of_citation_objects,
                         "URLS": list_of_urls,
                         "DOIS": list_of_dois}
        return citation_dict

    def return_url_array(self):
        """Returns a list of all matches to the url regex if present
        Not currently in use in this version of the code but may be relevant
        to future developers.
        Returns:
            (list): [A list of all matches to the url regex
        """
        pdf_text = self.__get_pdf_text__()
        url_regex = self.__get_url_regex__()
        return re.findall(url_regex, pdf_text)

    def return_doi_array(self):
        """Returns a list of all matches to the doi regex if present
                Not currently in use in this version of the code but may be
                relevant to future developers.
        Returns:
            list: A list of all matches to the doi regex
        """
        pdf_text = self.__get_pdf_text__()
        doi_regex = self.__get_doi_regex__()
        return re.findall(doi_regex, pdf_text)

    def is_pdf(self):
        """Determines if the file is .pdf

        Returns:
            True (Boolean): Indicates the file is .pdf
            False (Boolean): Indicates the file is not .pdf
        """
        if self.file_path.lower().endswith('.pdf'):
            return True
        else:
            return False

    def clear_analyzed_files(self):
        """
        Clears the analyzed files from the analyzed_files list
        Not currently in use in this version of the code but may be relevant
        to future developers.
        """
        self.analyzed_files = []

    def change_file(self, new_file_path):
        """Changes the file the loader is extracting data from
        Not currently in use in this version of the code but may be relevant
        to future developers.
        Args:
            new_file_path ([string]): [The new file path
        """
        self.file_path = new_file_path

    def __get_pdf_text__(self):
        """Extracts all the text from the pdf while removing
        superfluous/unmatched space characters

        Returns:
            text (string): A string of all pdf text
        Code from:
        https://stackoverflow.com/questions/56494070/how-to-use-pdfminer-six-with-python-3
        """
        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        converter = TextConverter(
            resource_manager, fake_file_handle, laparams=LAParams())
        page_interpreter = PDFPageInterpreter(resource_manager, converter)

        with open(self.file_path, 'rb') as fh:

            for page in PDFPage.get_pages(fh,
                                          caching=True,
                                          check_extractable=True):
                page_interpreter.process_page(page)

            text = fake_file_handle.getvalue()

        # close open handles
        converter.close()
        fake_file_handle.close()
        text = text.replace('\n', '').replace('\r', '  ')
        return text

    def __get_citation_regex__(self):
        """Gets the regex from the user defined file that extracts citations

        Returns:
           re.compile (dictionary): A dictionary containing the regex
        """
        with open(self.regex_path, 'r', errors='ignore') as f:
            regex_dict = json.load(f)
        return re.compile(regex_dict.get("IEEE"), re.MULTILINE)

    def __get_url_regex__(self):
        """Gets the regex from the config file that extracts urls
        Not currently in use in this version of the code but may be relevant
        to future developers.
        Returns:
            re.compile(dictionary): [Dictionary of the URL regex
        """
        with open(self.regex_path, 'r', errors='ignore') as f:
            regex_dict = json.load(f)
        return re.compile(regex_dict.get("URL"))

    def __get_doi_regex__(self):
        """Gets the regex from the user defined file that extracts DOI's
        Not currently in use in this version of the code but may be relevant
        to future developers.
        Returns:
            re.compile(dictionary): Dictionary containing doi regex
        """
        with open(self.regex_path, 'r', errors='ignore') as f:
            regex_dict = json.load(f)
        return re.compile(regex_dict.get("DOI"))

    def __has_file_been_read__(self):
        """Determines if the file has already been analyzed
        Not currently in use in this version of the code but may be relevant
        to future developers.
        Returns:
            True (Boolean): Indicates the file has been read
            False (Boolean): Indicates the file has not been read
        """
        if len(self.analyzed_files) > 0:
            for file in self.analyzed_files:
                if self.file_path == file:
                    return True
        return False
