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


query_string='''LOAD CSV with headers FROM 'file:///C:/Users/Rifat/Desktop/SDM_Property_Graph/Data/dblp_school.csv' AS row FIELDTERMINATOR ';'
CREATE (:school {art_info:row[0]}) return row[0];'''

query_string='''LOAD CSV with headers FROM 'file:///C:/Users/Rifat/Desktop/SDM_Property_Graph/Data/dblp_school.csv' AS row FIELDTERMINATOR ';'  return row limit 30; '''
conn.query(query_string, db='neo4j')


query_string='''LOAD CSV with headers FROM 'file:///C:/Users/Rifat/Desktop/SDM_Property_Graph/Data/dblp_school.csv' AS row FIELDTERMINATOR ';' with toInteger(row[0]) as ID, row[1] as school_name CREATE (:school {art_info:school_name }); '''



conn.query(query_string, db='neo4j')



query_string=''' import --mode=csv --database=neo4j --delimiter ";" --array-delimiter "|" --id-type INTEGER --nodes:article "dblp_article_header.csv,dblp_article.csv" '''




conn.query(query_string, db='neo4j')


import subprocess
subprocess.call(['sh', 'Data/neo4j_import.sh'])

 