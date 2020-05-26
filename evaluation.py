from datetime import datetime
from os import mkdir
from os import path

from statistics import stdev

from configuration import benchmark_relevant_results_file
from searching import WikiSearcherModule
import matplotlib.pyplot as plt
import numpy as np


class WikiEvaluator:

    def __init__(self):
        # File con la lista delle query di test ed i loro risultati importanti
        self.__relevant_results_file = benchmark_relevant_results_file
        # Modulo che si occupa della ricerca sull'indice wikipedia
        self.__searcher = WikiSearcherModule()

        # Dizionario che conterrà la precision su 10 livelli di recall per ogni query
        self.__precision_recall_dict = None
        # Dizionario che conterrà i valori di average precision per ogni query
        self.__average_precision_dict = None
        # Variabile che conterrà il valore di mean average precision sul set di query
        self.__mean_avg_precision = None
        # Lista delle medie tra query dei valori di precisione su ogni livello di recall (media per colonne)
        self.__mean_precision_for_level_list = None
        # Lista dei valori di deviazione standard sui valori medi di precisione su livello di recall
        self.__stdev_list = None
        # r_recall con r = 10
        self.__r_recall = None

    def precision_at_recall_levels(self, n_results=100):
        """
        Funzione che si occupa di  valutare la precision su 10 livelli di recall per ogni query tra quelle di default
        :return:
        """
        # Inizializzo il dizionario che conterrà i risultati
        self.__precision_recall_dict = dict()

        # Apro il file contenente le query ed i loro risultati rilevanti
        with open(self.__relevant_results_file) as relevant_res_file:
            # Inizialmente la query "attuale" e la "lista" dei risultati rilevanti sono nulli
            query = None
            relevant_results = None

            for line in relevant_res_file:
                # Pulisco la linea del file dai "whitespaces"
                clean_line = line.rstrip()
                if clean_line != "":

                    # Se la linea contiene la stringa di una query...
                    if clean_line[0] == "-":
                        # Allora valuto i valori di precision per la query precedente, prima di procedere
                        self.__eval_query(query, relevant_results, n_results)
                        # Inizializzo il dizionario dei risultati rilevanti alla nuova query
                        relevant_results = dict()
                        # Ricavo il titolo della nuova query
                        query = clean_line[3:-4]
                    # Se la riga ottenuta dal file non è una query la inserisco tra i risultati rilevanti alla query
                    elif relevant_results is not None:
                        relevant_results["".join([c if c != "_" else " " for c in clean_line])] = True

        self.__eval_query(query, relevant_results, n_results)
        return self.__precision_recall_dict

    def average_precision(self, n_results=100, n_relevant=10):
        try:
            assert n_relevant != 0
        except AssertionError:
            print("Error: the number of relevant files must be a positive number")
            raise ValueError
        try:
            assert n_relevant > 0
        except AssertionError:
            print("Error: the number of relevant files can't be zero")
            raise ZeroDivisionError

        self.__average_precision_dict = dict()

        if self.__precision_recall_dict is None:
            self.precision_at_recall_levels(n_results)
        for query, val in self.__precision_recall_dict.items():
            self.__average_precision_dict[query] = round(sum(val) / n_relevant, 3)

        return self.__average_precision_dict

    def mean_average_precision(self, n_results=100, n_relevant=10):
        if self.__average_precision_dict is None:
            self.average_precision(n_results, n_relevant)
        self.__mean_avg_precision = \
            round(sum([avg_p for avg_p in self.__average_precision_dict.values()]) / len(self.__average_precision_dict),
                  3)
        return self.__mean_avg_precision

    def mean_precision_for_rec_level(self, n_results=100):
        # Se i valori di precision per livello di recall di ogni query non sono già stati valutati chiamo la relativa
        # funzione
        if self.__precision_recall_dict is None:
            self.precision_at_recall_levels(n_results)

        # Divisore, è il numero di query complessivo
        divider = 0
        # Lista delle sommatorie per ogni valore di recall (sum(Pi) con "i" che varia da 1 a num_query)
        summations_list = []
        # Per ogni query prendo la lista dei valori di precision su n livelli di recall relativa ad essa
        for values_list in self.__precision_recall_dict.values():
            divider += 1
            position = 0
            # Per ogni livello di recall relativo alla query ne prendo la precision
            for value in values_list:
                # Sommo la precision di questa query ai valori di precision appartenenti allo stesso livello
                # ottenuti dalle altre query
                try:
                    summations_list[position] += value
                except IndexError:
                    summations_list.append(value)
                finally:
                    position += 1

        self.__mean_precision_for_level_list = []
        # Per ogni livello di recall divido la sua sommatoria di precision per il numero di query considerate
        for summation in summations_list:
            self.__mean_precision_for_level_list.append((summation / divider).__round__(3))

        return self.__mean_precision_for_level_list  # , self.__stdev_list

    def precision_stdev_for_level(self, n_results=100):
        if self.__precision_recall_dict is None:
            self.precision_at_recall_levels(n_results)

        self.__stdev_list = []

        # Calcolo la devizione standard sulle colonne della tabella di precision su n livelli di recall
        # (le colonne sono i livelli di recall)
        columns = []
        for values_list in self.__precision_recall_dict.values():
            position = 0
            for value in values_list:
                try:
                    columns[position].append(value)
                except IndexError:
                    columns.append([value])
                finally:
                    position += 1

        for column in columns:
            self.__stdev_list.append(stdev(column).__round__(3))

        return self.__stdev_list

    def r_recall(self, n_results=100):
        """
        ATTENZIONE: CODICE RIPETUTO PRESO DA precision_at_recall_levels E __eval_query, zona originale di questo
        metodo flaggata appositamente
        """

        # Apro il file contenente le query ed i loro risultati rilevanti
        with open(self.__relevant_results_file) as relevant_res_file:
            # Inizialmente la query "attuale" e la "lista" dei risultati rilevanti sono nulli
            query = None
            relevant_results = None
            self.__r_recall = dict()
            for line in relevant_res_file:
                # Pulisco la linea del file dai "whitespaces"
                clean_line = line.rstrip()
                if clean_line != "":

                    # Se la linea contiene la stringa di una query...
                    if clean_line[0] == "-":

                        ### ZONA ORIGINALE ###
                        # ESEGUO LA QUERY INDICATA E NE CALCOLO LA R-PRECISION CON R=10
                        if query is not None:
                            recalled = 0
                            results = self.__searcher.commit_query(query, n_results)
                            for res in results[:10]:
                                if relevant_results.get(res['title']) is not None:
                                    recalled += 1
                            self.__r_recall[query] = (recalled / 10)
                        ### FINE ZONA ORIGINALE ###

                        # Inizializzo il dizionario dei risultati rilevanti alla nuova query
                        relevant_results = dict()
                        # Ricavo il titolo della nuova query
                        query = clean_line[3:-4]
                    # Se la riga ottenuta dal file non è una query la inserisco tra i risultati rilevanti alla query
                    elif relevant_results is not None:
                        relevant_results["".join([c if c != "_" else " " for c in clean_line])] = True
            return self.__r_recall

    def __eval_query(self, query, relevant_results=None, n_results=100):
        # Eseguo l'operazione soltanto se la query non è nulla
        if query is not None:
            # Eseguo la query indicata
            results = self.__searcher.commit_query(query, n_results)
            # Inizializzo la lista della precision a "n" livelli di recall per la query indicata
            self.__precision_recall_dict[query] = []

            for res in results:
                # Controllo la rilevanza di ogni risultato
                if relevant_results is not None and relevant_results.get(res['title']) is not None:
                    relevant_results.pop(res['title'])
                    # Se un risultato è rilevante aggiungo un valore di precision alla lista
                    # precision = Numero_risultati_rilevanti_recuperati/Posizione_risultato_rilevante_attuale
                    self.__precision_recall_dict[query]. \
                        append(round((len(self.__precision_recall_dict[query]) + 1) / (res.rank + 1), 3))

                    if len(relevant_results) < 1:
                        break

            # print(relevant_results)


def get_dict_nth_key(dictionary, n=0):
    if n < 0:
        n += len(dictionary)
    for i, key in enumerate(dictionary.keys()):
        if i == n:
            return key
    raise IndexError("dictionary index out of range")


def get_dict_nth_value(dictionary, n=0):
    if n < 0:
        n += len(dictionary)
    for i, value in enumerate(dictionary.values()):
        if i == n:
            return value
    raise IndexError("dictionary index out of range")


class WikiEvaluatorPrinter:

    def __init__(self):
        self.__evaluator = WikiEvaluator()
        self.__precision_queries = self.__evaluator.precision_at_recall_levels(1147)
        self.__avg_precision = self.__evaluator.average_precision(1147)
        self.__mean_avg_p = self.__evaluator.mean_average_precision()
        self.__mean_precision_for_level_list = self.__evaluator.mean_precision_for_rec_level(1147)
        self.__stdev_list = self.__evaluator.precision_stdev_for_level(1147)
        self.__average_precision_dict = stdev(self.__evaluator.average_precision(1147).values())

    # calcolo dei valori di precision: stampa a video e scrittura su file csv; i file cvs vengono memorizzati in una
    # cartella data e sono nominati col timestamp di generazione
    def print_and_write_results(self, res_dir="Test_evaluation_csv_output", description=""):

        try:
            assert type(res_dir) is str
        except AssertionError:
            raise TypeError

        try:
            assert res_dir != ""
        except AssertionError:
            raise ValueError

        if not path.exists(res_dir):
            mkdir(res_dir)

        dt_string = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
        if description is not None and description != "":
            description = f" - {description}"

        file_name = f"{dt_string} Evaluation{description}.csv"
        file_with_path = path.join(path.dirname(__file__), res_dir, f"{file_name}")

        with open(file_with_path, "w") as out_file:
            out_file.write("\"Query\";\"0.1\";\"0.2\";\"0.3\";\"0.4\";\"0.5\";\"0.6\";\"0.7\";\"0.8\";\"0.9\";\"1"
                           "\";\"Relevant results retrieved\";\"AVG Precision\"\n")

            for key, value in self.__precision_queries.items():
                out_file.write(f"\"{key}\";")

                # scrivo le percentuali di precision
                for v_value in value:
                    out_file.write(f"\"{v_value}\";")

                # se ci sono meno di 10 risultati rilevanti, metto i restanti livelli a 0
                i = 0
                while len(value) + i < 10:
                    out_file.write("\"0\";")
                    i += 1

                out_file.write(f"\"{len(value)}\";\"{self.__avg_precision[key]}\"\n")

                # print(f"{key}: {value}\nRelevant results retrieved: {len(value)}")
                # print(f"Avg precision for {key}: {self.__avg_precision[key]}")
                # print("\n")

        print(f"MEAN AVERAGE PRECISION: {self.__mean_avg_p}\n")

        print(f"Precision media per livello: {self.__mean_precision_for_level_list}\n"
              f"Deviazione standard  per livello: {self.__stdev_list}\n"
              f"Deviazione standard average precision: {self.__average_precision_dict}")

        print(self.__evaluator.r_recall(1147))

    # stampa il grafico di una query identificata dal query number (0-29)
    def plot_graph_of_query_precision_levels(self, query_number=0):
        assert 0 <= query_number < 30

        query_name = get_dict_nth_key(self.__precision_queries, query_number)
        # estraggo i punti per gli assi
        x_points = np.linspace(0.1, 1, 10)
        y_precision_standard = get_dict_nth_value(self.__precision_queries, query_number)
        if len(y_precision_standard) < 10:
            for _ in range(10 - len(y_precision_standard)):
                y_precision_standard.append(0)
        y_precision_media_livello = self.__mean_precision_for_level_list
        y_upper_deviazione_standard_livello = []
        y_lower_deviazione_standard_livello = []
        if len(self.__stdev_list) != len(self.__mean_precision_for_level_list):
            print("ERRORE: La dimensione del vettore della deviazione standard non coincide con"
                  " il vettore dei valori medi")

        for i in range(min(len(self.__stdev_list), len(self.__mean_precision_for_level_list))):
            mean = self.__mean_precision_for_level_list[i]
            st_dev = self.__stdev_list[i]
            y_upper_deviazione_standard_livello.append(mean + st_dev)
            y_lower_deviazione_standard_livello.append(mean - st_dev)



        # in caso nella precision standard vi siano meno di 10 elementi, metto gli altri a zero
        i = 0
        while len(y_precision_standard) + i < 10:
            y_precision_standard.append(0)
            i += 1

        plt.plot(x_points, y_precision_standard, '-', label="Precision")  # precision "standard"
        plt.plot(x_points, y_precision_media_livello, '-', label="Precision Media")  # precision media per livello
        plt.plot(x_points, y_upper_deviazione_standard_livello, 'r:', label="Deviazione Standard")  # deviazione standard livello
        plt.plot(x_points, y_lower_deviazione_standard_livello, 'r:')

        plt.legend()
        plt.xlabel("Recall")
        plt.ylabel("Precision")
        plt.title(query_name)

        plt.show()


wiki_printer = WikiEvaluatorPrinter()
wiki_printer.print_and_write_results(description="")
wiki_printer.plot_graph_of_query_precision_levels(10)
