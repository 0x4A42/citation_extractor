import matplotlib.pyplot as plt
import json


"""Responsible for plotting graphs based on a dict of analyzed data
"""


def plot_bar_graph(upload_folder, file_name, output_file):
    """Generates a bar graph based on the classification of citations
    within the output file

    Args:
        upload_folder (string): The folder the file will be saved in
        file_name (string): The name of the file save the graph to
        output_file (string): The name of the json output file
    """
    plotting_dict = count_classification_from_file(
        upload_folder + "/" + output_file)
    plt.figure(figsize=(20, 3))
    plt.bar(range(len(plotting_dict)), list(plotting_dict.values()),
            align='center', width=0.3)
    plt.xticks(range(len(plotting_dict)), list(plotting_dict.keys()))
    plt.savefig(upload_folder + "/" + file_name)


def plot_pie_chart(file_name):
    """Generates a pie chart

    Args:
        file_name (string): The name of the file to plot a chart from
    """
    plotting_dict = {}
    for key in self.dict_of_analyzed_citations.keys():
        plotting_dict[key] = len(self.dict_of_analyzed_citations[key])
    plt.pie([float(v) for v in plotting_dict.values()],
            labels=plotting_dict.keys(), autopct=None)
    plt.savefig(file_name)


def count_classification_from_file(output_file):
    """Reads in the JSON output file and iterates through the objects.
    Updates a dictionary tracking the classifications with the amount
    found within the output file, in order to plot a graph from it

    Args:
        output_file (string): The name of the json output file

    Returns:
        classification_count (dictionary): A dictionary with a key of
        classifications and a value of the amount of times they showed in
        the json file
    """
    classification_count = {"Computer Architecture": 0,
                            "Cyber Security": 0, "Machine Learning": 0,
                            "Software Engineering": 0,
                            "Software Testing": 0,
                            "Blog": 0, "Newspapers": 0,
                            "Academic": 0, "Non-Academic": 0}
    with open(output_file) as json_file:
        data = json.load(json_file)
        for c in data.values():
            for x in c:
                if x['classification'] == "Computer Architecture":
                    classification_count['Computer Architecture'] += 1
                elif x['classification'] == "Cyber Security":
                    classification_count['Cyber Security'] += 1
                elif x['classification'] == "Machine Learning":
                    classification_count['Machine Learning'] += 1
                elif x['classification'] == "Software Engineering":
                    classification_count['Software Engineering'] += 1
                elif x['classification'] == "Software Testing":
                    classification_count['Software Testing'] += 1
                elif x['classification'] == "Blog":
                    classification_count['Blog'] += 1
                elif x['classification'] == "Newspapers":
                    classification_count['Newspapers'] += 1
                elif x['classification'] == "Academic":
                    classification_count['Academic'] += 1
                elif x['classification'] == "Non-Academic":
                    classification_count['Non-Academic'] += 1
        return classification_count
