from tkinter import *
from whoosh.searching import Results
from tkscrolledframe import ScrolledFrame
import webbrowser

class GuiHandler:
    def __init__(self, searcher):
        self.__searcher = searcher
        self._gui_initializer()

    def _gui_initializer(self):
        # dichiarazione colori
        self.__color_background = "#f0f0f0" # "#ffffff"
        self.__color_status_bar = "#f5f5f5"

        self.__window = Tk()
        self.__window.title("WikiSearch")
        self.__window.geometry("600x400")
        self.__window.minsize("400", "200")
        self.__window.configure(bg=self.__color_background)

        # ************************************************************************
        # ********************************* TOP **********************************
        # ************************************************************************

        # creazione frame TOP per l'immissione delle query
        self.__frame_top_query_input = Frame(bg=self.__color_background)
        self.__frame_top_query_input.pack(side=TOP)


        # creazione campi e bottoni per l'immissione delle query
        self.__entry_query = Entry(master=self.__frame_top_query_input, width=50)
        self.__entry_query.bind('<Return>', self._search_event)

        self.__button_search = Button(master=self.__frame_top_query_input,
                                      text="Search",
                                      command=self._search_event)

        self.__entry_query.pack(side="left")
        self.__button_search.pack(side="left", padx=5)

        # ************************************************************************
        # ******************************* CENTER *********************************
        # ************************************************************************
        self.__frame_scrolled = ScrolledFrame(self.__window)
        self.__frame_scrolled.bind_arrow_keys(self.__window)
        self.__frame_scrolled.bind_scroll_wheel(self.__window)

        self.__frame_center_query_result = self.__frame_scrolled.display_widget(Frame)

        self.__frame_scrolled.pack(
            fill=BOTH,
            expand=True
        )

        # ************************************************************************
        # ******************************* BOTTOM *********************************
        # ************************************************************************

        self.__frame_bottom_status_bar = Frame(bg=self.__color_status_bar)
        self.__frame_bottom_status_bar.pack(fill=X,
                                            side=BOTTOM)
        self.__label_credits = Label(master=self.__frame_bottom_status_bar,
                                     text="Developed by Mescoli and Terzulli",
                                     bg=self.__color_status_bar)
        self.__label_credits.pack(side="right")

        # dizionario usato nella gestione degli eventi click sui risultati
        # chiave: label corrispondente al singolo risultato
        # valore: titolo del risultato (servirà per generare l'url della pagina da aprire nel browser)
        self.__label_dict = dict()

    def _search_event(self, event=None):
        query_text = self.__entry_query.get()

        if len(query_text) > 0:
            # pulizia frame e dizionario label
            self.__frame_center_query_result = self.__frame_scrolled.display_widget(Frame)
            self.__label_dict = dict()

            # elaborazione query
            query_results: Results = self.__searcher.commit_query(query_text)

            # caricamento dei risultati nella gui
            if len(query_results) == 0:
                self._add_label_result(father_frame=self.__frame_center_query_result,
                                       text=f"La ricerca di - {query_text} - non ha prodotto risultati.",
                                       bg=self.__color_background,
                                       justify=LEFT)
            else:
                for res in query_results[:10]:
                    label_text = f"{res['title']}    | Score: {res.score}\nDescrizione fdsdsdfsfsfddffffsfsd"

                    self._add_label_result(article_title=res['title'],
                                           father_frame=self.__frame_center_query_result,
                                           text=label_text,
                                           bg=self.__color_background,
                                           justify=LEFT)

            # DEBUG
            debug = False
            if(debug):
                print(f"\nResults for: {query_text}\n")

                if len(query_results) == 0:
                    print("NESSUN RISULTATO")
                    self._add_label_result(father_frame=self.__frame_center_query_result,
                                           text=f"La ricerca di - {query_text} - non ha prodotto risultati.",
                                           bg=self.__color_background,
                                           justify=LEFT)
                else:
                    for x in query_results[:10]:
                        print(f"--Pos: {x.rank} Score:{x.score}\n"
                              f"Title: {x['title']} Id: {x['identifier']}\n"
                              f"Content: {x['content'][:256]}")

                    for res in query_results[:10]:
                        label_text = f"{res['title']}    | Score: {res.score}\nDescrizione fdsdsdfsfsfddffffsfsd"

                        self._add_label_result(article_title=res['title'],
                                               father_frame=self.__frame_center_query_result,
                                               text=label_text,
                                               bg=self.__color_background,
                                               justify=LEFT)

                print("\n==========================================================")
            # FINE DEBUG

    def gui_loader(self):
        self.__window.mainloop()

    def _url_open(self, url):
        webbrowser.open(url, new=2)

    def _url_generator(self, title):
        return "https://en.wikipedia.org/wiki/" + title

    def _label_result_on_click(self, event):
        title = self.__label_dict[event.widget]
        self._url_open(self._url_generator(title))
        print(f"DEBUG: click su {title}")

    def _add_label_result(self, father_frame, article_title=None, *args, **kwargs):
        label_result = Label(father_frame, *args, **kwargs)

        # controllo che si tratti di un risultato della query (il messaggio "nessun risultato" non ha bisogno di un
        # link)
        if article_title is not None:
            label_result.bind("<Button-1>", self._label_result_on_click)
            # memorizzo il "riferimento" lable ed il titolo corrispondente, per la gestione dell'evento click
            self.__label_dict[label_result] = article_title

        label_result.pack(anchor="w")
