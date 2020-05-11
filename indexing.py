#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: riccardo
"""

from os import mkdir
from os import path

from sys import exit

from whoosh.fields import TEXT, ID, Schema
from whoosh.index import create_in

import xml.sax as sax

from configuration import index_dir


class WikiIndexerModule:

    def __init__(self):
        # Creo il parser SAX
        self.__parser = sax.make_parser()
        # Ne disattivo i namespace
        self.__parser.setFeature(sax.handler.feature_namespaces, 0)
        # Creo un istanza dell'handler custom che abbiamo definito per parsare il dump di Wikipedia
        my_handler = WikiHandler()
        # Imposto l'handler creato come ContentHandler del nostro parser
        self.__parser.setContentHandler(my_handler)

    def write_index(self, xml_file):
        # Avvio il parsing del file selezionato
        self.__parser.parse(xml_file)


def index_writer_init():
    # Creazione dello schema dei documenti da indicizzare
    schema: Schema = Schema(title=TEXT(stored=True), identifier=ID(stored=True, unique=True), content=TEXT(stored=True))

    # Verifica dell'esistenza della cartella dell'indice
    if not path.exists(index_dir):
        # In caso la cartella non esista viene creata
        mkdir(index_dir)

    # Creazione dell'indice all'interno della cartella designata
    index = create_in(index_dir, schema)

    # La funzione restituisce un oggetto in grado di inserire (scrivere) documenti all'interno dell'indice
    return index.writer()


class WikiHandler(sax.handler.ContentHandler):

    def __init__(self):
        """
        current_element contiene un rapresentazione globale della posizione
        dell'elemento che che stiamo attualmente analizzando
        e che si troverà nell'ultima poszione
        """
        sax.handler.ContentHandler.__init__(self)
        self.__current_element = []     # Posizione elemento attuale
        self.__title = None             # Titolo della pagina Wikipedia
        self.__id = None                # Identificatore numerico della pagina Wikipedia
        self.__redirect = None          # Titolo della pagina di destinazione del redirect
        self.__text = ""                # Contenuto della pagina Wikipedia

        # Writer per l'indice del documento xml che si vuole parsare
        self.__idx_writer = None

        # Set di tag di cui si intende elaborare il testo contenuto
        self.__target_tags = {"title", "ns", "id", "text"}

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
        self.__idx_writer = index_writer_init()
        print("INDEX OPENED")

    def endDocument(self):
        """
        Con il termine del documento vengono "committati" (applicati)
        i cambiamenti fatti all'indice
        """
        self.__idx_writer.commit()
        print("INDEX COMMITTED")

    def startElement(self, tag, attributes):

        self.__skip = False if tag in self.__target_tags else True

        # Non ci interessa il contenuto del tag "redirect" (vuoto),
        # ma ci interessa il suo attributo (titolo pagina destinazione redirect)
        if tag == "redirect":
            self.__redirect = attributes["title"]

        # Appendiamo il tag che è stato aperto alla lista in modo da avere
        # contesto rispetto alla posizione attuale nel file xml
        self.__current_element.append(tag)

    def characters(self, content):

        if self.__skip is False:
            if self.__current_element[-1] == "title":
                self.__title = content

            elif self.__current_element[-1] == "ns":
                # la pagine è un articolo solo se ns == 0
                self.__is_article = (int(content) == 0)

            # Verifico che il tag "id" sia quello della pagina e non di un utente
            elif self.__current_element[-1] == "id" and self.__current_element[-2] == "page":
                self.__id = content

            elif self.__current_element[-1] == "text":
                # ci possono essere più tag "text" per una pagina
                self.__text += content

    def endElement(self, tag):
        # Se il tag dell'elemento che si chiude è "page" e la pagina è un articolo
        # inserisco i dati raccolti nell'indice (diventano un nuovo documento)
        if tag == "page" and self.__is_article is True:
            try:
                # Verifico che i valori dell'articolo siano stati effettivamente parsati e raccolti
                assert self.__title is not None
                assert self.__id is not None
                assert self.__text != ""

                self.__idx_writer.add_document(title=self.__title, identifier=self.__id, content=self.__text)

                # SEZIONE DI DEBUG
                #print(self.__title)
                #print(self.__id)
                #print(self.__text)
                # FINE SEZIONE DI DEBUG

                # Resetto le variabili
                self.__title = None
                self.__id = None
                self.__text = ""

            except AssertionError:
                print(f"ERRORE: L'articolo che si è tentato di inserire ha dei dati mancanti\n"
                      f"{self.__title}\n"
                      f"{self.__id}\n"
                      f"{self.__text}")
                # exit() # Da decidere se sia da considerare un "FATAL ERROR" o meno

        # Ogni volta che "esco" da un elemento ne elimino il tag dalla posizione attuale
        try:
            assert tag == self.__current_element[-1]  # Controllo che i tag siano stati aperti e chiusi correttamente
            self.__current_element.pop()
        except AssertionError:
            print(f"ERRORE: il tag/elemento {self.__current_element[-1]} è stato aperto e mai richiuso {tag}")
            exit(-1)
