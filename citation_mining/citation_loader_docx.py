import docx
import json
import re
from citation_mining.citation_obj import CitationObj
from citation_mining.citation_loader_base import CitationLoaderBase


class CitationLoaderDocx(CitationLoaderBase):
    def __init__(self, file_path, regex_path):
        """
            This class processes .docx files and extracts the
            citations from them
        Args:
            file_path (string): path to the PDF file you are looking to
            extract citations from
            regex_path (string): path for the user defined file to
            define the regexs

        Attributes:
            analysed_files (list): List containing files that have already
            been analyzed
        """
        self.file_path = file_path
        self.regex_path = regex_path
        self.analysed_files = []

    def is_docx(self):
        """Checks if the document is .docx

        Returns:
            True (Boolean): Indicates the file is .docx
            False (Boolean): Indicates the file is not .docx
        """
        if self.file_path.lower().endswith('.docx'):
            return True
        else:
            return False

    def return_citation_array(self):
        """Returns a list of all matches to the regex if present

        Returns:
            list_of_citation_objects (list): A list of all matches to the
            regex
        """
        if not self.__has_file_been_read__():
            list_of_citation_objects = []
            docx_text = self.get_document_text()
            citation_regex = self.__get_citation_regex__()
            citation_data = re.findall(citation_regex, docx_text)
            for citation in citation_data:

                list_of_citation_objects.append(CitationObj(
                    citation[1], citation[0], citation[2], self.file_path))
            self.analysed_files.append(self.file_path)
            return list_of_citation_objects
        else:
            print("File already analysed")

    def return_citation_dictionary(self):
        """Returns a dictionary of all matches to the regex
        if present

        Returns:
            citation_dict (dictionary): A dictionary of all matches to the
            regex
        """
        if not self.__has_file_been_read__():
            list_of_citation_objects = []
            docx_text = self.get_document_text()
            citation_regex = self.__get_citation_regex__()
            citation_data = re.findall(citation_regex, docx_text)
            for citation in citation_data:
                list_of_citation_objects.append(CitationObj(
                    citation[1], citation[0], citation[2], self.file_path))
            citation_dict = {"Citations": list_of_citation_objects}
            self.analysed_files.append(self.file_path)
            return citation_dict
        else:
            print("File already analysed")

    def __get_citation_regex__(self):
        """Gets the regex from the config file that extracts citations

        Returns:
           re.compile (dictionary): A dictionary containing the regex
        """
        with open(self.regex_path, 'r', errors='ignore') as f:
            regex_dict = json.load(f)
        return re.compile(regex_dict.get("IEEE"), re.MULTILINE)

    def get_document_text(self):
        """Gets the text from the filepath passed in.
        Iterates through each line within the document, checks if it is blank
        (len == 0), if so passes. If line has content in it, adds
        to parsed_text list for processing.

        Returns:
            parsed_text (list): A list of the document text containing all
            non-blank lines within the document
        """
        document_to_parse = docx.Document(self.file_path)
        parsed_text = []

        for line in document_to_parse.paragraphs:
            if len(line.text.strip()) == 0:
                pass
            else:
                parsed_text.append(line.text)
        return '\n'.join(parsed_text)

    def clear_analyzed_files(self):
        """Clears the analyzed files from the analysed_files list
        Not currently in use in this version of the code but may be relevant
        to future developers.
        """
        self.analysed_files = []

    def __has_file_been_read__(self):
        """Determines if the file has already been analyzed
        Not currently in use in this version of the code but may be relevant
        to future developers.
        Returns:
            True (Boolean): Indicates the file has been read
            False (Boolean): Indicates the file has not been read
        """
        if len(self.analysed_files) > 0:
            for file in self.analysed_files:
                if self.file_path == file:
                    return True
        return False
