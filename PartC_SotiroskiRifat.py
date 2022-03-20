def louvain(conn):
    querry='''CALL
    gds.graph.create(
        'myGraph', ['articles', 'keywords'], 'contains')
    YIELD
    graphName
    AS
    graph, nodeProjection, nodeCount
    AS
    nodes, relationshipCount
    AS rels

    CALL
    gds.louvain.stream('myGraph')
    YIELD
    nodeId, communityId, intermediateCommunityIds
    WITH
    gds.util.asNode(nodeId).article
    AS
    article, communityId
    RETURN
    communityId, count(article)'''
    
    return querry


def shortest_path(conn):
    querry1='''CALL gds.graph.create(
    'myGraph6',
    '*',
    {writtenby: {orientation: 'UNDIRECTED'},reviewedby:{orientation: 'UNDIRECTED'}}
    )
    
    YIELD
      graphName,
      nodeProjection,
      nodeCount,
      relationshipProjection,
      relationshipCount,
      createMillis'''
      
    conn.query(querry1, db='dblp')
    querry2='''MATCH (source:authors{author:'Asit Dan'}), (target:authors{author:'Giuseppe Amato'})
    CALL gds.shortestPath.dijkstra.stream('myGraph6', {
        sourceNode: source,
        targetNode: target
    })
    YIELD index, sourceNode, targetNode, totalCost, nodeIds, costs, path
    RETURN
        index,
        gds.util.asNode(sourceNode).name AS sourceNodeName,
        gds.util.asNode(targetNode).name AS targetNodeName,
        totalCost,
        [nodeId IN nodeIds | gds.util.asNode(nodeId).name] AS nodeNames,
        costs,
        nodes(path) as path
    ORDER BY index
    '''
    return conn.query(querry2, db='dblp')
    





