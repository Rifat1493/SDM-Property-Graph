from connection import connect

def step1(conn):
    query = '''
            CALL gds.louvain.write('louvain', {writeProperty: 'community'})
            YIELD communityCount, modularity, modularities
            '''
    
    conn.query(query, db='dblp')


#// journals
def step2(conn):
    # finding the communities for journals
    query_journals = '''
            MATCH p=(a:articles)-[r:published_inj]->(j:journals )
            WITH j as jour,  a.community as com, count(*) as nb
            WITH  jour, collect(com) as list_com, collect(nb) as list_nb
            UNWIND list_nb as r
            WITH jour, list_com, list_nb, sum(r) as sum, range(0,size(list_nb)-1,1) AS coll_size
            UNWIND coll_size AS idx
            WITH jour, list_com[idx] as com, 1.0*list_nb[idx]/sum as percentage
            ORDER BY jour, percentage desc
            // WHERE percentage > 0.9
            // RETURN jour, collect(com)[0] as final_community
            SET jour.community = final_community
            '''
    conn.query(query_journals, db='dblp')

    # finding the communities for conferences
    query_conferences = '''
                        MATCH p=(a:articles)-[r:published_inc]->(c:conferences )
                        WITH c as conf,  a.community as com, count(*) as nb
                        WITH  conf, collect(com) as list_com, collect(nb) as list_nb
                        UNWIND list_nb as r
                        WITH conf, list_com, list_nb, sum(r) as sum, range(0,size(list_nb)-1,1) AS coll_size
                        UNWIND coll_size AS idx
                        WITH conf, list_com[idx] as com, 1.0*list_nb[idx]/sum as percentage
                        ORDER BY conf, percentage desc
                        // WHERE percentage > 0.9
                        WITH conf, collect(com)[0] as final_community
                        SET conf.community = final_community
                        '''
    conn.query(query1, db='dblp')

def step3(conn):
    # finding the pagerank for articles of community 6
    # creating the subraph pageRank
    query = '''
            CALL gds.graph.create.cypher(
              'pageRank',
              'MATCH (a:articles {community: 6})RETURN id(a) as id',
              'MATCH (a1:articles {community:6})-[r:cited_by]->(a2:articles {community: 6}) RETURN id(a1) as source, id(a2) as target'
            )
            YIELD graphName AS graph, nodeQuery, nodeCount AS nodes, relationshipQuery, relationshipCount AS rels
            '''
    conn.query(query, db='dblp')

    # query used to show the results
    query = '''
            CALL gds.pageRank.stream('pageRank')
            YIELD nodeId, score
            RETURN gds.util.asNode(nodeId) AS name, score as pageRank
            ORDER BY pageRank DESC, name ASC
            '''
    conn.query(query, db='dblp')

    # query used to run the results of the pageRank as a property on the nodes of the article
    query = '''
            CALL gds.pageRank.write('pageRank', {
              maxIterations: 20,
              dampingFactor: 0.85,
              writeProperty: 'pagerank'
            })
            YIELD nodePropertiesWritten, ranIterations
            '''
    conn.query(query, db='dblp')

    # creating the top 100 for every conference
    query = '''
            MATCH (a:articles)-[r:published_inc]->(c:conferences)
            WHERE a.community=6 AND c.community=a.community
            WITH c.conference as conf, a.article as art, a.pagerank as part
            ORDER BY conf, part  desc
            RETURN conf, collect(art)[0..100]
            '''

    conn.query(query, db='dblp')



def step4(conn):
    # getting the top papers for that confrence and that community
    query = '''
            MATCH (a:articles)-[r:published_inc]->(c:conferences)
            WHERE a.community=6 AND c.community=a.community
            WITH c.conference as conf, a.article as art, a.pagerank as part
            ORDER BY conf, part  desc
            WITH conf, collect(art)[0..10] as list10
            UNWIND list10 as topArt
            MATCH (a2:articles {article: topArt})
            SET a2.isTop100 = true
            '''
    conn.query(query, db='dblp')

    # setting the gurus
    query = '''	
            MATCH (a:articles {isTop100: true})-[r:writtenby]->(au:authors) 
            WITH au as auth, count(a) as nb
            WHERE nb>=2
            SET auth.isGuru=true
            '''
    conn.query(query, db='dblp')

    
  
def run_recommender(conn):
    step1(conn)
    step2(conn)
    step3(conn)
    step4(conn)