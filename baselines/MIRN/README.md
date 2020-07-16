# MIRN
Multilingual version of IRN with MTransE's alignment method, used for cross-lingual KBQA.

## Environment(Using anaconda will make this easier)：
* Python 3.X 
    * Tensorflow-gpu 1.X (like 1.14, but not 2.0)
    * Scikit-learn
    * Jieba

## Training:
python train.py --dataset FR_fr_zh_fr
## Testing:
python test.py --dataset FR_fr_zh_fr
