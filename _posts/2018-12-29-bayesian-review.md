---
layout: post
title: "Bayesian statistics: short review of existing ressources"
tags: probability statistics bayesian
summary: A short non-exhaustive review on (online) books and tutorials about bayesian statistics
date: 2018-12-29 16:00:00
update: 2019-01-22 19:00:00
---


Bayesian analysis is something I have used during my PhD. During some recent research (holiday hobby), I came accross several very well written ressources on the web I want to share here.


# Key concepts

If you want to understand what is Bayesian analysis and why we need it, I particularly appreciate this video:

- [Introduction to Bayesian data analysis - part 1: What is Bayes?](https://www.youtube.com/watch?v=3OJEae7Qb_o) and next two parts. Video proposed by [Rasmus Bååth](http://sumsar.net/) with very clear highlight of the key concepts of bayesian data analysis. With simple examples, the author manages to make bayesian data analysis accessible.


# In-depth understanding


To go beyond those key concepts and understand how to use Bayesian analysis in real life, those two ressouces are a good start. Both show practical examples using [PyMC](https://github.com/pymc-devs/pymc) and/or [PyMC3](https://docs.pymc.io/).


- [Bayesian Methods for Hackers](http://camdavidsonpilon.github.io/Probabilistic-Programming-and-Bayesian-Methods-for-Hackers/): "online book" proposed by [Cameron Davidson-Pilon](https://dataorigami.net/). Written using jupyter notebook, this tutorial is well documented and easy to follow. The recommanded way to read the book is even to clone the repo to run the notebooks locally in order to be able to make changes and see the impact. You can see examples both with PyMC and PyMC3.
Note that a printed version exists, consider buying it if you like this work and can afford it.

- [Bayesian Analysis with Python](https://www.packtpub.com/big-data-and-business-intelligence/bayesian-analysis-python): this book has been written by [Osvaldo Martin](https://github.com/aloctavodia). Free version of the first edition are regularly made available from the publisher ([Free learning of the day offer](https://www.packtpub.com/packt/offers/free-learning/)). It has the advantage of being more exhaustive than the previous one.

- [Statistical Rethinking with Python and PyMC3](https://github.com/pymc-devs/resources/tree/master/Rethinking): again, those are jupyter notebooks based on the example written in the book "Statistical Rethinking". [Here](http://xcelab.net/rm/statistical-rethinking/) you can also find links to lecture material and videos.


# Tools

Beyond PyMC3 
The previous ressources already presented some tools to use bayesian analysis in real life examples. Here are some more:

- STAN and [PySTAN](https://pystan.readthedocs.io/en/latest/)
- A comparison between PyMC, STAN and a third package (Edward) can be found [here](https://statmodeling.stat.columbia.edu/2017/05/31/compare-stan-pymc3-edward-hello-world/)
- [ArviZ](https://arviz-devs.github.io/arviz/index.html) a powerfull library to create very interesting plots related to bayes analysis (compatible with both PyMC3 and PySTAN).


# Future

PyMC4 is already [in the pipes](https://github.com/pymc-devs/pymc4)! Main change is related to the deprecation of theano, used as backend to PyMC3.


Of course, there are many more ressources on the topic, I will update the list when I come accross a new interesting approach.


**UPDATE 2019-01-22** added reference to "Statistical Rethinking", STAN and ArviZ
