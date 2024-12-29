import csv
import sys
import requests
from operator import index
from guess_language import guess_language
import detectlanguage



detectlanguage.configuration.api_key = "043a69b0ad0ae4e69e332e73a403bed6"
# https://detectlanguage.com/

headers = {'User-Agent': 'rdf-ner/0.1 (https://www.um.es/docencia/pastor/; pastor@um.es)'}
url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'

node={}
concept={}
schema={}
collection=[]
label={}
relation={}
rel_schema={}
rel_concept={}
note={}
added_label={}

created_node={}
created_concept={}
created_concept_relation={}
created_schema_relation={}

index_label_concept={}
index_label_node={}

num_node=0
num_concept=0
num_schema=0
num_collection=0
num_relation=0
num_rel_schema=0
num_rel_concept=0
num_label=0
num_note=0

added_label={}


si_num=0
si_recognized=0

grupo_tesauros="series"
term_list=["LA","LAS","LOS","EL","Y","DE","EN","DEL"]
#tes_list=["BASPER","BIAPER","DASPER","PALPER"]
#tes_list=["BARLUG","BASLUG","BIALUG","DASLUG","FOTLUG","MUSLUG","PALLUG","PROLUG"]
#tes_list=["BARTEM","BASTEM","BIATEM","DASTEM","FOTTEM","MUSTEM","PALTEM","PROTEM"]
tes_list=["BARSER","BASSER","DASSER","FOTSER","PALSER","PROSER","SOPSER"]



def add_label(labeltext,id_node,label_source,lang_label,state,type,tes_source):
    global num_label
    global added_label
    global node
    global label
    global index_label_concept
    if added_label[labeltext]==0:
        num_label+=1
        label[num_label]={"id_label":num_label,"id_node":id_node,"label_text":labeltext,"label_source":label_source,"cod_language":lang_label,"state":state,"type":type,"tes_source":[tes_source]}
        node[id_node]["labels"].append(num_label)
        node[id_node]["has_label"]=True
        added_label[labeltext]=num_label
        index_label_node[labeltext]=id_node
    else:
        get_num_label=added_label[labeltext]
        if tes_source not in label[get_num_label]["tes_source"]:
            label[get_num_label]["tes_source"].append(tes_source)


def add_relation(source_label,target_label,state,type):
    global num_relation
    global num_rel_concept
    global relation
    global index_label_concept
    global created_concept_relation
    if source_label+"-"+type+"-"+target_label not in created_concept_relation:
        num_relation+=1
        num_rel_concept+=1       
        relation[num_relation]={"id_relation":num_relation,"state":state}
        source=index_label_concept[source_label]
        target=index_label_concept[target_label]
        rel_concept[num_rel_concept]={"id_rel_concept":num_rel_concept,"id_relation":num_relation,"type":type,"id_concept_source":source,"id_concept_target":target}
        concept[source]["relations"].append(num_rel_concept)
        created_concept_relation[source_label+"-"+type+"-"+target_label]=num_relation


print("Creando nodos......................")


# Create nodes, concepts and labels
for tes in tes_list:
    print("--------",tes)
    with open("tesauros/"+grupo_tesauros+"/"+tes+".csv",encoding="ISO-8859-1") as data:
        for reg in csv.DictReader(data,delimiter=";"):
            if reg["ID_TERMINO"]!="" and reg["ID_TERMINO"] not in created_node and reg["TIPO_RELACION"]!="USE":
                if reg["TERMINO"] not in index_label_concept:
                    num_node+=1
                    node[num_node]={"id_node":num_node,"id_source":reg["ID_TERMINO"],"state":reg["ESTADO"],"labels":[]}
                    num_concept+=1
                    concept[num_concept]={"id_concept":num_concept,"id_node":num_node,"relations":[]}
                    created_node[reg["ID_TERMINO"]]=num_node
                    created_concept[reg["ID_TERMINO"]]=num_concept
                    index_label_concept[reg["TERMINO"]]=num_concept
            added_label[reg["TERMINO"]]=0
            added_label[reg["TERMINO_RELACIONADO"]]=0



print("Creando etiquetas y relaciones......................")

file = open("results/personas-not-translated.csv","w")
print('"ID_TERMINO","TERMINO","IDIOMA_TERMINO","TERMINO_RELACIONADO","IDIOMA_TERMINO_RELACIONADO"',file=file)
for tes in tes_list:
    print("--------",tes)
    with open("tesauros/"+grupo_tesauros+"/"+tes+".csv",encoding="ISO-8859-1") as data:
        for reg in csv.DictReader(data,delimiter=";"):
            if reg["ID_TERMINO"]!="":

                if reg["TIPO_RELACION"] in ["NI","NA","FI"]:
                    num_note+=1
                    note[num_note]={"id_note":num_note,"id_node":index_label_concept[reg["TERMINO"]],"type":"scopeNote","cod_language":"es","text_note":reg["TERMINO_RELACIONADO"],"state":reg["ESTADO"]}

                if reg["TIPO_RELACION"]=="":
                    add_label(labeltext=reg["TERMINO"],id_node=concept[index_label_concept[reg["TERMINO"]]]["id_node"],label_source=reg["ID_TERMINO"],lang_label="es",state=reg["ESTADO"],type="prefLabel",tes_source=tes)

                if reg["TIPO_RELACION"]=="UP":
                    add_label(labeltext=reg["TERMINO"],id_node=concept[index_label_concept[reg["TERMINO"]]]["id_node"],label_source=reg["ID_TERMINO"],lang_label="es",state=reg["ESTADO"],type="prefLabel",tes_source=tes)
                    add_label(labeltext=reg["TERMINO_RELACIONADO"],id_node=index_label_node[reg["TERMINO"]],label_source=0,lang_label="es",state=reg["ESTADO"],type="altLabel",tes_source=tes)

                if reg["TIPO_RELACION"]=="TR":
                    add_label(labeltext=reg["TERMINO"],id_node=concept[index_label_concept[reg["TERMINO"]]]["id_node"],label_source=reg["ID_TERMINO"],lang_label="es",state=reg["ESTADO"],type="prefLabel",tes_source=tes)
                    add_label(labeltext=reg["TERMINO_RELACIONADO"],id_node=concept[index_label_concept[reg["TERMINO_RELACIONADO"]]]["id_node"],label_source=0,lang_label="es",state=reg["ESTADO"],type="prefLabel",tes_source=tes)
                    add_relation(reg["TERMINO"],reg["TERMINO_RELACIONADO"],state=reg["ESTADO"],type="related")
                    add_relation(reg["TERMINO_RELACIONADO"],reg["TERMINO"],state=reg["ESTADO"],type="related")


                if reg["TIPO_RELACION"]=="TG" and reg["TERMINO"]+"-broader-"+reg["TERMINO_RELACIONADO"] not in created_concept_relation:
                    add_label(labeltext=reg["TERMINO"],id_node=concept[index_label_concept[reg["TERMINO"]]]["id_node"],label_source=reg["ID_TERMINO"],lang_label="es",state=reg["ESTADO"],type="prefLabel",tes_source=tes)
                    add_label(labeltext=reg["TERMINO_RELACIONADO"],id_node=concept[index_label_concept[reg["TERMINO_RELACIONADO"]]]["id_node"],label_source=0,lang_label="es",state=reg["ESTADO"],type="prefLabel",tes_source=tes)
                    add_relation(reg["TERMINO"],reg["TERMINO_RELACIONADO"],state=reg["ESTADO"],type="broader")
                    add_relation(reg["TERMINO_RELACIONADO"],reg["TERMINO"],state=reg["ESTADO"],type="narrower")

                if reg["TIPO_RELACION"]=="SI":
                    si_num+=1
                    lang_termino=guess_language(reg["TERMINO"]+". "+reg["TERMINO"]+". "+reg["TERMINO"]+". "+reg["TERMINO"]+". "+reg["TERMINO"])
                    lang_termino_relacionado=guess_language(reg["TERMINO_RELACIONADO"]+". "+reg["TERMINO_RELACIONADO"]+". "+reg["TERMINO_RELACIONADO"]+". "+reg["TERMINO_RELACIONADO"]+". "+reg["TERMINO_RELACIONADO"])
                    if lang_termino=="es" or (lang_termino_relacionado=="en" and lang_termino!="en"):
                        add_label(labeltext=reg["TERMINO"],id_node=concept[index_label_concept[reg["TERMINO"]]]["id_node"],label_source=reg["ID_TERMINO"],lang_label="es",state=reg["ESTADO"],type="prefLabel",tes_source=tes)
                        add_label(labeltext=reg["TERMINO_RELACIONADO"],id_node=concept[index_label_concept[reg["TERMINO"]]]["id_node"],label_source=reg["ID_TERMINO"],lang_label=lang_termino_relacionado,state=reg["ESTADO"],type="prefLabel",tes_source=tes)
                        si_recognized+=1
                    elif lang_termino_relacionado=="es":
                        add_label(labeltext=reg["TERMINO"],id_node=concept[index_label_concept[reg["TERMINO"]]]["id_node"],label_source=reg["ID_TERMINO"],lang_label=lang_termino,state=reg["ESTADO"],type="prefLabel",tes_source=tes)
                        add_label(labeltext=reg["TERMINO_RELACIONADO"],id_node=concept[index_label_concept[reg["TERMINO_RELACIONADO"]]]["id_node"],label_source=reg["ID_TERMINO"],lang_label="es",state=reg["ESTADO"],type="prefLabel",tes_source=tes)
                        si_recognized+=1
                    elif lang_termino=="en" and lang_termino_relacionado!="en" and lang_termino_relacionado!="es":
                        add_label(labeltext=reg["TERMINO"],id_node=concept[index_label_concept[reg["TERMINO"]]]["id_node"],label_source=reg["ID_TERMINO"],lang_label="en",state=reg["ESTADO"],type="prefLabel",tes_source=tes)
                        add_label(labeltext=reg["TERMINO_RELACIONADO"],id_node=concept[index_label_concept[reg["TERMINO_RELACIONADO"]]]["id_node"],label_source=reg["ID_TERMINO"],lang_label="es",state=reg["ESTADO"],type="prefLabel",tes_source=tes)
                        si_recognized+=1 

                    elif lang_termino=="en" and lang_termino_relacionado=="en":
                        is_termino_es= any(" "+term+" " in " "+reg["TERMINO"]+" " for term in term_list)
                        is_termino_relacionado_es= any(" "+term+" " in " "+reg["TERMINO_RELACIONADO"]+" " for term in term_list)
                        if is_termino_es:
                            lang_termino="es"
                        if is_termino_relacionado_es:
                            lang_termino_relacionado="es"
                        if is_termino_es or is_termino_relacionado_es:
                            si_recognized+=1
                            add_label(labeltext=reg["TERMINO"],id_node=concept[index_label_concept[reg["TERMINO"]]]["id_node"],label_source=reg["ID_TERMINO"],lang_label=lang_termino,state=reg["ESTADO"],type="prefLabel",tes_source=tes)
                            add_label(labeltext=reg["TERMINO_RELACIONADO"],id_node=concept[index_label_concept[reg["TERMINO"]]]["id_node"],label_source=reg["ID_TERMINO"],lang_label=lang_termino_relacionado,state=reg["ESTADO"],type="prefLabel",tes_source=tes)
                    
                    else:
                        is_termino_es= any(" "+term+" " in " "+reg["TERMINO"]+" " for term in term_list)
                        is_termino_relacionado_es= any(" "+term+" " in " "+reg["TERMINO_RELACIONADO"]+" " for term in term_list)
                        if is_termino_es:
                            lang_termino="es"
                            lang_termino_relacionado="xxxx"
                        if is_termino_relacionado_es:
                            lang_terminoi="xxxx"
                            lang_termino_relacionado="es"
                        if is_termino_es or is_termino_relacionado_es:
                            si_recognized+=1
                            add_label(labeltext=reg["TERMINO"],id_node=concept[index_label_concept[reg["TERMINO"]]]["id_node"],label_source=reg["ID_TERMINO"],lang_label=lang_termino,state=reg["ESTADO"],type="prefLabel",tes_source=tes)
                            add_label(labeltext=reg["TERMINO_RELACIONADO"],id_node=concept[index_label_concept[reg["TERMINO"]]]["id_node"],label_source=reg["ID_TERMINO"],lang_label=lang_termino_relacionado,state=reg["ESTADO"],type="prefLabel",tes_source=tes)
                        else:
                            print('"'+reg["ID_TERMINO"]+'","'+reg["TERMINO"]+'","'+lang_termino+'","'+reg["TERMINO_RELACIONADO"]+'","'+lang_termino_relacionado+'"',file=file)

file.close()


print("Creando esquema de conceptos............................")
print("Total de conceptos: "+str(len(concept)))


num_node+=1
num_schema+=1
node[num_node]={"id_source":0,"state":"Aceptado"}
schema[num_schema]={"id_esquema":num_schema,"id_node":num_node}
num_label+=1
label[num_label]={"id_label":num_label,"id_node":num_node,"label_text":"Tesauro de series","cod_language":"es","state":"Aceptado","type":"prefLabel"}

for i in concept:
    if str(i)+"-inscheme-"+str(num_schema) not in created_schema_relation:
        num_relation+=1
        num_rel_schema+=1
        relation[num_relation]={"id_relation":num_relation,"state":"Aceptado"}
        rel_schema[num_rel_schema]={"id_rel_schema":num_rel_schema,"id_relation":num_relation,"id_schema":num_node,"id_concept":i}
        created_schema_relation[str(i)+"-inscheme-"+str(num_schema)]=num_relation

c=0
l=0
r=0
ner=0
offset_start=int(sys.argv[1])
offset_end=int(sys.argv[2])
try:
	first_start=int(sys.argv[3])
except:
	first_start=offset_start

print("Creando fichero con resultados............................")

with open("results/"+grupo_tesauros+"-"+str(offset_start)+"-"+str(offset_end)+".txt","a") as file:
    for k in concept:
        if concept[k]["id_concept"]>=offset_start and concept[k]["id_concept"]<=offset_end and concept[k]["id_concept"]>=first_start:
    
            if len(node[k]["labels"])>0:
                print("\n",concept[k]["id_concept"],file=file)
                c+=1
            for i in node[k]["labels"]:
                print("\t",label[i]["type"],":",label[i]["label_text"],"("+label[i]["cod_language"]+")     ",end="",file=file)
                l+=1
                for t in label[i]["tes_source"]:
                    print(" ["+t+"]",end="",file=file)
                print("",file=file)

            for m in concept[k]["relations"]:
                print("\t --- ",rel_concept[m]["type"],rel_concept[m]["id_concept_target"],file=file)
                r+=1
            
            for i in node[k]["labels"]:
                queried=False
                if label[i]["type"]=="prefLabel" and label[i]["cod_language"]=="es" and not queried:
                    queried=True
                    string_search=label[i]["label_text"].replace("\"","")
                    string_search=string_search.replace("\n","")
                    string_search=string_search.replace("=","")
                    string_search=string_search.replace("·"," ")
                    sparql_query="""SELECT ?item ?itemLabel ?type ?typeLabel WITH {
                        SELECT ?item WHERE {
                            SERVICE wikibase:mwapi {
                                bd:serviceParam wikibase:endpoint "www.wikidata.org";
                                wikibase:api "EntitySearch";
                                mwapi:search """+"\""+string_search+"\""+""";
                                mwapi:language "es".
                                ?item wikibase:apiOutputItem mwapi:item.
                                ?num wikibase:apiOrdinal true.
                            }
                            ?item (wdt:P279|wdt:P31) ?type
                        } ORDER BY ASC(?num) LIMIT 1 } AS %INCLUDE
                        WHERE {
                            INCLUDE %INCLUDE
                            SERVICE wikibase:label {bd:serviceParam wikibase:language "es,en"}
                            ?item (wdt:P279|wdt:P31) ?type .
                        }"""
                    try:
                        data = requests.get(url,headers=headers, params={'query': sparql_query, 'format': 'json'}).json()
                        if len(data["results"]["bindings"])>0:
                            types_string="("
                            ner_item=""
                            ner+=1
                            for result in data["results"]["bindings"]:
                                types_string+=" "+result["typeLabel"]["value"]+" ("+result["type"]["value"].replace("http://www.wikidata.org/entity/","")+")"
                                ner_item=result["item"]["value"]
                            types_string+=")"
                            types_string=types_string.replace("( ","(")

                            print(ner,"/",c,"   ",ner_item,"   ",types_string)
                            print("\t NER : "+ner_item," --- TYPE : "+types_string,file=file)
                    except:
                        print(sparql_query)
                        print(data["results"]["bindings"])
                        exit()





    # print("\n\nConcepts: ",c,"\nLabels: ",l,"\nRelations: ",r,"\nTranslated: ",si_recognized,"\nNot translated: ",si_num-si_recognized,"\n","NER: ",ner,"\n",file=file)
    file.close()
