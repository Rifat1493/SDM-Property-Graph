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

#3rd main
'''
MATCH (pub_ar:articles)-[r:published_inj]->(j:journals) 

match ()-[ct:cited_by]->(pub_ar) 
with j.journal as cite_jor,pub_ar.year as year,count(j) as cite_num
order by cite_jor,year 
with collect([cite_jor,year,cite_num]) as cites

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










conn.query(query_string, db='dblp')




match (arc:articles)<-[ct:cited_by]-(ar:articles)-[:published_inc]->(c:conferences) return c.conference,ar.title,count(arc)


 