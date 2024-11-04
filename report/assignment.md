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

    \usepackage{listings}
    \definecolor{codegreen}{rgb}{0,0.6,0}
    \definecolor{codegray}{rgb}{0.5,0.5,0.5}
    \definecolor{codepurple}{rgb}{0.58,0,0.82}
    \definecolor{backcolour}{rgb}{0.95,0.95,0.92}

    \lstdefinestyle{mystyle}{
        backgroundcolor=\color{backcolour},
        commentstyle=\color{codegreen},
        keywordstyle=\color{magenta},
        numberstyle=\tiny\color{codegray},
        stringstyle=\color{codepurple},
        basicstyle=\ttfamily\footnotesize,
        breakatwhitespace=false,
        breaklines=true,
        captionpos=b,
        keepspaces=true,
        numbers=left,
        numbersep=5pt,
        showspaces=false,
        showstringspaces=false,
        showtabs=false,
        tabsize=2
    }

    \lstset{style=mystyle}

date: "\\today"
---

Every source used to generate this report, as well as all of its graphs,
are available on [github](https://github.com/tzerbib/csci2390-assignments-dp).


# Part 1: Plain Aggregates and Privacy  

> *Question 1+2: Look at the result of this count query.
> Note that it does not include any name, email, or other
> personally identifiable information. What can you nevertheless
> learn about Kinan's musical tastes? What possible genres might
> they have chosen?
> Alternatively, what genres is it impossible for them to have chosen?*

Just by looking at the result of this query, we can gather some information
about Kinan.
First, Figure \ref{fig:heatmap-music-no-assump} gives us the probability
of his favorite music genre by age while not assuming anything about him.
With just this information, we are already able to say that it is
fairly improbable, although not impossible ($5\%$), that Kinan's favorite music
genre is Country. The most probable option so far would be Pop (almost $50\%$).

![Probability of Kinan's favorite music genre, supposing no external information\label{fig:heatmap-music-no-assump}](age_music_heatmap_0_120.png){height=250}

However, we can radically improve our result if we start making assumption
about Kinan's age. For instance, if we couple this table
with some public information like the fact that he received a Bachelor in 2015
(source: [https://www.babman.io/](https://www.babman.io/)), we can now only
look at the results of people that are 26 or older.
Figure \ref{fig:heatmap-music-26+} shows us the probability with this assumption made.
If it is correct, then we know that Kinan's favorite music is
not Country, nor House, or Hip Hop. Despite having reduced a lot the uncertainty,
we are still unable to figure Kinan's musical affinity with just that assumption.

![Probability of Kinan's favorite music genre, supposing that he is at least 26\label{fig:heatmap-music-26+}](age_music_heatmap_26_120.png){height=250px}

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
$ python3 client.py count age color | grep 30 | tr -d ' '
> |30|Black|1|
```

The confidence in this result depends on the confidence in our guess of Kinan's
age. If we only assume that he his 26 or more instead of exactly 30,
the probability for Kinan's favorite color to be black drops to 66\%,
while red occupies 33\% of the possible answers, as shown
by figure \ref{fig:heatmap-color-26+}.

![Probability of Kinan's favorite color, supposing that he is at least 26\label{fig:heatmap-color-26+}](age_color_heatmap_26_120.png){height=300px}

Finally, if we did not make any assumption about Kinan, then the probabilities
for his favorite colors are far more spread (see figure \ref{fig:heatmap-color-no-assump})

![Probability of Kinan's favorite color, supposing no external information\label{fig:heatmap-color-no-assump}](age_color_heatmap_0_120.png){height=250px}


\newpage
## k-anonymity

> *Question 4+5: What information can you learn about Kinan's favorite sport
> from the query ``python3 client.py count agegroup sport``? *

By running this command over our dataset, we can figure out that Kinan's
favorite sport is either Basketball (p=0.667) or Soccer (p=0.333).

However, when we couple this information with data from last year (assuming that
Kinan's answer didn't change), as the answer where pretty different
(American Football: p=0.2, Soccer: p=0.2, and Esport: p=0.6), we can deduce
that Kinan's favorite sport is Soccer (with p=1) as it is the only sport
in common between those datasets for 25+ people (assuming Kinan also was in this
category last year, meaning that he his now at least 26).

If the only information we had about Kinan is that he his in the 25-30 category
this year, and that he did vote last year, then we would have to consider both
results of the 20-25 and 25-30 category for last year.


# Part 2: Implementing Differential Privacy  

## Sensitivity  

The sensitivity of the query ``count age music`` is exactly 1, as removing
any user from the dataset will reduce the count of one of the favorite genre
for this age group by 1.


## Laplace Distribution

> *Question 6: What happens when the privacy parameter grows larger or smaller?
> How does that affect privacy? *

The larger the privacy parameter $\epsilon$ and the less modified the results
are from the original non-dp-ed query, thus the lower the privacy.

This is due to the fact that $b$ parametrizes the shape of
the Laplace Probability Density Function. The lower $\epsilon$ is and the larger
$b=\frac{\mathit{sensitivity}}{\epsilon}$ is, which flattens the Laplace curve,
meaning that the range of values that the Laplace distribution would give us
with some probability is way larger than the one for a lower $b$, that induces
a way thiner Laplace distribution, that has most of it's values centered
around $\mu$.

![Laplace Probability Density Function\label{img:laplace-pdf}](laplace_pdf.png){height=260px}

Figure \ref{img:laplace-pdf} shows the 95% density of
Laplace Probability Density Function, for $\beta = 0.5$ ($\epsilon = 2$)
and $\beta = 2$ ($\epsilon = 0.5$), centered in $\mu=1$.
The parameters used for getting the 95\% are from WolframAlpha
(I did not solve the equation myself to verify their correctness).


## A note on Privacy

With a naïve implementation of Differential Privacy that just adds
noïse using the Laplace Distribution, users actually don't get deniability!


Listing \ref{lst:naive-1} shows a corresponding implementation of
this naïve approach. The output of a query using this implementation is shown
in listing \ref{out:naive-1}. As we can see, the exact count for each age seems
to be protected. However, the mere fact that the line appears in the output
actually gives us a lot of information. 
As we can see, there is only one music genre associated with people that are 30.
So even if we don't know the exact amount of people in this group,
the line appearing already tells us that at least one person is 30 and answered
"Metal". If we were able to guess Kinan's age by external means we could then
easily deduce what his favorite music genre is with probability 1.
And reversely, if we know that Kinan likes Metal, then we would know that he his
either 21 or 30 and deduce his age from here.  
This naïve implementation **does not** provide deniability to the users.

\begin{lstlisting}[language=Python, escapechar=ä, caption=Naïve implementation of DP, label={lst:naive-1}]
def dp_histogram(mu, b):
  # Get the exact histogram without noise.
  headers, rows = count(["age", "music"], False)

  # Iterate over counts and apply the laplace noise.
  noised_rows = []
  for (age, music, value) in rows:
    noised_value = round(value + laplace(mu, b))

    # Append the noised value and associated group by labels.
    noised_rows.append((age, music, noised_value))

  return headers, noised_rows
\end{lstlisting}


~~~ { .bash caption="Output of the query \texttt{count age music} using the naïve DP implementation" label=out:naive-1}
$ python3 dp.py
> Using epsilon = 0.5
> 
> | age             | music           | COUNT           |
> ======================================================
> | 0               | House           | 1               |
> | 20              | Country         | 6               |
> | 20              | Pop             | 1               |
> | 21              | Hip Hop         | 8               |
> | 21              | House           | 8               |
> | 21              | Metal           | 2               |
> | 21              | Pop             | 3               |
> | 21              | Rock            | 0               |
> | 22              | Hip Hop         | 7               |
> | 22              | Pop             | 1               |
> | 23              | Pop             | 1               |
> | 24              | Pop             | -1              |
> | 27              | Rock            | 1               |
> | 29              | Pop             | 3               |
> | 30              | Metal           | 0               |
> =======================================================
~~~


A better approach would be to not disclose any result that is negative or null.

Listing \ref{lst:naive-2} shows such an implementation and listing \ref{out:naive-2},
a possible corresponding ouput.
In this case, knowing that Kinan is 30 is not enough to deduce his favorite
musical genre, as his result could simply have been removed from the output
after the addition of some noise.

However, this solution is still not enough to fully bound the amount
of information that is released by this output. If for some reason we were able
to know that Kinan was the only individual to be 30 in the dataset,
and if it happens that there is a line corresponding to this age in the output
(like in listing \ref{out:naive-2}), then Kinan would have no deniability,
while we would learn his favorite genre, with probability 1.

\begin{lstlisting}[language=Python, escapechar=ä, caption=DP implementation that only shows positive results, label={lst:naive-2}]
def dp_histogram(mu, b):
  # Get the exact histogram without noise.
  headers, rows = count(["age", "music"], False)

  # Iterate over counts and apply the laplace noise.
  noised_rows = []
  for (age, music, value) in rows:
    noised_value = round(value + laplace(mu, b))

    # Append the noised value and associated group by labels.
    ä{\color{red}if noised\_value > 0:}ä
        noised_rows.append((age, music, noised_value))

  return headers, noised_rows
\end{lstlisting}


~~~ { .bash caption="Output of the query \texttt{count age music} using listing \ref{lst:naive-2} implementation" label=out:naive-2 }
$ python3 ../dp.py
> Using epsilon = 0.5
>
> | age             | music           | COUNT           |
> =======================================================
> | 20              | Pop             | 1               |
> | 21              | Hip Hop         | 4               |
> | 21              | House           | 1               |
> | 21              | Pop             | 5               |
> | 22              | Hip Hop         | 9               |
> | 27              | Rock            | 1               |
> | 30              | Metal           | 4               |
> =======================================================
~~~



In order to fully bound the amount of information that can be learn from
the output, we should consider all possible couple *age-music* and apply
some Laplace noise on all of them, including couples that were not originally
present in the dataset.

Listing \ref{lst:correct} shows such an implementation, and listing \ref{out:correct}
a possible corresponding output. In this scenario, Kinan has full deniability,
as even if we know his age, and even if he his the sole representent
in the dataset, we can not know if his information is displayed by this output.

Note that this implementation can still reveal some information about Kinan,
such as an upperbound on his age, but only with high probability (it is unlikely,
but theoretically possible that all values of people above 30 have been mixed
with negative noise). A possible solution to this problem is to also include
all couple age-music for all possible ages. A variant of this implementation
that modifies the age bound can be found in ``dp.py``.


\newpage
\vspace*{-2.5cm}
\begin{lstlisting}[language=Python, escapechar=ä, caption=(Hopefully) Correct DP implementation that considers all possibilities, label={lst:correct}]
def dp_histogram(mu, b):
  # Get the exact histogram without noise.
  headers, rows = count(["age", "music"], False)

  # Gather existing ages and info
  ä\textcolor{red}{ages = set()}ä
  ä\textcolor{red}{infos = set()}ä
  ä\textcolor{red}{for a,i,c in rows:}ä
    ä\textcolor{red}{ages.add(int(a))}ä
    ä\textcolor{red}{infos.add(i)}ä

  ä\textcolor{red}{ages = list(ages)}ä
  ä\textcolor{red}{ages.sort()}ä
  ä\textcolor{red}{infos = list(infos)}ä

  #  Generate all ages between the min (except 0) and max
  ä\textcolor{red}{min\_a = ages[0] if ages[0] > 0 else ages[1]}ä
  ä\textcolor{red}{ages = ([] if ages[0] > 0 else [0]) + [i for i in range(min\_a, ages[-1]+1)]}ä

  # Initialise the results with zeros
  ä\textcolor{red}{rows\_d = \{\}}ä
  ä\textcolor{red}{for e in product(ages, infos, [0]):}ä
    ä\textcolor{red}{rows\_d[(e[0], e[1])] = e[2]}ä

  # Update real values
  ä\textcolor{red}{for a,m,c in rows:}ä
    ä\textcolor{red}{rows\_d[(int(a),m)] = c}ä
  ä\textcolor{red}{sorted(rows\_d.items())}ä # Prevent leaking information by reordering

  # Iterate over counts and apply the laplace noise.
  noised_rows = []
  for ä\textcolor{red}{(age, music), value}ä in ä\textcolor{red}{rows\_d.items():}ä
    noised_value = round(value + laplace(mu, b))

    # Append the noised value and associated group by labels.
    if noised_value > 0:
      noised_rows.append((age, music, noised_value))

  return headers, noised_rows
\end{lstlisting}

~~~ { .bash caption="Output of the query \texttt{count age music} using listing \ref{lst:correct} implementation" label=out:correct }
$ python3 ../dp.py
> Using epsilon = 0.5
>
> | age             | music           | COUNT           |
> =======================================================
> | 0               | Metal           | 3               |
> | 0               | Hip Hop         | 1               |
> | 0               | Pop             | 3               |
> | 21              | House           | 1               |
> | 21              | Rock            | 1               |
> | 21              | Metal           | 1               |
> | 21              | Hip Hop         | 4               |
> | 21              | Pop             | 1               |
> | 22              | Country         | 1               |
> | 23              | Rock            | 3               |
> | 24              | Country         | 1               |
> | 24              | Rock            | 2               |
> | 25              | Rock            | 1               |
> | 26              | Country         | 1               |
> | 26              | Metal           | 1               |
> | 26              | Hip Hop         | 2               |
> | 27              | Metal           | 1               |
> | 27              | Hip Hop         | 1               |
> | 28              | Rock            | 1               |
> | 29              | House           | 2               |
> | 29              | Country         | 1               |
> | 29              | Metal           | 5               |
> | 29              | Hip Hop         | 5               |
> | 29              | Pop             | 1               |
> | 30              | Country         | 1               |
> =======================================================
~~~


> *Question 7: Look at the plot generated with privacy parameter epsilon = 0.5.
> What is the most likely value? What is the expected (i.e., average) value?
> How do they relate to the actual value (i.e., the query excuted
> without any noise via client.py)? How does the plot change for different
> values of the privacy parameter?*

Observed frequency counts of generated privacy preserving queries
are simetrical towards the real non-dp-protected value + $\mu$.
Thus, the expected value for a protected query is exactly
the initial value + $\mu$.

![Generated result for $\epsilon=2, \beta=0.5$](dp-plot_2.png){height=250px}
![Generated results for $\epsilon=0.5, \beta=2$](dp-plot_0.5.png){height=250px}
\begin{figure}[!h]
  \caption{Generated results for different value of $\epsilon$, and their corresponding Laplace PDF}
  \label{fig:dp-muli-epsilon}
\end{figure}

Figure \ref{fig:dp-muli-epsilon} shows the plots generated when using
a privacy parameter $\beta=0.5$ ($\epsilon=2$) and $\beta=2$ ($\epsilon=0.5$).
We can observe that the generated count frequency follows the Laplace
Probability Density Function pretty well (I increased the number of iterations
for the histogram to better follow the curve).
As the Laplace PDF gets wider with larger values of $\beta$, so does
the distribution of the generated results (and by extension,
the standard deviation). A lower value of $\epsilon$ (meaning a bigger value of
$\beta$) is thus translated into more privacy, as generated results are more
likely to be significantly different from the initial value.


# Part 3: Differential Privacy and Composition  

If we are able to make multiple calls to a DP database, as the expected value
is the initial value $+ \mu$, after sufficiently many calls, averaging
the result makes the noise cancel, and we can find the expected value
with high confidence.

Supposing that the $\mu$ chosen was 0, we can find a good approximation
of the actual average age by programming experience by averaging
multiple outputs of the query ``dp avg age programming``.
The results, shown in listing \ref{lst:dp-prog-age}, are not enough to let
us guess Kinan's programming experience.
However, we can observe that two of the categories have an average above 26.
We know from the previous queries that only 3 people are above 24, meaning that
at least two of them are in those groups. Thus, we can say that there are fair
chances for Kinan to have at least 8 years of programming experience.

Moreover, it is almost impossible for an average containing Kinan to be below 21,
and it requires a lot of the individuals for an average age of a sample
containing Kinan to stay below 22. Thus, it is highly improbable for Kinan's
programming experience to be between 3 and 8 years. A more advanced statistical
study (that does not only look at each average separately but all together)
could probably guess the exact programming experience of Kinan with a very good
probability, thanks to the knowledge of the exact set of ages and their count
contained in the dataset.

It is still important to note that whithout knowing $\mu$ nor $\epsilon$,
it seems pretty impossible to be fully confident in any result (Was the number
of iteration enough to get a decent average? How much is the average shifted
from the initial value?).


~~~ { caption="Average result of multiple calls to ``dp avg age programming``" label=lst:dp-prog-age }
| programming                   | AVG(age)                      | 
=================================================================
| 0-3 Years                     | 23.35                         | 
| 3-5 Years                     | 21.84                         | 
| 5-8 Years                     | 20.91                         | 
| 8-10 Years                    | 26.78                         | 
| More than 10 Years            | 26.46                         | 
=================================================================
~~~

Listing \ref{lst:dp-prog-age-count} shows the average result of calls to
``dp count0 programming``. As we can see, only 2 people answered having more than
10 years of programming experience, and 1 answered having between 8
and 10 years.

From this information, focusing only on people above 25, we can deduce that
the 27 person is the one who answered between 8 and 10 years (which was me),
Kinan answered "more than 10 years", and shared the answer with someone who is
around 23 (a social attack allowed me to confirm that Franklin
is the second person who answered having more than 10 years
of programming experience, confirming our results), and the person
being 29 probably answered between 0 and 3 years, and was averaged with
one 20 and one 21 person.


~~~ { caption="Average result of multiple calls to ``dp count0 programming``" label=lst:dp-prog-age-count }
python3 ../composition.py
TESTING: the two histograms should be (almost) equal.

Exposing count:
Making 200 queries with noise. This may take a minute...

| programming                   | COUNT                         | 
=================================================================
| 0-3 Years                     | 3.0                           | 
| 3-5 Years                     | 8.0                           | 
| 5-8 Years                     | 4.0                           | 
| 8-10 Years                    | 1.0                           | 
| More than 10 Years            | 2.0                           | 
=================================================================
~~~

So Kinan is a 30 year old PhD who likes Metal and black (and maybe Black Metal),
and who has over 10 years of programming experience.


> *Question 10: Does the class you implemented suffice to truly enforce
> that a dataset is never used beyond a certain privacy budget?
> Can developers intentionally or unintentionally over-use the dataset
> beyond the privacy budget? At a very high level, how would you design
> a different privacy budget enforcment mechanism that does not suffer
> these drawbacks?*

As long as every request to the service goes through this budget tracker,
then yes it enforces that the dataset is not used beyond a certain privacy
budget. However, nothing forces developers to actually go through the budget
tracker for their request to the dataset (as shown in ``BudgetTracker.py:49``).

One way of preventing this would be for developpers to not be able to
query the dataset without going through the budget tracker (e.g. by using
class privacy settings). Thus, if each query to the dataset has to go through
the budget tracker, it will correctly update the budget and deny any
access after a certain point.

Moreover, it is important to note that developpers can also uncorrectly set 
the budget, in which case, even if the budget tracks correctly the each
access to the dataset, the average of those accesses still might leak
sensitive informations.
