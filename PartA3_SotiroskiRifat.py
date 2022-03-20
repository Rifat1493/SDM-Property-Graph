# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 19:19:13 2022

@author: Rifat
"""

from connection import connect

"""
Adding the affiliations
"""


def load_affiliations(conn):
    print("Load affiliations")
    query_string = '''load CSV WITH HEADERS FROM 'file:///university.csv' AS row FIELDTERMINATOR ','
                        CREATE (n:university {uni_id:row.`uni:ID`,name:row.`name:string[]`}) return n'''
    conn.query(query_string, db='dblp')

    query_string = ''' load CSV WITH HEADERS FROM 'file:///company.csv' AS row FIELDTERMINATOR ',' 
                         CREATE (n:company {com_id:row.`com:ID`,name:row.`name:string[]`}) return n'''
    conn.query(query_string, db='dblp')

    query_string = ''' load CSV WITH HEADERS FROM 'file:///affiliation_company.csv' AS row FIELDTERMINATOR ',' 
                        match (a:authors),(c:company) 
                        where (a.author_id)=(row.`:START_ID`) and (c.com_id)=row.`:END_ID` 
                        create (a)-[:affiliated_withc]->(c)'''
    conn.query(query_string, db='dblp')

    query_string = ''' 
    load CSV WITH HEADERS FROM 'file:///affiliation_university.csv' AS row FIELDTERMINATOR ','
    match (a:authors),(u:university) 
    where (a.author_id)=(row.`:START_ID`) and (u.uni_id)=row.`:END_ID`
    create (a)-[:affiliated_withu]->(u)
    '''
    conn.query(query_string, db='dblp')


"""
Updating the reviews and changing the porperties
"""
def add_properties(conn):
    print("Adding properties")
    query_suggest = """
                    MATCH(a: authors)-[r:reviewedby]-(ar:articles)
                    SET r.suggest = rand() < 0.66
                    """
    conn.query(query_suggest, db='dblp')
    query_article = """
                    MATCH(a: authors)-[r:reviewedby]-(ar:articles)
                    WITH ar, collect(r.suggest)
                    AS suggestions
                    WITH ar, size([x IN suggestions WHERE x = true]) AS rev, size(suggestions) as sizesug
                    SET ar.reviewed = sizesug = rev
                    """
    conn.query(query_article, db='dblp')


def update_graph(conn):
    add_properties(conn)
    load_affiliations(conn)
    print("Update done! A3")
