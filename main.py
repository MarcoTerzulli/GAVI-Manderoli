#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: riccardo
"""
import xml.sax as sax
from parsing import WikiHandler
from configuration import xml_file
from searching import WikiSearcherModule


#Verifico che main.py sia stato invocato come main del nostro programma

try:
    assert __name__ == "__main__"
except AssertionError:
    raise EnvironmentError


# Creo il parser SAX
parser = sax.make_parser()
# Ne disattivo i namespace
parser.setFeature(sax.handler.feature_namespaces, 0)

# Creo un istanza dell'handler custom che abbiamo definito per parsare il dump di Wikipedia
my_handler = WikiHandler()
# Imposto l'handler creato come ContentHandler del nostro parser
parser.setContentHandler(my_handler)

# Avvio il parsing del file selezionato
parser.parse(xml_file)

# Creo un instanza dell'oggetto searcher creato appositamente sul nostro indice
searcher = WikiSearcherModule()

query_txt = u'afghanistan'

results = searcher.commit_query(query_txt)

# DEBUG
if len(results) == 0:
    print("NESSUN RISULTATO")
else:
    for x in results[:10]:
        print(f"--Pos: {x.rank} Score:{x.score}\nTitle: {x['title']} Id: {x['identifier']}\nContent: {x['content'][:256]}")
# FINE DEBUG

