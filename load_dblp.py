# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 13:24:33 2022

@author: Rifat
"""
import connection

conn = connection.Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", pwd="1234")

#conn.query("CREATE OR REPLACE DATABASE coradb")

query_string =''' load CSV FROM 'file:///C:/Users/Rifat/Desktop/SDM_Property_Graph/Data/dblp_author.csv' AS row FIELDTERMINATOR ';'
CREATE (c:Company {companyId: row})'''

conn.query(query_string, db='neo4j')


query_string='''LOAD CSV WITH HEADERS FROM 'file:///C:/Users/Rifat/Desktop/SDM_Property_Graph/Data/dblp_school.csv' AS row
WITH row WHERE row.school IS NOT NULL
CREATE (c:Company {companyId: row.school})'''




query_string=''' import --mode=csv --database=neo4j --delimiter ";" --array-delimiter "|" --id-type INTEGER --nodes:article "dblp_article_header.csv,dblp_article.csv" '''




conn.query(query_string, db='neo4j')


import subprocess
subprocess.call(['sh', 'Data/neo4j_import.sh'])

 