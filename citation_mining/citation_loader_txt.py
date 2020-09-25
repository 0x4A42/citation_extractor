import re
import citation_mining.citation_loader_base
from citation_mining.citation_obj import CitationObj


class CitationLoaderTxt(
        citation_mining.citation_loader_base.CitationLoaderBase):

    def __init__(self, path):
        """This class is dedicated to loading text files and extracting
        the info into our given citation object

        Args:
            path (string): path to the text file you are looking to
            extract citations from

        Attributes:
            regex (string): The regex
            analysed_files (list): List containing the info of
            files that have already been analyzed

        """
        self.regex = r"\d*.(.*)\"(.*)\"(.*)|\d*.(.*)"
        self.path = path
        self.analyzed_files = []

    def return_citation_array(self):
        """Goes through the parsed text and extracts citations
            returns the results in a list

        Returns:
            citation_list (list): A list containing the extracted citations
        """
        f = open(self.path, "r")
        if not self.__has_file_been_read__():
            list_of_citations = []
            with open(self.path, 'r') as file:
                for string in self.__nonblank_lines__(file):

                    match = re.search(self.regex, string)
                    if match.group(1) is None:

                        list_of_citations.append(CitationObj(
                            match.group(4), [], "", self.path))
                    else:

                        list_of_authors = [match.group(1)]
                        list_of_citations.append(CitationObj(match.group(
                            2), list_of_authors, match.group(3), self.path))
            self.analyzed_files.append(self.path)
            return list_of_citations
        else:
            print("File already analyzed")

    def return_citation_dictionary(self):
        if not self.__has_file_been_read__():
            list_of_citations = []
            with open(self.path, 'r') as file:
                for string in self.__nonblank_lines__(file):
                    match = re.search(self.regex, string)
                    if match.group(1) is None:
                        list_of_citations.append(CitationObj(
                            match.group(4), [], "", self.path))
                        self.analyzed_files.append(self.path)
                    else:
                        list_of_authors = [match.group(1)]
                        list_of_citations.append(CitationObj(match.group(
                            2), list_of_authors, match.group(3), self.path))
                        self.analyzed_files.append(self.path)
            citation_dict = {"Citations": list_of_citations}
            self.analyzed_files.append(self.path)
            return citation_dict
        else:
            print("File already analyzed")

    def is_text(self):
        """Determines if the file is .txt

        Returns:
            True (Boolean): Indicates the file is .txt
            False (Boolean): Indicates the file is not .txt
        """
        if self.path.lower().endswith('.txt'):
            return True
        else:
            return False

    def change_file(self, new_file_path):
        """Changes the file the loader is extracting info from
        Not currently in use in this version of the code but may be relevant
        to future developers.
        Args:
            new_file_path (string): The new file path
        """
        self.path = new_file_path

    def clear_analyzed_files(self):
        """Clears the analyzed files from the analyzed_files list
            Not currently in use in this version of the code but may be
            relevant to future developers.
        """
        self.analyzed_files = []

    def __nonblank_lines__(self, file):
        """Removes all blank lines from the input file to help
        preserve ordering

        Args:
            file (file): The file to iterate through

        Yields:
            line (string): A line of text
        """
        for unstripped_line in file:
            line = unstripped_line.rstrip()
            if line:
                yield line

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
                if self.path == file:
                    return True
        return False
