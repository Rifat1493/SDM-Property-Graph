# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 19:19:13 2022

@author: Rifat
"""

import connection

conn = connection.Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", pwd="1234")


#conn.query("CREATE OR REPLACE DATABASE coradb")

query_string =''' load CSV FROM 'file:///university.csv' AS row FIELDTERMINATOR ','
CREATE (n:university {uni_id:row[0],name:row[1]}) return n'''

conn.query(query_string, db='dblp')


query_string =''' load CSV FROM 'file:///company.csv' AS row FIELDTERMINATOR ','
CREATE (n:company {com_id:row[0],name:row[1]}) return n'''

conn.query(query_string, db='dblp')


query_string =''' load CSV FROM 'file:///affiliation_company.csv' AS row FIELDTERMINATOR ','
match (a:authors),(c:company) where (a.author_id)=row[0] and (c.com_id)=row[1] create (a)-[:affiliated_withc]->(c)'''

conn.query(query_string, db='dblp')

query_string =''' 
load CSV FROM 'file:///affiliation_university.csv' AS row FIELDTERMINATOR ','
match (a:authors),(u:university) 
where (a.author_id)=row[0] and (u.uni_id)=row[1] 
create (a)-[:affiliated_withu]->(u)
'''

conn.query(query_string, db='dblp')