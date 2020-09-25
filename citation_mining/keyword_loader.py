import json


class KeywordLoader:
    def __init__(self, path):
        """This class loads file containing a json structure of keywords
        and search terms

        Args:
            path (string): path to the file containing the mapping of
            keyword to search terms
        """
        with open(path, 'r') as f:
            keywords_dict = json.load(f)
        self.dictionary_of_types_and_keywords = keywords_dict

    def return_types_of_keywords(self):
        """Returns a list of keys present in the file at path

        Returns:
            (list): A list of keys present in the file at path
        """
        return list(self.dictionary_of_types_and_keywords.keys())

    def return_dict_of_keywords(self):
        """Returns a dictionary of keyword/searchterm mapping

        Returns:
            (dictionary): A dictionary of keyword and search term mapping
        """
        return self.dictionary_of_types_and_keywords
