from configuration import file_set_xml
from os import path

with open("relevant_articles.xml", "w", encoding='utf-8') as dest_file:
    dest_file.write("<DOCUMENT>\n")
    for file_xml in file_set_xml:
        print(f"File: {file_xml}")

        file_path = path.join(path.dirname(__file__), "Xml_relevant_results", file_xml)
        with open(file_path, encoding='utf-8') as in_f:
        #with open(file_xml) as in_f:
            for line in in_f:
                dest_file.write("  "+line)

    dest_file.write("</DOCUMENT>\n")
