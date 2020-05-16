from configuration import file_set_xml

with open("relevant_articles.xml", "w") as dest_file:
    dest_file.write("<DOCUMENT>\n")
    for file_xml in file_set_xml:
        with open(file_xml) as in_f:
            for line in in_f:
                dest_file.write("  "+line)

    dest_file.write("</DOCUMENT>\n")
