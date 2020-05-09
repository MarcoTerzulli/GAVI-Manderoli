#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: riccardo
"""
import xml.sax as sax
from Parsing import WikiHandler

xml_file = "xml_snippet.xml"

#Verifico che Main.py sia stato invocato come main del nostro programma

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
