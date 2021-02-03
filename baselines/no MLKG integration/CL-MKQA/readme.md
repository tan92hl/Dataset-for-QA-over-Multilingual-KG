# CL-MKQA

## Description
- [MKQA.py](MKQA.py): the model script.
- [parseQuestion(enzh).py](parseQuestion(enzh).py): used to split and translate the predicates in the questions. The question datasets can be processed here.
- [RDF_Generator.py](RDF_Generator.py): used to generate RDF files for SPARQL.
- [buildList.py](buildList.py): used to create dictionary and alignment list. The alignment list can be replaced here.

## Data
All the data used are from MLPQ, but some modifications are made, like formatting, different versions of KB (1.0), etc.

## Use of this model

1. Given the knowledge base files, first build the RDF files with [RDF_Generator.py](RDF_Generator.py).
2. Given the question datasets, get the predictes and entities with [parseQuestion(enzh).py](parseQuestion(enzh).py).
3. Use [MKQA.py](MKQA.py) to read candidate predicates to get the answers.
4. Alignment list can be changed with [buildList.py](buildList.py).