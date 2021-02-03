
class ResourceData:
    def __init__(self,resource,confidence,frequency,type):
        self.resouce=resource
        self.confidence=confidence
        self.frequency=frequency
        self.type=type#0En；1Zh；2Fr
    def __eq__(self, other):
        return self.resouce==other.resouce and self.type==other.type
    def __str__(self):
        return self.resouce+str(self.type)
    def print(self):
        print(self.resouce, self.confidence, self.frequency,self.type)

class TripleData:
    def __init__(self,list,query,t):
        self.resource=[]
        for l in list:
            self.resource.append(l)
        self.tripleQuery=query
        self.calculateWeight()
        self.type=t#0En 1Zh 2Fr
        self.classify='triple'
        self.alignment=[]
        self.answer=[]
        self.answerType=''
        self.pairanswer=[]
        self.leftalignment = []
        self.rightalignment =[]
        self.pairalignment=[]
        self.lanswer=[]
        self.ranswer=[]

    def __eq__(self, other):
        return self.tripleQuery==other.tripleQuery


    def setanswer(self,a,type):
        self.answerType=type
        if type==0:
            self.ranswer=a
        if type==1:
            self.lanswer=a
        if type==2:
            self.pairanswer=a
            for an in a:
                self.lanswer.append(an[0])
                self.ranswer.append(an[1])
                self.answer.append(an[0])
                self.answer.append(an[1])


    def print(self):
        print(self.classify+str(len(self.resource))+self.tripleQuery)
        # if self.answerType==2:
        #     print('R!:leftalign:',len(self.leftalignment))
        #     for j in self.leftalignment:
        #         print(j)
        #     print('right :',len(self.rightalignment))
        #     for k in self.rightalignment:
        #         print(k)
        # else:
        #     print(self.answer)
    def addalignment(self,a):
        for al in self.alignment:
            if a.sameLeft==al.sameLeft:
                return
        self.alignment.append(a)
    def calculateWeight(self):
        c=0
        i=0
        for t in self.resource:
            i=i+1
            c=c+t.confidence+t.frequency
        self.weight=c/i

    def con5(self):
        for a in self.pairanswer:
            for la in self.leftalignment:
                for ra in self.rightalignment:
                    if (a[0]==la.sameLeft or a[0]==la.sameRight) and (a[1]==ra.sameLeft or a[1]==ra.sameRight):
                        self.pairalignment.append((la,ra))




class AlignmentData:
    def __init__(self,sameL,sameR,con):
        self.sameLeft=sameL
        self.sameRight=sameR
        self.confidence=con
        self.classify='alignment'
        self.leftTriple=set()
        self.rightTriple=set()

    def __eq__(self, other):
        return (self.sameLeft==other.sameLeft and self.sameRight==other.sameRight)or(self.sameLeft==other.sameRight and self.sameRight==other.sameLeft)
    def __str__(self):
        return self.sameLeft+self.sameRight
    def print(self):
        print(self.sameLeft+" sameas "+self.sameRight)
        # print('lefttriple:')
        # for i in self.leftTriple:
        #     print(i)
        # print('righttriple')
        # for j in self.rightTriple:
        #     print(j)

if __name__=="__main__":
    a=set()
    b=ResourceData("English",0.5,2)
    i=ResourceData("English",0.5,2)
    a.add(b)
    a.add(i)
    for c in a:
        c.print()