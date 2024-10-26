import sys
import os 

sys.path.append('../')
import client

import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np


DIR_PATH = os.path.dirname(os.path.realpath(__file__))


def q1_heatmap(min_age=0, max_age=120):
  header,results = client.count(["age", "music"], False)

  # Y axis
  styles = ["House", "Country", "Pop", "Hip Hop", "Metal", "Rock"]

  # Sorting results
  dict_res = {e: [] for e in styles}

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
  for s in styles:
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
  ax.set_yticks(np.arange(len(styles)))
  ax.set_yticklabels(styles)

  # Rotate the tick labels and set their alignment.
  # plt.setp(ax.get_xticklabels(), rotation=45, ha="right",rotation_mode="anchor")

  # Loop over data dimensions and create text annotations.
  for i in range(len(styles)):
    for j in range(len(ages)):
        text = ax.text(j, i, printed_res[i, j],
                       ha="center", va="center", color="w")
  
  # ax.set_title("Probability of prefered music genre by age")
  fig.tight_layout()

  # plt.show()
  
  plt.savefig(DIR_PATH + '/img/q1_heatmap_' + str(min_age) + '_' + str(max_age) + '.png')


if __name__ == "__main__":
  # Generate heatmap for question 1
  q1_heatmap()
  q1_heatmap(min_age=26)

  sys.exit(0)
