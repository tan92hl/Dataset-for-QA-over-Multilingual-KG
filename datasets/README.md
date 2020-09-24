
# Datasets
Information about the datasets in this directory. 

  ## [`Questions`](Questions) 
  This directory contains all the labeled natural language questions. 
 - All datasets are categorized by the type of questions into different sub-directories.
 - We name each dataset (text file) by its attributes. For example,  `r2r_en_zh_question_en` indicates the following attributes for this dataset:
	1. `r2r` means the triples used to construct this dataset are all `(dbr, dbp, dbr)`-kind, where `dbr` means an entity whose original prefix in DBPedia is `<http://dbpedia.org/resource/>` and `dbr` means it is a relation whose original prefix in DBPedia is `<http://dbpedia.org/property/>` before it is extracted and formatted.
	2. `en_zh_question` means questions in this dataset all require a reasoning direction of English knowledge base -> Chinese knowledge base.
	3. The trailing`en` indicates all the questions are in English.
 - Each dataset is a text file formatted in a CSV-like format with the following conventions:
	1. Each line is a data record.
	2. Each data record can be separated by a first-level separator (a TAB character "`	`") into the text of the question and the label (reasoning path).
	3. The reasoning path also contains the answer to this question. Path can be separated by a second-level separator ("`###`") into triples. Knowledge bases required for the reasoning of each triple is indicated by the file name.
	4. Each triple can be separated by a third-level separator ("`@@@`") into a `dbr` (entity), a `dbp` (relation) and a `dbr` (entity).
	5. The final answer to the question is the trailing `dbr` of the last triple.
## [`Triples_in_questions`](Triples_in_questions)
This directory contains all the data extracted from DBPedia (triples as knowledge bases in 3 languages) that can be used for the reasoning of the questions. Their names are self-explanatory.
 - For each file, each line is one alignment pair.
 - Each pair can be separated by "`&&&`" into a `dbr` (entity), a `dbp` (relation) and a `dbr` (entity).
## [`Alignments_in_Questions`](Alignments_in_Questions)
This directory contains all the cross-lingual entity alignments (IILs) extracted from DBPedia that can be used for the reasoning of the questions. Their names are self-explanatory.
 - For each file, each line is one alignment pair.
 - Each pair can be separated by "`@@@`" into the two aligned entities.

## RDF version
All the datasets are available in RDF format, under the 'RDF' directory in each of the '[Question](Questions)' datasets.
