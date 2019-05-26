---
layout: post
title: "A comparison of centrality algorithms on the Zachary Karate Club"
tags: graph neo4j
summary: Node importance algorithms illustration using Zachary's karate club dataset.
date: 2019-05-26 18:00:00
---

Here is a short article to illustrate the various centrality algorithms implemented in the Neo4j graph algorithms library. We will run some of these algorithms on the famous Zachary's Karate Club (ZKC) dataset, using R for nice graph visualizations.

## Dataset

The ZKC dataset was collected by Mr. Zachary and represent the member of its university karate club. Mr. Zachary created an edge between two nodes/members if they do share another activity apart from karate.

In R, we can use the `igraph` library that contains several example graphs, among which the ZKC. We can simply load it like this:

```
library(igraph)
library(glue)

z <-graph.famous("Zachary")
```

First, let's plot the graph to see what we are talking about. Since we will draw it several times, and to ease the comparison between each plot, we want each node to be at the same location each time. That's why we are first defining a layout:

```
lay <-layout.fruchterman.reingold(z)
plot(z, layout=lay, vertex.label.cex=1.5, main="Zachary Karate Club graph")
```


Here is our graph!


Next, let me define some configuration. First the color scale that will be used to show the node importance, from yellow (low importance) to red (high importance) with 100 intermediate colors. Then we will compare here the relative importance of nodes with a given centrality, so we are going to use the `norm` function to normalize centralities.

```
nColors = 100
palette = colorRampPalette(c("yellow", "red"))(nColors)
norm <- function(x) {x / sqrt(sum(x^2))}
```

Centrality is a way to measure node importance. This importance definition depends on the question you are asking about your data. Several answers exist. Let check a few of them.

## Degree

Degree centrality simply count the number of edges for each node. It is a measure of the "populatiry" of a node in terms of relationships  (think of friends in social media or links between web pages).

```
deg=degree(z)
deg = norm(deg)
dlab = as.integer(deg * 100)
degCol =palette[as.numeric(cut(deg,breaks=nColors))]
plot(z,layout = lay, vertex.color=degCol, vertex.size=deg*100, vertex.label.cex=1.5, main="Degree")
```

In that plot, both the node size and color indicate the centrality value. With that definition, most important members in ZKC are labelled 33, 34 or 1.


## Closeness

The closeness centrality is a bit different since it measures the average shortest distance between a node and all other nodes in the graph. In some ways, it can be compared to the "geometrical" center of the graph.

```
clos=closeness(z)
clos = norm(clos)
clab = as.integer(clos * 100)
closCol =palette[as.numeric(cut(clos,breaks=nColors))]
plot(z,layout = lay, vertex.color=closCol, vertex.size=clos*100, vertex.label.cex=1.5, main="Closeness")
```

## Betweenness

Betweenness centrality is a measure of how many paths are using a node. It can be used to find the critical nodes in a network. By critical I mean the nodes which, if disabled, would create the more problems (traffic jam, downtime, information lost...)

```
btw=betweenness(z)
btw = norm(btw)
blab = as.integer(btw * 100)
btwCol = palette[as.numeric(cut(btw, breaks=nColors))]
plot.igraph(z, layout=lay, vertex.color=btwCol, vertex.size=btw*100, vertex.label.cex=1.5, main="Betweenness")
```


## Page rank

Last algorithm we are going to talk about in this post in the Page rank. It is named after Larry Page, one of google co-founders. The algorithm was created in order to rank the link on google result page. Now, the algorithms have evolved and are more complicated, but it's still interesting to understand the principles.

It can be summarized by the following formula:

$$
PR(A) = (1 - d) + d \times \sum_{n} \frac{PR(n)}{C(n)}
$$

where:

- PR(i) is the page rank value for page i
- n are the neighbours of page A
- d is a damping factor
- C(i) is the number of links for page i

You can see below the reult of the page rank algorithm with different values of the damping factor.

```
dampings = c(0, 0.2, 0.5, 0.85, 1)
for (d in rev(dampings)) {
  pr=page.rank(z, damping = d)
  pr = norm(pr$vector)
  lab = as.integer(pr * 100)
  prCol =palette[as.numeric(cut(pr, breaks=nColors))]
  plot.igraph(z,layout=lay, vertex.color=prCol, vertex.size=pr*100, vertex.label.cex=1.5, main=glue("Page Rank with damping : d = {d}"))
}
```

This is an overview of what you can learn in the course intitled "Exploring Graph Algorithms with Neo4j", keep watching if you want to know more!
