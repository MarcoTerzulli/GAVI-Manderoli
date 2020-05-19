#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: riccardo
"""

from whoosh.index import EmptyIndexError, open_dir
from whoosh.qparser import QueryParser
from whoosh.searching import Results

from configuration import index_dir


class WikiSearcherModule:

    def __init__(self):

        # Apro l'indice precedentemente creato all'interno della cartella indicata
        try:
            self.__index = open_dir(index_dir)
        except (NameError, EmptyIndexError):
            print("Warning: trying to open index's directory using the default directory name")
            self.__index = open_dir("Wiki_index")

        # Ottengo un oggetto searcher dall'indice appena aperto
        self.__searcher = self.__index.searcher()
        # Ottento un oggetto in grado che parsi le quary fornitegli e le indirizzi al campo "content" del nostro schema
        self.__parser = QueryParser("content", schema=self.__index.schema)

    def commit_query(self, query_text):

        # Parso la stringa contenente il testo rappresentante la query
        query = self.__parser.parse(str(query_text))
        # Eseguo la query attraverso il searcher creato in precedenza
        results: Results = self.__searcher.search(query)

        # Restituisco la lista dei risultati
        return results

    @staticmethod
    def get_article_url(title):
        relative_url = "".join([c if c != " " else "_" for c in title])
        return "https://en.wikipedia.org/wiki/" + relative_url
