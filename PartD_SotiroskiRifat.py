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

