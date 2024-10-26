---
title: "Assignment 3: Differential Privacy in Practice"
output: pdf
author:
 - "Timothée ZERBIB"
 - "[tzerbib@cs.brown.edu](mailto:tzerbib@cs.brown.edu)"
header-includes: |
    \usepackage [margin=25mm, foot=15mm] {geometry}
    \usepackage{mathtools}
    \usepackage{xcolor}
    \usepackage[onelanguage, ruled, lined]{algorithm2e}
    \newcommand\comment[1]{\footnotesize\ttfamily\textcolor{green}{#1}}


date: "\\today"
---

Every source used to generate this report, as well as all of its graphs,
are available on github.


# Part 1: Plain Aggregates and Privacy  

> *Question 1+2: Look at the result of this count query.
> Note that it does not include any name, email, or other
> personally identifiable information. What can you nevertheless
> learn about Kinan's musical tastes? What possible genres might
> they have chosen?
> Alternatively, what genres is it impossible for them to have chosen?*

Just by looking at the result of this query, we can gather some information
about Kinan.
First, Figure \ref{fig:heatmap-no-assump} gives us the probability
of his favorite music genre by age while not assuming anything about him.
With just this information, we are already able to say that it is
fairly improbable, although not impossible ($5\%$), that Kinan's favorite music
genre is Country. The most probable option so far would be Pop (almost $50\%$).

![Probability of Kinan's favorite music genre, supposing no external information\label{fig:heatmap-no-assump}](q1_heatmap_0_120.png){height=415px}

However, we can radically improve our result if we start making assumption
about Kinan's age. For instance, if we couple this table
with some public information like the fact that he received a Bachelor in 2015
(source: [https://www.babman.io/](https://www.babman.io/)), we can now only
look at the results of people that are 26 or older.
Figure \ref{fig:heatmap-26+} shows us the probability with this assumption made.
If it is correct, then we know that Kinan's favorite music is
not Country, nor House, or Hip Hop. Despite having reduced a lot the uncertainty,
we are still unable to figure Kinan's musical affinity with just that assumption.

![Probability of Kinan's favorite music genre, supposing that he is at least 26\label{fig:heatmap-26+}](q1_heatmap_26_120.png){height=300px}

Now that we have reduced the space of possible solutions, it could
potentially be more feasible to distinguish the good musical genre
from the others. One approach would be to reduce even more the set of
possible genre, by getting a closer approximation on his age (by looking
at more precise information that can be fond on internet, or by simply asking
him while he's to focus on eating to be suspicious).
By doing this, we could eliminate all except one option, letting us only with
Metal with a probability of $100\%$.

Funilly enough, we could actually do the contrary and guess Kinan's age
by coupling the result from this ``count`` query with some information of
his personnal website.
We can easily guess from Kinan's personnal website that his favorite music genre
is Metal (based on the fact that he had a Metal band, and that he says that
we can find him at Metal shows if not on his computer for instance, or
that while I cannot access Twitter without an account, I can see a profile
with as a description "Kinan Bab, Computer Scientist, PhD candidate,
Heavy Metal and Beer").
As only 2 people answered Metal, and their age differs quite
significantly, supposing that Kinan is more than 21 is enough to get his age.


> *Question 3: Identify Kinan's favorite color.
> What is it? How easy or obvious is this to do, and why? *

If we assume that we guessed correctly Kinan's age, then finding his favorite
color is child play.
A simple call to ``count`` to link ages and color gives us the right answer,
as there is only one 30-years-old-person in the dataset.

```bash
python3 client.py count age color | grep 30 | tr -d ' '
|30|Black|1|
```


## k-anonymity

> *Question 4+5: What information can you learn about Kinan's favorite sport
> from the query ``python3 client.py count agegroup sport``? *

By running this command over our dataset, we can figure out that Kinan's
favorite sport is either Basketball (p=0.667) or Soccer (p=0.333).

However, when we couple this information with data from last year (assuming that
Kinan's answer didn't change), as the answer where pretty different
(American Football: p=0.2, Soccer: p=0.2, and Esport: p=0.6), we can deduce
that Kinan's favorite sport is Soccer (with p=1) as it is the only sport
in common between those datasets for 25+ people.


# Part 2: Implementing Differential Privacy  


