import sys
import os 

sys.path.append('../')
import client
import dp

import matplotlib.pyplot as plt
from matplotlib import colors, pyplot
import numpy as np


DIR_PATH = os.path.dirname(os.path.realpath(__file__))
IMG_PATH = DIR_PATH + '/img/'


def age_count_heatmap(group_name, group_elem, min_age=0, max_age=120):
  header,results = client.count(["age", group_name], False)

  # Sorting results
  dict_res = {e: [] for e in group_elem}

  ages = []
  n = 0

  for (age, style, count) in results:
    if int(age) >= min_age and int(age) <= max_age and count > 0:
      dict_res[style].append((age,count))
      ages.append(age)
      n += count


  # Filtering x axis
  ages = list(set(ages))
  ages = [int(e) for e in ages]
  ages.sort()

  # Adding a total column
  ages.append("Total")

  # Gathering all results in one table
  printed_res = []
  for s in group_elem:
    sl = []
    age_per_style = dict_res[s]
    age_total = 0
    for a in ages[:-1]:
      found = False
      for (age, nb) in age_per_style:
        if a == int(age):
          p = round(nb/float(n), 3)
          sl.append(p)
          age_total += p
          found = True
      if found == False:
        sl.append(0)
    sl.append(age_total)
    printed_res.append(sl)

  printed_res = np.array(printed_res)

  fig, ax = plt.subplots()
  im = ax.imshow(printed_res)


  # Show all ticks and label them with the respective list entries
  ax.set_xticks(np.arange(len(ages)))
  ax.set_xticklabels([str(e) for e in ages])
  ax.set_yticks(np.arange(len(group_elem)))
  ax.set_yticklabels(group_elem)

  # Rotate the tick labels and set their alignment.
  # plt.setp(ax.get_xticklabels(), rotation=45, ha="right",rotation_mode="anchor")

  # Loop over data dimensions and create text annotations.
  for i in range(len(group_elem)):
    for j in range(len(ages)):
        text = ax.text(j, i, printed_res[i, j],
                       ha="center", va="center", color="w")
  
  # ax.set_title("Probability of prefered music genre by age")
  fig.tight_layout()

  plt.savefig(IMG_PATH + 'age_' + group_name + '_heatmap_' + str(min_age) + '_' + str(max_age) + '.png', bbox_inches='tight')


from scipy.stats import laplace
from math import log
def lp(mus=[0], betas=[0.5], xmin=-10, xmax=10):
  x = np.linspace(xmin, xmax, 10000)

  fig, ax = plt.subplots()

  for mu, beta in zip(mus, betas):
    dist = laplace(mu, beta)
    # plot the Probability Density Function of x
    plt.plot(x, dist.pdf(x), label=r'$\mu=%i,\ \beta=%.1f$' % (mu, beta))

    #Fill under the curve
    plt.fill_between(
      x=x,
      y1=dist.pdf(x),
      where=(x>mu-beta*(2*log(2)+log(5))) & ((x<mu+beta*(2*log(2)+log(5)))),
      # color="b",
      alpha=0.2
    )

  plt.xlim(xmin, xmax)
  plt.ylim(0, 1.0)

  plt.xlabel('x')
  plt.ylabel(r'$p(x|\mu,\beta)$')

  plt.legend()
  
  plt.savefig(IMG_PATH + 'laplace_pdf.png', bbox_inches='tight')


def frequencies(n, epsilon, sensitivity=1):
  # We will store the frequency for each observed value in d.
  d = {}
  for i in range(n):
    headers, rows = dp.dp_histogram(epsilon, True)
    # Get the value of the first row (age 0 and hip hop).
    value = round(rows[0][-1])
    d[value] = d.get(value, 0) + 1

  # Turn the frequency dictionary into a plottable sequence.
  vmin, vmax = min(d.keys()) - 3, max(d.keys()) + 3
  xs = list(range(vmin, vmax + 1))
  ys = [d.get(x, 0) / n for x in xs]

  initial_value = value

  # Plot observed values
  pyplot.plot(xs, ys, 'o-', ds='steps-mid', label="Observed frequency")
  pyplot.xlabel("Count value")
  pyplot.ylabel("Frequency")

  # Plot laplace pdf
  x = np.linspace(vmin, vmax, 1000)
  dist = laplace(initial_value, sensitivity/epsilon)
  plt.plot(x, dist.pdf(x), label=r'Laplace PDF, $\mu=%i,\ \beta=%.1f$' % (initial_value, sensitivity/epsilon))

  plt.ylim(0, 1.0)
  plt.legend()
  plt.show()
  # pyplot.savefig(IMG_PATH + 'dp-plot_' + str(epsilon) + '.png')


if __name__ == "__main__":
  # Generate heatmap for question age/music
  # styles = ["House", "Country", "Pop", "Hip Hop", "Metal", "Rock"]
  # age_count_heatmap(group_name="music", group_elem=styles)
  # age_count_heatmap(group_name="music", group_elem=styles, min_age=26)

  # Heatmap for age/color
  # colors = ["Green", "Red", "Yellow", "Black", "Blue"]
  # age_count_heatmap(group_name="color", group_elem=colors)
  # age_count_heatmap(group_name="color", group_elem=colors, min_age=26)

  # Plot Laplace distribution
  # lp(mus=[1, 1], betas=[0.5, 2])

  # Plot observed frequencies
  # ns = [600,300]
  # epsilons = [0.5, 2]
  # for n,e in zip (ns, epsilons):
  #   print("Plotting for n=%i and e=%.1f ..." % (n,e))
  #   frequencies(n, e)

  sys.exit(0)
