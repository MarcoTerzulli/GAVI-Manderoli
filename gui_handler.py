from tkinter import *
from whoosh.searching import Results


class GuiHandler:
    def __init__(self, searcher):
        self.__searcher = searcher
        self._gui_initializer()

    def _gui_initializer(self):
        # dichiarazione colori
        self.__color_background = "#ffffff"
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
        self.__entry_query = Entry(
            master=self.__frame_top_query_input,
            width=50
        )
        self.__entry_query.bind('<Return>', self._search_event)

        self.__button_search = Button(
            master=self.__frame_top_query_input,
            text="Search",
            command=self._search_event()
        )

        self.__entry_query.pack(side="left")
        self.__button_search.pack(
            side="left",
            padx=5
        )

        # ************************************************************************
        # ******************************* CENTER *********************************
        # ************************************************************************
        # self.__frame_center_query_result = ScrollableFrame(self.__window, self.__color_background)
        self.__frame_center_query_result = ScrollableFrame(self.__window, "#008000")

        # DEBUG INIZIO
        for i in range(20):
            Label(self.__frame_center_query_result.scrollable_frame, text="Sample scrolling label", anchor=NW).pack()

        debug_auto = False
        if debug_auto:
            query_text = "afghanistan"
            if len(query_text) > 0:
                query_results: Results = self.__searcher.commit_query(query_text)

                # DEBUG
                if len(query_results) == 0:
                    print("DEBUG: nessun risultato")
                    Label(
                        self.__frame_center_query_result.scrollable_frame,
                        text="Nessun risultato",
                        bg=self.__color_background).pack()
                else:
                    for x in query_results[:10]:
                        # print(
                        #     f"--Pos: {x.rank} Score:{x.score}\nTitle: {x['title']} Id: {x['identifier']}\n"
                        #     f"Content: {x['content'][:256]}")

                        print(
                            f"--Pos: {x.rank} Score:{x.score}\nTitle: {x['title']}")
                    for res in query_results[:10]:
                        Label(
                            self.__frame_center_query_result.scrollable_frame,
                            text=f"--Pos: {res.rank}     Score: {res.score}\nTitle: {res['title']}",
                            bg=self.__color_background).pack(side=TOP)

        self.__frame_center_query_result.pack(
            fill=BOTH,
            expand=True
        )

        # ************************************************************************
        # ******************************* BOTTOM *********************************
        # ************************************************************************
        self.__frame_bottom_status_bar = Frame(bg=self.__color_status_bar)
        self.__frame_bottom_status_bar.pack(
            fill=X,
            side=BOTTOM
        )
        self.__label_credits = Label(
            master=self.__frame_bottom_status_bar,
            text="Developed by Mescoli and Terzulli",
            bg=self.__color_status_bar
        )
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
                    print(
                        f"--Pos: {x.rank} Score:{x.score}\nTitle: {x['title']} Id: {x['identifier']}\n"
                        f"Content: {x['content'][:256]}")
                for res in query_results[:10]:
                    Label(
                        self.__frame_center_query_result.scrollable_frame,
                        text=f"{res['title']}",
                        bg=self.__color_background).pack()
            print("\n==========================================================")

        # FINE DEBUG

    def gui_loader(self):
        self.__window.mainloop()


class ScrollableFrame(Frame):
    def __init__(self, container, background, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        self.canvas = Canvas(self, bg=background)

        scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
