import numpy as np
import pandas as pd
import re

# parameters
dataFolder = "../data"
infilePrefix = "indiv_results_"
years = range(1959, 2017)
years.remove(1980)    # no IMO in 1980
outfile1 = "all_indiv_results_1981-2016.csv"
outfile2 = "all_indiv_results_1959-2016.csv"

# read in all the individual results by year
dfs = [(year, pd.read_csv(dataFolder + "/" + infilePrefix + str(year) + ".csv",
                   encoding="utf-8")) for year in years]

# add a year column to the DataFrames
for year, df in dfs:
    df.insert(0, 'Year', year)

# The competition format was standardised from 1981 onwards (to 6 questions of 7 points
# each). Before that, there could be 6 or 7 problems a year.
# We create 2 consolidated dataframes: The first just has data from 1981 onwards,
# while the second has data from the 1st IMO in 1959 onwards.

# FIRST DF: 1981 onwards
newdfs = [result for result in dfs if result[0] >= 1981]
indivResults1981Onwards = pd.concat([df for (year, df) in newdfs])

# clean-up some stray unicode characters
indivResults1981Onwards = indivResults1981Onwards.replace(re.compile(u"\xa7"), "")

# write out to file
indivResults1981Onwards.to_csv(dataFolder + "/" + outfile1,
                               index=False, encoding="utf-8")


# SECOND DF: 1959 onwards
# for years which only have 6 problems (i.e. 12 columns in total), we add a dummy column
# for P7.
for year, df in dfs:
    if len(df.columns) == 12:
        df.insert(9, 'P7', np.nan)

indivResults1959Onwards = pd.concat([df for (year, df) in dfs])

# clean-up some stray unicode characters
indivResults1959Onwards = indivResults1959Onwards.replace(re.compile(u"\xa7"), "")

# write out to file
indivResults1959Onwards.to_csv(dataFolder + "/" + outfile2,
                               index=False, encoding="utf-8")
