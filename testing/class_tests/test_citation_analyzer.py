import unittest

from citation_mining.citation_analyzer import CitationAnalyzer
from citation_mining.citation_obj import CitationObj


class TestCitationAnalyzer(unittest.TestCase):
    dictOfKeywords = {"Test": ["a "],
                      "Test2": ["i "]}
    arrayOfCitations = [CitationObj("a title","a author","a journal", "a id"), CitationObj("i title", ["i author", "ii author"] , "i journal", "i id")]

    def test_that_results_are_expected(self):
        analyzer = CitationAnalyzer(self.arrayOfCitations, self.dictOfKeywords)
        self.assertEqual(analyzer.return_dict_of_assigned_citations_classifications()["Test"].__getitem__(0).get_title(), "a title")
        self.assertEqual(analyzer.return_dict_of_assigned_citations_classifications()["Test2"].__getitem__(0).get_title(), "i title")

if __name__ == '__main__':
    unittest.main()
