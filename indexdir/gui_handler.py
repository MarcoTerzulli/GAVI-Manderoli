from tkinter import *
#from tkinter.ttk import *

def gui_form_test():
    # dichiarazione colori
    color_background="#ffffff"
    color_status_bar="#f5f5f5"

    window = Tk()
    window.title("WikiSearch")
    window.geometry("600x400")
    window.configure(bg=color_background)

    # ****************************** TOP ******************************
    # creazione frame TOP per l'immissione delle query
    frame_top_query_input = Frame(bg=color_background)
    frame_top_query_input.pack(side=TOP)

    # creazione campi e bottoni per l'immissione delle query
    entry_query = Entry(
        master=frame_top_query_input,
        width=50
    )
    button_search = Button(
        master=frame_top_query_input,
        text="Search",
        command=button_search_click()
    )

    entry_query.pack(side="left")
    button_search.pack(
        side="left",
        padx=5
    )

    # **************************** BOTTOM *****************************
    frame_bottom_status_bar = Frame(bg=color_status_bar)
    frame_bottom_status_bar.pack(
        fill=X,
        side=BOTTOM
    )
    label_credits = Label(
        master=frame_bottom_status_bar,
        text="Developed by Mescoli and Terzulli",
        bg=color_status_bar
    )
    label_credits.pack(side="right")

    window.mainloop()

def button_search_click():
    #TO-DO roba per azionare la query e generare un output
    return None