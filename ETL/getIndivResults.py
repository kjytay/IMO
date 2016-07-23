import urllib2
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import os
import re

def getIndivResultsForYear(year):
    """Returns the individual IMO results for the provided year as a
    pandas dataframe."""

    url = "http://www.imo-official.org/year_individual_r.aspx?year=" + str(year)
    html = urllib2.urlopen(url)
    soup = BeautifulSoup(html, "lxml")

    # get the table
    table = soup.table

    # get column names
    colNames = [th.text for th in table.tr.findAll("th")]

    # clean up the field names: only keep alphanumeric characters
    colNames = [re.sub("[^A-Za-z0-9]", "", col) for col in colNames]

    # get data
    rows = table.findAll('tr')
    data = [[td.text for td in tr.findAll("td")] for tr in rows]
    data.pop(0)  # this is to remove data from the header row

    # put data & column names into a pandas dataframe
    df = pd.DataFrame(data, columns = colNames)

    return df


if __name__ == "__main__":

    dataFolder = "../data"
    outfilePrefix = "indiv_results_"
    # If not already created, create a "data" folder
    if not os.path.exists(dataFolder):
        os.mkdir(dataFolder)

    # Years in which the IMO has been held thus far: 1959-2016 (except 1980).
    # The competition format was only standardised in 1981; before that,
    # the number of questions varied from year to year.
    years = range(1959, 2017)
    years.remove(1980)

    for year in years:
        df = getIndivResultsForYear(year)
        df.to_csv(dataFolder + "/" + outfilePrefix + str(year) + ".csv",
                  index=False, encoding="utf-8")
