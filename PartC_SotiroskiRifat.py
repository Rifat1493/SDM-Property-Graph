def louvain(conn):
    CALL
    gds.graph.create(
        'myGraph', ['articles', 'keywords'], 'contains')
    YIELD
    graphName
    AS
    graph, nodeProjection, nodeCount
    AS
    nodes, relationshipCount
    AS    rels

    CALL
    gds.louvain.stream('myGraph')
    YIELD
    nodeId, communityId, intermediateCommunityIds
    WITH
    gds.util.asNode(nodeId).article
    AS
    article, communityId
    RETURN
    communityId, count(article)




