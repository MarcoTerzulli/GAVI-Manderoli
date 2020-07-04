# GAVI-Manderoli
Exam project of *Gestione dell'Informazione*. Developed by **Riccardo Mescoli** and **Marco Terzulli**.


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
* A Windows or Linux or MacOS based machine
* Python 3.7+
```

### Installing

Unpack the zip archive and install the following libraries.

Whoosh installation

```
pip3 install whoosh
```

tkscrolledframe installation (needed by the GUI)

```
pip3 install tkscrolledframe
```

End with an example of getting some data out of the system or using it for a little demo

## Running the project

You can either use the provided index or generate a new one.

### Using the provided index

Simply run the project within an IDE or a terminal

```
python main.py
```

The GUI will be loaded.

### Generating a new index

Delete the Wiki_index folder. Run the project within an IDE or a terminal 

```
python main.py
```

The indexing log will be printed in the console or terminal in real time.
After the index is commited, the GUI will be loaded.

### Submitting a query

After the GUI is loaded, you will be able to submit the queries using the textbox in the top of the page. You can simply press the Enter button of the keyboard or left-click on the Search button with your mouse.

### Opening a result

After you have submitted a valid query, you can left-click on the result titles to open the respective Wikipedia article in your default browser.

### Query Expansion

After you have submitted a valid query, you can search for similar articles by left-click on the "More like this" button of a result.


## Built With

* [JetBrains Pycharm](https://www.jetbrains.com/pycharm/) - The IDE we used for development and testing
* [Python](https://www.python.org/) - Programming Language
* [Whoosh](https://pypi.org/project/Whoosh/) - Used for Information Retrieval

## Authors

* **Riccardo Mescoli** 
* **Marco Terzulli** 
