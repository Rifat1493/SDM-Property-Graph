# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 13:24:33 2022

@author: Rifat
"""
from connection import connect
import connection
#conn.query("CREATE OR REPLACE DATABASE coradb")

query_string =''' load CSV FROM 'file:///C:/Users/Rifat/Desktop/SDM_Property_Graph/Data/dblp_author.csv' AS row FIELDTERMINATOR ';'

'''
conn = connection.Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", pwd="1234")

#1st one
query_string='''
match (arc:articles)<-[ct:cited_by]-(ar:articles)-[:published_inc]->(c:conferences)
with  c.conference as con,ar.title as til,count(arc) as num
order by con,num desc
with con,collect([til,num])[..3] as arti
return con,arti


'''

#3rd one
query_string='''
MATCH (ar:articles)-[r:published_inj]->(j:journals) 
with j.journal as pub_jor,ar.year as pub_year,count(ar.year) as pub_num
order by pub_year
with pub_jor,collect([pub_year,pub_num]) as fpub_num

MATCH (arc:articles)<-[ct:cited_by]-(ar:articles)-[r:published_inj]->(j:journals) 
with pub_jor,fpub_num,arc.year as cite_year,count(arc.year) as cite_num
order by cite_year
with pub_jor,fpub_num,collect([cite_year,cite_num]) as fcite_num
return pub_jor,fpub_num,fcite_num

'''

#3rd main impact factor
'''
MATCH p=(pub_ar:articles)-[r:published_inj]->(j:journals) 

match p1= ()-[ct:cited_by]->(pub_ar) 
with j.journal as cite_jor,pub_ar.year as year,count(p) as cite_num
order by cite_jor,year 
with collect([cite_jor,year,cite_num]) as list
unwind list as x
match (pub_ar:articles{year:x[1]-1})-[r:published_inj]->(j:journals{journal:x[0]})
with x[0] as name,x[1] as year,x[2] as cite_num,count(pub_ar) as pub_num1
with collect([name,year,cite_num,pub_num1]) as list
unwind list as x
match (pub_ar:articles{year:x[1]-2})-[r:published_inj]->(j:journals{journal:x[0]})
 with x[0] as name,x[1] as year,(toFloat(x[2])/(x[3]+count(pub_ar))) as impact_factor
with name,avg(impact_factor) as impact_factor
return name,round(impact_factor, 2) as impact_factor

'''



#shortest path
'''
MATCH (start:authors{author:'Asit Dan'})
MATCH (end:author) where end<>start
WITH start, end limit 5
CALL gds.allShortestPaths.dijkstra.stream(start, end, 'dist')
YIELD node_id, dist
WITH start, node_id,dist
return algo.getNodeById(node_id)
'''





#### shortest path
CALL gds.graph.create(
    'myGraph',
    '*',
{writtenby: {orientation: 'UNDIRECTED'},reviewedby:{orientation: 'UNDIRECTED'}}
)

MATCH (source:authors{author:'Asit Dan'}), (target:authors{author:'Giuseppe Amato'})
CALL gds.shortestPath.dijkstra.stream('myGraph2', {
    sourceNode: source,
    targetNode: target
})
YIELD index, sourceNode, targetNode, totalCost, nodeIds, costs, path
RETURN
    index,
    gds.util.asNode(sourceNode).name AS sourceNodeName,
    gds.util.asNode(targetNode).name AS targetNodeName,
    totalCost,
    [nodeId IN nodeIds | gds.util.asNode(nodeId).name] AS nodeNames,
    costs,
    nodes(path) as path
ORDER BY index




optional match (pub_ar1:articles{year:x[1]-2})-[r:published_inj]->(j:journals{journal:x[0]})
with x[0] as name,x[1] as year,x[2] as cite_num,count(pub_ar) as pub_num1,count(pub_ar1) as pub_num2








conn.query(query_string, db='dblp')

# neo4j admin command
neo4j-admin import --database=dblp --nodes=journals=import/journal.csv --nodes=conferences=import/conference.csv --nodes=authors=import/authors.csv --nodes=articles=import/articles.csv --nodes=keywords=import/keywords.csv --relationships=writtenby=import/author_writes_article.csv --relationships=reviewedby=import/article_reviewedby_author.csv --relationships=published_inj=import/article_publishedin_journal.csv --relationships=published_inc=import/article_publishedin_conference.csv --relationships=contains=import/article_keywords.csv --relationships=cited_by=import/article_cites.csv --skip-duplicate-nodes=true --force
 