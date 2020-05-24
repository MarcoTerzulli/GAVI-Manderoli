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
            self.__average_precision_dict[query] = sum(val)/n_relevant

        return self.__average_precision_dict

    def mean_average_precision(self, n_results=100, n_relevant=10):
        if self.__average_precision_dict is None:
            self.average_precision(n_results, n_relevant)
        self.__mean_avg_precision = \
            sum([avg_p for avg_p in self.__average_precision_dict.values()])/len(self.__average_precision_dict)
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
                    # Se un risultato è rilevante aggiungo un valore di precision allalista
                    # precision = Numero_risultati_rilevanti_recuperati/Posizione_risultato_rilevante_attuale
                    self.__precision_recall_dict[query].\
                        append((len(self.__precision_recall_dict[query]) + 1) / (res.rank + 1))

                    if len(relevant_results) < 1:
                        break

            print(relevant_results)


# esecuzione e stampa dei valori di precision sui livelli di recall definiti per ogni query (num risultati rilevanti)
evaluator = WikiEvaluator()
precision = evaluator.precision_at_recall_levels(1147)
avg_precision = evaluator.average_precision(1147)
mean_avg_p = evaluator.mean_average_precision()
for key, value in precision.items():
    print(f"{key}: {value}\nRelevant results retrieved: {len(value)}")
    print(f"Avg precision for {key}: {avg_precision[key]}")
    print("\n")

print(f"MEAN AVERAGE PRECISION: {mean_avg_p}")
