from tkinter import *
from whoosh.searching import Results
from tkscrolledframe import ScrolledFrame


class GuiHandler:
    def __init__(self, searcher):
        self.__searcher = searcher
        self._gui_initializer()

    def _gui_initializer(self):
        # dichiarazione colori
        self.__color_background = "#f5f5f5" #"#ffffff"
        self.__color_status_bar = "#f5f5f5"

        self.__window = Tk()
        self.__window.title("WikiSearch")
        self.__window.geometry("600x400")
        self.__window.configure(bg=self.__color_background)

        # ************************************************************************
        # ********************************* TOP **********************************
        # ************************************************************************

        # creazione frame TOP per l'immissione delle query
        self.__frame_top_query_input = Frame(bg=self.__color_background)
        self.__frame_top_query_input.pack(side=TOP)

        # creazione campi e bottoni per l'immissione delle query
        self.__entry_query = Entry(master=self.__frame_top_query_input,
                                   width=50)

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

    def _search_event(self, event=None):
        # TO-DO roba per azionare la query e generare un output
        query_text = self.__entry_query.get()
        if len(query_text) > 0:
            query_results: Results = self.__searcher.commit_query(query_text)
            # DEBUG
            print(f"\nResults for: {query_text}\n")

            if len(query_results) == 0:
                print("NESSUN RISULTATO")
            else:
                for x in query_results[:10]:
                    print(f"--Pos: {x.rank} Score:{x.score}\n"
                          f"Title: {x['title']} Id: {x['identifier']}\n"
                          f"Content: {x['content'][:256]}")

                for res in query_results[:10]:
                    Label(self.__frame_center_query_result,
                          text=f"{res['title']}    | Score: {res.score}",
                          bg=self.__color_background).pack()

            print("\n==========================================================")

        # FINE DEBUG

    def gui_loader(self):
        self.__window.mainloop()

