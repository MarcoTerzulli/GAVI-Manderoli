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
        self.__color_window_background = "#f0f0f0"  # "#ffffff"
        self.__color_status_bar_background = "#f0f0f0"
        self.__color_results_background = "#f3f3f3"
        self.__color_results_font = "blue"
        self.__color_results_font_hover = "#003c8f"
        self.__color_more_like_this_font = "#795548"
        self.__color_more_like_this_font_hover = "#a98274"
        self.__font_size_default = 11

        self.__window = Tk()
        self.__window.title("WikiSearch")
        self.__window.geometry("600x400")
        self.__window.minsize("550", "200")
        self.__window.configure(bg=self.__color_window_background)

        # ************************************************************************
        # ********************************* TOP **********************************
        # ************************************************************************

        # creazione frame TOP per l'immissione delle query
        self.__frame_top_query_input = Frame(bg=self.__color_window_background)
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
        self.__frame_scrolled = ScrolledFrame(self.__window, bg=self.__color_results_background, scrollbars="vertical")
        self.__frame_scrolled.bind_arrow_keys(self.__window)
        self.__frame_scrolled.bind_scroll_wheel(self.__window)

        self.__frame_center_query_result = self.__frame_scrolled.display_widget(Frame)
        self.__frame_center_query_result.configure(bg=self.__color_results_background)

        self.__frame_scrolled.pack(
           fill=BOTH,
           expand=True
        )



        # ************************************************************************
        # ******************************* BOTTOM *********************************
        # ************************************************************************

        self.__frame_bottom_status_bar = Frame(bg=self.__color_status_bar_background)
        self.__frame_bottom_status_bar.pack(fill=X,
                                            side=BOTTOM)
        self.__label_credits = Label(master=self.__frame_bottom_status_bar,
                                     text="Developed by Mescoli and Terzulli",
                                     bg=self.__color_status_bar_background)
        self.__label_credits.pack(side="right")

        # dizionario usato nella gestione degli eventi click sui risultati
        # chiave: label corrispondente al singolo risultato
        # valore: titolo del risultato (servirà per generare l'url della pagina da aprire nel browser)
        self.__label_dict = dict()

        # Label per query expansion
        self.__label_more = dict()

    def _search_event(self, event=None):
        query_text = self.__entry_query.get()

        if len(query_text) > 0:
            # pulizia frame e dizionario label
            #self.__frame_center_query_result = self.__frame_scrolled.display_widget(Frame)
            #self.__frame_center_query_result = Frame(self.__frame_scrolled, bg=self.__color_background)

            self.__label_dict = dict()
            self.__label_more = dict()

            # elaborazione query
            query_results: Results = self.__searcher.commit_query(query_text)

            # caricamento dei risultati nella gui
            self.__results_management(query_text, query_results)

    def gui_loader(self):
        self.__window.mainloop()

    @staticmethod
    def _url_open(url):
        webbrowser.open(url, new=2)

    def _label_result_on_click(self, event):
        title = self.__label_dict[event.widget]
        self._url_open(self.__searcher.get_article_url(title))

    def _label_on_enter(self, event):
        event.widget.configure(fg=self.__color_results_font_hover, font=Font(size=self.__font_size_default, underline=1, weight='bold'))

    def _label_more_on_enter(self, event):
        event.widget.configure(fg=self.__color_more_like_this_font_hover, font=Font(size=self.__font_size_default-1, underline=1))

    def _label_on_leave(self, event):
        event.widget.configure(fg=self.__color_results_font, font=Font(size=self.__font_size_default, underline=0, weight='bold'))

    def _label_more_on_leave(self, event):
        event.widget.configure(fg=self.__color_more_like_this_font, font=Font(size=self.__font_size_default-1, underline=0))

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

        label_result.pack(anchor="w", expand=True)

    def _add_label_more_like_this(self, father_frame, bounded_result, *args, **kwargs):
        label_more_like_this = Label(father_frame, *args, **kwargs)

        label_more_like_this.bind("<Button-1>", self._label_more_like_this_on_click)
        label_more_like_this.bind("<Enter>", self._label_more_on_enter)
        label_more_like_this.bind("<Leave>", self._label_more_on_leave)

        self.__label_more[label_more_like_this] = bounded_result

        label_more_like_this.pack(anchor="w", expand=True)

    def _add_label_highlight(self, father_frame, bounded_result, *args, **kwargs):
        label_highlight = Label(father_frame, *args, **kwargs)

        #label_highlight.bind("<Button-1>", self._label_more_like_this_on_click)
        #label_highlight.bind("<Enter>", self._label_more_on_enter)
        #label_highlight.bind("<Leave>", self._label_more_on_leave)

        #self.__label_more[label_more_like_this] = bounded_result

        label_highlight.pack(anchor="w", expand=True)

    def _label_more_like_this_on_click(self, event):
        base_res = self.__label_more[event.widget]
        new_res = self.__searcher.get_similar_articles(base_res)
        self.__results_management(base_res['title']+" (EXPANSION)", new_res)

    def _highlight_formatter(self, highlight_text):
        new_text = ''
        max_char = 90
        for line in highlight_text.splitlines():
            i = 0
            while i * max_char < line.__len__():
                new_text += line[i*max_char : (i+1)*max_char] + '\n'
                i+=1

        # rimuovo l'ultimo newline
        if new_text[-1] == '\n':
            new_text = new_text[:new_text.__len__() -1]

        return new_text

    def __results_management(self, query_text, query_results):

        for widget in self.__frame_center_query_result.winfo_children():
            widget.destroy()

        if len(query_results) == 0:
            self._add_label_result(father_frame=self.__frame_center_query_result,
                                   text=f"La ricerca di - {query_text} - non ha prodotto risultati.",
                                   bg=self.__color_results_background,
                                   justify=LEFT,
                                   font=Font(size=self.__font_size_default))
        else:
            for res in query_results[:10]:
                label_text = f"{res['title']}"
                self._add_label_result(article_title=res['title'],
                                       father_frame=self.__frame_center_query_result,
                                       text=label_text,
                                       bg=self.__color_results_background,
                                       justify=LEFT,
                                       cursor="hand2",
                                       font=Font(size=self.__font_size_default, weight='bold'),
                                       fg=self.__color_results_font)

                __highlight_text = self.__searcher.get_result_highlights(res)
                __highlight_text = self._highlight_formatter(__highlight_text)
                if __highlight_text.__len__() > 0:
                    self._add_label_highlight(self.__frame_center_query_result,
                                              res,
                                              text=__highlight_text,
                                              bg=self.__color_results_background,
                                              justify=LEFT,
                                              font=Font(size=self.__font_size_default - 2))

                self._add_label_more_like_this(self.__frame_center_query_result,
                                               res,
                                               text="More like this\n",
                                               bg=self.__color_results_background,
                                               justify=LEFT,
                                               cursor="hand2",
                                               font=Font(size=self.__font_size_default-1),
                                               fg=self.__color_more_like_this_font)
                print(self.__searcher.get_result_highlights(res)+"\n\n")
            Label(self.__frame_center_query_result, bg=self.__color_results_background, text=((" " * 1000) + ("\n" * 30)), justify=LEFT).pack()


