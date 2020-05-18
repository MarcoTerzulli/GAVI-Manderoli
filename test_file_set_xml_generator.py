def file_set_xml_generator():

    with open("test_relevant_titles.txt", "r") as r_file:
        with open("test_file_set_xml.txt", 'w') as w_file:

            for line in r_file:
                # è il risultato di una query
                if ".csv" not in line and "-----" not in line and len(line) > 1:
                    line = line.strip("\n")

                    try:
                        w_file.write(f"\'{line.replace(':', '-')}.xml\',\n")
                    except IOError:
                        print(f"\nERROR: Write failed")


file_set_xml_generator()