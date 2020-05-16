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
from bz2 import BZ2File
from xml_downloader import xml_download

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
    if xml_file.find(".bz2") != -1:
        with BZ2File(xml_file) as bz2_xml_file:
            indexer.write_index(bz2_xml_file)
    else:
        indexer.write_index(xml_file)
    searcher = WikiSearcherModule()

# Caricamento della gui
gui = GuiHandler(searcher)
gui.gui_loader()
