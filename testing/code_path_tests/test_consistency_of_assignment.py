import unittest
from citation_mining.citation_analyzer import CitationAnalyzer
from citation_mining.citation_loader_bibtex import CitationLoaderBibTex
from citation_mining.citation_loader_dblp import CitationLoaderDBLP
from citation_mining.citation_loader_pdf import CitationLoaderPDF
from citation_mining.citation_loader_txt import CitationLoaderTxt
from citation_mining.citation_loader_docx import CitationLoaderDocx
from citation_mining.keyword_loader import KeywordLoader


class TestConsistencyOfAssignment(unittest.TestCase):
    pdf_file_location = "../test_documents/Calderon.pdf"
    bibtext_file_location = "../test_documents/bibtextData"
    text_file_location = "../test_documents/data.txt"
    dblp_file_location = "../test_documents/DBLP_Snippet.txt"
    pdf_regex_location = "../../static/json/pdfloaderregex.json"
    docx_file_location = "../test_documents/sample_citations_second.docx"
    keyword_dict = KeywordLoader(
        "../flask_tests/static/json/KeywordsArray.json").return_dict_of_keywords()

    comp_arch_string = "Computer Architecture"
    cyber_sec_string = "Cyber Security"
    machine_learning_string = "Machine Learning"
    software_eng_string = "Software Engineering"
    testing_string = "Software Testing"
    blog_string = "Blog"
    newspaper_string = "Newspapers"
    academic_string = "Academic"
    non_academic_string = "Non-Academic"

    def test_txt_analysis(self):
        """[Ensures the txt analysis consistently pulls the same amount of
        citations]
        """
        loader = CitationLoaderTxt(self.text_file_location)
        analyzer = CitationAnalyzer(
            loader.return_citation_array(), self.keyword_dict)
        txt_dict = analyzer.return_dict_of_assigned_citations_classifications()
        self.assertEqual(1288, len(txt_dict[self.academic_string]))
        self.assertEqual(254, len(txt_dict[self.non_academic_string]))
        self.assertEqual(2, len(txt_dict[self.blog_string]))
        self.assertEqual(0, len(txt_dict[self.comp_arch_string]))
        self.assertEqual(2, len(txt_dict[self.cyber_sec_string]))
        self.assertEqual(4, len(txt_dict[self.machine_learning_string]))
        self.assertEqual(1, len(txt_dict[self.software_eng_string]))
        self.assertEqual(2, len(txt_dict[self.testing_string]))
        self.assertEqual(0, len(txt_dict[self.newspaper_string]))

    def test_bibtext_analysis(self):
        """[Ensures the bibtex analysis consistently pulls the same amount of
         citations]
        """
        loader = CitationLoaderBibTex(self.bibtext_file_location)
        analyzer = CitationAnalyzer(
            loader.return_citation_array(), self.keyword_dict)
        bib_dict = analyzer.return_dict_of_assigned_citations_classifications()
        self.assertEqual(2, len(bib_dict[self.academic_string]))
        self.assertEqual(0, len(bib_dict[self.non_academic_string]))
        self.assertEqual(0, len(bib_dict[self.blog_string]))
        self.assertEqual(0, len(bib_dict[self.comp_arch_string]))
        self.assertEqual(0, len(bib_dict[self.cyber_sec_string]))
        self.assertEqual(0, len(bib_dict[self.machine_learning_string]))
        self.assertEqual(0, len(bib_dict[self.software_eng_string]))
        self.assertEqual(0, len(bib_dict[self.testing_string]))
        self.assertEqual(0, len(bib_dict[self.newspaper_string]))

    def test_dblp_analysis(self):
        """[Ensures the dblp analysis consistently pulls the same amount of
         citations]
        """
        loader = CitationLoaderDBLP(self.dblp_file_location)
        analyzer = CitationAnalyzer(
            loader.return_citation_array(), self.keyword_dict)
        dblp_dict = analyzer.return_dict_of_assigned_citations_classifications()
        self.assertEqual(3, len(dblp_dict[self.academic_string]))
        self.assertEqual(1, len(dblp_dict[self.non_academic_string]))
        self.assertEqual(0, len(dblp_dict[self.blog_string]))
        self.assertEqual(0, len(dblp_dict[self.comp_arch_string]))
        self.assertEqual(0, len(dblp_dict[self.cyber_sec_string]))
        self.assertEqual(0, len(dblp_dict[self.machine_learning_string]))
        self.assertEqual(0, len(dblp_dict[self.software_eng_string]))
        self.assertEqual(0, len(dblp_dict[self.testing_string]))
        self.assertEqual(0, len(dblp_dict[self.newspaper_string]))

    def test_pdf_analysis(self):
        """[Ensures the pdf analysis consistently pulls the same amount of
         citations]
        """
        loader = CitationLoaderPDF(
            self.pdf_file_location, self.pdf_regex_location)
        analyzer = CitationAnalyzer(
            loader.return_citation_array(), self.keyword_dict)
        pdf_dict = analyzer.return_dict_of_assigned_citations_classifications()
        self.assertEqual(26, len(pdf_dict[self.academic_string]))
        self.assertEqual(1, len(pdf_dict[self.non_academic_string]))
        self.assertEqual(0, len(pdf_dict[self.blog_string]))
        self.assertEqual(0, len(pdf_dict[self.comp_arch_string]))
        self.assertEqual(0, len(pdf_dict[self.cyber_sec_string]))
        self.assertEqual(0, len(pdf_dict[self.machine_learning_string]))
        self.assertEqual(0, len(pdf_dict[self.software_eng_string]))
        self.assertEqual(0, len(pdf_dict[self.testing_string]))
        self.assertEqual(0, len(pdf_dict[self.newspaper_string]))

    def test_docx_analysis(self):
        """[Ensures the docx analysis consistently pulls the same amount of
        citations]
        """
        loader = CitationLoaderDocx(
            self.docx_file_location, self.pdf_regex_location)
        analyzer = CitationAnalyzer(
            loader.return_citation_array(), self.keyword_dict)
        docx_dict = analyzer.return_dict_of_assigned_citations_classifications()
        self.assertEqual(71, len(docx_dict[self.academic_string]))
        self.assertEqual(9, len(docx_dict[self.non_academic_string]))
        self.assertEqual(2, len(docx_dict[self.blog_string]))
        self.assertEqual(0, len(docx_dict[self.comp_arch_string]))
        self.assertEqual(0, len(docx_dict[self.cyber_sec_string]))
        self.assertEqual(0, len(docx_dict[self.machine_learning_string]))
        self.assertEqual(1, len(docx_dict[self.software_eng_string]))
        self.assertEqual(0, len(docx_dict[self.testing_string]))
        self.assertEqual(0, len(docx_dict[self.newspaper_string]))


if __name__ == '__main__':
    unittest.main()
