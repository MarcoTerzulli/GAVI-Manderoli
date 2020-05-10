#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: riccardo
"""

from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh.searching import Results

from configuration import index_dir


class SearcherModule:

    def __init__(self):

        # Apro l'indice precedentemente creato all'interno della cartella indicata
        self.index = open_dir(index_dir)
        # Ottengo un oggetto searcher dall'indice appena aperto
        self.searcher = self.index.searcher()
        # Ottento un oggetto in grado che parsi le quary fornitegli e le indirizzi al campo "content" del nostro schema
        self.parser = QueryParser("content", schema=self.index.schema)

    def commit_query(self, query_txt):

        # Parso la stringa contenente il testo rappresentante la query
        query = self.parser.parse(str(query_txt))
        # Eseguo la query attraverso il searcher creato in precedenza
        results: Results = self.searcher.search(query)

        # DEBUG
        if len(results) == 0:
            print("NESSUN RISULTATO")
        else:
            for x in results[10:]:
                print(f"--Pos: {x.rank} Title: {x['title']} Id: {x['identifier']} Content: {x['content'][256:]}")
        # FINE DEBUG

        # Restituisco la lista dei risultati
        return results
