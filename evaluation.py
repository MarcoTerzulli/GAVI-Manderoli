from datetime import datetime
from os import mkdir
from os import path

from statistics import stdev, mean

from configuration import benchmark_relevant_results_file
from searching import WikiSearcherModule
import matplotlib.pyplot as plt
import numpy as np
import pickle


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
        with open(self.__relevant_results_file, encoding='utf-8') as relevant_res_file:
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
            self.__average_precision_dict[query] = sum(val) / n_relevant

        return self.__average_precision_dict

    def mean_average_precision(self, n_results=100, n_relevant=10):
        if self.__average_precision_dict is None:
            self.average_precision(n_results, n_relevant)
        self.__mean_avg_precision = \
            sum([avg_p for avg_p in self.__average_precision_dict.values()]) / len(self.__average_precision_dict)
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
            self.__mean_precision_for_level_list.append((summation / divider))

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
            self.__stdev_list.append(stdev(column))

        return self.__stdev_list

    def r_recall(self, n_results=100):
        """
        ATTENZIONE: CODICE RIPETUTO PRESO DA precision_at_recall_levels E __eval_query, zona originale di questo
        metodo flaggata appositamente
        """

        # Apro il file contenente le query ed i loro risultati rilevanti
        with open(self.__relevant_results_file, encoding='utf-8') as relevant_res_file:
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
                        self.__eval_r_recall_query(query, relevant_results, n_results)
                        ### FINE ZONA ORIGINALE ###

                        # Inizializzo il dizionario dei risultati rilevanti alla nuova query
                        relevant_results = dict()
                        # Ricavo il titolo della nuova query
                        query = clean_line[3:-4]
                    # Se la riga ottenuta dal file non è una query la inserisco tra i risultati rilevanti alla query
                    elif relevant_results is not None:
                        relevant_results["".join([c if c != "_" else " " for c in clean_line])] = True
            self.__eval_r_recall_query(query, relevant_results, n_results)
            return self.__r_recall

    def __eval_r_recall_query(self, query, relevant_results=None, n_results=100):
        if query is not None:
            recalled = 0
            results = self.__searcher.commit_query(query, n_results)
            for res in results[:10]:
                if relevant_results.get(res['title']) is not None:
                    recalled += 1
            self.__r_recall[query] = (recalled / 10)

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
                        append((len(self.__precision_recall_dict[query]) + 1) / (res.rank + 1))

                    if len(relevant_results) < 1:
                        break

            print(query)
            print(relevant_results)


def get_dict_nth_key(dictionary, n=0):
    if n < 0:
        n += len(dictionary)
    for i, key in enumerate(dictionary.keys()):
        if i == n:
            return key
    raise IndexError("Dictionary index out of range")


def get_dict_nth_value(dictionary, n=0):
    if n < 0:
        n += len(dictionary)
    for i, value in enumerate(dictionary.values()):
        if i == n:
            return value
    raise IndexError("Dictionary index out of range")


def sort_dict(dictionary, revers=False):
    return {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1], reverse=revers)}

def sort_dict_in_same_order_of_another(dictionary_original, dictionary_unordered):
    if dictionary_original.__len__() != dictionary_unordered.__len__():
        raise IndexError("Dictionaries must have the same number of items")
    else:
        new_dict = {}
        for key in dictionary_original:
            new_dict[key] = dictionary_unordered[key]
        return new_dict


class WikiEvaluatorPrinter:

    def __init__(self):
        self.__evaluator = WikiEvaluator()
        self.__precision_queries_dict = self.__evaluator.precision_at_recall_levels(1147)
        self.__avg_precision_dict = self.__evaluator.average_precision(1147)
        self.__mean_avg_precision = self.__evaluator.mean_average_precision()
        self.__mean_precision_for_level_list = self.__evaluator.mean_precision_for_rec_level(1147)
        self.__stdev_for_level_list = self.__evaluator.precision_stdev_for_level(1147)
        self.__stedv_average_precision = stdev(self.__evaluator.average_precision(1147).values())
        self.__r_recall_dict = self.__evaluator.r_recall(1147)

        # sort del dizionario con i valori di recall
        self.__r_recall_dict = sort_dict(self.__r_recall_dict, True)

        # strutture dati per eventuale import
        self.__imported_precision_queries_dict = None
        self.__imported_avg_precision_dict = None
        self.__imported_mean_avg_precision = None
        self.__imported_mean_precision_for_level_list = None
        self.__imported_stdev_for_level_list = None
        self.__imported_stedv_average_precision = None
        self.__imported_r_recall_dict = None

    # scrittura su file csv dei valori di precision per le query; i file cvs vengono memorizzati in una
    # cartella data e sono nominati col timestamp di generazione
    def csv_write_precision_at_recall_levels(self, res_dir="Test_evaluation_output", description=""):
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
            description = f"{description} - "

        file_name = f"{dt_string} {description}Precision_At_Recall_Levels.csv"
        file_with_path = path.join(path.dirname(__file__), res_dir, f"{file_name}")

        with open(file_with_path, "w") as out_file:
            out_file.write("\"Query\";\"0.1\";\"0.2\";\"0.3\";\"0.4\";\"0.5\";\"0.6\";\"0.7\";\"0.8\";\"0.9\";\"1"
                           "\";\"Relevant results retrieved\";\"AVG Precision\"\n")

            for key, value in self.__precision_queries_dict.items():
                out_file.write(f"\"{key}\";")

                # scrivo le percentuali di precision
                for v_value in value:
                    out_file.write(f"\"{v_value}\";")

                # se ci sono meno di 10 risultati rilevanti, metto i restanti livelli a 0
                i = 0
                while len(value) + i < 10:
                    out_file.write("\"0\";")
                    i += 1

                out_file.write(f"\"{len(value)}\";\"{self.__avg_precision_dict[key]}\"\n")

    # stampa console dei di precision per le query ecc
    def console_write_results(self):
        for key, value in self.__precision_queries_dict.items():
            print(f"{key}: {value}\nRelevant results retrieved: {len(value)}")
            print(f"Avg precision for {key}: {self.__avg_precision_dict[key]}\n")

        print(f"\nMean Average Precision: {self.__mean_avg_precision}\n")
        print(f"Precision media per livello: {self.__mean_precision_for_level_list}\n"
              f"Deviazione standard  per livello: {self.__stdev_for_level_list}\n"
              f"Deviazione standard average precision: {self.__stedv_average_precision}")

        print(f"\n{self.__evaluator.r_recall(1147)}")

    # scrittura su file di tutti i valori calcolati dall'evaluation. Si utilizza un dizionario per rendere più facile
    # la successiva importazione
    def export_evaluation_data(self, res_dir="Test_evaluation_output", description=""):
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

        # creazione file di output
        dt_string = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
        if description is not None and description != "":
            description = f"{description} - "

        file_name = f"{dt_string} {description}Data Export.dat"
        file_with_path = path.join(path.dirname(__file__), res_dir, f"{file_name}")

        # creazione dizionario per export
        data = {'precision_queries_dict': self.__precision_queries_dict,
                'avg_precision_dict': self.__avg_precision_dict,
                'mean_avg_precision': self.__mean_avg_precision,
                'mean_precision_for_level_list': self.__mean_precision_for_level_list,
                'stdev_for_level_list': self.__stdev_for_level_list,
                'stedv_average_precision': self.__stedv_average_precision,
                'r_recall_dict': self.__r_recall_dict}

        with open(file_with_path, "wb") as out_file:
            pickle.dump(data, out_file)

        print("\nDATA EXPORTED SUCCESSFULLY")

    # impott da file di tutti i valori calcolati dall'evaluation
    def import_evaluation_data(self, file_name, res_dir="Test_evaluation_output", description=""):
        file_with_path = path.join(path.dirname(__file__), res_dir, f"{file_name}")

        with open(file_with_path, "rb") as in_file:
            data = pickle.load(in_file)

        self.__imported_precision_queries_dict = data['precision_queries_dict']
        self.__imported_avg_precision_dict = data['avg_precision_dict']
        self.__imported_mean_avg_precision = data['mean_avg_precision']
        self.__imported_mean_precision_for_level_list = data['mean_precision_for_level_list']
        self.__imported_stdev_for_level_list = data['stdev_for_level_list']
        self.__imported_stedv_average_precision = data['stedv_average_precision']
        self.__imported_r_recall_dict = data['r_recall_dict']

        print("\nDATA IMPORTED SUCCESSFULLY")

    # stampa il grafico di una query identificata dal query number (0-29)
    def plot_graph_of_query_precision_levels(self, query_number=0, compare_with_imported_data=False):
        try:
            assert 0 <= query_number < 30
        except AssertionError:
            raise ValueError

        query_name = get_dict_nth_key(self.__precision_queries_dict, query_number)
        # estraggo i punti per gli assi
        x_points = np.linspace(0.1, 1, 10)
        y_precision_standard = get_dict_nth_value(self.__precision_queries_dict, query_number)
        # y_precision_media_livello = self.__mean_precision_for_level_list
        # y_upper_deviazione_standard_livello = []
        # y_lower_deviazione_standard_livello = []

        #for i in range(min(len(self.__stdev_for_level_list), len(self.__mean_precision_for_level_list))):
            #    mean = self.__mean_precision_for_level_list[i]
            #    st_dev = self.__stdev_for_level_list[i]
            #    y_upper_deviazione_standard_livello.append(mean + st_dev)
        #    y_lower_deviazione_standard_livello.append(mean - st_dev)

        # in caso nella precision standard vi siano meno di 10 elementi, metto gli altri a zero
        if len(y_precision_standard) < 10:
            for _ in range(10 - len(y_precision_standard)):
                y_precision_standard.append(0)

        # calcolo nuovamente la media per livello escludendo il valore della query in questione
        y_precision_media_livello = [(self.__mean_precision_for_level_list[i] * 30 - y_precision_standard[i]) / 29
                                     for i in range(10)]

        plt.plot(x_points, y_precision_standard, '-', label="Precision")  # precision "standard"
        plt.plot(x_points, y_precision_media_livello, '-', label=f"Precision Media senza {query_name}")  # precision media per livello
        # plt.plot(x_points, y_upper_deviazione_standard_livello, 'r:', label="Deviazione Standard")  # deviazione standard livello
        # plt.plot(x_points, y_lower_deviazione_standard_livello, 'r:')
        # plt.plot(x_points, self.__mean_precision_for_level_list, '-', label="Precision Media Completa")  # precision media per livello

        # eventuale caricamento e stampa dei dati importati
        if compare_with_imported_data:
            y_imported_precision_standard = get_dict_nth_value(self.__imported_precision_queries_dict, query_number)

            if len(y_imported_precision_standard) < 10:
                for _ in range(10 - len(y_imported_precision_standard)):
                    y_imported_precision_standard.append(0)

            y_imported_precision_media_livello = [(self.__imported_mean_precision_for_level_list[i] * 30 -
                                                   y_imported_precision_standard[i]) / 29 for i in range(10)]

            plt.plot(x_points, y_imported_precision_standard, ':', label="Precision Precedente")  # precision "standard"
            plt.plot(x_points, y_imported_precision_media_livello, ':',
                     label=f"Precision Media Precedente senza {query_name}")  # precision media per livello

        plt.legend()
        plt.xlabel("Recall")
        plt.ylabel("Precision")
        plt.title(query_name)

        plt.xticks(np.arange(0.1, 1.1, 0.1))
        plt.grid(color='#CCCCCC')

        plt.show()

    # stampa il grafico della avg precision confrontato alla map
    def plot_graph_of_queries_avg_precision_vs_map(self, compare_with_imported_data=False):

        x_dict = dict(self.__avg_precision_dict)
        x_dict['MEAN AVERAGE PRECISION'] = self.__mean_avg_precision
        x_dict = sort_dict(x_dict, True)

        deviazione_standard = stdev(self.__avg_precision_dict.values())
        upperstdev = self.__mean_avg_precision + deviazione_standard
        lowerstdev = self.__mean_avg_precision - deviazione_standard

        x_points = list(range(1, len(x_dict) + 1))
        y_bar_heights = []
        bar_labels = []
        y_man_points = []
        y_up_stedev_points = []
        y_low_stedev_points = []

        # popolamento delle altezze delle barre e delle rispettive labels
        for key, value in x_dict.items():
            bar_labels.append(key)
            y_bar_heights.append(value)

        # popolamento della lista dei punti in y per la man (tutti uguali)
        for _ in range(1, len(x_dict) + 1):
            y_man_points.append(self.__mean_avg_precision)

        # popolamento della lista dei punti in y per la up stedev (tutti uguali)
        for _ in range(1, len(x_dict) + 1):
            y_up_stedev_points.append(upperstdev)

        # popolamento della lista dei punti in y per la low stdev (tutti uguali)
        for _ in range(1, len(x_dict) + 1):
            y_low_stedev_points.append(lowerstdev)

        if not compare_with_imported_data:
            bar_list = plt.bar(x_points, y_bar_heights, width=0.8, color=['orange'])
            plt.plot(x_points, y_man_points, 'r:', label="Mean Average Precision", linewidth=2)  # precision "standard"
            bar_list[bar_labels.index('MEAN AVERAGE PRECISION')].set_color('r')  # coloro la barra della man

            plt.plot(x_points, y_up_stedev_points, 'g:', label="Standard Deviation", linewidth=2)  # upper stdev
            plt.plot(x_points, y_low_stedev_points, 'g:', linewidth=2)  # upper stdev
        else:
            x_imported_dict = dict(self.__imported_avg_precision_dict)
            x_imported_dict['MEAN AVERAGE PRECISION'] = self.__imported_mean_avg_precision
            x_imported_dict = sort_dict_in_same_order_of_another(x_dict, x_imported_dict)

            y_imported_bar_heights = []
            y_imported_man_points = []

            # popolamento delle altezze delle barre e delle rispettive labels
            for key, value in x_imported_dict.items():
                y_imported_bar_heights.append(value)

            # popolamento della lista dei punti in y per la man (tutti uguali)
            for _ in range(1, (len(x_imported_dict) + 1) * 2):
                y_imported_man_points.append(self.__imported_mean_avg_precision)

            # popolamento della lista dei punti in y per la man (tutti uguali)
            y_man_points = []
            for _ in range(1, (len(x_dict) + 1) * 2):
                y_man_points.append(self.__mean_avg_precision)

            x_points = list(range(1, (len(x_dict)) * 2 + 1, 2))
            x_imported_points = list(range(2, (len(x_dict) + 1) * 2, 2))

            bar_list = plt.bar(x_points, y_bar_heights, width=0.8, color=['orange'])
            plt.plot(list(range(1, (len(x_dict) + 1) * 2)), y_man_points, 'r:', label="Mean Average Precision", linewidth=2)  # precision "standard"
            bar_list[bar_labels.index('MEAN AVERAGE PRECISION')].set_color('r')  # coloro la barra della man

            imported_bar_list = plt.bar(x_imported_points, y_imported_bar_heights, width=-0.8,  align='edge', color=['#0277BD'])
            plt.plot(list(range(1, (len(x_dict) + 1) * 2)), y_imported_man_points, 'b:', label="Mean Average Precision Precedente",
                     linewidth=1)  # precision "standard"
            imported_bar_list[bar_labels.index('MEAN AVERAGE PRECISION')].set_color('b')  # coloro la barra della man


        plt.legend()
        plt.xticks(x_points, bar_labels, rotation='vertical')
        plt.ylabel("Precision")
        plt.title("Queries\' Average Precision vs Mean Average Precision")

        plt.show()

    # stampa il grafico delle r recall confrontato alla media delle r recall
    def plot_graph_of_queries_rrecall_vs_avg_recall(self, compare_with_imported_data=False):

        x_dict = dict(self.__r_recall_dict)
        avg_recall = mean(self.__r_recall_dict[k] for k in self.__r_recall_dict)
        x_dict['AVERAGE 11-RECALL'] = avg_recall
        x_dict = sort_dict(x_dict, True)

        deviazione_standard = stdev(self.__r_recall_dict.values())
        upperstdev = avg_recall + deviazione_standard
        lowerstdev = avg_recall - deviazione_standard

        x_points = list(range(1, len(x_dict) + 1))
        y_bar_heights = []
        bar_labels = []
        y_avg_points = []
        y_up_stedev_points = []
        y_low_stedev_points = []

        # popolamento delle altezze delle barre e delle rispettive labels
        for key, value in x_dict.items():
            bar_labels.append(key)
            y_bar_heights.append(value)

        # popolamento della lista dei punti in y per la man (tutti uguali)
        for _ in range(1, len(x_dict) + 1):
            y_avg_points.append(avg_recall)

        # popolamento della lista dei punti in y per la up stedev (tutti uguali)
        for _ in range(1, len(x_dict) + 1):
            y_up_stedev_points.append(upperstdev)

        # popolamento della lista dei punti in y per la low stdev (tutti uguali)
        for _ in range(1, len(x_dict) + 1):
            y_low_stedev_points.append(lowerstdev)

        if not compare_with_imported_data:
            bar_list = plt.bar(x_points, y_bar_heights, width=0.8, color=['orange'])
            plt.plot(x_points, y_avg_points, 'r:', label="Average Recall", linewidth=2)
            bar_list[bar_labels.index('AVERAGE 11-RECALL')].set_color('r')  # coloro la barra della avg
            plt.plot(x_points, y_up_stedev_points, 'g:', label="Standard Deviation", linewidth=2)  # upper stdev
            plt.plot(x_points, y_low_stedev_points, 'g:', linewidth=2)  # upper stdev
        else:
            x_imported_dict = dict(self.__imported_r_recall_dict)
            imported_avg_recall = mean(self.__imported_r_recall_dict[k] for k in self.__imported_r_recall_dict)
            x_imported_dict['AVERAGE 11-RECALL'] = imported_avg_recall
            x_imported_dict = sort_dict_in_same_order_of_another(x_dict, x_imported_dict)

            y_imported_bar_heights = []
            y_imported_avg_points = []

            x_points = list(range(1, (len(x_dict)) * 2 + 1, 2))
            x_imported_points = list(range(2, (len(x_dict) + 1) * 2, 2))

            # popolamento delle altezze delle barre e delle rispettive labels
            for key, value in x_imported_dict.items():
                y_imported_bar_heights.append(value)

            # popolamento della lista dei punti in y per la man (tutti uguali)
            for _ in range(1, (len(x_imported_dict) + 1) * 2):
                y_imported_avg_points.append(imported_avg_recall)

            # popolamento della lista dei punti in y per la man (tutti uguali)
            y_avg_points = []
            for _ in range(1, (len(x_imported_dict) + 1) * 2):
                y_avg_points.append(avg_recall)

            bar_list = plt.bar(x_points, y_bar_heights, width=0.8, color=['orange'])
            plt.plot(list(range(1, (len(x_dict) + 1) * 2)), y_avg_points, 'r:', label="Average Recall", linewidth=2)
            bar_list[bar_labels.index('AVERAGE 11-RECALL')].set_color('r')  # coloro la barra della avg

            imported_bar_list = plt.bar(x_imported_points, y_imported_bar_heights, width=-0.8, align='edge',
                                        color=['#0277BD'])
            plt.plot(list(range(1, (len(x_dict) + 1) * 2)), y_imported_avg_points, 'b:',
                     label="Average Recall Precedente",
                     linewidth=1)  # precision "standard"
            imported_bar_list[bar_labels.index('AVERAGE 11-RECALL')].set_color('b')  # coloro la barra della man


        plt.legend()
        plt.xticks(x_points, bar_labels, rotation='vertical')
        plt.ylabel("R Recall")
        plt.title("Queries\' 11 Recall vs Average 11-Recall")

        plt.show()


wiki_printer = WikiEvaluatorPrinter()
#wiki_printer.csv_write_precision_at_recall_levels(description="0_AND")
#wiki_printer.export_evaluation_data(description="AND")
# wiki_printer.console_write_results()
#wiki_printer.plot_graph_of_query_precision_levels(1)
#wiki_printer.plot_graph_of_queries_avg_precision_vs_map()
#wiki_printer.plot_graph_of_queries_rrecall_vs_avg_recall()

wiki_printer.import_evaluation_data("2020-06-02_21.29.11 0_AND - Data Export.dat")
wiki_printer.plot_graph_of_query_precision_levels(2, True)
wiki_printer.plot_graph_of_query_precision_levels(14, True)
wiki_printer.plot_graph_of_query_precision_levels(13, True)
wiki_printer.plot_graph_of_queries_avg_precision_vs_map(True)
wiki_printer.plot_graph_of_queries_rrecall_vs_avg_recall(True)
#wiki_printer.plot_graph_of_query_precision_levels(14)
