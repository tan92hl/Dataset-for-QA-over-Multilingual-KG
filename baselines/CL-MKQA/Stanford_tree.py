from stanfordcorenlp import StanfordCoreNLP
from nltk.tree import *


def Clean(line):
    line = line.split(' : ')[1].replace(',\n','')
    line = line.replace('"','')
    return line

def QuestionEextract(filename):
    qlist = []
    allset = []
    qlpair = ['','','']
    paralfile = open('multi_'+filename,'w',encoding='utf-8')
    with open(filename,encoding='utf-8') as f:
        for line in f:
            if '"question" ' in line:
                allset.append(qlist)
                paralfile.write(str(qlist)+'\n',)
                qlist = []
            if '"language"' in line:
                if '' not in qlpair:
                    qlist.append(qlpair)
                qlpair = ['','','']
                qlpair[0] = Clean(line)
            if '"string"' in line:
                qlpair[1] = Clean(line)
            if '"keywords"' in line:
                qlpair[2] = Clean(line)
            
    paralfile.close()
    return allset

def rewrite_Rule(line):
    Rule_list = [['how big','the size of'],
       ['How deep','the depth of'],
       ['How did',''],
       ['How heavy','the weigth of'],
       ['How high','the height of'],
       ['How large','the size of'],
       ['How many','the quantity of'],
       ['How much','the quantity of'],
       ['How often','the frequency of'],
       ['How short','the height of'],
       ['How tall','the height of'],
       ['How long','the length of'],
       ['How','the way of'],

       ['that produces',''],
       ['that were',''],
       ['that won',''],
       ['that',''],
       
       ['What did',''],
       ['What is',''],
       ['What other','the other'],
       ['What was',''],
       ['What',''],

       ['when did','the time'],
       ['when was','the time'],
       ['when were','the time'],
       ['where is','the place of'],
       ['where was','the place of'],
       
       ['In which','the'],
       ['Which american','the one'],
       ['Which ancient','the one'],
       ['Which artistic','the one'],
       ['Which european','the one'],
       ['Which frequent','the one'],
       ['Which military','the one'],
       ['Which','the one'],

       ['Who does','the person'],
       ['Who founded','the person'],
       ['Who has','the person'],
       ['Who is','the person'],
       ['Who was','the person'],
       ['Who were','the person'],
       ['Whom did','the person'],
       ['Who','the person']]
    for rule in  Rule_list:
        line = line.replace(rule[0],rule[1])
    return line


def parse_tree(sentence,nlp):
    sentence = sentence.replace('实体','entity')
    sentence = sentence.replace('entité','entity')
    tree = nlp.parse(sentence)
    #print(tree)
    tree = tree.replace('(','( ')
    tree = tree.replace(')',' )')
    retree = tree.split(' ')
    savenum = {}
    newtree = ''
    for t in retree:
        if t!='' and t!='(' and t!=')' and t!=')\n':
           if t.replace('\n','') not in savenum.keys():
              savenum[t.replace('\n','')] = 1
              if '\n' in t:
                 t = t.replace('\n','') + str(savenum[t.replace('\n','')]) + '\n'
              else:
                 t = t.replace('\n','') + str(savenum[t.replace('\n','')])
           else:
              savenum[t.replace('\n','')] += 1
              if '\n' in t:
                 t = t.replace('\n','') + str(savenum[t.replace('\n','')]) + '\n'
              else:
                 t = t.replace('\n','') + str(savenum[t.replace('\n','')])
        newtree += t + ' '
    newtree = newtree.replace('( ','(')
    newtree = newtree.replace(' )',')')
    print(newtree)
    tree = Tree.fromstring(tree)
    tree = Tree.fromstring(newtree)
    return tree

def MultiTreePaths(root):
    def helper(root, path, res):
        if type(root)==str:
            res.append(path +str(root))
            return
        l=len(root)
        for i in range(l):
                if len(root)>=i:
                    if root[i]:
                        helper(root[i], path +str(root.label()) +'->', res)
    if root is None:
        return []
    l = []
    helper(root, '', l)
    return l

#def Keywords2subtree(keywordslist):  #2 keywords

def FindkeyPath(keywords,pathlist):
    keypath = []
    check = False
    if ' ' in keywords:
       keywords = keywords.split(' ')
       #print(keywords)
       for i in range(len(pathlist)):
           if keywords[-1].lower() in pathlist[i].lower():
              checkpoint = i
              for j in range(len(keywords)-1):
                  if keywords[-1-(j+1)].lower() in pathlist[i-(j+1)].lower():   
                     check = True
                  else:
                     check = False
                     break
       if check:
          for i in range(len(keywords)):
              keypath.append(pathlist[checkpoint-i])
          return keypath
       else:
          for w in keywords:
              kp = FindkeyPath(w,pathlist)
              for p in kp:
                  keypath.append(p)
          return keypath

    else:
       for p in pathlist:
           if keywords.lower() in p.lower():
              keypath.append(p) 
           else:
              pass
       return keypath      

def SaveKeyPath(QALD_9_Train,QALD_9_Test,lan):    
    analysisfile = open('analysis_'+lan+'.txt','w')
    trainset = QuestionEextract('qald-9-train-multilingual.json')[1:]         
    testset = QuestionEextract('qald-9-test-multilingual.json')[1:]   
    mergeset = trainset+testset
    enset = []
    q_extraction_list = []
    for line in mergeset:
        for q in line:
            if lan in q:
                enset.append([q[1],q[2]])
    for line in enset:
        analysisline = ''
        #print(line[0])
        #line[0] = line[0].lower()
        #line[1] = line[1].lower()
        analysisline += line[0] + '\t' + line[1]
        tree = parse_tree(line[0],lan)
        #tree.draw()
        analysisline += str(tree) + '\n'
        line[1] = line[1].replace('\n','')
        keywords = line[1].split(', ')
        #print(keywords)
        pathlist = MultiTreePaths(tree)
        keypath = []
        for keyword in keywords:
            keypath = keypath + FindkeyPath(keyword,pathlist)
        #print(keypath)
        length = []
        splitkeypath = []
        for p in keypath:
            p = p.split('->') 
            splitkeypath.append(p)
            length.append(len(p))
        num = min(length)       
        #print(splitkeypath)
        for i in range(num):
            ifsame = []
            for j in range(len(keypath)):
                if splitkeypath[j][i] not in ifsame:
                   ifsame.append(splitkeypath[j][i])
            if len(ifsame) == 1:
               pass
            else:
               break
        subtreelist = []
        for k in range(len(keypath)):
            subtree = splitkeypath[k][:i+1]
            merge_subtree = ''
            for p in subtree:
                merge_subtree += p+'->'
            if merge_subtree not in subtreelist:
               subtreelist.append(merge_subtree)
        #print(subtreelist)
        analysisline += str(subtreelist) + '\n'
            #subtree_label.append(print(splitkeypath[0][:i]))
        q_extraction = ''
        for path in pathlist:
            for subtree in subtreelist:
                if subtree in path:
                   extraction = path.split('->')[-1]
                   #print(extraction)
                   q_extraction += extraction + ' '
                else:
                   pass
        for i in range(10):
            q_extraction = q_extraction.replace(str(i+1)+' ',' ')
        #print(q_extraction,'\n')
        q_extraction = rewrite_Rule(q_extraction)
        analysisline += q_extraction.replace('  ',' ')+'\n\n'
        q_extraction_list.append(q_extraction)
        print(analysisline)
        analysisfile.write(analysisline,)
        #break
    analysisfile.close()
    return q_extraction_list


def extract_WH(QALD_9_Train,QALD_9_Test,lan):
    trainset = QuestionEextract('qald-9-train-multilingual.json')[1:]         
    testset = QuestionEextract('qald-9-test-multilingual.json')[1:]   
    nlp = StanfordCoreNLP(r'/home/yiming/workspace/program/stanford-corenlp-full-2015-12-09/',lang=lan)
    new = open('WH_.txt','w')
    WH_label = ['WDT','WP','WP$','WRB']
    VB_label = ['VBD','VBZ','JJ','RB']
    mergeset = trainset+testset
    enset = []
    WHlist = []
    for line in mergeset:
        for q in line:
            if lan in q:
                enset.append([q[1],q[2]])
    for line in enset:
        line = (nlp.pos_tag(line[0]))
        for i in range(len(line)):
            if line[i][1] in WH_label:
               if (line[i][1]).lower() not in WHlist:
                  WHlist.append((line[i][0]).lower())
               if line[i+1][1] in VB_label:
                  if (line[i][0]+' '+line[i+1][0]).lower() not in WHlist:
                     WHlist.append((line[i][0]+' '+line[i+1][0]).lower())
    WHlist = (list(set(WHlist))) 
    for W in WHlist:
        new.write(W+'\n',)      
    new.close()   
    return None




'Which people were born in Heraklion '

'''


QALD_9_Train = 'qald-9-train-multilingual.json'
QALD_9_Test = 'qald-9-test-multilingual.json'
lan = 'en'
#lan = 'fr'
q_extraction_list = SaveKeyPath(QALD_9_Train,QALD_9_Test,lan)
for q in q_extraction_list:
    print(q)
    break 
#extract_WH(QALD_9_Train,QALD_9_Test,lan)

test1
line = 'Give me the websites of companies with more than 500000 employees.'
keywords =['website', ' company', ' employee', ' more than 500000']
tree = parse_tree(line,'en')
tree.draw()
print(keywords)
pathlist = MultiTreePaths(tree)
for p in pathlist:
    print(p)
#print(FindkeyPath('Munich',pathlist))
keypath = []
for keyword in keywords:
    keypath = keypath + FindkeyPath(keyword,pathlist)
print(keypath)

test2
line = 'What are the top-10 action role-playing video games according to IGN?'
keywords =['top-10', 'action', 'role-playing games', 'IGN']
tree = parse_tree(line,'en')
#tree.draw()
print(keywords)
pathlist = MultiTreePaths(tree)
keypath = []
print(pathlist)
for keyword in keywords:
    print(FindkeyPath(keyword,pathlist))
 
test3
line = 'Where did Hillel Slovak die?'
keywords =['Hillel Slovak', 'death place']
tree = parse_tree(line,'en')
#tree.draw()
print(keywords)
pathlist = MultiTreePaths(tree)
keypath = []
print(pathlist)
for keyword in keywords:
    print(FindkeyPath(keyword,pathlist))

for line in open('QALD-9_en_Question.txt').readlines():
    tree = parse_tree(line,'en')
    pathlist = MultiTreePaths(tree)
    keypath = []
    for keyword in keywords:
        keypath = keypath + FindkeyPath(keyword,pathlist)
    print(keypath)
    break
 
What are the five boroughs of New York? five boroughs, New York


        for subtree in subtreelist:
            for path in pathlist:
                if subtree in path:
                   extraction = path.split('->')[-1]
                   #print(extraction)
                   q_extraction += extraction + ' '
                else:
                   pass

(ROOT
  (S
    (VP (VB List)
      (NP (DT all) (NNS boardgames))
      (PP (IN by)
        (NP (NNP GMT))))
    (. .)))

line = 'What are the five boroughs of New York?'
keywords = ['five boroughs', 'New York']

tree = parse_tree(line,'en')
pathlist = MultiTreePaths(tree)
keypath = []
#print(pathlist)
for keyword in keywords:
    keypath = keypath + FindkeyPath(keyword,pathlist)
print(keypath)
print(tree.productions())
tree.draw()
'''
nlp = StanfordCoreNLP(r'./stanfordParser/stanford-corenlp-full-2015-12-09',lang='fr')
q="é"
parse_tree(q,nlp)