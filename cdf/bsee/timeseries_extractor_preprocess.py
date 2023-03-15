import pandas as pd
import os


def LoadFile(file:str):
    dataFrame = pd.read_csv(file, dtype=str, encoding='latin1', header=None)
    dataFrame.columns = [
        "LEASE_NUMBER",
        "COMPLETION_NAME",
        "PRODUCTION_DATE",
        "DAYS_ON_PROD",
        "PRODUCT_CODE",
        "MON_O_PROD_VOL",
        "MON_G_PROD_VOL",
        "MON_WTR_PROD_VOL",
        "API_WELL_NUMBER",
        "WELL_STAT_CD",
        "LEASE_AREA_BLOCK",
        "OPERATOR_NUM",
        "SORT_NAME",
        "FIELD_NAME_CODE",
        "INJECTION_VOLUME",
        "PROD_INTERVAL_CD",
        "FIRST_PROD_DATE",
        "UNIT_AGT_NUMBER",
        "UNIT_ALOC_SUFFIX"
    ]

    numRows = len(dataFrame.index)
    print(f'{file} Num Rows: {numRows}')
    filename = file.split('/')[-1]

    csv_file = file+".csv"

    dataFrame.to_csv(csv_file, sep=',', index=False)

    return numRows


def main():
    years = range(2022, 1995, -1)
    #years = range(2022, 2022, -1)
    cwd = os.getcwd()
    files = [f'{cwd}/cdf/bsee/data/timeseries/ogora{y}delimit.txt' for y in years]
    files.insert(0, f'{cwd}/cdf/bsee/data/timeseries/ogoradelimit.txt') # current year

    totalrows = 0
    for f in files:
        totalrows = totalrows + LoadFile(f)

    print(f"TOTAL ROWS {totalrows}")

if __name__ == "__main__":
   main()