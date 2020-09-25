import citation_mining.citation_loader_base as citation_loader_base
from citation_mining.citation_obj import CitationObj

import bibtexparser


class CitationLoaderBibTex(citation_loader_base.CitationLoaderBase):

    def __init__(self, path):
        """This class is dedicated to loading bibtext files and
            extracting the info into our given citation object

        Args:
            path (string): Path to the bibtex file you are looking
            to extract citations from
        """
        self.path = path
        self.analyzedFiles = []

    def return_citation_array(self):
        """Goes through the parsed text and extracts the citations based
            on the regex.

        Returns:
            citation_list (list): The results of the extracted citations
        """
        if not self.__has_file_been_read__():
            with open(self.path) as bibtex_file:
                bib_database = bibtexparser.load(bibtex_file)

            bib_dict = bib_database.get_entry_dict()
            citation_list = []
            for key, item in bib_dict.items():
                authors = self.__split_authors__(item.get('author'))
                citation_list.append(CitationObj(
                    item.get('title'), authors, item.get('journal'),
                    self.path))
            self.analyzedFiles.append(self.path)
            return citation_list
        else:
            print("File already analyzed")

    def return_citation_dictionary(self):
        """Goes through the parsed text and extracts the citations based
            on the regex.

        Returns:
            citation_dict (dictionary): The results of the extracted
            citations
        """
        if not self.__has_file_been_read__():
            with open(self.path) as bibtex_file:
                bib_database = bibtexparser.load(bibtex_file)
            bib_dict = bib_database.get_entry_dict()
            citation_list = []
            for key, item in bib_dict.items():
                authors = self.__split_authors__(item.get('author'))
                citation_list.append(CitationObj(
                    item.get('title'), authors, item.get('journal'),
                    self.path))
                self.analyzedFiles.append(self.path)
            citation_dict = {"Citations": citation_list}
            return citation_dict
        else:
            print("File already analyzed")

    def is_bibtex(self):
        """Determines is the file is bibtext or not

        Returns:
            True (Boolean): Represents that the file is bibtex
            False (Boolean): Represents that the file is not bibtex
        """
        try:
            with open(self.path) as bibtex_file:
                bib_database = bibtexparser.load(bibtex_file)

            bib_dict = bib_database.get_entry_dict()
            if bool(bib_dict):
                return True
            else:
                return False
        except:
            return False

    def clear_analyzed_files(self):
        """Clears files from the analyzed files array,
            can be useful if looking to ensure consistency on same files
        """
        self.analyzedFiles = []

    def __split_authors__(self, authorstring):
        """splits the author string into a list of authors

        Args:
            authorstring (string): String of authors

        Returns:
            processed_string (list): A list of authors
        """
        processed_string = authorstring.replace(
            "{", "").replace("}", "").replace(" ", "")
        return processed_string.split("and")

    def __has_file_been_read__(self):
        """Determines whether or not the file has been read already
        Not currently in use in this version of the code but may be relevant
        to future developers.
        Returns:
            True (Boolean): File has been analysed
            False (Boolean): File has not been analysed
        """
        if len(self.analyzedFiles) > 0:
            for file in self.analyzedFiles:
                if self.path == file:
                    return True
        return False
