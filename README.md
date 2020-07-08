# WikiSearch - Exam project of Gestione dell'Informazione
Exam project of *Gestione dell'Informazione*. Developed by **Riccardo Mescoli** and **Marco Terzulli**.


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for evaluation and testing purposes.

### Prerequisites

What things you need to install the software and how to install them

```
* A Windows or Linux or MacOS based machine
* Python 3.7+
* Python Pip3
```

### Installing

1. Unpack the zip archive and install the following libraries.

2. *Whoosh* installation.<br />
Run the following command in a terminal:

```
pip3 install whoosh
```

3. *tkscrolledframe* installation (needed by the GUI).<br />
Run the following command in a terminal:

```
pip3 install tkscrolledframe
```

4. **Linux Only** *tkinter* installation (needed by the GUI).<br />
On some Linux distributions tkinter module will not be installed by default with Python3.<br />
Run the following command in a terminal as SuperUser:

```
apt-get install python3-tk
```


## Running the project

You can either use the provided index or generate a new one.

### Using the provided index

Simply run the project within an IDE or a terminal

```
python main.py
```
or
```
python3 main.py
```

The GUI will be loaded.<br />
**Common issue**: the previous command could raise an error while trying to open the index. 
Whoosh indexes are operating system dependent: you are probably using a different operating system than the one was used to generate it. 
The program will automatically try to delete the index and to generate a new one, but sometimes this operation could not be possibile.
In this case, follow the next step to generate a new index.

### Generating a new index

Delete the Wiki_index folder. Run the project within an IDE or a terminal 

```
python main.py
```
or
```
python3 main.py
```

The indexing log will be printed in the console or terminal in real time.<br />
After the index is commited, the GUI will be loaded.

### Submitting a query

After the GUI is loaded, you will be able to submit the queries using the textbox in the top of the page. 
You can simply press the Enter button of the keyboard or left-click on the Search button with your mouse.

### Opening a result

After you have submitted a valid query, you can left-click on the result titles to open the respective Wikipedia article in your default browser.

### Query Expansion

After you have submitted a valid query, you can search for similar articles by left-clicking on the "More like this" button of a result.


## Built With

* [JetBrains Pycharm](https://www.jetbrains.com/pycharm/) - The IDE we used for development and testing
* [Python](https://www.python.org/) - Programming Language
* [Whoosh](https://pypi.org/project/Whoosh/) - Used for Information Retrieval


## Authors

* **Riccardo Mescoli** 
* **Marco Terzulli** 

## Known Issues

* After pressing the "More like this" button of a result, the scrollbar position remains the same and the page is not bringed back to the start position. 
You have to manually scroll the page to see the first results.

* Pressing the left and right arrow keys of the keyboard will horizontally scroll the page, but a horizontal scrollbar is not going to appear. 
This also happens if these keys are pressed inside the query textbox.
