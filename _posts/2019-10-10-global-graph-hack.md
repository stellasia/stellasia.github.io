---
layout: post
title: "Global GraphHack 2019 and neomap project"
tags: neo4j graph
summary: The path to Global GraphHack 2019 featured project
date: 2019-10-10 18:08:08:00
---


## Global Graph Hack 2019

Last summer [Neo4j](http://neo4j.com) announced a fully remote hackathon to be held in September 2019. I had no clue what this will be about, nor whether I had the skills to join, but I decided to register and see what I could do there.

As expected, the theme was revealed begining of September as:

> The Theme: "Extending the Graph Ecosystem" 

> Your task is to build something using or extending Neo4j that can benefit others in the community.  It can be an extension of something that already exists or something completely new. Code and documentation must be shared and explained how it can be used by others. 


## neomap

### The idea

That's kind of broad! But also offers a lot of flexibility. I first thought about extending an algorithm from the graph algorithms library or playing around with embeddings since this is my first interest. But then I thought this would be useful to many people, and decided to go with something more related to visualization. In my past experiences, I had the opportunity to work with geodata, where being able to visualize this data on a map is fundamental.

Although all graphs do not have spatial attributes, geodata is part of Neo4j and I thought having a simple tool to visualize that kind of data would be useful to the community.

On top of that, the challenge was quite big for me, with poor experience with front-end. I did some CSS, a bit of Javascript from time to time, but no real experience with modern frameworks.

Nonetheless, let's try, and see what happens! In the worst case scenario, I would discover I have no talent for front-end and never try again.

### Development

So, I started by a quick search about the modern JS frameworks. As already stated above, I am not an expert, but I found React reusable components to be quite nice (that's probably not the only framework doing this though). So let's get started!

It took me some time to understand how `npm` works (not sure I've fully understood yet by the way...) but managed to have a first dummy working app.

I discovered a rich ecosystem and used several existing components like:

- [`react-bootstrap`](https://react-bootstrap.github.io/);
- [`react-leaflet`](https://react-leaflet.js.org/) for the map component itself;
- [Neo4j `base-app-kit`](https://github.com/neo4j-apps/graph-app-kit) of course, providing nice components to manage the Neo4j graph connection.

I confess the last one is the one I had to struggle more with... Still some work to do from me to fully understand why.


### Result

After this month of work during evenings and week-ends, I ended up with a working interface, allowing to show nodes with specific labels and latitude/longitude properties as markers or heatmap on a default Open Street Map base layer. Important to me was also the ability to be more flexible and allow the user to select the nodes to show directly with Cypher.

The demonstration video is available here:

<iframe width="560" height="315" src="https://www.youtube.com/embed/rhBG_crLMRM" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


### Follow-up

Many improvements can be done on this first project. I plan for instance to add support for:

- [neo4j-spatial](https://neo4j-contrib.github.io/spatial/) library;
- Relationships visualization;
- And more depending on your feedback!

If you want to try it, check the installation instructions on [github](https://github.com/stellasia/neomap/).

If you want to contribute (more than welcome), you can start by checking the list of [opened issues](https://github.com/stellasia/neomap/issues). If you think you can contribute to one of them, feel free to assign yourself and start coding!
