import time
import Levenshtein
from buildList import *
from ResourceData import *
from SparqlSearch import *
from gurobipy import *

questionFile='./data/MLPQ/question/en-zh/2-hop/r2r_en_zh_question_en'
phraseFile='./phrase/en-zh/2-hop/r2r_en_zh_question_en_phrase'
outputFile='./output/en-zh/3-hop/r2r_en_en_zh_question_en_output'
resourcePrexEn = "http://dbpedia.org/resource/"
propertyPrexEn = "http://dbpedia.org/property/"
resourcePrexFr="http://fr.dbpedia.org/resource/"
propertyPrexFr="http://fr.dbpedia.org/property/"
resourcePrexZh = "http://zh.dbpedia.org/resource/"
propertyPrexZh = "http://zh.dbpedia.org/property/"
EnRDF = "En_triple.rdf"
ZhRDF = "Zh_triple.rdf"
FrRDF="Fr_triple.rdf"
ThresHold = 0.84
zhThresHold=0.8
sparqlSearch = SparqlSearch()
phraseList=[]
questionList=[]
answerList=[]



def buildQAList():
    with open(questionFile, 'r', encoding='utf-8')as f:
        for line in f:
            line = line.split('\t')
            q=line[0]
            if q[-1]=='?':
                q=q[:-1]
            questionList.append(q)
            answer = line[1].split('@@@')
            if len(answer)>6:
                an = [answer[0], answer[1], answer[3], answer[5]]  # 3hop
            else:
                an=[answer[0],answer[1],answer[3]]#2hop
            answerList.append(an)

def buildPhrase():
    with open(phraseFile, 'r', encoding='utf-8')as f:
        for line in f:
            line=line[:-1]
            line=line.replace('bitrh','birth')
            p=line.split('###')[1]
            phrase=p.split('@@@')
            phraseList.append(phrase)

def analysisQuestion(question,phrase):
    if question[-1]=='?':
        question=question[:-1]
    #print('analyzing...')
    #print(phrase)
    candidateResource = []
    candidateProperty = []
    p=phrase[-1]
    if p in enResourceDic:
        candidateResource.append(ResourceData(p, 1, 1, 0))
    if p in zhResourceDic:
        candidateResource.append(ResourceData(p, 1, 1, 1))
    if p in frResourceDic:
        candidateResource.append(ResourceData(p, 1, 1, 2))
    parse = []
    seg = set()
    for ph in phrase[:-1]:
        if '&' in ph:
            p = ph.split('&')
            parse.append((p[0].replace(' ', ''), p[1].replace(' ', '')))
            seg.add(p[0].replace(' ', ''))
    samePhrase = []
    for s in seg:
        num = 0
        same = []
        for ph in parse:
            if ph == '':
                continue
            if ph[0] == s:
                for pro in enPropertyList:
                    con = Levenshtein.ratio(pro, ph[1])
                    if con > ThresHold:
                        new = ResourceData(pro, con, 1, 0)
                        candidateProperty.append(new)
                        same.append(new)
                        num += 1
                for pro in zhPropertyList:
                    con = Levenshtein.ratio(pro, ph[1])
                    if con > zhThresHold:
                        new = ResourceData(pro, con, 1, 1)
                        candidateProperty.append(new)
                        same.append(new)
                        num += 1
                for pro in frPropertyList:
                    con = Levenshtein.ratio(pro, ph[1])
                    if con > ThresHold:
                        new = ResourceData(pro, con, 1, 2)
                        candidateProperty.append(new)
                        same.append(new)
                        num += 1
            if num > 1:
                samePhrase.append(same)

    cr=[]
    cp=[]

    for c in candidateResource:
        f=0
        for i in cr:
            if i==c:
                f=1
        if f==1:
            continue
        else:
            cr.append(c)
    for c in candidateProperty:
        f = 0
        for i in cp:
            if i == c:
                f = 1
        if f == 1:
            continue
        else:
            cp.append(c)
    candidate = [cr, cp]
    sameP=[]
    for s in samePhrase:
        sset=[]
        for c in s:
            f=0
            for i in sset:
                if i==c:
                    f=1
            if f==1:
                continue
            else:
                sset.append(c)
        sameP.append(sset)
    #print('------resource analyze!------')
    # for i in cr:
    #     i.print()
    #print('-----property----')
    # for i in cp:
    #     i.print()
    # print('analyzing done!')
    # print('---------same phrase--------')
    # for i in sameP:
    #     print('same:')
    #     for s in i:
    #         print(str(s))
    return sameP, candidate

def generateTriple(samePharse, candidate):
    res = candidate[0]
    pro = candidate[1]
    #print('len pro ' + str(len(pro)))
    erEnTriple = []
    erZhTriple = []
    erFrTriple=[]
    erTriple = []
    for tri in enKG:
        for en in res:
            if en.type==0:
                if en.resouce==tri[0]:
                    for p in pro:
                        if p.type==0 and p.resouce==tri[1]:
                            triple = '<' + resourcePrexEn + en.resouce + '> <' + propertyPrexEn + p.resouce + "> ?V2"
                            erEnTriple.append(TripleData([en, p], triple,0))
                if en.resouce==tri[1]:
                    for p in pro:
                        if p.type==0 and p.resouce==tri[1]:
                            triple = "?V1 <" + propertyPrexEn + p.resouce + "> <" + resourcePrexEn + en.resouce + '>'
                            erEnTriple.append(TripleData([en, p], triple,0))
        for p in pro:
            if p.type==0 and p.resouce==tri[1]:
                triple = "?V1 <" + propertyPrexEn + p.resouce + "> ?V2"
                erEnTriple.append(TripleData([p], triple,0))
    for tri in zhKG:
        for en in res:
            if en.type==1:
                if en.resouce==tri[0]:
                    for p in pro:
                        if p.type==1 and p.resouce==tri[1]:
                            triple = '<' + resourcePrexZh + en.resouce + '> <' + propertyPrexZh + p.resouce + "> ?V2"
                            erZhTriple.append(TripleData([en, p], triple,1))
                if en.resouce==tri[1]:
                    for p in pro:
                        if p.type==1 and p.resouce==tri[1]:
                            triple = "?V1 <" + propertyPrexZh + p.resouce + "> <" + resourcePrexZh + en.resouce + '>'
                            erZhTriple.append(TripleData([en, p], triple,1))
        for p in pro:
            if p.type==1 and p.resouce==tri[1]:
                triple = "?V1 <" + propertyPrexZh + p.resouce + "> ?V2"
                erZhTriple.append(TripleData([p], triple,1))
    for tri in frKG:
        for en in res:
            if en.type == 2:
                if en.resouce == tri[0]:
                    for p in pro:
                        if p.type == 2 and p.resouce == tri[1]:
                            triple = '<' + resourcePrexFr + en.resouce + '> <' + propertyPrexFr + p.resouce + "> ?V2"
                            erFrTriple.append(TripleData([en, p], triple,2))
                if en.resouce == tri[1]:
                    for p in pro:
                        if p.type == 2 and p.resouce == tri[1]:
                            triple = "?V1 <" + propertyPrexFr + p.resouce + "> <" + resourcePrexFr + en.resouce + '>'
                            erFrTriple.append(TripleData([en, p], triple,2))
        for p in pro:
            if p.type == 2 and p.resouce == tri[1]:
                triple = "?V1 <" + propertyPrexFr + p.resouce + "> ?V2"
                erFrTriple.append(TripleData([p], triple,2))
    erEn=[]
    erFr=[]
    erZh=[]
    for c in erEnTriple:
        f=0
        for i in erEn:
            if i==c:
                f=1
        if f==1:
            continue
        else:
            erEn.append(c)
    for c in erFrTriple:
        f=0
        for i in erFr:
            if i==c:
                f=1
        if f==1:
            continue
        else:
            erFr.append(c)
    for c in erZhTriple:
        f=0
        for i in erZh:
            if i==c:
                f=1
        if f==1:
            continue
        else:
            erZh.append(c)

    erTriple = [erEn, erZh,erFr]
    # print('-=====en3:====')
    # for i in erEn:
    #     i.print()
    # print('------zh3----')
    # for i in erZh:
    #     i.print()
    # print('-------Fr-------')
    # for i in erFr:
    #     i.print()
    Con1 = addSameTriple(erTriple, samePharse)
    return erTriple, Con1

def addSameTriple(ert, SP):
    Con1Set = []
    for sp in SP:
        s = []
        for res in sp:
            for tr in ert[0]:
                for trres in tr.resource:
                    if res.resouce == trres.resouce and trres.type == res.type:
                        s.append(tr)
            for tr in ert[1]:
                for trres in tr.resource:
                    if res.resouce == trres.resouce and trres.type == res.type:
                        s.append(tr)
            for tr in ert[2]:
                for trres in tr.resource:
                    if res.resouce == trres.resouce and trres.type == res.type:
                        s.append(tr)
        Con1Set.append(s)
    return Con1Set


def alignmentByTable(erTriple):
    #print('alignmrnt')
    same = []
    Con4 = []
    #print('searching...')
    for t in erTriple[0]:  # English Triple
        # print(t)
        s = ''
        if t.tripleQuery[0] == '<':  # judge the type of triple
            s = sparqlSearch.search(t.tripleQuery, "?V2", 0)
            if len(s) == 0:
                continue
            t.setanswer(s, 0)
        elif t.tripleQuery[-1] != '2':
            s = sparqlSearch.search(t.tripleQuery, "?V1", 0)
            if len(s) == 0:
                continue
            t.setanswer(s, 1)
        else:
            s = sparqlSearch.searchPair(t.tripleQuery, "?V1?V2", 0)
            if len(s) == 0:
                continue
            t.setanswer(s, 2)

    for t in erTriple[1]:  # Chinese Triple
        if t.tripleQuery[0] == '<':  # judge the type of triple
            s = sparqlSearch.search(t.tripleQuery, "?V2", 1)
            if len(s) == 0:
                continue
            t.setanswer(s, 0)
        elif t.tripleQuery[-1] != '2':
            s = sparqlSearch.search(t.tripleQuery, "?V1", 1)
            if len(s) == 0:
                continue
            t.setanswer(s, 1)
        else:
            s = sparqlSearch.searchPair(t.tripleQuery, '?V1?V2', 1)
            if len(s) == 0:
                continue
            t.setanswer(s, 2)

    for t in erTriple[2]:  # Fr Triple
        if t.tripleQuery[0] == '<':  # judge the type of triple
            s = sparqlSearch.search(t.tripleQuery, "?V2", 2)
            if len(s) == 0:
                continue
            t.setanswer(s, 0)
        elif t.tripleQuery[-1] != '2':
            s = sparqlSearch.search(t.tripleQuery, "?V1", 2)
            if len(s) == 0:
                continue
            t.setanswer(s, 1)
        else:
            s = sparqlSearch.searchPair(t.tripleQuery, '?V1?V2', 2)
            if len(s) == 0:
                continue
            t.setanswer(s, 2)
    #print('search done')
    totalTriple = erTriple[0] + erTriple[1] + erTriple[2]
    leftAnswer={}
    rightAnswer={}
    for tri in totalTriple:
        if len(tri.lanswer)!=0:
            for a in tri.lanswer:
                leftAnswer[a]=''
        if len(tri.ranswer)!=0:
            for a in tri.ranswer:
                rightAnswer[a]=''
    #build alignment
    for r in rightAnswer:
        if r in leftAnswer:
            a = AlignmentData(r, r, 1)
            f = 0
            for s in same:
                if s == a:
                    f = 1
            if f == 0:
                same.append(a)
        if r in zhEnalignment:
            ralign=zhEnalignment[r]
            ralign=ralign.split('\t')
            for ra in ralign:
                a=None
                if '$$$$$' in ralign:
                    right=ra.split('$$$$$')
                    if right[0]+'$$' in leftAnswer:
                        a = AlignmentData(r,right[0]+'$$',float(right[1]))
                        f = 0
                        for s in same:
                            if s == a:
                                f = 1
                        if f == 0:
                            same.append(a)
                else:
                    right = ra.split('$$$')
                    if right[0] in leftAnswer:
                        a = AlignmentData(r, right[0], float(right[1]))
                        f = 0
                        for s in same:
                            if s == a:
                                f = 1
                        if f == 0:
                            same.append(a)
        if r in enZhalignment:
            ralign=enZhalignment[r]
            ralign=ralign.split('\t')
            for ra in ralign:
                if '$$$$$' in ralign:
                    right=ra.split('$$$$$')
                    if right[0]+'$$' in leftAnswer:
                        a = AlignmentData(r,right[0]+'$$',float(right[1]))
                        f = 0
                        for s in same:
                            if s == a:
                                f = 1
                        if f == 0:
                            same.append(a)
                else:
                    right = ra.split('$$$')
                    if right[0] in leftAnswer:
                        a = AlignmentData(r, right[0], float(right[1]))
                        f = 0
                        for s in same:
                            if s == a:
                                f = 1
                        if f == 0:
                            same.append(a)
    #add triple
    for s in same:
        for tri in totalTriple:
            if s.sameLeft in tri.ranswer:
                s.leftTriple.add(tri.tripleQuery)
            if s.sameRight in tri.lanswer:
                s.rightTriple.add(tri.tripleQuery)
    #con4:
    # for tri in totalTriple:
    #     for s in same:
    #         if s.sameLeft in tri.ranswer:
    #             tri.rightalignment.append(s)
    #         if s.sameRight in tri.lanswer:
    #             tri.leftalignment.append(s)
    for tri in totalTriple:
        num0 = 0
        num1 = 0
        con40 = []
        con41 = []
        for s in same:
            if s.sameLeft in tri.ranswer:
                con40.append(s)
                num0 += 1
            if s.sameRight in tri.lanswer:
                con41.append(s)
                num1 += 1
        if num0 > 1:
            Con4.append(con40)
        if num1 > 1:
            Con4.append(con41)
    result = [list(totalTriple), list(same)]
    # print("alignmnet Done")
    # for i in same:
    #     i.print()
    # print('----Con4---')
    # for i in Con4:
    #     print('con4')
    #     for ii in i:
    #         print(str(ii))

    return result, Con4

def ILPByGurobi(result, Con1Set, Con4):
    triple = result[0]
    alignment = result[1]
    # construct weight array
    tripleLength = len(triple)
    alignmentLength = len(alignment)
    #print('length', tripleLength, alignmentLength)
    tripleWeight = []
    alignmentWeight = []
    tripleCover = []
    for t in triple:
        t.calculateWeight()
        tripleWeight.append(t.weight)
        tripleCover.append(len(t.resource))
    for a in alignment:
        alignmentWeight.append(a.confidence)
    #print('construct the constraint set')
    Same = []
    # Contraint1:
    if len(Con1Set) != 0:
        for s in Con1Set:
            subcon = [0] * tripleLength
            for t in s:
                for index, tr in enumerate(triple):
                    if t.tripleQuery == tr.tripleQuery:
                        subcon[index] = 1
            Same.append(subcon)
    else:
        Same.append([0] * tripleLength)
    # Constraint2
    ER = []
    for t in triple:
        if len(t.resource) == 2:
            ER.append(1)
        else:
            ER.append(0)
    # Constraint3
    AliLeft = []
    AliRight = []
    for a in alignment:
        left = [0] * tripleLength
        right = [0] * tripleLength
        for index, tr in enumerate(triple):
            for at in a.leftTriple:
                if tr.tripleQuery == at:
                    left[index] = 1
            for at in a.rightTriple:
                if tr.tripleQuery == at:
                    right[index] = 1
        AliLeft.append(left)
        AliRight.append(right)
    # print('-----alignment left-----')
    # for i in AliLeft:
    #     print(i)
    # print('------alignment right------')
    # for i in AliRight:
    #     print(i)
    # Constraint4:
    SameAli = []
    for c in Con4:
        con4 = [0] * alignmentLength
        for index, a in enumerate(alignment):
            for ca in c:
                if ca.leftTriple == a.leftTriple:
                    con4[index] = 1
        SameAli.append(con4)
    #Constraint5:
    ConflictAli = []
    for t in triple:  # 情况一：对于一个resource不能对应多个alignment
        if t.answerType == 2:
            con5 = [0] * alignmentLength
            for index, a in enumerate(alignment):
                for ta in t.leftalignment:
                    if a.sameLeft == ta[0]:
                        con5[index] = 1
            ConflictAli.append(con5)

            con5 = [0] * alignmentLength
            for index, a in enumerate(alignment):
                for ta in t.rightalignment:
                    if a.sameLeft == ta[0]:
                        con5[index] = 1
            ConflictAli.append(con5)

            # 情况二：对齐导致不存在三元组
            t.con5()
            for pa in t.pairalignment:
                con5 = [1] * alignmentLength
                for index, a in enumerate(alignment):
                    if a.sameLeft == pa[0][0] or a.sameLeft == pa[0][1] or a.sameRight == pa[1][0] or a.sameRight == \
                            pa[1][1]:
                        con5[index] = 0
                ConflictAli.append(con5)
        else:
            con5 = [0] * alignmentLength
            for index, a in enumerate(alignment):
                for ta in t.alignment:
                    if a.sameLeft == ta[0]:
                        con5[index] = 1
            ConflictAli.append(con5)
    # Gurobi
    #print('gurobi begin!')
    m = Model('ILP')
    finalTriple = m.addVars(tripleLength, vtype=GRB.BINARY, name="finalTriple")
    finalAlignment = m.addVars(alignmentLength, vtype=GRB.BINARY, name="finalAlignment")
    m.setObjective(sum(finalTriple[i] * tripleWeight[i] for i in range(tripleLength)) + sum(
        finalAlignment[i] * alignmentWeight[i] for i in range(alignmentLength)) + sum(
        finalTriple[i] * tripleCover[i] for i in range(tripleLength)), GRB.MAXIMIZE)
    for i in range(len(Same)):
        m.addConstr((sum(finalTriple[j] * Same[i][j] for j in range(tripleLength)) <= 1),
                    'con1_' + str(i))  # constraint1
    m.addConstr(sum(finalTriple[i] * ER[i] for i in range(tripleLength)) >= 1, 'con2')  # constraint2
    for i in range(alignmentLength):
        m.addConstr((sum(finalTriple[j] * AliLeft[i][j] for j in range(tripleLength))) * finalAlignment[i] >= 1 *
                    finalAlignment[i], 'con3l_' + str(i))  # constraint3
        m.addConstr((sum(finalTriple[j] * AliRight[i][j] for j in range(tripleLength))) * finalAlignment[i] >= 1 *
                    finalAlignment[i], 'con3r_' + str(i))
    # for i in range(tripleLength):
    #     m.addConstr((sum(finalAlignment[j] * Con4left[i][j] for j in range(alignmentLength))) * finalTriple[i] <= 1 *
    #                 finalTriple[i], 'con4l_' + str(i))  # constraint3
    #     m.addConstr((sum(finalAlignment[j] * Con4Right[i][j] for j in range(alignmentLength))) * finalTriple[i] <= 1 *
    #                 finalTriple[i], 'con42_' + str(i))

    for i in range(len(SameAli)):
        m.addConstr(quicksum(finalAlignment[j] * SameAli[i][j] for j in range(alignmentLength)) <= 1,
                    'con4_' + str(i))  # constraint4
    for i in range(len(ConflictAli)):
        m.addConstr(quicksum(finalAlignment[j] * ConflictAli[i][j] for j in range(alignmentLength)) <= 1,
                    'con5_' + str(i))  # constraint5
    #print('gurobi optimize!')
    #m.write('msqa.lp')
    start = time.time()
    m.optimize()
    #print('optimize done!')
    end = time.time()
    status = m.Status
    if status == GRB.Status.INF_OR_UNBD or status == GRB.Status.INFEASIBLE or status == GRB.Status.UNBOUNDED:
        ##print('infeasible modle')
        return (-1, [])
    if status != GRB.Status.OPTIMAL:
       # print('stop with status', str(status))
        return (0, [])
    # for i in m.getVars():
    #     print(i.varName, i.x)
    finalQuery = []
    for i in range(tripleLength):
        if finalTriple[i].x == 1:
            finalQuery.append(triple[i])
            # print('triplechose',i)
    for i in range(alignmentLength):
        if finalAlignment[i].x == 1:
            finalQuery.append(alignment[i])
            # print('alichose',i)
            # print('alignmentlink:',AliLeft[i],AliRight[i])
            # alignment[i].print()
    #print(str(end - start))
    return 1, finalQuery


class QA:
    def __init__(self, question,phrase):
        self.question = question
        self.phrase=phrase

    def FindAnswer(self):
        samePharse, candidate = analysisQuestion(self.question,self.phrase)
        erTriple, Con1 = generateTriple(samePharse, candidate)
        result, Con4 = alignmentByTable(erTriple)
        # for s in result[0]:
        #     s.print()
        # for s in result[1]:
        #     s.print()
        status, finalQuery = ILPByGurobi(result, Con1, Con4)
        #print('final query!', status)
        if status == -1 or status == 0:
            #print('answer failed')
            return [], candidate
        #print('len', len(finalQuery))
        answerPath=[]
        for i in finalQuery:
            if i.classify=='triple':
                for r in i.resource:
                    answerPath.append(r.resouce)
            # if i.classify=='alignment':
            #     answerPath.append(i.sameRight)
            #     answerPath.append(i.sameLeft)
            #i.print()
        print(answerPath)
        return answerPath, candidate


if __name__ == '__main__':
    buildPhrase()
    buildQAList()
    for i in range(0,len(questionList)):
        start=time.time()
        q=QA(questionList[i],phraseList[i])
        answer, candidate = q.FindAnswer()
        end=time.time()
        rec=[]
        for can in candidate:
            for c in can:
                rec.append(str(c))
        answerCorrect=answerList[i]
        result=0
        if set(answer)==set(answerCorrect):
            result=1
        if i%1000==0:
            print(i)
        print(end-start)
        with open(outputFile,'a',encoding='utf-8')as f:
            f.write(str(result)+'@@@'+'#'.join(rec)+'@@@'+'#'.join(answer)+'@@@'+'#'.join(answerCorrect)+'\n')

