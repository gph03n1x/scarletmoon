README NEEDS UPDATE
-------------------


### Scarlet Moon
Inverted Indexer project from information retrieval.
Implemented with python 3.6.0


### Dependencies

```bash
pip install -r requirements.txt
bash bin/install_redis.sh
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



```bash
redis-4.0.10/src/redis-server
# You need to use only one worker else the results get somehow messed up.
celery worker -A scarlet.celery --loglevel=info -B -P solo
python scarlet.py
```

### Running the unittests

```bash
python -m unittest discover
```