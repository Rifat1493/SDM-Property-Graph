# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 19:19:13 2022

@author: Rifat
"""

def citation_query(conn):
    querry='''
    match (arc:articles)<-[ct:cited_by]-(ar:articles)-[:published_inc]->(c:conferences)
    with  c.conference as con,ar.title as til,count(arc) as num
    order by con,num desc
    with con,collect([til,num])[..3] as arti
    return con,arti '''
    conn.query(querry, db='dblp')
    


def communities_query(conn):
    querry = '''MATCH (au:authors)<-[w:writtenby]-(a:articles)-[r:published_inc]->(c:conferences)
                WITH c.conference as conferences, au.author as authors, count(r.edition) as nb_pub
                WHERE nb_pub >= 4
                RETURN conferences, collect(authors) as community
                LIMIT 25'''
    conn.query(querry, db='dblp')
    # // for each conference, the authors who published in more than 4 editions

    # show example:
    # MATCH p=(au:authors {author: "Jim Melton"})<-[w:writtenby]-(a:articles)-[r:published_inc]->(c:conferences)
    # RETURN p
    # LIMIT 20


def impact_factor_query(conn):
    #not done with it
    querry='''MATCH p=(pub_ar:articles)-[r:published_inj]->(j:journals) 

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
    return name,round(impact_factor, 2) as impact_factor'''
    conn.query(querry, db='dblp')
    
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
    conn.query(querry, db='dblp')
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



