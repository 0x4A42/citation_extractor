import json
from itertools import chain
from citation_mining.citation_obj import CitationObj


class CitationJsonManager:
    def __init__(self):
        """Class that saves citations to valid JSON and can load this json
            back into a list of citations.
            Only contains static methods so should not be implemented.
            This file was written by the original developer.
        """
        pass

    @staticmethod
    def write_to_file(file_path, dict_of_citations):
        """[Writes the dictionary of classified citation to a json format at
            location file_path]

        Args:
            file_path ([string]): [the path the json will be saved to]
            dict_of_citations ([dictionary]): [the citations that will be
            transformed to json]
        """
        list_of_analysed_components = list(
            chain.from_iterable(list(dict_of_citations.values())))

        list_of_id = []
        dict_of_id = {}
        for i in list_of_analysed_components:
            if list_of_id.count(i.get_id()) == 0:
                list_of_id.append(i.get_id())
                temp_list = []
                current_id = i.get_id()
                for item in list_of_analysed_components:
                    if item.get_id() == current_id:
                        serialised_item = item.convert_to_dict()
                        temp_list.append(serialised_item)
                dict_of_id[current_id] = temp_list

        with open(file_path, 'a') as fp:
            json.dump(dict_of_id, fp, indent=4)
            fp.write("\n")

    @staticmethod
    def load_from_file_to_array(file_path):
        """Loads saved Json citations to array

        Args:
            file_path (String): The path to the json file to be loaded

        Returns:
            list_of_citations (list): A list of citations
        """
        list_of_citations = []
        with open(file_path, 'r') as file:
            for string in file:
                cit_dict = json.loads(string)
                for id_list in cit_dict.values():
                    for citation in id_list:
                        title = citation.pop("title")
                        journal = citation.pop("journal")
                        author = citation.pop("author")
                        id = citation.pop("id")
                        classification = citation.pop("classification")
                        temp_citation = CitationObj(title, author, journal, id)
                        temp_citation.set_classification(classification)
                        list_of_citations.append(temp_citation)
        return list_of_citations

    @staticmethod
    def load_from_file_to_dict(file_path):
        """Loads saved Json citations to a dictionary

        Args:
            file_path (string): The path to the json file to be loaded

        Returns:
            dictionary_of_loaded_results (dictionary): A dictionary
            of citations
        """
        list_of_citations = CitationJsonManager.load_from_file_to_array(
            file_path)
        classifications = []
        for citation in list_of_citations:
            if citation.get_classification() not in classifications:
                classifications.append(citation.get_classification())

        dictionary_of_loaded_results = {}
        for classification in classifications:
            citation_list = []
            for citation in list_of_citations:
                if citation.get_classification() == classification:
                    citation_list.append(citation)
            dictionary_of_loaded_results[classification] = citation_list

        return dictionary_of_loaded_results
