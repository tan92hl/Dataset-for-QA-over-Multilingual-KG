
# MLPQ: A Dataset for Path Question Answering over Multilingual Knowledge Graphs
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE.txt)

> Knowledge Graph-based Multilingual Question Answering (KG-MLQA), as one of the essential subtasks in Knowledge Graph-based Question Answering (KGQA), emphasizes that questions on the KGQA task can be expressed in different languages to solve the lexical gap between questions and knowledge graph(s). However, the existing KG-MLQA works mainly focus on the semantic parsing of multilingual questions but ignore the questions that require integrating information from cross-lingual knowledge graphs (CLKG). This paper extends KG-MLQA to Cross-lingual KG-based multilingual Question Answering (CLKGQA) and constructs the first CLKGQA dataset over multilingual DBpedia named MLPQ, which contains 300K questions in English, Chinese, and French. We further propose a novel KG sampling algorithm based on subgraph structural features and obtain KGs for MLPQ, making the evaluated methods compatible with our datasets. To evaluate the dataset, we put forward a general question answering framework whose core idea is to transform CLKGQA into KG-MLQA. We first use the Cross-lingual Entity Alignment (CLEA) model to merge CLKG into a single KG and get the answer to the question by the Multi-hop QA model combined with the Multilingual pre-training model. Then we establish two baselines for MLPQ, one of which uses Google translation to obtain alignment entities, and the other adopts the recent CLEA model. Experiments show that the simple combination of the existing QA and CLEA methods fails to obtain the ideal performances on CLKGQA. Moreover, the availability of our benchmark contributes to the community of question answering and entity alignment.

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
There are a total of 300K questions in MLPQ, which covers three language pairs (**English-Chinese**, **English/French**, and **Chinese/French**), and requires a **2-hop** or **3-hop** cross-lingual path inference to answer each question.

### Dataset creation
We establish MLPQ through a semi-automatic process shown in the following picture:
![Dataset Creation](resources/dataset_creation.png)

### Statistics

<table class="MsoTableGrid" border="1" cellspacing="0" cellpadding="0" style="border-collapse:collapse;border:none;mso-border-alt:solid windowtext .5pt;
 mso-yfti-tbllook:1184;mso-padding-alt:0cm 5.4pt 0cm 5.4pt">
 <tbody><tr style="mso-yfti-irow:0;mso-yfti-firstrow:yes">
  <td width="69" rowspan="2" style="width:51.55pt;border:solid windowtext 1.0pt;
  border-left:none;mso-border-top-alt:solid windowtext .5pt;mso-border-bottom-alt:
  solid windowtext .5pt;mso-border-right-alt:solid windowtext .5pt;padding:
  0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">KG pair<o:p></o:p></span></p>
  </td>
  <td width="74" rowspan="2" style="width:55.25pt;border-top:solid windowtext 1.0pt;
  border-left:none;border-bottom:solid windowtext 1.0pt;border-right:none;
  mso-border-left-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-left-alt:solid windowtext .5pt;mso-border-bottom-alt:solid windowtext .5pt;
  padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">Language<o:p></o:p></span></p>
  </td>
  <td width="69" rowspan="2" style="width:51.5pt;border-top:solid windowtext 1.0pt;
  border-left:none;border-bottom:solid windowtext 1.0pt;border-right:none;
  mso-border-top-alt:solid windowtext .5pt;mso-border-bottom-alt:solid windowtext .5pt;
  padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">2-hop<o:p></o:p></span></p>
  </td>
  <td width="69" rowspan="2" style="width:51.5pt;border-top:solid windowtext 1.0pt;
  border-left:none;border-bottom:solid windowtext 1.0pt;border-right:none;
  mso-border-top-alt:solid windowtext .5pt;mso-border-bottom-alt:solid windowtext .5pt;
  padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">3-hop<o:p></o:p></span></p>
  </td>
  <td width="137" colspan="2" style="width:102.5pt;border:none;border-top:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">Relation pairs in questions<o:p></o:p></span></p>
  </td>
  <td width="137" colspan="2" style="width:102.5pt;border:none;border-top:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">Average length<o:p></o:p></span></p>
  </td>
 </tr>
 <tr style="mso-yfti-irow:1">
  <td width="68" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">2-hop<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">3-hop<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">2-hop<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">3-hop<o:p></o:p></span></p>
  </td>
 </tr>
 <tr style="mso-yfti-irow:2">
  <td width="69" rowspan="3" style="width:51.55pt;border-top:none;border-left:none;
  border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;mso-border-right-alt:solid windowtext .5pt;
  padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span class="SpellE"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">en-zh</span></span><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt"><o:p></o:p></span></p>
  </td>
  <td width="74" style="width:55.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-left-alt:solid windowtext .5pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-left-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">English<o:p></o:p></span></p>
  </td>
  <td width="69" style="width:51.5pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="right" style="text-align:right"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">14,656<o:p></o:p></span></p>
  </td>
  <td width="69" style="width:51.5pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="right" style="text-align:right"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">29,815<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="right" style="text-align:right"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">1,250<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="right" style="text-align:right"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">2,628<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">12.4<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">15.5<o:p></o:p></span></p>
  </td>
 </tr>
 <tr style="mso-yfti-irow:3">
  <td width="74" style="width:55.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-left-alt:solid windowtext .5pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-left-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">Chinese<o:p></o:p></span></p>
  </td>
  <td width="69" style="width:51.5pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="right" style="text-align:right"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">14,852<o:p></o:p></span></p>
  </td>
  <td width="69" style="width:51.5pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="right" style="text-align:right"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">29,643<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="right" style="text-align:right"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">1,251<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="right" style="text-align:right"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">2,637<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">17.2<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">21.7<o:p></o:p></span></p>
  </td>
 </tr>
 <tr style="mso-yfti-irow:4">
  <td width="74" style="width:55.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-left-alt:solid windowtext .5pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-left-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">French<o:p></o:p></span></p>
  </td>
  <td width="69" style="width:51.5pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="right" style="text-align:right"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">15,169<o:p></o:p></span></p>
  </td>
  <td width="69" style="width:51.5pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="right" style="text-align:right"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">30,360<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="right" style="text-align:right"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">1,251<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="right" style="text-align:right"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">2,626<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">11.3<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">16.1<o:p></o:p></span></p>
  </td>
 </tr>
 <tr style="mso-yfti-irow:5">
  <td width="69" rowspan="3" style="width:51.55pt;border-top:none;border-left:none;
  border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;mso-border-right-alt:solid windowtext .5pt;
  padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span class="SpellE"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">en-fr</span></span><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt"><o:p></o:p></span></p>
  </td>
  <td width="74" style="width:55.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-left-alt:solid windowtext .5pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-left-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">English<o:p></o:p></span></p>
  </td>
  <td width="69" style="width:51.5pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="right" style="text-align:right"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">15,289<o:p></o:p></span></p>
  </td>
  <td width="69" style="width:51.5pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="right" style="text-align:right"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">18,154<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="right" style="text-align:right"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">1,138<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="right" style="text-align:right"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">3,575<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">12.3<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">15.5<o:p></o:p></span></p>
  </td>
 </tr>
 <tr style="mso-yfti-irow:6">
  <td width="74" style="width:55.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-left-alt:solid windowtext .5pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-left-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">Chinese<o:p></o:p></span></p>
  </td>
  <td width="69" style="width:51.5pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="right" style="text-align:right"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">15,831<o:p></o:p></span></p>
  </td>
  <td width="69" style="width:51.5pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="right" style="text-align:right"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">18,035<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="right" style="text-align:right"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">1,141<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="right" style="text-align:right"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">3,578<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">17.8<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">21.8<o:p></o:p></span></p>
  </td>
 </tr>
 <tr style="mso-yfti-irow:7">
  <td width="74" style="width:55.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-left-alt:solid windowtext .5pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-left-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">French<o:p></o:p></span></p>
  </td>
  <td width="69" style="width:51.5pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="right" style="text-align:right"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">15,867<o:p></o:p></span></p>
  </td>
  <td width="69" style="width:51.5pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="right" style="text-align:right"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">17,993<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="right" style="text-align:right"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">1,144<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="right" style="text-align:right"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">3,580<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">11.7<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">14.7<o:p></o:p></span></p>
  </td>
 </tr>
 <tr style="mso-yfti-irow:8">
  <td width="69" rowspan="3" style="width:51.55pt;border-top:none;border-left:none;
  border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;mso-border-right-alt:solid windowtext .5pt;
  padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span class="SpellE"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">zh-fr</span></span><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt"><o:p></o:p></span></p>
  </td>
  <td width="74" style="width:55.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-left-alt:solid windowtext .5pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-left-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">English<o:p></o:p></span></p>
  </td>
  <td width="69" style="width:51.5pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="right" style="text-align:right"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">8,373<o:p></o:p></span></p>
  </td>
  <td width="69" style="width:51.5pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="right" style="text-align:right"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">17,800<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="right" style="text-align:right"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">759<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="right" style="text-align:right"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">1,674<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">11.6<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">16.0<o:p></o:p></span></p>
  </td>
 </tr>
 <tr style="mso-yfti-irow:9">
  <td width="74" style="width:55.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-left-alt:solid windowtext .5pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-left-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">Chinese<o:p></o:p></span></p>
  </td>
  <td width="69" style="width:51.5pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="right" style="text-align:right"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">8,414<o:p></o:p></span></p>
  </td>
  <td width="69" style="width:51.5pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="right" style="text-align:right"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">17,877<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="right" style="text-align:right"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">758<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="right" style="text-align:right"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">1,677<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">17.5<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">21.4<o:p></o:p></span></p>
  </td>
 </tr>
 <tr style="mso-yfti-irow:10">
  <td width="74" style="width:55.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-left-alt:solid windowtext .5pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-left-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">French<o:p></o:p></span></p>
  </td>
  <td width="69" style="width:51.5pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="right" style="text-align:right"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">8,495<o:p></o:p></span></p>
  </td>
  <td width="69" style="width:51.5pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="right" style="text-align:right"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">17,856<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="right" style="text-align:right"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">758<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="right" style="text-align:right"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">1,668<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">12.1<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">14.9<o:p></o:p></span></p>
  </td>
 </tr>
 <tr style="mso-yfti-irow:11">
  <td width="69" rowspan="2" style="width:51.55pt;border-top:none;border-left:none;
  border-bottom:solid windowtext 1.0pt;border-right:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;mso-border-right-alt:solid windowtext .5pt;
  padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">Sum<o:p></o:p></span></p>
  </td>
  <td width="74" rowspan="2" style="width:55.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-left-alt:solid windowtext .5pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-left-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">-<o:p></o:p></span></p>
  </td>
  <td width="69" rowspan="2" style="width:51.5pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="right" style="text-align:right"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">116,946<o:p></o:p></span></p>
  </td>
  <td width="69" rowspan="2" style="width:51.5pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="right" style="text-align:right"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">197,533<o:p></o:p></span></p>
  </td>
  <td width="68" rowspan="2" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="right" style="text-align:right"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">3,157<o:p></o:p></span></p>
  </td>
  <td width="68" rowspan="2" style="width:51.25pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-top-alt:solid windowtext .5pt;mso-border-top-alt:solid windowtext .5pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="right" style="text-align:right"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">9,484<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;mso-border-top-alt:solid windowtext .5pt;
  padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">12.2/17.5/11.6<o:p></o:p></span></p>
  </td>
  <td width="68" style="width:51.25pt;border:none;mso-border-top-alt:solid windowtext .5pt;
  padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">15.6/21.6/15.4<o:p></o:p></span></p>
  </td>
 </tr>
 <tr style="mso-yfti-irow:12;mso-yfti-lastrow:yes">
  <td width="137" colspan="2" style="width:102.5pt;border:none;border-bottom:solid windowtext 1.0pt;
  mso-border-bottom-alt:solid windowtext .5pt;padding:0cm 5.4pt 0cm 5.4pt">
  <p class="MsoNormal" align="center" style="text-align:center"><span lang="EN-US" style="font-size:7.5pt;mso-bidi-font-size:8.0pt">(English/Chinese/French)<o:p></o:p></span></p>
  </td>
 </tr>
</tbody></table>


### Use of the datasets
- The datasets are available in two formats. One is in RDF format, the other is in a custom format similar to the datasets used in [IRN](https://github.com/zmtkeke/IRN/tree/master/PathQuestion).
- All the datasets are in the [datasets](./datasets) directory. For explanation of file naming convensions and our custom format, please refer to this directory for further information.

## Baselines
- We established 3 baseline models of MLPQ.
- The latest baseline combines [**NMN**](https://github.com/StephanieWyt/NMN) and [**UHop**](https://github.com/zychen423/UHop.git) on our latest dataset that have integrated bilingual KGs. It is the one that achieves highest scores on our datasets.
- The other 2 older models use [MTransE](https://github.com/muhaochen/MTransE-tf) and are tested on the 1.0 version of our datasets:
  - **MIRN** is based on the popular multi-hop reasoning model [IRN](https://github.com/zmtkeke/IRN/tree/master).
  - **CL-MKQA** is based on a [multiple KGQA model](https://dl.acm.org/doi/10.5555/3016100.3016335)
- Baseline codes are in the [baselines](baselines) directory. To try these baselines, please refer to this directory for further information.

## Versions and future work

### Version 1.2 update
Recreated the datasets to address the diversity problem and the redundancy problem in the datasets. As a result, we now have fewer questions. Also added a new baseline framework combining NMN and UHop with Bert.
### Version 1.1 update
In this slightly improved version, we corrected many grammatical errors and added the RDF version of all the datasets.

### Current version
- Currently the MLPQ version is `1.2`. We expect to further the work and provide datasets of higher quality and more variety in the future.
- Because the generation of MLPQ is semi-automatic and relies on manually crafted templates and machine translation to some degree, there might be some minor problems in the text. We try to improve the quality of MLPQ by post-editing and there should be very few problems now. However, if you find any errors in the dataset, please contact us, thanks.

### Future work
For now, MLPQ mainly contains 2-hop and 3-hop path questions. In the future, we plan to adopt retelling generation based on web resources to create a greater abundance of question expressions. The path question is merely one subset of complex questions; we also plan to update and augment factoriented complex questions with property information and to explore aggregate-typed complex questions.

## License
This project is licensed under the GPL3 License - see the [LICENSE](LICENSE.txt) file for details
