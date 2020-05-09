#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 17:33:45 2019

@author: riccardo
"""

from whoosh.index import open_dir
from whoosh.qparser import QueryParser

class searcher_module():

    def __init__(self):
        
        self.index = open_dir("indexdir")
        
        self.searcher = self.index.searcher()
        #print(list(self.searcher.lexicon("content")))
        self.parser = QueryParser("content", schema=self.index.schema)
    
    
    def commit_query(self, query_txt):
        if type(query_txt) == str:
            query = self.parser.parse(query_txt)
            results = self.searcher.search(query)
            if len(results) == 0:
                print("Empty result!!")
            else:
                for x in results[10:]:
                    print(r"--Pos: {} Title: {} Id: {} Content: {}".format(x.rank,x["title"],x["identifier"], x["content"]))
        else:
            print("ERROR: UNVALID QUERY VALUE")