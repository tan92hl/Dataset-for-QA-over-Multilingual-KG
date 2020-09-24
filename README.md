
# MLPQ: A Dataset for Path Question Answering over Multilingual Knowledge Graphs
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE.txt)

> Existing Knowledge Graph based Multilingual Question Answering (KG-MLQA) works mainly focus on the semantic parsing of multilingual questions, but ignore the combination
of multilingual knowledge, which makes the QA system fail to break through the limitation of monolingual resources and has no potential to cover all of questions. Through a semiautomatic template synthesis process, we present MLPQ, a parallel path question answering dataset based on bilingual knowledge graphs extracted from DBpedia, which contains 827k questions and covers three language pairs (Chinese/English, Chinese/French, and English/French). Each question in MLPQ includes two or three relations, and requires the integration of information from bilingual knowledge graphs. Based on the MLPQ, we propose the first QA task over multilingual KGs, named Cross-lingual Path Question (CLPQ). The popular path question answering and multiple knowledge question answering (QA) models are used to establish two baselines of MLPQ. Experiments show that existing QA models cannot precisely respond to CLPQ. This work may further promote the development of Multilingual KGQA and information retrieval.

## Table of contents
  1. [Datasets](#datasets)
       1. [Overview](#overview)
       2. [Dataset creation](#dataset-creation)
       3. [Statistics](#statistics)
       4. [Use of the datasets](#use-of-the-datasets)
  2. [Baselines](#baselines)
  3. [Versions and future work](#versions-and-future-work)
       1. [Version 1.1 update](#version-11-update)
       2. [Current version](#current-version)
       3. [Future work](#future-work)
  4. [License](#license)

## Datasets

### Overview
There are a total of 827k questions in MLPQ, which covers three language pairs (**Chinese/English**, **Chinese/French**, and **English/French**), and requires a **2-hop** or **3-hop** cross-lingual path inference to answer each question.

### Dataset creation
We establish MLPQ through a four-step semi-automatic process: 
1. **Triple pairs selection**: obtain the candidate triple pairs (2-hop and 3-hop) based on the Inter Language Links(ILLs) of DBpedia;
2. **Construction of templates**: build single-hop templates and synthesize them into multi-hop templates;
3. **Diversity**: increase the template diversity by paraphrases;
4. **The building of Questions**: generate questions by adding topic entities into templates.

For more detailed explanation, please refer to our paper.

### Statistics

Number of triple pairs extracted from Dpedia to generate questions of CLPQ (Top-200 relations of each language):

|  Language pair | Direction | 2-hop | 3-hop |
| --- | --- | --- | --- |
|  en-zh | en→zh | 2743557 | 5022783 |
|   | zh→en | 9415 | 32895 |
|  zh-fr | zh→fr | 8618 | 20443 |
|   | fr→zh | 506695 | 769711 |
|  en-fr | en→fr | 533786 | 1708099 |
|   | fr→en | 10816641 | 4868011 |
 
Statistics of each subset of MLPQ, ”Q” means
”questions”, ”Lan” means ”language”:

|  Lan. pair | type | Q.Lan | #Q | #Ent | #Rel |
| :---: | :---: | :---: | :---: | :---: | :---: |
|  en-zh | 2-hop | en | 65741 | 49016 | 89 |
|   |  | zh | 129535 | 49225 | 89 |
|   | 3-hop | en | 97107 | 68143 | 198 |
|   |  | zh | 85167 | 21368 | 147 |
|  zh-fr | 2-hop | zh | 59650 | 22690 | 86 |
|   |  | fr | 27850 | 22532 | 86 |
|   | 3-hop | zh | 34796 | 12938 | 146 |
|   |  | fr | 35076 | 30732 | 189 |
|  en-fr | 2-hop | en | 71605 | 52913 | 77 |
|   |  | fr | 49061 | 53012 | 77 |
|   | 3-hop | en | 93249 | 62988 | 185 |
|   |  | fr | 78229 | 72505 | 172 |

### Use of the datasets
- The datasets are available in two formats. One is in RDF format, the other is in a custom format similar to the datasets used in [IRN](https://github.com/zmtkeke/IRN/tree/master/PathQuestion).
- All the datasets are in the [datasets](./datasets) directory. For explanation of file naming convensions and our custom format, please refer to this directory for further information.

## Baselines
- We establish two baseline models of MLPQ based on the popular multi-hop reasoning model [IRN](https://github.com/zmtkeke/IRN/tree/master/PathQuestion) and [multiple KGQA model](https://dl.acm.org/doi/10.5555/3016100.3016335), combined with a representative [Cross-ingual Entity Aligment (CLEA) model](https://github.com/muhaochen/MTransE-tf).
- The two baselines are called **MIRN** and **CL-MKQA** respectively.
- Baseline codes are in the [baselines](baselines) directory. To try these baselines, please refer to this directory for further information.

## Versions and future work

### Version 1.1 update
In this slightly improved version, we corrected many grammatical errors and added the RDF version of all the datasets.

### Current version
- Currently the MLPQ version is `1.1`. We expect to further the work and provide datasets of higher quality and more variety in the future.
- Because the generation of MLPQ is semi-automatic and relys on manually crafted templates and machine translation to some degree, there might be some minor problems in the text. We try to improve the quality of MLPQ by post-editing and there should be very few problems now. However, if you find any errors in the dataset, please contact us, thanks.

### Future work
For now, MLPQ mainly contains 2-hop and 3-hop path questions. In the future, we plan to adopt retelling generation based on web resources to create a greater abundance of question expressions. The path question is merely one subset of complex questions; we also plan to update and augment factoriented complex questions with property information and to explore aggregate-typed complex questions.

## License
This project is licensed under the GPL3 License - see the [LICENSE](LICENSE.txt) file for details
