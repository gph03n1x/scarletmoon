README NEEDS UPDATE
-------------------


### Scarlet Moon
Inverted Indexer project from information retrieval.
Implemented with python 3.6.0


### Dependencies

```bash
pip install -r requirements.txt
pip install spacy  # Installation failed on my windows machine.
python -m spacy download en_core_web_sm
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

### Using scarlet


```bash
nameko run scarlet
```

### Interacting with the service.

TODO.


### Running the unittests

```bash
python -m unittest discover
```

