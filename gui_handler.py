from tkinter import *
from tkinter.font import *

from whoosh.searching import Results
from tkscrolledframe import ScrolledFrame
import webbrowser


class GuiHandler:
    def __init__(self, searcher):
        self.__searcher = searcher
        self._gui_initializer()

    def _gui_initializer(self):
        # dichiarazione colori
        self.__color_background = "#f0f0f0"  # "#ffffff"
        self.__color_status_bar = "#f0f0f0"
        self.__color_results = "#f3f3f3"
        self.__font_size_default = 10

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
        self.__frame_scrolled = ScrolledFrame(self.__window, bg=self.__color_results, scrollbars="vertical")
        self.__frame_scrolled.bind_arrow_keys(self.__window)
        self.__frame_scrolled.bind_scroll_wheel(self.__window)

        self.__frame_center_query_result = self.__frame_scrolled.display_widget(Frame)
        self.__frame_center_query_result.configure(bg=self.__color_results)
        self.__frame_center_query_result.pack(fill=BOTH, expand=True)

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
            #self.__frame_center_query_result = self.__frame_scrolled.display_widget(Frame)
            #self.__frame_center_query_result = Frame(self.__frame_scrolled, bg=self.__color_background)

            for widget in self.__frame_center_query_result.winfo_children():
                widget.destroy()

            self.__label_dict = dict()

            # elaborazione query
            query_results: Results = self.__searcher.commit_query_with_disambiguation(query_text)

            # caricamento dei risultati nella gui
            if len(query_results) == 0:
                self._add_label_result(father_frame=self.__frame_center_query_result,
                                       text=f"La ricerca di - {query_text} - non ha prodotto risultati.",
                                       bg=self.__color_results,
                                       justify=LEFT,
                                       font=Font(size=self.__font_size_default))
            else:
                for res in query_results[:10]:
                    label_text = f"{res['title']}"
                    self._add_label_result(article_title=res['title'],
                                           father_frame=self.__frame_center_query_result,
                                           text=label_text,
                                           bg=self.__color_results,
                                           justify=LEFT,
                                           cursor="hand2",
                                           font=Font(size=self.__font_size_default))

    def gui_loader(self):
        self.__window.mainloop()

    @staticmethod
    def _url_open(url):
        webbrowser.open(url, new=2)

    def _label_result_on_click(self, event):
        title = self.__label_dict[event.widget]
        self._url_open(self.__searcher.get_article_url(title))

    def _label_on_enter(self, event):
        event.widget.configure(fg="blue", font=Font(size=self.__font_size_default, underline=1))

    def _label_on_leave(self, event):
        event.widget.configure(fg="black", font=Font(size=self.__font_size_default, underline=0))

    def _add_label_result(self, father_frame, article_title=None, *args, **kwargs):
        label_result = Label(father_frame, *args, **kwargs)

        # controllo che si tratti di un risultato della query (il messaggio "nessun risultato" non ha bisogno di un
        # link)
        if article_title is not None:
            label_result.bind("<Button-1>", self._label_result_on_click)
            label_result.bind("<Enter>", self._label_on_enter)
            label_result.bind("<Leave>", self._label_on_leave)

            # memorizzo il "riferimento" lable ed il titolo corrispondente, per la gestione dell'evento click
            self.__label_dict[label_result] = article_title

        label_result.pack(anchor="w")