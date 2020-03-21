---
layout: post
title: "Data scientist duties"
tags: data
summary: Thoughts about ethical AI and the role of data scientists
date: 2020-03-21 11:00:08:00
---


"Responsible AI" has been around for quite  a long time. Today, all big companies provide advices and best practices to use AI in a ethical way. As an example, you can take a look at the recommendations from those big tech companies:

- [Google](https://ai.google/responsibilities/responsible-ai-practices/)
- [Microsoft]https://www.microsoft.com/en-us/ai/responsible-ai()

Other initiatives have also arisen from the large community of data scientists over there.

It also comes with by new laws, fixing the limits of data usage to respect user's privacy (GDPR in Europe in provably the most famous example).

Looking into all these ressources, it seems to me that, as a Data Scientist, I have a role to play in this area. I have extracted two important points that, in my opinion, are fully under the responsability of each data scientist; awarness and teaching.


## Awareness

We are living in a fantastic era. Thanks to computers and the very smart people programming them, we are able to achieve incredible results and help many people in their day to day life (e.g. document automatic classification), healthcare (cancer detection), mobility (semi-autonomous cars are already there!), leisure and so on and so forth.

But, as we all know, the best models is the world has its own limits. It is our **duty**, as people producing these models, to be **aware** of these limitations. Each part of the data pipeline, from the data collection to the model performance evaluation can be somehow biased. 


### Data, range and extrapolation

Long before machine learning becomes so popular, every scientists already knew that observing a linear relation between two variables X and Y for X ranging from 10 to 20 does not mean that this relation will still be true for X=60. THe same holds for machine learning model: depending on the training data, the range of validity of the model is reduced.

The same idea is probably responsible for the under average performances of face recognition models when it comes to black people ([source](https://www.nist.gov/news-events/news/2019/12/nist-study-evaluates-effects-race-age-sex-face-recognition-software)). The train dataset does not cover this part of the population, and the algorithm cannot learn without examples.


### Model

Even with the perfect dataset, covering all your target valuees, each model is **never** 100% accurate. For instance, because some features have to be left apart or are simply not accessible. In any case, the model performances have to be **properly** measured. I say "properly" because I still see too often people reporting 90% accuracy on a classification problem with heavily imbalanced datasets for instance. This performance metric is obviously unfair and do not encapsulate well the real felt performances.


### Impact

I think it is crucial for data scientists to be aware of the consequences of their work. What happens if the model is wrong?

Will simply a document be misclassified or an important refund refused because the proof was not found?

Will someone have to wait 15 more minutes for his pizza, or ambulances blocked in a terrible traffic jam that was not anticipated?

The consequences of course do not only depends on us, and that's why the next topic is almost as important as this one. When such a bias is identified and, ideally, quantified, we can not keep it for ourselves, I think we have the duty to explain to all the involved people the above mentioned caveats about the particular usage of AI you want to implement.



## Teaching

Once you manage to define the model limitations, even if small, it is important and even crucial that they are communicated in a clear way to both the management and the person that will use this new feature. In both cases, it will save you hours of headache trying to explain to the management why your model can not make coffee and to the end user why it is not 200% accurate. Be proactive!

... and communicate and repeat until it is understood again and again and again.


### To your pairs

You are maybe not the only data scientist in your company and probably not the only data scientit in the world working on your current topic. If you discover a bias in your data or an algorithm, it is important to communicate this finding to all of them, not only because you are a team, but because each of the team member has the same role of educating non-expert, and they should be all aligned to deliver the same message.

Think also that other people might have ideas to quickly reduce the bias, without extra cost. Think for instance of the under-sampling technique to reduce the impact of imbalanced dataset in classification tasks.


### To decision makers

Of course decision makers have to be aware of the limitations as well. The ones deciding to use a given algorithm in production should know everything about the pros and cons. That's why, we, as data scientists, need to provide accurate metrics to quantifiy model performance, the range of validity and the impact of the final users. 

### To final users

That's something I do not see very often as a final user myself in most of the cases. Companies tell me they have this new fantastic feature that will totally make my life easier, but they never tell me in which cases. I am probably totally biased here, but I think we could avoid so many critism, doubts and pseudo-scandals related to AI by a better vulgarization. Yes, an image classification algorithm can not be 100% accurate (so far) and yes sometimes a cookie will be identifed as a dog, or the other way around.

![Chihuahua or muffin](https://external-preview.redd.it/BVA08vSHxrSC4B0sGBtrGM6q7sBzbhUluvr7SFmYzhM.jpg?auto=webp&s=fbfd6a93e1f4d982f79f31d33cd12fa7a83f7be3)

That's also where the quantification of the consequences of a misclassification are important and needs to be communicated to the users. Transparency is important and processes allowing them to report a mistake from the algortihm might be considered.


## Summary

I want to repeat here that I am not against AI or progess in general, I am a data scientist myself and proud of it. But I truly believe that to make the future of AI as beautiful as we can imagine, these steps are crucial. I hear so many times comments like "Facebook moderation system is shit, it accepts this picture but not this artwork" or "Image recognition doesn't work, it can recognize a dog from a cookie!". If we want public opinion to support the progress, tell them that there will still be jobs for them in the future, we have to explain and explain and explain again. And for this, we need to have a personal and unbiased (as much as possible) thinking about the consequences of our work.

Then, everyone has its own ethics, and it is up to you and your conscience to decide if a loan request has to be rejected because some of the buyer's friends have had some unemployment issues in the past.

Thank you for reading, hoping this brings some food for thought!



## Ressources

- [RESPONSIBLE ARTIFICIAL INTELLIGENCE by Prof. Dr. Virginia Dignum](https://ec.europa.eu/jrc/communities/sites/jrccties/files/03_dignum_v.pdf)

- Extra reading for French-speaking readers:
    - [Serment d'Hippocrate pour Data Scientist](https://hippocrate.tech/)
