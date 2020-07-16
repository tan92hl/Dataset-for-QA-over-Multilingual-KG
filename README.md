
# MLPQ

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

MLPQ is a parallel path question answering dataset based on bilingual knowledge graphs extracted from DBpedia which adds “cross-lingual path question (CLPQ)” as a new subtask in KG-MLQA.

For more details about the generation of MLPQ, please refer to our paper.

## Datasets

There are a total of 827k questions in MLPQ, which covers three language pairs (**Chinese/English**, **Chinese/French**, and **English/French**), and requires a **2-hop** or **3-hop** cross-lingual path inference to answer each question.
- All the datasets are in the [datasets](./datasets) directory. Please refer to this directory for further information, such as dataset formats, file naming convetions, etc.
- For now we are using custom-defined data formats, following the same practice as some related works (e.g., [IRN](https://github.com/zmtkeke/IRN/tree/master/PathQuestion)'s `PathQuestion` dataset), which require some very simple parsing. To enable easier use, we will publish the datasets in more common formats like CSV or JSON in the recent future.
## Baselines
The code for two baseline models are also open-source in this repository. Please refer to our paper for further details about these baselines.

- Baseline codes are in the [baselines](baselines) directory. Please refer to this directory for further information about how to run them.

## Versions

Currently the MLPQ version is `1.0`. We expect to further the work and provide datasets of higher quality and more variety in the future.

- Because the generation of MLPQ is semi-automatic and relys on manually crafted templates and machine translation to some degree, there might be some issues (like grammatical errors) in the text. We will try to improve the quality of MLPQ and a newer version with higher quality will be published very soon.
- For now, MLPQ mainly contains 2-hop and 3-hop path questions. For future work, we will generalize MLPQ with more complex questions and possibly other types of triples.
