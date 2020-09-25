class CitationObj:
    def __init__(self, title, author, journal, id):
        """This class represents the main object used to store
        info relating to a single citation

        Args:
            title (string): title of citation
            author (string): author of citation
            journal (string): journal citation was published in
            id (int): file that citation came from

        Attributes:
            classification (string): Classification of the citation,
            defaults to unassigned.
        """
        self.title = title
        self.author = author
        self.journal = journal
        self.id = id
        self.classification = "Unassigned"

    def get_title(self):
        """returns the title of the citation

        Returns:
            title (string): title of citation
        """
        return self.title

    def get_author(self):
        """returns the author of the citation

        Returns:
            author (string): author of citation
        """
        if type(self.author) == list:
            return str(self.author).strip('[]')
        else:
            return self.author

    def get_journal(self):
        """Returns the journal of the citation

        Returns:
            journal (string): journal citation was published in
        """
        return self.journal

    def get_classification(self):
        """Returns the classification of the citation

        Returns:
            classification (string): Classification of the citation
        """
        return self.classification

    def get_id(self):
        """returns the title of the citation

        Returns:
            id (int): file that citation came from
        """
        return self.id

    def set_classification(self, new_classification):
        """Changes classification to new_classification

        Args:
            new_classification (string): represents the classification of
            the citation
        """
        self.classification = new_classification

    def convert_to_dict(self):
        """Creates a dict that can be saved as valid json without
        a custom serializer. preceded by class and module to allow us to
        validate data.txt we are loading

        Returns:
            obj_dict(dictionary): Dictionary filled with citation data
        """
        #  Populate the dictionary with object meta data.txt
        obj_dict = {
        }
        #  Populate the dictionary with object properties
        obj_dict.update(self.__dict__)
        return obj_dict
