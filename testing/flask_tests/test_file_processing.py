import file_processing
import logging
import os
from site_main import app
import unittest


class FlaskTest(unittest.TestCase):
    logging.shutdown()
    pdf_file_location = "../test_documents/Calderon.pdf"
    bibtext_file_location = "../test_documents/bibtextData"
    txt_file_location = "../test_documents/data.txt"
    dblp_file_location = "../test_documents/DBLP_Snippet.txt"
    docx_file_location = "../test_documents/sample_citations_second.docx"
    png_file_location = "../test_documents/file-upload-icon.png"
    upload_path = "test_cleanup"

    def setUp(self):
        app.config['TESTING'] = True

    def test_extract_citations_pdf(self):
        """
        Asserts consistent length of extraction in pdf
        """
        pdf_array = file_processing.extract_citations(self.pdf_file_location)
        self.assertEqual(27, len(pdf_array))

    def test_extract_citations_docx(self):
        """
        Asserts consistent length of extraction in docx
        """
        docx_array = file_processing.extract_citations(self.docx_file_location)
        self.assertEqual(83, len(docx_array))

    def test_extract_citations_txt(self):
        """
        Asserts consistent length of extraction in txt
        """
        txt_array = file_processing.extract_citations(self.txt_file_location)
        self.assertEqual(1553, len(txt_array))

    def test_extract_citations_dblp(self):
        """
        Asserts consistent length of extraction in dblp
        """
        dblp_array = file_processing.extract_citations(self.dblp_file_location)
        self.assertEqual(4, len(dblp_array))

    def test_extract_citations_bibtex(self):
        """
        Asserts consistent length of extraction in bibtex
        """
        bibtex_array = file_processing.extract_citations(
            self.bibtext_file_location)
        self.assertEqual(2, len(bibtex_array))

    def test_extract_citations_else(self):
        """
        Asserts extraction array is None when an unsupported
        file type is processed
        """
        blank_array = file_processing.extract_citations(self.png_file_location)
        self.assertTrue(blank_array is None)

    def test_start_citation_analysis_docx(self):
        """
        Asserts consistent length of dictionary in docx
        """
        docx_array = file_processing.extract_citations(self.docx_file_location)
        docx_dict = file_processing.start_citation_analysis(docx_array)
        self.assertEqual(10, len(docx_dict))

    def test_start_citation_analysis_pdf(self):
        """
        Asserts consistent length of dictionary in pdf
        """
        pdf_array = file_processing.extract_citations(self.pdf_file_location)
        pdf_dict = file_processing.start_citation_analysis(pdf_array)
        self.assertEqual(10, len(pdf_dict))

    def test_start_citation_analysis_txt(self):
        """
        Asserts consistent length of dictionary in txt
        """
        txt_array = file_processing.extract_citations(self.txt_file_location)
        txt_dict = file_processing.start_citation_analysis(txt_array)
        self.assertEqual(10, len(txt_dict))

    def test_start_citation_analysis_dblp(self):
        """
        Asserts consistent length of dictionary in dblp
        """
        dblp_array = file_processing.extract_citations(self.dblp_file_location)
        dblp_dict = file_processing.start_citation_analysis(dblp_array)
        self.assertEqual(10, len(dblp_dict))

    def test_start_citation_analysis_bibtex(self):
        """
        Asserts consistent length of dictionary in bibtex
        """
        bibtex_array = file_processing.extract_citations(self.bibtext_file_location)
        bibtex_dict = file_processing.start_citation_analysis(bibtex_array)
        self.assertEqual(10, len(bibtex_dict))

    def test_write_citations_to_file_docx(self):
        """
        Asserts output file is created for docx
        """
        docx_array = file_processing.extract_citations(self.docx_file_location)
        docx_dict = file_processing.start_citation_analysis(docx_array)
        file_processing.write_citations_to_file_json(
            docx_dict, self.upload_path)
        self.assertTrue(os.path.exists(self.upload_path + '/output.txt'))

    def test_write_citations_to_file_pdf(self):
        """
        Asserts output file is created for pdf
        """
        pdf_array = file_processing.extract_citations(self.pdf_file_location)
        pdf_dict = file_processing.start_citation_analysis(pdf_array)
        file_processing.write_citations_to_file_json(
            pdf_dict, self.upload_path)
        self.assertTrue(os.path.exists(self.upload_path + '/output.txt'))

    def test_generate_results_chart(self):
        """Asserts graph file is created
        """
        os.remove(self.upload_path + '/output.txt')
        txt_array = file_processing.extract_citations(self.docx_file_location)
        txt_dict = file_processing.start_citation_analysis(txt_array)
        file_processing.write_citations_to_file_json(
            txt_dict, self.upload_path)
        file_processing.generate_results_chart(self.upload_path)
        self.assertTrue(os.path.exists(self.upload_path + '/results_graph.png'))

    def test_create_zip(self):
        """
        Asserts zip file is created
        """
        open('test_cleanup/output.txt', 'a').close()
        zip_name = 'results_file.zip'
        file_processing.create_zip(self.upload_path, zip_name)
        self.assertTrue(os.path.exists(self.upload_path + '/' + zip_name))


if __name__ == "__main__":
    unittest.main()
