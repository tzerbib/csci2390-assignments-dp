import requests
import traceback
import json
import sys

URL = "http://18.208.128.210:3000"

def help():
  print("This file exposes three functions: avg(...), count(...), and count0(...).")
  print("")
  print("1) avg(target, keys, dp): computes the average of the target column grouped by the given keys")
  print("      keys: list of strings: the columns to group the result by")
  print("      target: string: the column to compute the average over, must be a numeric column")
  print("      dp: boolean: True if the avg should be differentially private, False otherwise")
  print("")
  print("2) count(keys, dp): groupes the data by the given keys, and computes the count of submissions for each combination of those keys")
  print("      keys: list of strings: the columns to group by")
  print("      dp: boolean: True if the count should be differentially private, False otherwise")
  print("")
  print("3) count0(keys, dp): same as count, but excludes data points with age = 0")
  print("")
  print("The keys available are:")
  print("1) 'age': number: the age in years, 0 means unknown")
  print("2) 'agegroup': string: the age group")
  print("3) 'color': string: the favorite color")
  print("4) 'music': string: the favorite music genre")
  print("5) 'programming': string: how long has the person been programming")
  print("6) 'sport': string: the favorite sport")
  print("")
  print("You can import this file into your own python script using 'import client' and then use the above functions.")
  print("Alternatively, you can use run this file from the command line to explore the data , for example:")
  print(" $ python3 client.py count age music             # count per music and age")
  print(" $ python3 client.py dp count programming age    # count per programming and age with dp noise added")
  print(" $ python3 client.py dp avg age sport color      # average age per sport and color with dp noise added")


def _query(agg, keys, target, dp):
  query = {
    "agg": agg,
    "keys": keys,
    "target": target,
    "dp": dp
  }
  params = {"q": json.dumps(query)}
  response = requests.get(url=URL, params=params)
  if response.ok:
    return [tuple(row) for row in response.json()]
  raise ValueError("Error detected during query execution: {}".format(response.text))

def _pretty_print(headers, result):
  print("")
  row_format = "| " + ("{:<30}| " * len(headers))
  print(row_format.format(*headers))
  print("=" * (32 * len(headers)) + "=")
  for row in result:
    print(row_format.format(*row))
  print("=" * (32 * len(headers)) + "=")
  print("")

def avg(keys, target, dp):
  headers = tuple(keys) + ("AVG({})".format(target), )
  result = _query("avg", keys, target, dp)
  return headers, result

def count(keys, dp):
  headers = tuple(keys) + ("COUNT", )
  result = _query("count", keys, "", dp)
  return headers, result

def count0(keys, dp):
  headers = tuple(keys) + ("COUNT", )
  result = _query("count0", keys, "", dp)
  return headers, result


if __name__ == "__main__":
  arguments = sys.argv[1:]
  # Print help message
  if len(arguments) == 0 or arguments[0] == "help":
    help()
    sys.exit(0)

  # Execute query.
  try:
    dp = False
    if arguments[0] == "dp":
      arguments = arguments[1:]
      dp = True

    operation = arguments[0]
    if operation == "avg":
      target = arguments[1]
      keys = arguments[2:]
      headers, result = avg(keys, target, dp)
    elif operation == "count":
      keys = arguments[1:]
      headers, result = count(keys, dp)
    elif operation == "count0":
      keys = arguments[1:]
      headers, result = count0(keys, dp)
    else:
      print("Unrecognizable operation {}".format(operation))
      sys.exit(1)
  except ValueError as e:
    print(e)
    sys.exit(1)
  except Exception as e:
    print(e)
    traceback.print_exc()
    sys.exit(1)

  # Pretty print
  _pretty_print(headers, result)
