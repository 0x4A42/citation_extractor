import unittest

from citation_mining.citation_obj import CitationObj


# test_citation duplicated instead of using a instance of it due to
# mutation leading to possible non
class TestCitationObj(unittest.TestCase):

    def test_correct_default_assignment(self):
        """Ensures that assignment starts as unsigned
        """
        test_citation = CitationObj("", "", "", "")
        self.assertEqual("Unassigned", test_citation.get_classification())

    def test_changing_assignment(self):
        """Ensures change assignment works
        """
        test_citation = CitationObj("", "", "", "")
        test_citation.set_classification("Trial")
        self.assertEqual("Trial", test_citation.get_classification())

    def test_correct_convert_to_dict(self):
        """Ensure that the convert to dict functon is returning the fields as
        expected
        """
        test_citation = CitationObj("", "", "", "")
        dict = test_citation.convert_to_dict()
        self.assertEqual(5, len(dict))

    def test_correct_getters(self):
        """[Ensure getters functioning as intended]
        """
        test_citation = CitationObj("", "", "", "")
        self.assertEqual("", test_citation.get_author())
        self.assertEqual("", test_citation.get_journal())
        self.assertEqual("", test_citation.get_title())
