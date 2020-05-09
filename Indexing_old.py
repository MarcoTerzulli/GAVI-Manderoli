#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 16:23:34 2019

@author: riccardo
"""

from whoosh.index import create_in
from whoosh.fields import TEXT, ID, Schema
import os, os.path

def indexWriter_creator():


    schema = Schema(title=TEXT(stored=True), identifier=ID(stored=True), content=TEXT(stored=True))

    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
        
    index = create_in("indexdir", schema)

    return index.writer()


