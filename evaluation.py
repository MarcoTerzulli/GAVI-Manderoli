from configuration import benchmark_relevant_results_file
from searching import WikiSearcherModule


class WikiEvaluator:

    def __init__(self):
        # File con la lista delle query di test ed i loro risultati importanti
        self.__relevant_results_file = benchmark_relevant_results_file
        # Modulo che si occupa della ricerca sull'indice wikipedia
        self.__searcher = WikiSearcherModule()

        # Dizionario che conterrà la precision su 10 livelli di recall per ogni query
        self.__recall_levels_dict = None

    def precision_recall_levels(self, n_results=100):
        """
        Funzione che si occupa di  valutare la precision su 10 livelli di recall per ogni query tra quelle di default
        :return:
        """
        # Inizializzo il dizionario che conterrà i risultati
        self.__recall_levels_dict = dict()

        # Apro il file contenente le query ed i loro risultati rilevanti
        with open(self.__relevant_results_file) as relevant_res_file:
            # Inizialmente la query "attuale" e la "lista" dei risultati rilevanti sono nulli
            query = None
            rel_res = None

            for line in relevant_res_file:
                # Pulisco la linea del file dai "whitespaces"
                clean_line = line.rstrip()
                if clean_line != "":

                    # Se la linea contiene la stringa di una query...
                    if clean_line[0] == "-":
                        # E non è la prima query che leggo dal file...
                        if query is not None:
                            # Allora valuto i valori di precision per la query precedente, prima di procedere
                            self.__eval_query(query, rel_res, n_results)
                        # Inizializzo il dizionario dei risultati rilevanti alla nuova query
                        rel_res = dict()
                        # Ricavo il titolo della nuova query
                        query = clean_line[3:-4]
                    # Se la riga ottenuta dal file non è una query la inserisco tra i risultati rilevanti alla query
                    elif rel_res is not None:
                        rel_res["".join([c if c != "_" else " " for c in clean_line])] = True

        return self.__recall_levels_dict

    def __eval_query(self, query, rel_res=None, n_results=100):
        # Eseguo la query indicata
        results = self.__searcher.commit_query(query, n_results)
        # Inizializzo la lista della precision a "n" livelli di recall per la query indicata
        self.__recall_levels_dict[query] = []

        for res in results:
            # Controllo la rilevanza di ogni risultato
            if rel_res is not None and rel_res.get(res['title']) is not None:
                # Se un risultato è rilevante aggiungo un valore di precision allalista
                # precision = Numero_risultati_rilevanti_recuperati/Posizione_risultato_rilevante_attuale
                self.__recall_levels_dict[query].append((len(self.__recall_levels_dict[query]) + 1) / (res.rank + 1))


# esecuzione e stampa dei valori di precision sui livelli di recall definiti per ogni query (num risultati rilevanti)
results = WikiEvaluator().precision_recall_levels()
for key, value in results.items():
    print(f"{key}: {value}\n {len(value)}")





