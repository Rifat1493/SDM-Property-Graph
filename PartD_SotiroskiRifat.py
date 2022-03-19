1. In order to get the communities we use the same grpah and write the community on every article.
CALL
gds.louvain.write('myGraph', {writeProperty: 'community'})
YIELD
communityCount, modularity, modularities

2. Add a community to the conferences/journals. If 90% of the articles are connected with that commnuity, then assign that one.

// check