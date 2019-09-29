---
layout: post
title: "Recommendation API with Neo4j and GraphQL"
tags: graph neo4j
summary: Deploy a recommendation engine in 5 minutes with Neo4J and Graph QL
date: 2019-08-16 20:00:00
---


## Graph DB schema

We will be using a quite simple schema, considering only People, Items that can be Products or whatever, and relationships:

- Friendship between two Person
- Link between one Person and one Item

It is illustrated below:

![Graph schema](img/reco_graph_ql_schema.png)


## GraphQL schema

### Friendship

You need to install the graphQL plugin. When using Neo4j desktop, it's as simple as going to the management tab and clicking the install button.

So, to begin with, here is the schema we will create:

	type Person {
		email: String,
		items: [Item] @relation(name: "LINKED_TO", direction: "OUT")
		friends: [Person] @relation(name: "FRIEND_WITH", direction: "BOTH")
	}
	type Item {
	    id: Int,
		people: [Person] @relation(name: "LINKED_TO", direction: "IN")
	}


To let the graphQL plugin know about it, we just have to call the procedure ` graphql.idl` like this:

	CALL graphql.idl('
		type Person {
			email: String,
			items: [Item] @relation(name: "LINKED_TO", direction: "OUT")
			friends: [Person] @relation(name: "FRIEND_WITH", direction: "BOTH")
	   }
	   type Item {
		   id: Int,
		   people: [Person] @relation(name: "LINKED_TO", direction: "IN")
	   }
	')


We can check the schema we created with:

    CALL graphql.schema()


If you're not happy with it, you can still:

    CALL graphql.reset()


But let's try it out! For HTTP requests via the terminal, I use [httpie](https://httpie.org/), similar to `curl` but much intuitive and nicer.

First, let's write the query in `query.txt`:

	{ Person(email: "1a@gg.com") {
		email
		friends {
			email
		}
	  }
	}

Calling the API is then as simple as:

    http POST http://neo4j:admin@localhost:7474/graphql/ query=@query.txt

Which prints this nice JSON result:

	{
    "data": {
        "Person": [
            {
                "email": "1a@gg.com",
                "friends": [
                    {
                        "email": "5e@gg.com"
                    },
                    {
                        "email": "3c@gg.com"
                    },
                    {
                        "email": "2b@gg.com"
                    }
                ]
            }
        ]
    }
	}

You can customize the fields you want the API to return based on your specific needs.

But let's talk about recommendation now.


### Recommendation

If we were to write the Cypher query to retrieve items linked to friends of a given person, it would look like:


    MATCH (p:Person {email: "1a@gg.com"})-[:FRIEND_WITH]-(:Person)-[:LINKED_TO]->(j:Item) 
	WHERE NOT (p)-[:LINKED_TO]->(j) 
	RETURN j 

Adding this to our grqphQL schema is as easy as modifying the schema to add ` reco` field in the `Person` type:

		reco: [Item]
     	   @cypher(statement: "MATCH (this)-[:FRIEND_WITH]-(:Person)-[:LINKED_TO]->(j:Item) WHERE NOT (this)-[:LINKED_TO]->(j) RETURN j LIMIT 3")


The query could then look like:

	{ Person(email: "1a@gg.com") {
		email
		reco {
			id
		}
	  }
	}

Which brings:

	{
    "data": {
        "Person": [
            {
                "email": "1a@gg.com",
                "reco": [
                    {
                        "id": 1
                    },
                    {
                        "id": 5
                    },
                    {
                        "id": 4
                    }
                ]
            }
        ]
    }
	}

Many improvements can be done on this basic recommendation engine, taking into account how many friends are linked to the item, friends of friends... 

