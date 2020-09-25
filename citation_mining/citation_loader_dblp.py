import json
import citation_mining.citation_loader_base as citation_loader_base
from citation_mining.citation_obj import CitationObj


class CitationLoaderDBLP(citation_loader_base.CitationLoaderBase):

    def __init__(self, path):
        """This class is dedicated to loading the dblp dataset(v11) from here
            and extracting the info into our given citation object

        Args:
            path (String): Path to the DBLP v11 format file you are trying
            to extract citations from
        Attributes:
            analysed_files (list): List containing files that have already
            been analyzed
        """
        self.path = path
        self.analysed_files = []

    def return_citation_array(self):
        """Goes through the parsed text and extracts citations
            returns the results in a list

        Returns:
            citation_list (list): A list containing the extracted citations
        """
        if not self.__has_file_been_read__():
            citation_list = []
            with open(self.path, 'r') as file:
                for string in file:
                    json_string = json.loads(string)
                    authors = self.__get_authors_names__(json_string)
                    journal = self.__get_journals_name__(json_string)
                    citation_list.append(CitationObj(
                        json_string.get('title'), authors, journal, self.path))
            self.analysed_files.append(self.path)
            return citation_list
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
            citation_list = []
            with open(self.path, 'r') as file:
                for string in file:
                    json_string = json.loads(string)
                    authors = self.__get_authors_names__(json_string)
                    journal = self.__get_journals_name__(json_string)
                    citation_list.append(CitationObj(
                        json_string.get('title'), authors, journal, self.path))
            citation_dict = {"Citations": citation_list}
            self.analysed_files.append(self.path)
            return citation_dict
        else:
            print("File already analyzed")

    def is_dblp(self):
        """Determines whether or not the file is dblp format

        Returns:
            True (Boolean): Indicates the file is dblp
            False (Boolean): Indicates the file is not dblp
        """
        try:
            with open(self.path, 'r') as file:
                for string in file:
                    try:
                        json_string = json.loads(string)
                        if json_string.get('n_citation') is None or\
                            json_string.get(
                                'doc_type') is None or json_string.get(
                                'venue') is None:
                            return False
                        return True
                    except:
                        return False
        except:
            return False

    def clear_analyzed_files(self):
        """Clears the analyzed files from the analysed_files list
            Not currently in use in this version of the code but may be
            relevant to future developers.
        """
        self.analysed_files = []

    def __get_authors_names__(self, json_string):
        """Extracts the authors names from the dbpl dataset

        Args:
            json_string (string): A string of all authors.

        Returns:
            list_of_authors (list): A list of all authors from the file.
        """
        authors = json_string.get('authors')
        list_of_authors = []
        for author in authors:
            list_of_authors.append(author.get('name'))
        return list_of_authors

    def __get_journals_name__(self, json_string):
        """Extracts the journals name from the dblp dataset

        Args:
            json_string (string): A string of all journal names.

        Returns:
            venue.get: Name of thr journal
        """
        venue = json_string.get('venue')
        return venue.get('raw')

    def __has_file_been_read__(self):
        """Determines if the file has already been analyzed.
        Not currently in use in this version of the code but may be relevant
        to future developers.

        Returns:
            True (Boolean): Indicates the file has been read
            False (Boolean): Indicates the file has not been read
        """
        if len(self.analysed_files) > 0:
            for file in self.analysed_files:
                if self.path == file:
                    return True
        return False
