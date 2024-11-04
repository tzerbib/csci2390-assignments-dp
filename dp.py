from client import count, _pretty_print
from matplotlib import pyplot
from numpy import random
from itertools import product

import sys

# Return a random sample from laplace with mean/loc = mu and scale/spread b.
def laplace(mu, b):
  # TODO: implement laplace sampling or use numpy's laplace.
  return random.laplace(mu, b)

# Return a noised histogram that is epsilon-dp.
def dp_histogram(epsilon, keep_negative=True, bound_noise=0, min_bound=0, max_bound=120):
  # TODO: Find out the parameters for the noise distribution.
  sensitivity = 1
  mu = 0
  b = sensitivity/epsilon
  
  # Get the exact histogram without noise.
  headers, rows = count(["age", "music"], False)

  # Gather existing ages and info
  ages = set()
  infos = set()
  for a,i,c in rows:
    ages.add(int(a))
    infos.add(i)

  ages = list(ages)
  ages.sort()
  (null, min_a) = (False, ages[0]) if ages[0] > 0 else (True, ages[1])
  ages = [i for i in range(max(min_bound, min_a-bound_noise), min(max_bound, ages[-1]+bound_noise)+1)]
  ages = [0] + ages if null else ages
  infos = list(infos)

  # Initialise the results with zeros
  rows_d = {}
  for e in product(ages, infos, [0]):
    rows_d[(e[0], e[1])] = e[2]

  # Update real values
  for a,m,c in rows:
    rows_d[(int(a),m)] = c
  sorted(rows_d.items()) # Prevent leaking information by reordering

  # Iterate over counts and apply the laplace noise.
  noised_rows = []
  for (age, music), value in rows_d.items():
    # TODO: compute the noised value.
    # TODO: round the noised_value to the closest integer.
    noised_value = round(value + laplace(mu, b))

    # Append the noised value and associated group by labels.
    if keep_negative or noised_value > 0:
      noised_rows.append((age, music, noised_value))

  return headers, noised_rows

# Plot the frequency of counts for the first group
# (age 0 and Hip Hop).
def plot(epsilon):
  ITERATIONS = 150

  # We will store the frequency for each observed value in d.
  d = {}
  for i in range(ITERATIONS):
    headers, rows = dp_histogram(epsilon, True)
    # Get the value of the first row (age 0 and hip hop).
    value = round(rows[0][-1])
    d[value] = d.get(value, 0) + 1

  # Turn the frequency dictionary into a plottable sequence.
  vmin, vmax = min(d.keys()) - 3, max(d.keys()) + 3
  xs = list(range(vmin, vmax + 1))
  ys = [d.get(x, 0) / ITERATIONS for x in xs]

  # Plot.
  pyplot.plot(xs, ys, 'o-', ds='steps-mid')
  pyplot.xlabel("Count value")
  pyplot.ylabel("Frequency")
  pyplot.savefig('dp-plot.png')


# Run this for epsilon 0.5
if __name__ == "__main__":
  epsilon = 0.5
  if len(sys.argv) > 1:
    epsilon = float(sys.argv[1])

  print("Using epsilon =", epsilon)
  headers, rows = dp_histogram(epsilon, False, bound_noise=0)
  _pretty_print(headers, rows)

  # Plotting code.
  '''
  print("Plotting, this may take a minute ...")
  plot(epsilon)
  print("Plot saved at 'dp-plot.png'")
  '''
