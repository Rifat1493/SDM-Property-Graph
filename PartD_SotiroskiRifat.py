1. In order to get the communities we use the same grpah and write the community on every article.
CALL
gds.louvain.write('myGraph', {writeProperty: 'community'})
YIELD
communityCount, modularity, modularities

2. Add a community to the conferences/journals. If 90% of the articles are connected with that commnuity, then assign that one.

// journals

MATCH p=(a:articles)-[r:published_inj]->(j:journals )
WITH j as jour,  a.community as com, count(*) as nb
WITH  jour, collect(com) as list_com, collect(nb) as list_nb
UNWIND list_nb as r
WITH jour, list_com, list_nb, sum(r) as sum, range(0,size(list_nb)-1,1) AS coll_size
UNWIND coll_size AS idx
WITH jour, list_com[idx] as com, 1.0*list_nb[idx]/sum as percentage
order by jour, percentage desc
// where percentage > 0.9
// return jour, collect(com)[0] as final_community
set jour.community = final_community

// conf
MATCH p=(a:articles)-[r:published_inc]->(c:conferences )
WITH c as conf,  a.community as com, count(*) as nb
WITH  conf, collect(com) as list_com, collect(nb) as list_nb
UNWIND list_nb as r
WITH conf, list_com, list_nb, sum(r) as sum, range(0,size(list_nb)-1,1) AS coll_size
UNWIND coll_size AS idx
WITH conf, list_com[idx] as com, 1.0*list_nb[idx]/sum as percentage
order by conf, percentage desc
// where percentage > 0.9
with conf, collect(com)[0] as final_community
set conf.community = final_community

3.
// pagerannk for 6

CALL gds.graph.create.cypher(
  'pageRank',
  'MATCH (a:articles {community: 6})RETURN id(a) as id',
  'MATCH (a1:articles {community:6})-[r:cited_by]->(a2:articles {community: 6}) RETURN id(a1) as source, id(a2) as target'
)
YIELD
  graphName AS graph, nodeQuery, nodeCount AS nodes, relationshipQuery, relationshipCount AS rels
  
  
CALL gds.pageRank.stream('a')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId) AS name, score as pageRank
ORDER BY pageRank DESC, name ASC  
  

CALL gds.pageRank.write('a', {
  maxIterations: 20,
  dampingFactor: 0.85,
  writeProperty: 'pagerank'
})
YIELD nodePropertiesWritten, ranIterations

// change to 100 creating top 100 for each conference/community
MATCH (a:articles)-[r:published_inc]->(c:conferences)
WHERE a.community=6 AND c.community=a.community
WITH c.conference as conf, a.article as art, a.pagerank as part
ORDER BY conf, part  desc
RETURN conf, collect(art)[0..3]

// step 4
// adding the istop100
MATCH (a:articles)-[r:published_inc]->(c:conferences)
WHERE a.community=6 AND c.community=a.community
WITH c.conference as conf, a.article as art, a.pagerank as part
ORDER BY conf, part  desc
WITH conf, collect(art)[0..10] as list10
UNWIND list10 as topArt
MATCH (a2:articles {article: topArt})
SET a2.isTop100 = true

//adding the gurus
	
MATCH (a:articles {isTop100: true})-[r:writtenby]->(au:authors) 
WITH au as auth, count(a) as nb
WHERE nb>=2
SET auth.isGuru=true
  
