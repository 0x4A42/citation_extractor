import re


class CitationAnalyzer:
    def __init__(self, array_of_citations, dict_of_keywords):
        """This class uses the dictionary of citations and array of
            user defined keywords to assign citations.
            This class was written by the original developer.

        Args:
            array_of_citations (list): Array of citations extracted from a
            loader
            dict_of_keywords (dictionary): Dictionary of keyword/searchterm
            mappings extracted by keyword loader
        """
        self.array_of_citations = array_of_citations
        self.dict_of_keywords = dict_of_keywords

    def return_dictionary_of_two_comparable_citations(self, dictionary_key_one,
                                                      dictionary_key_two):
        """Separates all available citations into two groups as defined by
            the user

        Args:
            dictionary_key_one (string): represents a key in
             dict_of_keywords
            dictionary_key_two (string): represents a key in
             dict_of_keywords

        Returns:
            (dictionary): A dictionary containing two groups of citations
             as defined.
        """
        list_of_one_citations = []
        list_of_two_citations = []
        list_of_unassigned_citations = []
        for citation in self.array_of_citations:
            citation_string = self.__generate_author_string__(
                citation.get_author()) + " " + citation.get_title() \
                + " " + citation.get_journal()
            one_key_matches = self.__count_of_keyword_matches__(
                citation_string, dictionary_key_one)
            two_key_matches = self.__count_of_keyword_matches__(
                citation_string, dictionary_key_two)
            if one_key_matches > two_key_matches:
                citation.set_classification(dictionary_key_one)
                list_of_one_citations.append(citation)
            elif two_key_matches > one_key_matches:
                citation.set_classification(dictionary_key_two)
                list_of_two_citations.append(citation)
            else:
                citation.set_classification("Unassigned")
                list_of_unassigned_citations.append(citation)

        return {dictionary_key_one: list_of_one_citations, dictionary_key_two:
                list_of_two_citations, "Unassigned":
                list_of_unassigned_citations}

    def return_dict_of_assigned_citations_classifications(self):
        """Separates all available citations into the sections defined
           by user in the keywords file

        Returns:
            [function call]: A call to the
            __generate_dict_of_keys_to_classification__() function
        """
        for citation_instance in self.array_of_citations:
            citation_string = ""
            citation_string = citation_string.join(
                citation_instance.get_author()) + \
                citation_instance.get_title()\
                + citation_instance.get_journal()
            max_keyword_matches = 0
            for key in self.dict_of_keywords:
                current_key_matches = 0
                for keyword in self.dict_of_keywords.get(key):
                    pattern = re.compile(keyword)
                    if pattern.search(citation_string):
                        current_key_matches += 1
                if current_key_matches > max_keyword_matches:
                    max_keyword_matches = current_key_matches
                    citation_instance.set_classification(key)
        return self.__generate_dict_of_keys_to_classification__()

    def __count_of_keyword_matches__(self, citation_string, key_string):
        """Given a key_string that is present in array_of_keywords how many
            matches are there

        Args:
            citation_string (string): The citation being analyzed
            key_string (type): The key which search terms will be
            used to analyze citation_string

        Returns:
            matches (int): The number of matches of key_string
             in citation_string
        """
        matches = 0
        for keyword in self.dict_of_keywords.get(key_string):
            pattern = re.compile(keyword)
            if pattern.search(citation_string):
                matches += 1
        return matches

    def __generate_author_string__(self, list_of_authors):
        """Given a list of authors return a string separated by spaces

        Args:
            list_of_authors (list): List of authors that will be changed
            to one string

        Returns:
            author_string (string): A string containing all authors
        """
        author_string = ""
        return author_string.join(list_of_authors)

    def __generate_dict_of_keys_to_classification__(self):
        """Given the current assignment state of self.array_of_citations
            and creates a dictionary linking the keys to the
            citations assignment

        Returns:
            dict_of_assigned_citations (dictionary): A dictionary containing
            the assigned citations
        """
        dict_of_assigned_citations = {}
        # duplicating citation dataset to filter as matches go on meaning
        #       it should result in quicker allocation
        # can be removed to reduce memory load at expense of speed
        list_of_unassigned = []
        for key in self.dict_of_keywords:
            list_of_current_key = []
            for citation_instance in self.array_of_citations:
                if key == citation_instance.get_classification():
                    list_of_current_key.append(citation_instance)
                if "Unassigned" == citation_instance.get_classification():
                    list_of_unassigned.append(citation_instance)
            dict_of_assigned_citations[key] = list_of_current_key
        dict_of_assigned_citations["Unassigned"] = list_of_unassigned
        return dict_of_assigned_citations
