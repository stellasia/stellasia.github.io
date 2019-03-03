---
layout: post
title: "Neo4j: use an existing graph"
tags: graph neo4j
summary: You can directly use an existing graph db in your local environment.
date: 2019-03-03 10:00:00
---

Usually, data comes from in CSV format, in which case you can use cypher `LOAD CSV` statement or the neo4j import tool if the csv is large. But sometimes, you can directly find the graph data in neo4j format. Here is how to "import" this kind of data in your local environment.

I recommand using the [Neo4j desktop application](https://neo4j.com/developer/neo4j-desktop/) which easily allows creating and managing several databases.

In this application, you can create a graph DB, choosing the Neo4j version you want to use. In this example, I created a graph `Graph_Tutorial_1` using Neo4j 3.5.3.

![Neo4j desktop!](/img/posts/neo4j_desktop.png){:width="100%"}

From there, you can click on `Manage`. A new view appears when you can see the details, logs, manage settings and plugins.

The two important tabs to import a new graph are `Terminal`, and possibly `Settings`.

In the `Terminal` tab, you can:

    cd data/databases
	
the default path to the graph db. If the db has never been started, this folder is empty, otherwise it contains the `graph.db` folder, which is the main data folder of Neo4j (default setting). If such a folder exists, rename it. Then create an empty `graph.db` folder.

Then, we need to download some data. In this example, I use the [credit card fraud dataset](https://www.dropbox.com/s/4uij4gs2iyva5bd/credit%20card%20fraud.zip) (linked from [here](https://neo4j.com/graphgist/credit-card-fraud-detection)). You can now extract the zip file into the `graph.db` directory you have just created.

Once this is done, try starting the graph (Start/Play button at the top). 

If an error appears, that mean that you are using a most up-to-date version of Neo4j than the one used to create the data. We will just tell Neo4j it can upgrade the data for us. For this, ensure your database is stopped and go to the `Settings` tab in your graph management view and add this line:

    dbms.allow_upgrade=true
	
Then start again your database and everything should be working just fine.
