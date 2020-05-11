#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: riccardo
"""


from indexing import WikiIndexerModule
from configuration import xml_file
from searching import WikiSearcherModule
from gui_handler import GuiHandler

"""
import xml.sax as sax
from parsing import WikiHandler
from configuration import xml_file
"""

# Verifico che main.py sia stato invocato come main del nostro programma

try:
    assert __name__ == "__main__"
except AssertionError:
    raise EnvironmentError

"""
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
"""

indexer = WikiIndexerModule()
indexer.write_index(xml_file)

gui = GuiHandler()
gui.gui_loader()


# Creo un instanza dell'oggetto searcher creato appositamente sul nostro indice
#searcher = WikiSearcherModule()
#query_text = u'afghanistan'
#results = searcher.commit_query(query_text)

