from os import mkdir
from os import path


def queries_order_generator(res_dir="Queries_results_order"):
    try:
        assert type(res_dir) is str
    except AssertionError:
        raise TypeError

    try:
        assert res_dir != ""
    except AssertionError:
        raise ValueError

    # se la cartella esiste, suppongo che contenga già i file
    if not path.exists(res_dir):
        mkdir(res_dir)

        print("QUERIES ORDER GENERATOR STARTED")

        with open("test_relevant_titles.txt", "r") as r_file:
            query_file = None
            counter_order = 0
            file_name = None

            for title in r_file:
                # è una query
                if ".csv" in title and "-----" not in title:
                    file_name = title.strip("\n").split(".csv", 1)[0][3:]
                    file_with_path = path.join(path.dirname(__file__), res_dir, f"{file_name}.txt")

                    # chiudo eventuali file aperti
                    if query_file is not None:
                        query_file.close()

                    try:
                        query_file = open(file_with_path, 'w')
                    except IOError:
                        print(f"\nERROR: Opening {file_name} failed")
                    counter_order = 0

                # è il risultato di una query
                if ".csv" not in title and "-----" not in title and len(title) > 1 and query_file is not None:
                    title = title.strip("\n")

                    try:
                        if query_file is not None: # non dovrebbe mai esserlo, se tutto va bene
                            query_file.write(f"{counter_order}|{title}\n")
                    except IOError:
                        print(f"\nERROR: Writing {query_file} failed")

                    counter_order += 1

        # chiudo eventuali file aperti
        if query_file is not None:
            query_file.close()
        print(f"QUERIES ORDER GENERATED\n")


queries_order_generator()
