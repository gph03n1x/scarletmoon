### Scarlet Moon
Inverted Indexer project from information retrieval.
Implemented with python 3.6.0

### Dependencies

This project uses beautiful soup 4 for sgm parsing .
```bash
pip install beautifulsoup4
```

### Adding documents

```bash
usage: scan.py [-h] -f FILTER -d DIRECTORY -o OUTPUT
scan.py: error: the following arguments are required: -f/--filter, -d/--directory, -o/--output
```

Filters are grep like filters.

Directory is the directory you want to scan and add to the token tree.

Output is the name of the tokentree , which is going to get stored at the storage folder.


```bash
python scan.py -f *.sgm -d reuters -o tokentree
```

### Using scarletmoon

The application loads by default the tokentree.pickle and is intended for
terminal use because it cleans the screen and uses getch.ex

```bash
[*] :load [file path]
[*] Loads a file into the current btree
[*] :index save [filename]
[*] Saves the current btree in the specified filename
[*] :index load [filename]
[*] Loads the btree from the specified filename
[*] :freq [number]
[*] Shows the [number] most frequent tokens.
[*] :size
[*] Shows the size of the btrees
[*] :debug
[*] Shows information from sys._debugmallocstats()
[*] :exit
[*] Exits the application
```