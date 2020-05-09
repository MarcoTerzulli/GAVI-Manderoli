#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: riccardo
"""

from whoosh.index import create_in
from whoosh.fields import TEXT, ID, Schema
import os, os.path

index_dir = "indexdir"

def indexWriter_creator():

    schema = Schema(title=TEXT(stored=True), identifier=ID(stored=True), content=TEXT(stored=True))

    if not os.path.exists(index_dir):
        os.mkdir(index_dir)

    index = create_in(index_dir,schema,)

    return index.writer()


