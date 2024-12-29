import csv
import sys
import requests
from operator import index


c=0
pl=0
al=0
bro=0
nar=0
rel=0
ner=0
inc=0
ner_stats={}
filename=sys.argv[1]

with open("results/"+filename) as fp:
    line = fp.readline()
    while line:
        linea=line.strip()
        if linea.isdigit():
            id=linea
            c+=1
            line=fp.readline()
            linea=line.strip()
            if "prefLabel" not in linea:
                inc+=1
                print(id)
            else:
                pl+=1
        if "altLabel" in linea: al+=1
        if "related" in linea: rel+=1
        if "broader" in linea: bro+=1
        if "narrower" in linea: nar+=1
        if "NER : " in linea:
            ner+=1
            types=linea.split("  --- TYPE : (")[1].replace(")","").split(" ")
            for t in types:
                if t not in ner_stats:
                    ner_stats[t]={"num":1}
                else:
                    ner_stats[t]["num"]+=1
        line = fp.readline()
    fp.close()
print("Número de conceptos: "+str(c)+"\nNúmero prefLabel: "+str(pl)+"\nNúmero altLabel: "+str(al)+"\nIncoherencias etiquetado prefLabel altLabel: "+str(inc)+"\nRelaciones jerárquicas genéricas: "+str(bro)+"\nRelaciones jerárquicas específicas: "+str(nar)+"\nRelaciones asociativas: "+str(rel)+"\nNúmero NER: "+str(ner)+" "+str(ner/c*100))


sorted = sorted(ner_stats.items(), key=lambda x:x[1]["num"], reverse=True)
for i in sorted:
    index=i[0]
    num=ner_stats[index]["num"]
    if num/ner*100>=1:
        print(index,num,num/ner*100)
 
#print(sorted)
