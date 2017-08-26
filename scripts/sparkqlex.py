from SPARQLWrapper import SPARQLWrapper, JSON

Name=""
Director=""

MovieInfo={}

def AddToDict(Key,Value):
	global MovieInfo
#	print Key
#	print Value
	values=[]
	if Key in MovieInfo.keys():
		MovieInfo[Key].append(Value)
	else:
		values.append(Value)
		MovieInfo[Key] = values 

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
print "Name"
Name=raw_input()
print "Director"
Director=raw_input()
query="PREFIX dbO: <http://dbpedia.org/ontology/> PREFIX dbR: <http://dbpedia.org/resource/> SELECT ?x,?label WHERE {?x rdfs:label ?name .?x rdf:type dbO:Film. ?x rdfs:label ?label "
if len(Director):
	query = query + ". ?x dbO:director dbR:" + Director

query = query + " FILTER(bif:contains(?name," + "\"" + Name  + "\"" +"))}"

sparql.setQuery(query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
	print result["x"]["value"]
	print result["label"]["value"]
	print "Correct? (0 = No,1 = Yes)"
	choice = int(raw_input())
	if choice == 1:
		URI = result["x"]["value"]
		break
	else:
		continue

new_query = "PREFIX dbO: <http://dbpedia.org/ontology/> PREFIX dbR: <http://dbpedia.org/resource/> SELECT ?p,?o WHERE {<" + URI + ">?p ?o. ?o rdf:type dbO:Person }"
sparql.setQuery(new_query)
sparql.setReturnFormat(JSON) 
results = sparql.query().convert()

for result in results["results"]["bindings"]:
	predicate = result["p"]["value"].split('/')[-1].lower()
	value=result["o"]["value"]
	print predicate
	print value
	print predicate.find("direct")
	if predicate.find("director") >= 0: 
		AddToDict("Director",value)	
	if predicate.find("cinema") >= 0:
		AddToDict("Cinematography",value)	
	if predicate.find("edit") >= 0:
		AddToDict("Editor",value)	
	if predicate.find("write") >= 0:
		AddToDict("Writer",value)	
	if predicate.find("star") >= 0:
		AddToDict("Starring",value)	
print MovieInfo


