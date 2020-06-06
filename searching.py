#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: riccardo
"""

from whoosh.index import EmptyIndexError, open_dir
from whoosh.qparser import OrGroup, QueryParser
from whoosh.searching import Results
from nltk.wsd import lesk
from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords

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
        self.__parser = QueryParser("content", schema=self.__index.schema, group=OrGroup)
        #self.__parser = QueryParser("content", schema=self.__index.schema)

    def commit_query(self, query_text, n_results=10):

        # Parso la stringa contenente il testo rappresentante la query
        query = self.__parser.parse(str(query_text))
        # Eseguo la query attraverso il searcher creato in precedenza
        results: Results = self.__searcher.search(query, limit=n_results)

        # Restituisco la lista dei risultati
        return results

    def commit_query_with_disambiguation(self, query_text, n_results=10):
        tokens = word_tokenize(query_text)
        tagged_tokens = pos_tag(tokens)
        query_synonym = []
        for tt in tagged_tokens:
            if tt[1] in {'NN', 'NNS', 'NNP', 'NNPS'}:
                noun_synonym = lesk(tokens, tt[0], 'n')

                if noun_synonym is not None:
                    query_synonym.append("".join([c if c != "_" else " " for c in noun_synonym.name().split(sep='.')[0]]))
        expanded_query = query_text+"".join([" "+noun_synonym+" " for noun_synonym in query_synonym])
        print(expanded_query)
        return self.commit_query(expanded_query, n_results)

    @staticmethod
    def get_article_url(title):
        relative_url = "".join([c if c != " " else "_" for c in title])
        return "https://en.wikipedia.org/wiki/" + relative_url
