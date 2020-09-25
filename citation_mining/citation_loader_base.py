from abc import abstractmethod


class CitationLoaderBase:

    @abstractmethod
    def return_citation_array(self):
        """Return a array of all citations matched from base input
        """
        pass

    @abstractmethod
    def return_citation_dictionary(self):
        """Return a dictionary of all citations matched from base input
        """
        pass
