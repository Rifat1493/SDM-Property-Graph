from connection import connect

def louvain(conn):
    print("Running Louvain")
    create_louvain = '''
                    CALL gds.graph.create(
                        'louvain', ['articles', 'keywords'], 'contains')
                    YIELD graphName AS graph, nodeProjection, nodeCount AS nodes, relationshipCount AS rels
                    '''
    conn.query(create_louvain, db='dblp')

    run_louvain =   '''
                    CALL gds.louvain.stream('louvain')
                    YIELD nodeId, communityId, intermediateCommunityIds
                    WITH gds.util.asNode(nodeId).article AS article, communityId
                    RETURN communityId, count(article)
                    '''
    
    conn.query(run_louvain, db='dblp')

def shortest_path(conn):
    print("Running Dijkstra")
    create_dijkstra = '''CALL gds.graph.create(
                        'dijkstra', '*', {writtenby: {orientation: 'UNDIRECTED'},reviewedby:{orientation: 'UNDIRECTED'}}
                        )
                        YIELD
                          graphName,
                          nodeProjection,
                          nodeCount,
                          relationshipProjection,
                          relationshipCount,
                          createMillis
                        '''
    conn.query(create_dijkstra, db='dblp')


    run_dijkstra =  ''' MATCH (source:authors{author:'Asit Dan'}), (target:authors{author:'Giuseppe Amato'})
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
    conn.query(run_dijkstra, db='dblp')
    
def run_algorithms(conn):
    louvain(conn)
    shortest_path(conn)