#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: riccardo
"""

import xml.sax as sax
from Indexing import indexWriter_creator

class WikiHandler(sax.ContentHandler):

    def __init__(self):
        """
        current_element contiene un rapresentazione globale della posizione
        dell'elemento che che stiamo attualmente analizzando
        e che si troverà nell'ultima poszione
        """
        sax.ContentHandler.__init__(self)
        self.__current_element = []        # Posizione elemento attuale
        self.__title = ""               # Titolo della pagina Wikipedia
        self.__id = ""                  # Identificatore numerico della pagina Wikipedia
        self.__redirect = ""            # Titolo della pagina di destinazione del redirect
        self.__text = ""                # Contenuto della pagina Wikipedia

        # Set di tag di cui si intende elaborare il testo contenuto
        self.__target_tags = {"title","ns","id","text"}

        # Flag che indica se la pagina corrente è un articolo (ns = 0)
        self.__is_article = False

        # Flag che indica se saltare l'elaborazione dell'elemento corrente
        # True se non è un elemento target
        self.__skip = False
    def startDocument(self):
        """
        Con l'inizio del documento xml viene creato l'indice che conterrà
        le pagine Wikipedia che ne verranno estratte
        """
        self.__idx_writer = indexWriter_creator()
        print("INDEX OPENED")

    def endDocument(self):
        """
        Con il termine del documento vengono "committati" (applicati)
        i cambiamenti fatti all'indice
        """
        self.__idx_writer.commit()
        print("INDEX COMMITTED")

    def startElement(self, tag, attributes):

        if tag in self.__target_tags:
            self.__skip = False
        else:
            self.__skip = True

        # Non ci interessa il contenuto del tag "redirect" (vuoto),
        # ma ci interessa il suo attributo (titolo pagina destinazione redirect)
        if tag == "redirect":
            self.__redirect = attributes["title"]

        # Appendiamo il tag che è stato aperto alla lista in modo da avere
        # contesto rispetto alla posizione attuale nel file xml
        self.__current_element.append(tag)

    def characters(self, content):

        if self.__skip == False:
            if self.__current_element[-1] == "title":
                self.__title = content

            elif self.__current_element[-1] == "ns":
                # la pagine è un articolo solo se ns == 0
                self.__is_article = (content == 0)

            # Verifico che il tag "id" sia quello della pagina e non di un utente
            elif self.__current_element[-1] == "id" and self.__current_element[-2] == "page":
                self.__id = content

            elif self.__current_element[-1] == "text":
                # ci possono essere più tag "text" per una pagina
                self.__text += content

    def endElement(self, tag):
        # Se il tag dell'elemento che si chiude è "page" e la pagina è un articolo
        # inserisco i dati raccolti nell'indice (diventano un nuovo documento)
        if tag == "page" and self.__is_article == True:
            self.idx_writer.add_document(title=self.__title, identifier=self.__id, content=self.__text)
            # Resetto la variabile "text"
            self.__text = ""

        # Ogni volta che "esco" da un elemento ne elimino il tag dalla posizione attuale
        self.__current_element.pop()
