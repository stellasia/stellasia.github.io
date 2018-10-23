---
layout: post
title: "My first hackthon"
category: misc
summary: Thoughts about my participation in the lux4good hackthon
date: 2018-10-23 21:00:00
---

You know hackathon, those events where you are asked to code, just code for at least 24 hours non stop? Well, this is not exactly how it works, but this was my impression before last week. With this image in mind, I was not really enthousiast in joining such an event.

But during last summer, I heard about the [lux4good hackthon](http://lux4good.org/), and a friend of mine convinced me to try. I was mainly convinced by the hackathon topic (not yet another "develop a mobile app" thing). The idea was to work on a project related to social, environmental or other topic classified in the "non-lucrative" "good" area.

In praticse, I register with a team of 5 other person, mainly data scientists, hence the team name #nodata.

About two weeks before the opening, we received a list of subjects and were asked to provided an ordered list of three topics we would like to work on. Each team was then assigned a project based on this choice. We got out first choice: creation of a dashboard for companies to measure and monitor diversity among their employees, supported by [IMS Luxembourg](http://imslux.lu/). 

The project owner sent us some documentation about the project to us shortly after project awarding, but frankly, none of us really had the time to study them. Fortunately, our PO was able to attend the first part of the hackathon on Friday evening, and we could discuss with her about her expectations and better define what we could do for this project, which was really helpful!

After a moment of hesitation, each of us took a piece of work: in our data-oriented team, only two or three of us knew enough of front-end to start development for the final demonstration, and I was part of them. We choose django as baseline, but after rethinkning about it, I think it was not the best choice, too complicated, especially because in the end, none of the view was really linked to a model, for the demonstration we chose to only use hard coded values.

Anyway, it was quite funny to start a django website structure in a few hours. When we left the hackathon location around 11pm on Friday, the site structure was ready, including static loading with the development server.

We turned back on the Saturday morning around 8am. After a good and generous dinner the day before, we had a good and generous breakfast!

The other part of the team had already started thinking about the pages that should be created on our website, so we could continue working on this. After lunch (good and....), we decided to continue the devs until 3pm, in order to focus on the pitch and demonstration after that.

I forgot to mention, there was a kind of additionnal stress for this event due to the jury composition: SAR Grand Duchess of Luxembourg was part of it, together with the "Ministre du travail", important people here in Luxembourg.

The pitch. A five-minute speech to explain the project, the problem and how our solution would help solving it. I did not talked much about the project so far. IMS faced several challenges:

1. Measure diversity inside companies. Diversity in terms of gender, race, religion, disabled people, age...
2. Provide clear indicators to these companies in order for them to know how good/bad they are with respect to a national mean and/or with respect to other companies of comarable size;
3. Encourage companies to take actions to improve these indicators;
4. Provide tools to each company to follow the evolution;
5. Be able to extract some global stats for IMS.

Relying on an existing pdf form, we created an interactive form through a website. From the answers, we proposed to quantify the diversity thanks to a radar/spider chart with different axes representing a kind of diversity. To incite companies to take actions, two axes were proposed:
- Gamification: companies could be given badges (bronze, silver, gold) for genre, age... diversity;
- Action definition and follow-up: companies can define some actions to improve their ranking (eg, hire at least four women within one year). The impact of the action should be visible on an "expected radar chart after action is completed".

After the actions are marked as completed, we can change the company's indicators, without having to fill the initial form again.

This is the message that we tried to convey during the speech. And seems like it worked since we got the second price!

Beside the result, I will mainly remember from this experience the team work and how we managed to get organized quickly.

I hope the ideas developped here will give birth to something interesting and that will actually move the lines.

Before finishing, I have to say a big thanks to the organizers (we had all information on time, everthing was great!), the project owner and my amazing team mates!

The github repo for this hackathon can be found [here](https://github.com/stellasia/l4gims) (forked from [this one](https://github.com/remil1000/l4gims), thanks Remi!).
