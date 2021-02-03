import rdflib
import re
from buildList import *
resourcePrexEn="http://dbpedia.org/resource/"
propertyPrexEn="http://dbpedia.org/property/"
resourcePrexFr="http://fr.dbpedia.org/resource/"
propertyPrexFr="http://fr.dbpedia.org/property/"
resourcePrexZh="http://zh.dbpedia.org/resource/"
propertyPrexZh="http://zh.dbpedia.org/property/"
def buildZhRDF():
    graph = rdflib.Graph()
    for res in zhKG:
        entity1 = rdflib.URIRef(resourcePrexZh+res[0].replace('&',''))
        relation = rdflib.URIRef(propertyPrexZh+res[1].replace('&',''))
        entity2 = rdflib.URIRef(resourcePrexZh+res[2].replace('&',''))
        graph.add((entity1, relation, entity2))
    graph.serialize("Zh_triple.rdf")

def buildFrRDF():
    graph = rdflib.Graph()
    for res in frKG:
        entity1 = rdflib.URIRef(resourcePrexFr+res[0])
        relation = rdflib.URIRef(propertyPrexFr+res[1])
        entity2 = rdflib.URIRef(resourcePrexFr+res[2])
        graph.add((entity1, relation, entity2))
    graph.serialize("Fr_triple.rdf")

def buildEnRDF():
    graph = rdflib.Graph()
    for res in enKG:
        entity1 = rdflib.URIRef(resourcePrexEn+res[0].replace('&',''))
        relation = rdflib.URIRef(propertyPrexEn+res[1].replace('&',''))
        entity2 = rdflib.URIRef(resourcePrexEn+res[2].replace('&',''))
        graph.add((entity1, relation, entity2))
    graph.serialize("En_triple.rdf")

def sparQLSearch(s,v,file):
    rule=re.compile('\'(.*?)\'')
    result=[]
    g = rdflib.Graph()
    g.parse(file, format="xml")
    search = "select "+v+" where{"+s+"}"
    l = list(g.query(search))
    print(l)
    for ll in l:
        filt=rule.findall(str(ll))
        for f in filt:
            result.append(f.split('/')[-1])
    print("search result! ",s,result)
    return result

def sparqlPairSearch(s,v,file):
    rule = re.compile('\'(.*?)\'')
    result = []
    g = rdflib.Graph()
    g.parse(file, format="xml")
    search = "select " + v + " where{" + s + "}"
    l = list(g.query(search))
    print(l)
    for pair in l:
        filtpair=[]
        p0=pair[0].split('/')[-1]
        p1=pair[1].split('/')[-1]
        filtpair.append(p0)
        filtpair.append(p1)
        result.append(filtpair)
    print("search result! ", s, result)
    return result

if __name__=='__main__':
    buildEnRDF()
    # buildZhRDF()
    # buildFrRDF()

