from datetime import datetime
from os import mkdir
from os import path

from configuration import benchmark_relevant_results_file
from searching import WikiSearcherModule


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
            self.__average_precision_dict[query] = round(sum(val)/n_relevant, 3)

        return self.__average_precision_dict

    def mean_average_precision(self, n_results=100, n_relevant=10):
        if self.__average_precision_dict is None:
            self.average_precision(n_results, n_relevant)
        self.__mean_avg_precision = \
            round(sum([avg_p for avg_p in self.__average_precision_dict.values()])/len(self.__average_precision_dict), 3)
        return self.__mean_avg_precision

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
                    self.__precision_recall_dict[query].\
                        append(round((len(self.__precision_recall_dict[query]) + 1) / (res.rank + 1), 3))

                    if len(relevant_results) < 1:
                        break

            # print(relevant_results)


# calcolo dei valori di precision: stampa a video e scrittura su file csv; i file cvs vengono memorizzati in una cartella
# data e sono nominati col timestamp di generazione
def print_and_write_results(res_dir="Test_evaluation_csv_output", description=""):
    evaluator = WikiEvaluator()
    precision = evaluator.precision_at_recall_levels(1147)
    avg_precision = evaluator.average_precision(1147)
    mean_avg_p = evaluator.mean_average_precision()

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
                       "\";\"Relevant results retrieved\";\"AVG Precision\";\"Mean Average Precision\"\n")

        for key, value in precision.items():
            print(f"{key}: {value}\nRelevant results retrieved: {len(value)}")
            print(f"Avg precision for {key}: {avg_precision[key]}")
            print("\n")

            out_file.write(f"\"{key}\";")

            # scrivo le percentuali di precision
            for v_value in value:
                out_file.write(f"\"{v_value}\";")

            # se ci sono meno di 10 risultati rilevanti, metto i restanti livelli a 0
            i = 0
            while len(value) + i < 10:
                out_file.write("\"0\";")
                i += 1

            out_file.write(f"\"{len(value)}\";\"{avg_precision[key]}\";\"{mean_avg_p}\"\n")

        print(f"MEAN AVERAGE PRECISION: {mean_avg_p}")


print_and_write_results(description="")
