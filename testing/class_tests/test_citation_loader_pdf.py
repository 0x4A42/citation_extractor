import unittest

from citation_mining.citation_loader_pdf import CitationLoaderPDF


class TestCitationLoaderPDF(unittest.TestCase):
    pdf_file_location = "../test_documents/Calderon.pdf"
    pdf_regex_location = "../../static/json/pdfloaderregex.json"
    loader = CitationLoaderPDF(pdf_file_location, pdf_regex_location)
    citation_array = loader.return_citation_array()
    loader.clear_analyzed_files()
    citation_dict = loader.return_citation_dictionary()
    expected_dict_keys = ['IEEE']
    expected_title_string = "2016"
    docx_file_location = "../test_documents/sample_citations_second.docx"
    not_file_type_loader = CitationLoaderPDF(
        docx_file_location, pdf_regex_location)

    def test_is_pdf(self):
        """Asserts the file is .pdf
        """
        self.assertTrue(self.loader.is_pdf())

    def test_is_not_pdf(self):
        """Asserts the file is not .pdf
        """
        self.assertFalse(self.not_file_type_loader.is_pdf())

    def test_pdf_loader_array_size(self):
        """Asserts that the same number of values are extracted each time]
        """
        self.assertEqual(27, len(self.citation_array))

    def test_pdf_loader_array_consistency(self):
        """Asserts that the ordering of the array is consistent
        """
        self.assertEqual(
            self.citation_array[0].get_title(), self.expected_title_string)

    def test_pdf_loader_dict_key_length(self):
        """Asserts that the number of keys in the dict is consistent
        """
        self.assertEqual(1, len(self.citation_dict.keys()))

    def test_pdf_loader_dict_key_names(self):
        """Asserts that the key names are as expected
        """
        self.assertEqual(list(self.citation_dict), self.expected_dict_keys)

    def test_pdf_loader_dict_values_length(self):
        """Asserts that the number of values in the dict is consistent
        """
        self.assertEqual(
            27, len(self.citation_dict[self.expected_dict_keys[0]]))

    def test_pdf_loader_dict_consistency(self):
        """Asserts that the ordering of the dict is consistent
        """
        self.assertEqual(self.citation_dict[self.expected_dict_keys[0]]
                         [0].get_title(), self.expected_title_string)

    def test_pdf_loader_same_length_in_array_and_dict(self):
        """Asserts that the dict and array are loaded with the same values
        """
        self.assertEqual(
            len(self.citation_dict[self.expected_dict_keys[0]]),
            len(self.citation_array))


if __name__ == '__main__':
    unittest.main()
