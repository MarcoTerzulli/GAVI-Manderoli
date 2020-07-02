#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: riccardo
"""

from whoosh.index import EmptyIndexError, open_dir
from whoosh.qparser import OrGroup, QueryParser
from whoosh.searching import Results, Hit
import re

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
        return self.__results_setup(results)

    def get_similar_articles(self, base_result):

        try:
            assert isinstance(base_result, Hit)
        except AssertionError:
            raise TypeError

        return self.__results_setup(base_result.more_like_this('content'))

    def get_result_highlights(self, result):
        cleaned_content = result['content']
        highlights = self.__cleanhtml(result.highlights('content', text=cleaned_content, top=5))
        highlights = highlights
        print(highlights)
        return highlights

    @staticmethod
    def get_article_url(title):
        relative_url = "".join([c if c != " " else "_" for c in title])
        return "https://en.wikipedia.org/wiki/" + relative_url

    @staticmethod
    def __cleanhtml(raw_html):
        cleanr = re.compile(r'<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});|\[\[|\]\]|\{\{|\}\}')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext

    @staticmethod
    def __results_setup(results):
        results.fragmenter.charlimit = 500
        results.fragmenter.surround = 50

        return results
