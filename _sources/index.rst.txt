.. Scarlet Moon documentation master file, created by
   sphinx-quickstart on Wed Jun 14 17:07:57 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Scarlet Moon's documentation!
========================================

This application creates an inverted index in the form of a binary tree
for each letter (a, b, c, d, ...), digit (0-9).

Search operators: [:and:, :or:, :not:]

Searching for hurricanes :

.. code-block:: bash

   # hurricanes
   [*] Article :WEST TEXAS COTTON CROP UNSCATHED BY STORM
       Document:reuters\reut2-018.sgm
       tf-idf  : 0.04846927182717779
   [*] Article :UK SUGAR FACTORY CLOSES DUE TO SHORTAGE OF BEET
       Document:reuters\reut2-021.sgm
       tf-idf  : 0.04326451780546743
   [*] Article :CUBA SUGAR CROP SEEN AT LEAST SAME AS LAST YEAR
       Document:reuters\reut2-004.sgm
       tf-idf  : 0.043119820421502655


Searching for documents with the word election but not the word banks

.. code-block:: bash

   # elections :not: banks
   [*] Article :HONEYWELL <HON> ELECTS NEW CHIEF EXECUTIVE
       Document:reuters\reut2-020.sgm
       tf-idf  : 0.4582163400957904
   [*] Article :H.J. HEINZ <HNZ> ELECTS NEW CHAIRMAN
       Document:reuters\reut2-003.sgm
       tf-idf  : 0.3532084288238384
   [*] Article :INFOTRON <INFN> NAMES NEW CHAIRMAN
       Document:reuters\reut2-003.sgm
       tf-idf  : 0.3260385496835432
   [*] Article :K-TRON <KTII.O> ELECTS NEW PRESIDENT
       Document:reuters\reut2-018.sgm
       tf-idf  : 0.3082546287917135
   [*] Article :DIRECT ACTION <DMK> CALLS SHAREHOLDER MEETING
       Document:reuters\reut2-020.sgm
       tf-idf  : 0.3027500818490043
   [*] Type [n] for next results
   [*] >>>> [p] for previous results
   [*] >>>> [q] to leave results


** Core documentation: **

.. toctree::
   :maxdepth: 4

   btree
   getch
   identifier
   ngrams
   terminal
   tokens
   categorizer
   documents
   logic
   ngrams
   porter
   querying
   SGM
   tfidf


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
