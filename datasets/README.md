
# Datasets
Information about the datasets in this directory. 

The structure of this directory is as follows:

```
📦datasets
 ┣ 📂KGs
 ┃ ┣ 📂fusion_bilingual_KGs
 ┃ ┃ ┣ 📂ILLs_fusion
 ┃ ┃ ┃ ┣ 📜merged_ILLs_KG_en_fr.txt
 ┃ ┃ ┃ ┣ 📜merged_ILLs_KG_en_zh.txt
 ┃ ┃ ┃ ┗ 📜merged_ILLs_KG_zh_fr.txt
 ┃ ┃ ┗ 📂NMN_fusion
 ┃ ┃ ┃ ┣ 📜merged_NMN_KG_en_fr.txt
 ┃ ┃ ┃ ┣ 📜merged_NMN_KG_en_zh.txt
 ┃ ┃ ┃ ┗ 📜merged_NMN_KG_zh_fr.txt
 ┃ ┗ 📂sampled_monolingual_KGs
 ┃ ┃ ┣ 📜Sampled_en.txt
 ┃ ┃ ┣ 📜Sampled_fr.txt
 ┃ ┃ ┗ 📜Sampled_zh.txt
 ┣ 📂Questions
 ┃ ┣ 📂en-fr
 ┃ ┃ ┣ 📂2-hop
 ┃ ┃ ┃ ┣ 📂rdf_version
 ┃ ┃ ┃ ┃ ┣ 📜en_fr_2h_en_question_rdf
 ┃ ┃ ┃ ┃ ┣ 📜en_fr_2h_fr_question_rdf
 ┃ ┃ ┃ ┃ ┗ 📜en_fr_2h_zh_question_rdf
 ┃ ┃ ┃ ┣ 📜en_fr_2h_en_question.txt
 ┃ ┃ ┃ ┣ 📜en_fr_2h_fr_question.txt
 ┃ ┃ ┃ ┗ 📜en_fr_2h_zh_question.txt
 ┃ ┃ ┗ 📂3-hop
 ┃ ┃ ┃ ┣ 📂rdf_version
 ┃ ┃ ┃ ┃ ┣ 📜en_fr_3h_en_question_rdf
 ┃ ┃ ┃ ┃ ┣ 📜en_fr_3h_fr_question_rdf
 ┃ ┃ ┃ ┃ ┗ 📜en_fr_3h_zh_question_rdf
 ┃ ┃ ┃ ┣ 📜en_fr_3h_en_question.txt
 ┃ ┃ ┃ ┣ 📜en_fr_3h_fr_question.txt
 ┃ ┃ ┃ ┗ 📜en_fr_3h_zh_question.txt
 ┃ ┣ 📂en-zh
 ┃ ┃ ┣ 📂2-hop
 ┃ ┃ ┃ ┣ 📂rdf_version
 ┃ ┃ ┃ ┃ ┣ 📜en_zh_2h_en_question_rdf
 ┃ ┃ ┃ ┃ ┣ 📜en_zh_2h_fr_question_rdf
 ┃ ┃ ┃ ┃ ┗ 📜en_zh_2h_zh_question_rdf
 ┃ ┃ ┃ ┣ 📜en_zh_2h_en_question.txt
 ┃ ┃ ┃ ┣ 📜en_zh_2h_fr_question.txt
 ┃ ┃ ┃ ┗ 📜en_zh_2h_zh_question.txt
 ┃ ┃ ┗ 📂3-hop
 ┃ ┃ ┃ ┣ 📂rdf_version
 ┃ ┃ ┃ ┃ ┣ 📜en_zh_3h_en_question_rdf
 ┃ ┃ ┃ ┃ ┣ 📜en_zh_3h_fr_question_rdf
 ┃ ┃ ┃ ┃ ┗ 📜en_zh_3h_zh_question_rdf
 ┃ ┃ ┃ ┣ 📜en_zh_3h_en_question.txt
 ┃ ┃ ┃ ┣ 📜en_zh_3h_fr_question.txt
 ┃ ┃ ┃ ┗ 📜en_zh_3h_zh_question.txt
 ┃ ┗ 📂zh-fr
 ┃ ┃ ┣ 📂2-hop
 ┃ ┃ ┃ ┣ 📂rdf_version
 ┃ ┃ ┃ ┃ ┣ 📜zh_fr_2h_en_question_rdf
 ┃ ┃ ┃ ┃ ┣ 📜zh_fr_2h_fr_question_rdf
 ┃ ┃ ┃ ┃ ┗ 📜zh_fr_2h_zh_question_rdf
 ┃ ┃ ┃ ┣ 📜zh_fr_2h_en_question.txt
 ┃ ┃ ┃ ┣ 📜zh_fr_2h_fr_question.txt
 ┃ ┃ ┃ ┗ 📜zh_fr_2h_zh_question.txt
 ┃ ┃ ┗ 📂3-hop
 ┃ ┃ ┃ ┣ 📂rdf_version
 ┃ ┃ ┃ ┃ ┣ 📜zh_fr_3h_en_question_rdf
 ┃ ┃ ┃ ┃ ┣ 📜zh_fr_3h_fr_question_rdf
 ┃ ┃ ┃ ┃ ┗ 📜zh_fr_3h_zh_question_rdf
 ┃ ┃ ┃ ┣ 📜zh_fr_3h_en_question.txt
 ┃ ┃ ┃ ┣ 📜zh_fr_3h_fr_question.txt
 ┃ ┃ ┃ ┗ 📜zh_fr_3h_zh_question.txt
 ┣ 📂Templates
 ┃ ┣ 📂en
 ┃ ┃ ┣ 📜en_pattern_body_en.txt
 ┃ ┃ ┣ 📜en_pattern_body_fr.txt
 ┃ ┃ ┣ 📜en_pattern_body_zh.txt
 ┃ ┃ ┣ 📜en_pattern_en.txt
 ┃ ┃ ┣ 📜en_pattern_fr.txt
 ┃ ┃ ┗ 📜en_pattern_zh.txt
 ┃ ┣ 📂fr
 ┃ ┃ ┣ 📜fr_pattern_body_en.txt
 ┃ ┃ ┣ 📜fr_pattern_body_fr.txt
 ┃ ┃ ┣ 📜fr_pattern_body_zh.txt
 ┃ ┃ ┣ 📜fr_pattern_en.txt
 ┃ ┃ ┣ 📜fr_pattern_fr.txt
 ┃ ┃ ┗ 📜fr_pattern_zh.txt
 ┃ ┗ 📂zh
 ┃ ┃ ┣ 📜zh_pattern_body_en.txt
 ┃ ┃ ┣ 📜zh_pattern_body_fr.txt
 ┃ ┃ ┣ 📜zh_pattern_body_zh.txt
 ┃ ┃ ┣ 📜zh_pattern_en.txt
 ┃ ┃ ┣ 📜zh_pattern_fr.txt
 ┃ ┃ ┗ 📜zh_pattern_zh.txt
 ┗ 📜README.md
```

  ## [`Questions`](Questions) 
  This directory contains all the parallel questions corresponding to the three bilingual KGs of "en-fr","en-zh" and "zh-fr". 
 - All datasets are categorized by the type of questions into different sub-directories.
 - We name each dataset (text file) by its attributes. For example,  `en_fr_2h_en_question` indicates the following attributes for this dataset:
	- `en_fr` means the triples used to construct this dataset are from the English and French versions of DBPedia.
	- `2h` denotes that this question requires 2-hop reasoning.
	- `en_question` means all the questions are in English.
 - We provide each dataset in two formats, one is the standard RDF-format (in `rdf_version` directories), the other is a CSV-like format (`.txt` files) with the following conventions:
	- Each line is a data record.
	- Each data record can be separated by a first-level separator (a TAB character "`	`") into the text of the question, the answer and the reasoning path.
	- The reasoning path can be separated by a second-level separator ("`#`") into triples.
## [`Templates`](Templates)
This directory contains parallel templates (patterns) for relations in English, Chinese and French, in case you find them useful.
## [`KGs`](KGs)
This directory contains all the KGs used in question generation.
- `sampled_monolingual_KGs` contains the sampled KGs using the ICS approach.
- `fusion_bilingual_KGs` contains bilingual KGs that are created through entity alignments, either with IILs (ground truth) or NMN model predictions.