from connection import connect

def citation_query(conn):
    print("Citation query")
    query = '''
            MATCH (ar:articles)-[:published_inc]->(c:conferences)
            MATCH ()-[ct:cited_by]->(ar:articles)
            WITH  c.conference as con,ar.title as til,count(ar) as num
            ORDER BY con,num desc
            WITH con,collect([til,num])[..3] as arti
            RETURN con,arti  
            '''

    conn.query(query, db='dblp')
    


def communities_query(conn):
    print("Communities query")
    query = '''
            MATCH (au:authors)<-[w:writtenby]-(a:articles)-[r:published_inc]->(c:conferences)
            WITH c.conference as conferences, au.author as authors, count(r.edition) as nb_pub
            WHERE nb_pub >= 4
            RETURN conferences, collect(authors) as community
            LIMIT 25
            '''
    conn.query(query, db='dblp')
    # // for each conference, the authors who published in more than 4 editions

    # show example:
    # MATCH p=(au:authors {author: "Jim Melton"})<-[w:writtenby]-(a:articles)-[r:published_inc]->(c:conferences)
    # RETURN p
    # LIMIT 20


def impact_factor_query(conn):
    print("Impact factor")
    query = '''
            MATCH p=(pub_ar:articles)-[r:published_inj]->(j:journals) 
            MATCH p1= ()-[ct:cited_by]->(pub_ar) 
            WITH j.journal as cite_jor,pub_ar.year as year,count(p) as cite_num
            ORDER BY cite_jor,year 
            WITH collect([cite_jor,year,cite_num]) as list
            UNWIND list as x
            MATCH (pub_ar:articles{year:x[1]-1})-[r:published_inj]->(j:journals{journal:x[0]})
            WITH x[0] as name,x[1] as year,x[2] as cite_num,count(pub_ar) as pub_num1
            WITH collect([name,year,cite_num,pub_num1]) as list
            UNWIND list as x
            MATCH (pub_ar:articles{year:x[1]-2})-[r:published_inj]->(j:journals{journal:x[0]})
            WITH x[0] as name,x[1] as year,(toFloat(x[2])/(x[3]+count(pub_ar))) as impact_factor
            WITH name,avg(impact_factor) as impact_factor
            RETURN name,round(impact_factor, 2) as impact_factor
            '''
    conn.query(query, db='dblp')
    
def hindex_query(conn):
    print("H-index")
    query = ''' MATCH ()<-[c:cited_by]-(ar:articles)-[w:writtenby]->(a:authors)
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
    conn.query(query, db='dblp')
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



def run_all_queries(conn):
    citation_query(conn)
    communities_query(conn)
    impact_factor_query(conn)
    hindex_query(conn)