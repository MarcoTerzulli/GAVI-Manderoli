import pandas as pd

filepool = {
    'siteen.wikipedia.org 99 balloons.csv',
    'siteen.wikipedia.org Apple.csv',
    'siteen.wikipedia.org Computer Programming.csv',
    'siteen.wikipedia.org DNA.csv',
    'siteen.wikipedia.org Do gees see god.csv',
    'siteen.wikipedia.org Epigenetics.csv',
    'siteen.wikipedia.org Eye of Horus.csv',
    'siteen.wikipedia.org Financial meltdown.csv',
    'siteen.wikipedia.org Hollywood.csv',
    'siteen.wikipedia.org Justin Timberlake.csv',
    'siteen.wikipedia.org Least Squares.csv',
    "siteen.wikipedia.org Madam I'm Adam.csv",
    'siteen.wikipedia.org Mars robots.csv',
    'siteen.wikipedia.org Maya.csv',
    'siteen.wikipedia.org Mean Average Precision.csv',
    'siteen.wikipedia.org Microsoft.csv',
    'siteen.wikipedia.org Much ado about nothing.csv',
    'siteen.wikipedia.org Page six.csv',
    'siteen.wikipedia.org Physics Nobel Prizes.csv',
    'siteen.wikipedia.org Precision.csv',
    'siteen.wikipedia.org Read the manual.csv',
    'siteen.wikipedia.org Roman Empire.csv',
    'siteen.wikipedia.org Solar energy.csv',
    'siteen.wikipedia.org Spanish Civil War.csv',
    'siteen.wikipedia.org Statistical Significance.csv',
    'siteen.wikipedia.org Steve Jobs.csv',
    'siteen.wikipedia.org The Maya.csv',
    'siteen.wikipedia.org Triple Cross.csv',
    'siteen.wikipedia.org Tuscany.csv',
    'siteen.wikipedia.org US Constitution.csv'
}

with open("test_relevant_titles.txt", "w") as w_file:

    for filename in filepool:
        w_file.write("\n---"+"".join(word + " " for word in filename.split(sep=" ")[1:])+"\n")
        
        table = pd.read_csv(filename, sep=";") 
        urls = table["Url"].astype(str) 

        for u in urls:
            w_file.write(u.split(sep="/")[-1]+"\n")