import unittest

from citation_mining.citation_loader_bibtex import CitationLoaderBibTex
from citation_mining.citation_loader_dblp import CitationLoaderDBLP
from citation_mining.citation_loader_pdf import CitationLoaderPDF
from citation_mining.citation_loader_txt import CitationLoaderTxt
from citation_mining.citation_loader_docx import CitationLoaderDocx


class TestConsistentLoading(unittest.TestCase):
    citations_string = "Citations"
    pdf_file_location = "../test_documents/Calderon.pdf"
    bibtext_file_location = "../test_documents/bibtextData"
    text_file_location = "../test_documents/data.txt"
    dblp_file_location = "../test_documents/DBLP_Snippet.txt"
    pdf_regex_location = "../../static/json/pdfloaderregex.json"
    docx_file_location = "../test_documents/sample_citations_second.docx"

    def test_pdf_loader_citations_array(self):
        loader = CitationLoaderPDF(self.pdf_file_location, self.pdf_regex_location)
        self.assertEqual(27, len(loader.return_citation_array()))

    def test_pdf_loader_url(self):
        loader = CitationLoaderPDF(self.pdf_file_location, self.pdf_regex_location)
        self.assertEqual(3, len(loader.return_url_array()))

    def test_pdf_loader_doi(self):
        loader = CitationLoaderPDF(self.pdf_file_location, self.pdf_regex_location)
        self.assertEqual(1, len(loader.return_doi_array()))

    def test_bibtex_loader_array(self):
        loader = CitationLoaderBibTex(self.bibtext_file_location)
        self.assertEqual(2, len(loader.return_citation_array()))

    def test_bibtex_loader_dict(self):
        loader = CitationLoaderBibTex(self.bibtext_file_location)
        self.assertEqual(2, len(loader.return_citation_dictionary()[self.citations_string]))

    def test_text_loader_array(self):
        loader = CitationLoaderTxt(self.text_file_location)
        self.assertEqual(1553, len(loader.return_citation_array()))

    def test_text_loader_dict(self):
        loader = CitationLoaderTxt(self.text_file_location)
        self.assertEqual(1553, len(loader.return_citation_dictionary()[self.citations_string]))

    def test_dblp_loader_array(self):
        loader = CitationLoaderDBLP(self.dblp_file_location)
        self.assertEqual(4, len(loader.return_citation_array()))

    def test_dblp_loader_dict(self):
        loader = CitationLoaderDBLP(self.dblp_file_location)
        self.assertEqual(4, len(loader.return_citation_dictionary()[self.citations_string]))

    def test_docx_loader_array(self):
        loader = CitationLoaderDocx(self.docx_file_location, self.pdf_regex_location)
        self.assertEqual(83, len(loader.return_citation_array()))

    def test_docx_loader_dict(self):
        loader = CitationLoaderDocx(self.docx_file_location, self.pdf_regex_location)
        self.assertEqual(83, len(loader.return_citation_dictionary()[self.citations_string]))


if __name__ == '__main__':
    unittest.main()
