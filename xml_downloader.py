from os import mkdir
from os import path
from time import time, sleep

from pip._vendor import requests


def xml_download(xml_dir="Xml_relevant_results"):
    try:
        assert type(xml_dir) is str
    except AssertionError:
        raise TypeError

    try:
        assert xml_dir != ""
    except AssertionError:
        raise ValueError

    #se la cartella esiste, suppongo che contenga già i file
    if not path.exists(xml_dir):
        mkdir(xml_dir)

        print("DOWNLOAD STARTED")
        time_start = time()

        with open("test_relevant_titles.txt", "r") as r_file:
            for title in r_file:
                if ".csv" not in title and len(title) > 1:
                    title = title.strip("\n")
                    url = "https://en.wikipedia.org/wiki/Special:Export/" + title
                    file_with_path = path.join(path.dirname(__file__), xml_dir, f"{title}.xml")

                    try:
                        open(file_with_path, 'wb').write(requests.get(url).content)
                    except IOError:
                        print(f"ERRORE: Download di {title}.xml fallito")

                    #print(file_with_path)
                    print(f"Download di {title}.xml")

        time_diff_s = int(time() - time_start)
        time_total_m = int(time_diff_s / 60)
        time_total_s = time_diff_s - time_total_m * 60
        print(f"DOWNLOAD COMPLETED IN {time_total_m}M AND {time_total_s}S\n")