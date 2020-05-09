#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: riccardo
"""

from whoosh.index import create_in
from whoosh.fields import TEXT, ID, Schema
from os import mkdir
from os import path

index_dir = "indexdir"


def index_writer_creator():

    # Creazione dello schema dei documenti da indicizzare
    schema: Schema = Schema(title=TEXT(stored=True), identifier=ID(stored=True), content=TEXT(stored=True))

    # Verifica dell'esistenza della cartella dell'indice
    if not path.exists(index_dir):
        # In caso la cartella non esista viene creata
        mkdir(index_dir)

    # Creazione dell'indice all'interno della cartella designata
    index = create_in(index_dir, schema)

    # La funzione restituisce un oggetto in grado di inserire (scrivere) documenti all'interno dell'indice
    return index.writer()
