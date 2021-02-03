from buildList import *
from langconv import *
from buildList import *
enPhraseList=[]
frPhraseList=[]
zhParseList=[]
zh2EnPhrase=[]
fr2EnPhrase=[]
enZhDic=[]
enFrDic=[]
pattern = re.compile(r'[\u4e00-\u9fa5]')
with open('./data/MLPQ/templates/fr/fr_Single_hop_template_phrase', 'r', encoding='utf-8')as f:
    for line in f:
        if line == '\t\n':
            continue
        if line[-1] == '\n':
            line = line[:-1]
        phrase = line.split('\t')[1]
        index = phrase.find('entity')
        phrase = phrase[:index]
        phrase = phrase.rstrip(' ')
        phrase = phrase.lstrip(' ')
        if phrase[:2] == 'l':
            phrase = phrase[2:]
        if phrase[-2:] == "l'":
            phrase = phrase[:-3]
        if phrase[-2:] == 'de':
            phrase = phrase[:-3]
        frPhraseList.append(phrase)
with open('./data/MLPQ/templates/zh/zh_Single_hop_template_phrase', 'r', encoding='utf-8')as f:
    for line in f:
        if line == '\t\n':
            continue
        if line[-1] == '\n':
            line = line[:-1]
        parse = line.split('\t')[1]
        phrase = parse.replace(' ', '')
        if 'entity的' in phrase:
            phrase = phrase[phrase.find('entity的') + 7:]
        elif 'entity所属的' in phrase:
            phrase = phrase[phrase.find('entity所属的') + 9:]
        elif 'entity所属于的' in phrase:
            phrase = phrase[phrase.find('entity所属于的') + 10:]
        elif 'entity使用的' in phrase:
            phrase = phrase[phrase.find('entity使用的') + 9:]
        elif 'entity所属' in phrase:
            phrase = phrase[phrase.find('entity所属') + 9:]
        else:
            ph = phrase.find('entity')
            if ph < len(phrase) - ph - 6:
                phrase = phrase[ph + 6:]
            else:
                phrase = phrase[:ph]
        zhParseList.append(phrase)
def buildParserList(parseFile,plist):
    with open(parseFile, 'r', encoding='utf-8')as f:
        for line in f:
            if line=='\t\n':
                continue
            if line[-1]=='\n':
                line=line[:-1]
            phrase = line.split('\t')[1]
            if ' that' in phrase:
                phrase = phrase[:phrase.find(' that ')]
            elif 'of entity' in phrase:
                phrase = phrase[:phrase.find('of entity')]
            elif "of the entity" in phrase:
                phrase = phrase[:phrase.find('of the entity')]
            elif "entity's" in phrase:
                phrase = phrase[phrase.find("entity's") + 8:]
            else:
                f = phrase.find('entity')
                if f < len(phrase) - f - 6:
                    phrase = phrase[f + 6:]
                else:
                    phrase = phrase[:f]
            plist.append(phrase)
def findPredict(question):
    entity = ''
    result = []
    ques = question.split(' ')
    for q in ques:
        if q[-2:] == '\'s':
            q = q[:-2]
        if q in enResourceDic or q in zhResourceDic or q in frResourceDic:
            entity = q
    if entity == '':
        print('No entity! ' + question)
        ens = []
        for zh in enResourceDic:
            if zh in question:
                ens.append(zh)
        for zh in zhResourceDic:
            if zh in question:
                ens.append(zh)
        # for zh in frResourceDic:
        #     if zh in question:
        #         ens.append(zh)
        max = ''
        for e in ens:
            if len(e) > len(max):
                max = e
        entity = max
    for p in enPhraseList:
        if p!='' and len(p.replace(' ',''))>1 and p in question:
            p1 = ' ' + p + ' '
            p1 = p1.replace(' the ', ' ')
            p1 = p1.replace(' where ', ' ')
            p1 = p1.replace(' there ', ' ')
            p1 = p1.replace(' is ', ' ')
            p1 = p1.replace('bitrh', 'birth')
            p1 = p1.replace(' ', '')
            result.append(p+'&'+p1)
    for p in enFrDic:
        if p!='' and len(p.replace(' ',''))>1 and p in question:
            pFr = ' ' + enFrDic[p]
            pFr = pFr.replace(' le ', '')
            pFr = pFr.replace(' la ', '')
            pFr = pFr.replace(' Quelle ', '')
            pFr = pFr.replace(' Quel ', '')
            pFr = pFr.replace(' ', '')
            result.append(p + '&' +pFr )
    for p in enZhDic:
        if p!='' and len(p.replace(' ',''))>1 and p in question:
            zh=enZhDic[p]
            zh = zh.replace(' ', '')
            zh = zh.replace('所属的', '')
            zh = Converter('zh-hant').convert(zh)
            result.append(p + '&' +zh )
    result = list(set(result))
    result.append(entity)
    return result
def parseEnQuestion(qFile,pFile):
    questionList=[]
    with open(qFile,'r',encoding='utf-8')as f:
        for line in f:
            if line=='\t\n':
                continue
            q=line.split('\t')[0]
            if q[-1]=='?' or q[-1]=='？':
                q=q[:-1]
            questionList.append(q)
    for i in range(0,len(questionList)):
        questionList[i]=questionList[i].replace('bitrh','birth')
        phrase=findPredict(questionList[i])
        print(phrase)
        with open(pFile, 'a', encoding='utf-8')as file:
            file.write(questionList[i]+'###'+'@@@'.join(phrase)+'\n')
buildParserList('./data/MLPQ/templates/en/en_Single_hop_template_phrase',enPhraseList)
buildParserList('./data/MLPQ/templates/zh/zh_Single_hop_template(Google_translation_en)_phrase',zh2EnPhrase)
buildParserList('./data/MLPQ/templates/fr/fr_Single_hop_template(Google_translation_en)_phrase',fr2EnPhrase)
enZhDic=dict(zip(zh2EnPhrase,zhParseList))
enFrDic=dict(zip(fr2EnPhrase,frPhraseList))
prexQ='./data/MLPQ/question/'
prexP='./phrase/'
p=['en-zh/2-hop/r2r_en_zh_question_en','en-zh/2-hop/r2r_zh_en_question_en','en-zh/3-hop/r2r_en_en_zh_question_en','en-zh/3-hop/r2r_en_zh_en_question_en','en-zh/3-hop/r2r_zh_en_en_question_en']
q=['en-zh/2-hop/r2r_en_zh_question_en_phrase','en-zh/2-hop/r2r_zh_en_question_en_phrase','en-zh/3-hop/r2r_en_en_zh_question_en_phrase','en-zh/3-hop/r2r_en_zh_en_question_en_phrase','en-zh/3-hop/r2r_zh_en_en_question_en_phrase']
for i in range(0,len(p)):
    print(p[i])
    parseEnQuestion(prexQ+p[i],prexP+q[i])
