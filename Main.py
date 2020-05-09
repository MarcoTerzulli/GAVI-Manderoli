#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 16:23:34 2019

@author: riccardo
"""
import xml.sax
from xml_parsing_old import WikiHandler
from Searching_old import searcher_module
from bz2file import BZ2File

path = "/home/riccardo/Studio/Gestione_dell_informazione/PROGETTO/enwiki-20190101-pages-articles-multistream.xml.bz2"

xml_file = BZ2File(path)


if ( __name__ == "__main__"):

   # create an XMLReader
   parser = xml.sax.make_parser()
   # turn off namepsaces
   parser.setFeature(xml.sax.handler.feature_namespaces, 0)

   # override the default ContextHandler
   Handler = WikiHandler()
   parser.setContentHandler( Handler )
   
   #parser.parse("xml_test.xml")
   parser.parse(xml_file)
 
   searcher = searcher_module()
   
   #lancio una query definita a tempo di scrittura
   searcher.commit_query(u"the")
   
