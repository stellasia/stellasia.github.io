---
layout: post
title: "Migration guide for the course 'Exploring graph algorithms with Neo4j'"
tags: neo4j
summary: "A small guide to follow the course using the Graph Data Science plugin instead of the Graph Algorithms library."
date: 2020-05-03 16:00:00:00
---


## The course

In 2019, I was asked to record a video course about the Graph Algorithms library (GA) released by Neo4j. These videos are available on the [publisher website](https://www.packtpub.com/eu/application-development/exploring-graph-algorithms-neo4j-video).

Even if the main concepts about the algorithms remain unchanged (centrality algorithms are still centrality algorithms), the Graph Algorithms library is being deprecated by the Neo4j team in favor of a more optimized version called [Graph Data Science plugin](https://neo4j.com/docs/graph-data-science/current/) (GDS) also available on [GitHub](https://github.com/neo4j/graph-data-science).

A very detailed migration guide has been created by the Neo4j folks and is available [here](https://neo4j.com/docs/graph-data-science/current/appendix-b/).

In this post, I will focus on the changes to be made to follow the above mentioned course using the GDS. This update is mandatory is you are using Neo4j 4, since only the GDS (starting from its version 1.2) is compatible with this version of Neo4j.

> While all GA procedures were within the `algo.*` namespace, in the GDS all procedures start with `gds.*` 

## Graph projection

### Named VS anonymous projections

Even if creating named projected graphs was already possible in the Graph Algorithm plugin, this functionality was not really highlighted and is not used at all in the videos.

In the GDS on the contrary, a lot of examples are given using a named projected graph created using `gds.graph.create` procedure. But it is still possible to use anonymous projected graphs using either native or cypher projection:

- Native projection: `nodeProjection` and `relationshipProjection` allow to configure the list of nodes, relaitonships and their properties that need to be copied into the in-memory projected graph.
- Cypher projection: the nodes and relationships to use are selected through a Cypher statement. For this, include `nodeQuery` and/or `relationshipQuery` to the configuration map.


### Relationship projection

**Important difference**: while the projected graph in the GA was by default undirected, the projected graph in the GDS by default uses the relationships in their native direction. In order to use undirected relationships, you need to use:

A typical relationship projection will have the following structure:

```
     relationshipProjection: {
         SUBWAY: {  // type of the relationships in the projected graph
	      type: "SUBWAY",  // type of the relationships in the Neo4j graph to be copied
	      orientation: "UNDIRECTED",  // relationship orientation: NATIVE (default), REVERSE or UNDIRECTED
		  aggregation: "SINGLE",  // what to do with parallel relationships? SINGLE means take only one of them
	      properties: ["weight"]  // list of relationship properties to include in the projected graph
	    }
     },
```


## Algorithms

With the GDS, all algorithms share the same signature:

- `gds.<algo_path>(graphName, configurationMap)` if using a named projected graph, which is not our case
- `gds.<algo_path>(configurationMap)` if using an anonymouse projected graph.

Some of them are fully optimized and _production-ready_. They are accessible directly through `gds.<algoName>` procedures. There are two other cases:

- the algorithms back-ported from the GA but not yet optimized are in the `gds.alpha` namespace. They are not stable and might suffer from performance issues
- the algorithms being improved but still in testing mode are in the `gds.beta` namespace


### Stream or write

While in the GA, the write mode was triggered by adding a `write: true` configuration parameter, this behavior is now handled by the procedure name:

- `gds.pageRank.stream` to stream the results back to the user.
- `gds.pageRank.write` to write the results back to the Neo4j graph. The procedure signatures are similar, except that the write mode accepts another paramter: `writeProperty` to configure the name of the property the results will be written into.


### Shortest path

> All the algorithms in the shortest path section are still in the `alpha` tier of the GDS.


While in the GA we were writting:

```
MATCH (A:City {name: "A"})
MATCH (E:City {name: "E"})
CALL algo.shortestPath.stream(A, E, null, {relationshipQuery: "ROAD"})
YIELD nodeId, cost
RETURN algo.getNodeById(nodeId).name, cost
```

In the GDS we now have to use the following syntax:

```
MATCH (A:City {name: "A"})
MATCH (E:City {name: "E"})
CALL gds.alpha.shortestPath.stream({
	startNode: A, 
	endNode: E, 
	nodeProjection: "*",
    relationshipProjection: {
       ROAD: {
	      type: "ROAD",
	      orientation: "UNDIRECTED"
       }
   }
})
YIELD nodeId, cost
RETURN gds.util.asNode(nodeId).name, cost
```

- `nodeProjection: "*"` means 'use all nodes in the graph'
- `relationshipProjection:` takes only relationships with type `ROAD`, but consider them undirected, contrarily to the native Neo4j graph where relationships are directed.

Also note that the util functions `algo.getNodeById` has been moved to `gds.util.asNode`.


### Centrality

> The PageRank algorithm is a production-ready algorithm from GDS 1.0


- GA:
    ```
	CALL algo.pageRank.stream(null, null, {direction: "BOTH", dampingFactor: 0.5, iterations: 50})
	YIELD nodeId, score
	RETURN algo.getNodeById(nodeId).pId, score
	ORDER BY score DESC
    ```
- GDS:
    ```
	CALL gds.pageRank.stream({
		   nodeProjection: "*",
		   relationshipProjection: {
			   LINKED_TO: {
				   type: "LINKED_TO",
				   orientation: "UNDIRECTED",
				   aggregation: "SINGLE"
			   }
		   },
		   dampingFactor: 0.5,
		   maxIterations: 50
	})
	YIELD nodeId, score
	RETURN gds.util.asNode(nodeId).pId, score
	ORDER BY score DESC
	```

Closeness and betweenness are both in the alpha tier:

- `gds.alpha.closeness.stream` or `gds.alpha.closeness.write`
- `gds.alpha.betweeness.stream` or `gds.alpha.betweeness.write`

Their usage is similar to the ones of PageRank.


### Community detection

> Weakly Connected Components (Union Find), Louvain and Label Propagation algorithms are all part of the production quality algorithms!


Example with Union find or Weakly connected components, native projection and stream mode:

- GA:
    ```
	CALL algo.unionFind.stream("Person", null)
	YIELD nodeId, setId
	RETURN algo.getNodeById(nodeId).pId, setId
	ORDER BY setId	
	```
- GDS:
    ```
	CALL gds.wcc.stream({
		nodeProjection: "Person",
		relationshipProjection: "*"
	}) 
	YIELD nodeId, componentId as setId
	RETURN gds.util.asNode(nodeId).pId, setId
	ORDER BY setId
	```

Example with the Louvain algorithm, cypher projection and write mode:

- GA:
    ```
	CALL algo.louvain("MATCH (p:Product) RETURN id(p) as id",
		  "MATCH (p:Product)<-[:ORDERS]-(:Order)-[:ORDERS]->(q:Product) RETURN id(p) as source, id(q) as target", 
                  {direction: "BOTH", graph: "cypher", writeProperty: "louvain"})
	YIELD nodes, communityCount
	RETURN nodes, communityCount
	```
	
- GDS:
    ```
	CALL gds.louvain.write({
		nodeQuary: "MATCH (p:Product) RETURN id(p) as id",
		relationshipQuery: "MATCH (p:Product)<-[:ORDERS]-(:Order)-[:ORDERS]->(q:Product) RETURN id(p) as source, id(q) as target", 
		writeProperty: "louvain"
	})
	YIELD nodes, communityCount
	RETURN nodes, communityCount
	```


I hope this small guide will help you follow the course using the GDS as well! The full update of the code file associated with the course ([link](https://github.com/PacktPublishing/Exploring-Graph-Algorithms-with-Neo4j)) is ongoing and will be published here soon. In the meantime, do not hesitate to contact me in case of any problem with the course!
