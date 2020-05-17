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

from configuration import index_dir, relevant_pages


class WikiIndexerModule:
    """
    Modulo di gestione del parsing e dell'indicizzazione
    """
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


def index_writer_init(idx_dir="Wiki_index"):
    """
    Funzione che inizializza un indice nella cartella indicata come parametro (str) e ne restituisce il writer
    :param idx_dir:
    :return:
    """
    try:
        assert type(idx_dir) is str
    except AssertionError:
        raise TypeError

    try:
        assert idx_dir != ""
    except AssertionError:
        raise ValueError

    # Creazione dello schema dei documenti da indicizzare
    schema: Schema = Schema(title=TEXT(stored=True),
                            identifier=ID(stored=True, unique=True),
                            content=TEXT(stored=True))

    # Verifica dell'esistenza della cartella dell'indice
    if not path.exists(idx_dir):
        # In caso la cartella non esista viene creata
        mkdir(idx_dir)

    # Creazione dell'indice all'interno della cartella designata
    index = create_in(idx_dir, schema)

    # La funzione restituisce un oggetto in grado di inserire (scrivere) documenti all'interno dell'indice
    return index.writer()


class WikiHandler(sax.handler.ContentHandler):
    """
    Modulo di gestione del parsing per sax
    """

    def __init__(self):
        """
        current_element contiene un rapresentazione globale della posizione
        dell'elemento che che stiamo attualmente analizzando
        e che si troverà nell'ultima poszione
        """
        sax.handler.ContentHandler.__init__(self)
        self.__current_element = []     # Posizione dell' elemento attuale nel documento
        self.__title = None             # Titolo della pagina Wikipedia
        self.__id = None                # Identificatore numerico della pagina Wikipedia
        self.__redirect = None          # Titolo della pagina di destinazione del redirect
        self.__text = ""                # Contenuto della pagina Wikipedia

        # Writer per l'indice del documento xml che si vuole parsare
        self.__idx_writer = None

        # Set di tag di cui si intende elaborare il testo contenuto
        self.__target_tags = {"title", "id", "text"}

        # Definisco il set di titoli delle pagine che si ritengono rilevanti (quelle che si intende indicizzare)
        self.__relevant_pages = self.__get_relevant_pages__()

        # Flag che indica se la pagina corrente è tra quelle indicate come rilevanti
        self.__is_relevant = False

        # Flag che indica se saltare l'elaborazione dell'elemento corrente
        # True se non è un elemento target
        self.__skip = False

    @staticmethod
    def __get_relevant_pages__():
        """
        Metodo statico che restituisce il set di titoli di pagine ritenute rilevanti tra quelle presenti nel file xml,
        nel caso il set sia vuoto o non sia stato definito restituisce None
        """
        try:
            assert type(relevant_pages) is set
            assert len(relevant_pages) > 0

            return relevant_pages
        except (NameError, AssertionError):
            return None

    def startDocument(self):
        """
        Con l'inizio del documento xml viene creato l'indice che conterrà
        le pagine Wikipedia che ne verranno estratte
        """
        try:
            idx_dir = index_dir
            self.__idx_writer = index_writer_init(idx_dir)
        except (NameError, TypeError, ValueError):
            print("Warning: creating index's directory using the default directory name")
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

        # Non ci interessa il contenuto del tag "redirect" (vuoto), ma ci interessa il suo attributo
        # (titolo pagina destinazione redirect), motivo per cui dobbiamo acquisire il dato in "startElement"
        if tag == "redirect" and self.__is_relevant is True:
            self.__redirect = attributes["title"]

        # Appendiamo il tag che è stato aperto alla lista in modo da avere
        # contesto rispetto alla posizione attuale nel file xml
        self.__current_element.append(tag)

    def characters(self, content):

        if self.__current_element[-1] == "title":
            if self.__relevant_pages is None or content in self.__relevant_pages:
                self.__title = content
                self.__is_relevant = True
            else:
                self.__is_relevant = False

        if self.__skip is False and self.__is_relevant is True:
            # Verifico che il tag "id" sia quello della pagina e non di un utente
            if self.__current_element[-1] == "id" and self.__current_element[-2] == "page":
                self.__id = content

            elif self.__current_element[-1] == "text":
                # ci possono essere più tag "text" per una pagina
                self.__text += content

    def endElement(self, tag):
        # Se il tag dell'elemento che si chiude è "page" e la pagina è un articolo
        # inserisco i dati raccolti nell'indice (diventano un nuovo documento)
        if tag == "page" and self.__is_relevant is True:
            try:
                self.__add_page_to_index()
            except ValueError:
                print(f"ERROR: the article has missing data\n"
                      f"{self.__title}\n"
                      f"{self.__id}\n"
                      f"{self.__text}")
                # exit() # Da decidere se sia da considerare un "FATAL ERROR" o meno
            finally:
                # Resetto le variabili
                self.__title = None
                self.__id = None
                self.__redirect = None
                self.__text = ""

        # Ogni volta che "esco" da un elemento ne elimino il tag dalla posizione attuale
        try:
            assert tag == self.__current_element[-1]  # Controllo che i tag siano stati aperti e chiusi correttamente
            self.__current_element.pop()
        except AssertionError:
            print(f"ERROR: the tag/element {self.__current_element[-1]} has been opened but never closed")
            exit(-1)

    def __add_page_to_index(self):
        # Verifico che i valori dell'articolo siano stati effettivamente parsati e raccolti
        try:
            assert self.__title is not None
            assert self.__id is not None
            assert self.__text != ""
        except AssertionError:
            raise ValueError

        # Inserisco la pagina nell'indice
        print(f"Indexing of {self.__title}")
        self.__idx_writer.add_document(title=self.__title,
                                       identifier=self.__id,
                                       content=self.__text)
