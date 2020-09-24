import re
rule = re.compile(r'\[(.*?)\]')
rule1=re.compile(r'\<(.*?)\>')
rule2=re.compile(r'\'(.*?)\'')
#find answer:

enKG=[]
zhKG=[]
frKG=[]
zhResourceDic={}
zhPropertyList=[]
enResourceDic={}
enPropertyList=[]
frResourceDic={}
frPropertyList=[]
# ZhEnAlignment={}
# ZhFrAlignment={}
# EnFrAlignment={}
enFile='./data/extracted_en_KG'#'./data/MLPQ_data/MLPQ_EN_ideal'#'./data/extracted_en_KG'
zhFile='./data/extracted_zh_KG'#'./data/MLPQ_data/MLPQ_ZH_ideal'#'./data/extracted_zh_KG'
frFile='./data/extracted_fr_KG'#'./data/MLPQ_data/MLPQ_FR_ideal'#'./data/extracted_fr_KG'
with open(enFile,'r',encoding='utf8')as f:
    for line in f:
        t = line.split('@@@')
        t[2] = t[2][:-1]
        if len(t) == 3:
            tt = (t[0], t[1], t[2])
            enResourceDic[t[0]]=''
            enResourceDic[t[2]]=''
            enPropertyList.append(t[1])
            enKG.append(tt)
with open(zhFile,'r',encoding='utf8')as f:
    for line in f:
        t = line.split('@@@')
        t[2] = t[2][:-1]
        if len(t) == 3:
            tt = (t[0], t[1], t[2])
            zhResourceDic[t[0]] = ''
            zhResourceDic[t[2]] = ''
            zhPropertyList.append(t[1])
            zhKG.append(tt)

with open(frFile,'r',encoding='utf8')as f:
    for line in f:
        t = line.split('@@@')
        t[2] = t[2][:-1]
        if len(t) == 3:
            tt = (t[0], t[1], t[2])
            frResourceDic[t[0]] = ''
            frResourceDic[t[2]] = ''
            frPropertyList.append(t[1])
            frKG.append(tt)

# with open('./data/Ideal/en_zh_predictions.txt', 'r', encoding='UTF-8')as sameAs:
#     for line in sameAs:
#         pair=line.split('&&&')
#         ZhEnAlignment[pair[0]]=pair[1][:-1]
# with open('./data/Ideal/zh_en_predictions.txt', 'r', encoding='UTF-8')as sameAs:
#     for line in sameAs:
#         pair=line.split('&&&')
#         ZhEnAlignment[pair[0]]=pair[1][:-1]
#
# with open('./data/Ideal/fr_zh_predictions.txt', 'r', encoding='UTF-8')as sameAs:
#     for line in sameAs:
#         pair = line.split('&&&')
#         ZhFrAlignment[pair[0]]=pair[1][:-1]
# with open('./data/Ideal/zh_fr_predictions.txt', 'r', encoding='UTF-8')as sameAs:
#     for line in sameAs:
#         pair = line.split('&&&')
#         ZhFrAlignment[pair[0]]=pair[1][:-1]
#
# with open('./data/Ideal/fr_en_predictions.txt', 'r', encoding='UTF-8')as sameAs:
#     for line in sameAs:
#         pair = line.split('&&&')
#         EnFrAlignment[pair[0]]=pair[1][:-1]
# with open('./data/Ideal/en_fr_predictions.txt', 'r', encoding='UTF-8')as sameAs:
#     for line in sameAs:
#         pair = line.split('&&&')
#         EnFrAlignment[pair[0]]=pair[1][:-1]
#top10 alignment
enFralignment={}
frEnalignment={}
enZhalignment={}
zhEnalignment={}
frZhalignment={}
zhFralignment={}
with open('./data/ideal_alignment/en_fr_predictions_hits@10.txt', 'r', encoding='utf-8')as f:
    for line in f:
        dic=line[:-1].split('&&&')
        enFralignment[dic[0]]=dic[1]
with open('./data/ideal_alignment/fr_en_predictions_hits@10.txt', 'r', encoding='utf-8')as f:
    for line in f:
        dic=line[:-1].split('&&&')
        frEnalignment[dic[0]]=dic[1]
with open('./data/ideal_alignment/en_zh_predictions_hits@10.txt', 'r', encoding='utf-8')as f:
    for line in f:
        dic=line[:-1].split('&&&')
        enZhalignment[dic[0]]=dic[1]
with open('./data/ideal_alignment/zh_en_predictions_hits@10.txt', 'r', encoding='utf-8')as f:
    for line in f:
        dic=line[:-1].split('&&&')
        zhEnalignment[dic[0]]=dic[1]
with open('./data/ideal_alignment/fr_zh_predictions_hits@10.txt', 'r', encoding='utf-8')as f:
    for line in f:
        dic=line[:-1].split('&&&')
        frZhalignment[dic[0]]=dic[1]
with open('./data/ideal_alignment/zh_fr_predictions_hits@10.txt', 'r', encoding='utf-8')as f:
    for line in f:
        dic=line[:-1].split('&&&')
        zhFralignment[dic[0]]=dic[1]