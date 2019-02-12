---
layout: post
title: "Neo4j certification"
tags: graph neo4j
summary: I passed the neo4j graph database certification.
date: 2018-12-22 16:00:00
---

Today is a good day. First, it the first day of Christmas holidays. But this is not the reason why it is a special day and deserve a post. The reason is that I just passed the neo4j certitication, and I wanted to share this with you.

Neo4j is probably the most famous implementation of graph databases. 

We are mainly used to relational database, where data is stored into tables, each table representing a type of entities. Relationships between entities are modelled by foreign keys.

In a graph database instead, each entity is represented as a node `()`. Nodes have labels to distinguish the kind of entities (MOVIE and ACTOR for instance can be two labels). A (directed) relationship `[]` can be created between two nodes, here again with a given label, such as `ACTED_IN` or `DIRECTED_BY`. This will be represented like:

    (leonardo:ACTOR)-[:PLAYED_IN]->(titanic:MOVIE)
    (titanic:MOVIE)-[:DIRECTED_BY]->(cameron:ACTOR)

The query language used by neo4j (actually, it was developped by this company and finally open-sourced) is Cypher. 

I will not enter into the details of cypher right now, yYou can find more about it for instance [here](https://neo4j.com/graphacademy/online-training/getting-started-graph-databases-using-neo4j/).

Let's go back to the certification itself. Is is free and can be taken whenever you want [online](https://neo4j.com/graphacademy/neo4j-certification/). A score of 80% or more is required to pass.

The prgram includes graph model and cypher, but also the supported neo4j drivers and the available configuration to use it in production. The most difficult part for me was the last one, since I never had so far to use neo4j on production and didn't knew a lot about configuration. But the *large community* have produced *tons of material* on the topic, so that was enough to document myself on the topic.

At the end, I achieved a score of 85% (__[Certificate](https://graphacademy.neo4j.com/certificates/43898ee59d183928339d23f5e21d52276054b3b133d48a03e71bebab024ad242.pdf).__), not bad if you know I have been learning the graph database for only one month.

Hope I will be able to put this new knowledge into practice in real-world situations!

See you soon and 

$$
y = \frac{ \ln (\frac{x}{m} - sa)}{r^2}
$$

or Merry Christmas!
