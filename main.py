#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: riccardo
"""
from whoosh.index import EmptyIndexError

from indexing import WikiIndexerModule
from configuration import xml_file
from searching import WikiSearcherModule
from gui_handler import GuiHandler


# Verifico che main.py sia stato invocato come main del nostro programma
try:
    assert __name__ == "__main__"
except AssertionError:
    raise EnvironmentError

# Provo a generare un WikiSearcherModule sull'indice, se l'indice non esiste lo creo e ripeto l'operazione
try:
    searcher = WikiSearcherModule()
except EmptyIndexError:
    print("Warning: creating new index")
    indexer = WikiIndexerModule()
    indexer.write_index(xml_file)
    searcher = WikiSearcherModule()

gui = GuiHandler(searcher)
gui.gui_loader()
