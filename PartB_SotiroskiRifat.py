# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 19:19:13 2022

@author: Rifat
"""

def citation_query():
    querry='''
    match (arc:articles)<-[ct:cited_by]-(ar:articles)-[:published_inc]->(c:conferences)
    with  c.conference as con,ar.title as til,count(arc) as num
    order by con,num desc
    with con,collect([til,num])[..3] as arti
    return con,arti '''

    return querry


def communities_query(conn):
    querry = '''MATCH (au:authors)<-[w:writtenby]-(a:articles)-[r:published_inc]->(c:conferences)
                WITH c.conference as conferences, au.author as authors, count(r.edition) as nb_pub
                WHERE nb_pub >= 4
                RETURN conferences, collect(authors) as community
                LIMIT 25'''
    # // for each conference, the authors who published in more than 4 editions

    # show example:
    # MATCH p=(au:authors {author: "Jim Melton"})<-[w:writtenby]-(a:articles)-[r:published_inc]->(c:conferences)
    # RETURN p
    # LIMIT 20


def impact_factor_query(conn):
    #not done with it
    querry='''MATCH (pub_ar:articles)-[r:published_inj]->(j:journals) 
    match ()-[ct:cited_by]->(pub_ar) 
    with j.journal as cite_jor,pub_ar.year as year,count(j) as cite_num
    order by cite_jor,year 
    with collect([cite_jor,year,cite_num]) as cites'''

def hindex_query(conn):
    querry = '''MATCH ()<-[c:cited_by]-(ar:articles)-[w:writtenby]->(a:authors)
                WITH a as authors, ar.title as titles, count(*) as nb
                order by nb desc
                WITH authors, collect(nb) as citations
                CALL {
                    WITH citations
                    WITH *, [x in range(0, size(citations)-1)] as enumerate
                    ORDER BY citations desc
                    WITH *, size([x in enumerate WHERE citations[x] >= x+1 ]) as hindex
                    RETURN  hindex
                }
                return authors, citations, hindex
                ORDER BY hindex desc
                LIMIT 25'''

    # for running examples

        # WITH [3,0,6,1,5] as citations
        # CALL {
        #     with citations
        #     with *, [x in range(0, size(citations)-1)] as enumerate
        #     order by citations desc
        #     WITH size([x in enumerate WHERE citations[x] >= x+1 ]) as hindex
        #     return hindex
        # }
        # return hindex



