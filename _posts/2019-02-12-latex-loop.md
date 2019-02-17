---
layout: post
title: "Using loops to simplify your LaTeX documents"
tags: latex
summary: pgffor package to use for loops in LaTeX
date: 2019-02-12 20:01:08:00
---

I often fall into the case where I want to create some slides showing the same plots for different scenarios, e.g. for different users. In those cases, you just need a coherent naming conventions for your plots, for instance:

    Figures/
	    1/
		    plot.png
			hist.png
		2/
			plot.png
			hist.png
	    ....
		10/
			plot.png
			hist.png

Then, the magic of `pgffor` enters into the game. Like in any other language (almost), you can use a `for` loop in a latex document. Minimal Working Example:

    \documentclass{beamer}
    \usepackage{pgffor}
 
    \begin{document}

    \foreach \n in {0,...,9}{
        \begin{frame}{Driver example \n }
			\begin{columns}
				\begin{column}{0.5\textwidth}\centering\small
				Plot \\
				\includegraphics[width=\textwidth]{Figures/\n /plot.png}
				\end{column}
				\begin{column}{0.5\textwidth}\centering\small
				Hist \\
				\includegraphics[width=\textwidth]{Figures/\n /hist.png}
				\end{column}
			\end{columns}
		\end{frame}
	}
 
	\end{document}

If even works for "list of strings":

    \foreach \n in {varibleA,
                    varB,
                    VariableC} {
        \n
    }

No more excuses to have the distribution of variable `A` on the slide named ` B`!


