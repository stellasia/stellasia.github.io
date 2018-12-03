---
layout: post
title: "Coding exercice: kind of morse code with errors"
category: python
summary: My solution to a coding exercice that was given to me a few times ago using graphs and recursion.
date: 2018-12-03 20:00:00
---

# Challenge

The challenge was the following:

Given a "morse" code following the rule describe on the image below:

![Challenge morse code](/img/posts/morse.png){:width="50%"}

For instance:

- "." = "E"
- ".." = "I"
- "-.-" = "K"

You will be given a "word" made of up to three symbols. Some symbols may be missing and replaced with a question mark "?". You have to determine all possible letters matching the word. For instance, if given "?", the program should return "['E', 'T']". For the input word ".?", it should return "['I', 'A']".

Wow wow wow. That was my first reaction. Then I thought of the work I have been doing on graphs for the past few weeks and the following idea came to my mind. 

# My solution

This exercice makes me think of a graph structure, with path search. So, I started by creating a graph, where each edge is defined by a starting node (letter at level l), ending node (letter at level l+1) and the symbol between them:

{% highlight python %}
DASH = "-"
POINT = "."

GRAPH = (
  # (node_start, link, node_end)
  (None, POINT, "E"),
  (None, DASH, "T"),
  ("E", POINT, "I"),
  ("E", DASH, "A"),
  ("I", POINT, "S"),
  ("I", DASH, "U"),
  ("A", POINT, "R"),
  ("A", DASH, "W"),
  ("T", POINT, "N"),
  ("T", DASH, "M"),
  ("N", POINT, "D"),
  ("N", DASH, "K"),
  ("M", POINT, "G"),
  ("M", DASH, "O")
)
{% endhighlight %}


## Exploring the graph with no missing letter

With this graph structure, you can see that, for instance, ".." corresponds to "None POINT 'E' POINT 'I'" = 'I'. Let's write the corresponding code to "read" the graph:

{% highlight python %}
def morse(word, node=None):
  if len(word) == 0:
    return None
  start = word[0]
  rest_of_word = word[1:] if len(word) > 1 else None
  for sn, e, fn in GRAPH:
    if (sn == node and e == start):
      if rest_of_word is not None: # continue exploring the graph for the rest of the word, staring from the current final node
          return morse(rest_of_word, fn)
      else: # if word iteration is done, the current final node is the result
        return fn
{% endhighlight %}


Code that can be tested with:

    if __name__ == "__main__":
        print(morse("..")) # 'I'


Here is a picture illustrating what is going on:

![Recursion illustration](/img/posts/recursion_expl.png){:width="80%"}


## Extending previous code to take into account missing letters

Our code should now return a list of possiblities instead of a single letter.  Here are the changes to the previous version in order to make it work:

{% highlight python %}
QUESTION = "?"

def morse2(word, node=None):
  if len(word) == 0:
    return [] # returns an empty list if no solution
  start = word[0]
  rest_of_word = word[1:] if len(word) > 1 else None
  possibilities = [] # the list that will store our final result
  for sn, e, fn in GRAPH:
    if (sn == node 
        and (start == e or start == QUESTION)): # change condition, we also consider this edge if the current letter is a question mark
      if rest_of_word is not None:
          ps = morse2(rest_of_word, fn) # our morse2 function returns a list of possibilities, that must all be taken into account in the final result
          possibilities.extend(ps)
      else:
        possiblities.append(fn)
  return possibilities
{% endhighlight %}


And, as usual, an example usage of this function:

    if __name__ == "__main__":
        print(morse2("?.")) # ['I', 'N']


Works like a charm! I love graphs!
