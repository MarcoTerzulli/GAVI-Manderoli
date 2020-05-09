#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: riccardo
"""
from bz2file import BZ2File


dest_file = r"xml_explor.xml"

path = "/home/riccardo/Studio/Gestione_dell_informazione/enwiki-20190101-pages-articles-multistream.xml.bz2"

xml_file = BZ2File(path)

with open(dest_file, "w+") as dest:
    with xml_file as source:
        i = 0
        for line in source:
            dest.write(line.__str__()+"\n")
            i += 1
            if i == 2000:
                break
