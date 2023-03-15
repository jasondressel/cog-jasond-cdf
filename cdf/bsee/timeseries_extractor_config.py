import pandas as pd
import os


def process(file:str):
    print(f"- path: {file}")
    print(f"  key-column: NA")
    print(f"  destination:")
    print(f"    database: bsee:timeseries:rawdb")
    print(f"    table: ogora")
  

def main():
    years = range(2022, 1995, -1)
    #years = range(2022, 2022, -1)
    cwd = os.getcwd()
    files = [f'{cwd}/cdf/bsee/data/timeseries/ogora{y}delimit.txt.csv' for y in years]
    files.insert(0, f'{cwd}/cdf/bsee/data/timeseries/ogoradelimit.txt.csv') # current year

    totalrows = 0
    for f in files:
        process(f)


if __name__ == "__main__":
   main()