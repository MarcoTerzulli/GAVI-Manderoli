#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 16:23:34 2019

@author: riccardo
"""


#PARSING FILE XML
import xml.sax
from Indexing import indexWriter_creator

class WikiHandler( xml.sax.ContentHandler ):
    def __init__(self):
        """
        CurrentData contiene un rapresentazione globale della posizione 
        dell'elemento che che stiamo attualmente analizzando
        e che si troverà nell'ultima poszione
        """
        self.CurrentData = []
        self.Title = ""
        self.Id = ""
        self.Redirect = ""
        self.Text = ""
        
        self.skip = False
    
    def startDocument(self):
        self.idx_writer = indexWriter_creator()
        print("INDEX OPENED")

    def endDocument(self):
        self.idx_writer.commit()
        print("INDEX COMMITTED")
    
    def startElement(self, tag, attributes):
    
    #Distinguo i casi da trattare da quelli che non servono,
    #in particolare nel caso di elementi omonimi ma con posizione e scopo diversi
        
        if tag == "id" and self.CurrentData[-1] != "page":
            self.skip = True
        else :
            self.skip = False
            
        if self.skip == False:
            self.CurrentData.append(tag)
            
            if tag == "redirect":
                self.Redirect = attributes["title"]
    
    def endElement(self, tag):
    
        if self.skip == False:
        #INZIO SEZIONE DI DEBUG
            """
                if self.CurrentData[-1] == "title":
                    print(f"\n\n**TITLE: {self.Title}**\n") 
                    
                elif self.CurrentData[-1] == "id":
                    print(f"--ID: {self.id}\n") 
                
                elif self.CurrentData[-1] == "redirect":
                    print(f"--REDIRECT TO: {self.Redirect}")
                elif self.CurrentData[-1] == "text":
                    print(f"--TEXT: {self.Text}")
            """
        #FINE SEZIONE DI DEBUG
            if self.CurrentData[-1] == "page":
                self.idx_writer.add_document(title = self.Title, identifier = self.Id, content = self.Text)
                self.Text = ""
            
            self.CurrentData.pop()
        
    
    def characters(self, content):
    
        if self.skip == False:
            if self.CurrentData[-1] == "title":
                self.Title = content
                
            elif self.CurrentData[-1] == "id":
                self.Id = content
            
            #else if self.CurrentData[-1] == "redirect":
            
            elif self.CurrentData[-1] == "text":
                self.Text += content