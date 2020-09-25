import citation_mining.citation_presenter as citation_presenter
from citation_mining.citation_analyzer import CitationAnalyzer
from citation_mining.citation_json_manager import CitationJsonManager
from citation_mining.citation_loader_bibtex import CitationLoaderBibTex
from citation_mining.citation_loader_dblp import CitationLoaderDBLP
from citation_mining.citation_loader_pdf import CitationLoaderPDF
from citation_mining.citation_loader_txt import CitationLoaderTxt
from citation_mining.citation_loader_docx import CitationLoaderDocx
from citation_mining.keyword_loader import KeywordLoader
import config
from zipfile import ZipFile

"""
This module is responsible for the processing of files uploaded to the system.
Functions exist to extract citations, process them, generate a chart, and
create a zip of results.
"""


def extract_citations(file_path):
    """This function first determines the file type by checking the extension.
        Then, uses the relevant loader to extract citations from the file.

    Args:
        file_path (string): The path to the file to extract citations from

    Returns:
        results_array (list): A list containing the citations that have been
        extracted from the document
    """
    loader_text = CitationLoaderTxt(file_path)
    loader_bib = CitationLoaderBibTex(file_path)
    loader_dblp = CitationLoaderDBLP(file_path)
    regex_location = "static/json/pdfloaderregex.json"
    loader_pdf = CitationLoaderPDF(file_path, regex_location)
    loader_doc = CitationLoaderDocx(file_path, regex_location)
    if loader_bib.is_bibtex():
        results_array = loader_bib.return_citation_array()
        return results_array
    elif loader_dblp.is_dblp():
        results_array = loader_dblp.return_citation_array()
        return results_array
    elif loader_pdf.is_pdf():
        results_array = loader_pdf.return_citation_array()
        return results_array
    elif loader_doc.is_docx():
        results_array = loader_doc.return_citation_array()
        return results_array
    elif loader_text.is_text():
        results_array = loader_text.return_citation_array()
        return results_array
    else:
        pass


def start_citation_analysis(citation_array):
    """Analyses the citations and categorises them based on the
      config set up in KeywordsArray.json

    Args:
        citation_array (list): A list containing the citations that have
        been extracted from the document

    Returns:
        dict_of_results dictionary: A dictionary containing the classified
        citations
    """
    keywords_file_location = "static/json/KeywordsArray.json"
    keywords_loader = KeywordLoader(keywords_file_location)
    analyzer = CitationAnalyzer(
        citation_array, keywords_loader.return_dict_of_keywords())
    dict_of_results = analyzer.\
        return_dict_of_assigned_citations_classifications()
    return dict_of_results


def write_citations_to_file_json(citation_dict, upload_path):
    """Writes the results of the citations to output_json.txt, which will
       be served for the user to download. This is a pure json file,
       which can then be processed by the user.
       More useful for the technical user.

    Args:
        citation_dict (dictionary ): contains extracted citation data.txt]
        upload_path (string): the path to where this session's files
        are stored
    """
    results_file = upload_path + "/output.txt"
    CitationJsonManager.write_to_file(results_file,
                                      citation_dict)


def generate_results_chart(upload_path):
    """Generates a bar graph for the citations that have been extracted

    Args:
        upload_path (string): the path to where this session's files
        are stored]
    """
    citation_presenter.plot_bar_graph(
        upload_path + "/",  config.GRAPH_FILE, config.JSON_FILE_NAME)


def create_zip(upload_path, results_zip_file_name):
    """Creates a zip of output.txt and the analysis graph
    https://thispointer.com/python-how-to-create-a-zip-archive-from-multiple-files-or-directory/

    Args:
        upload_path (string): the path to where this session's files
        are stored
        results_zip_file_name (string): the name of the zip file.
    """
    # create a ZipFile object
    results_zip = ZipFile(upload_path + "/" + results_zip_file_name, 'w')
    # Add files to the zip
    results_zip.write(upload_path + '/' + config.JSON_FILE_NAME)
    # results_zip.write(upload_path + '/' + config.GRAPH_FILE)
    results_zip.close()
