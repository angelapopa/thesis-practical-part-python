from dask import dataframe as dd
import os

import pandas as pd

# https://towardsdatascience.com/how-to-handle-large-datasets-in-python-with-pandas-and-dask-34f43a897d55
# https://dumps.wikimedia.org/other/clickstream/2018-12/

# Dask is a robust Python library for performing distributed and parallel computations.
# It also provides tooling for dynamic scheduling of Python-defined tasks(something like Apache Airflow).
# It’s tightly integrated with NumPy and provides Pandas with dataframe-equivalent structures — the dask.dataframes —
# that are based on lazy loading and can be used to perform dataframe operations in chunks and in parallel.
# It also automatically supports grouping by performing data shuffling under the hood.

# The dataset size is 1.4 Gb, so it carries significant risk of memory overload. That’s why I split the study into two parts.
# First, I implemented the analysis on a limited data subset using just the Pandas library.
# #Then I attempted to do exactly the same on the full set using Dask.

# The very first memory optimization step we can perform already at this point (assuming we know our table structure by now)
# is specifying the columns data types during the import (via the dtype= input parameter).
# That way, we can force Pandas to convert some values into types with a significantly lower memory footprint.
# That may not make much sense if you’re dealing with a few thousand rows, but will make a noticeable difference in a few millions!
# For example, if you know that a column should only have positive integers,
# use unsigned integer type (uint32) instead of the regular int type (or worse — float, which may sometimes happen automatically).

here = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(here, 'clickstream-enwiki-2018-12.tsv')

# read the data in with pandas
'''
df = pd.read_csv(filename,
                 delimiter="\t",
                 names=["coming_from", "article", "referrer_type", "n"],
                 dtype={"referrer_type": "category",
                        "n": "uint32"}
                 )
'''

# read the data in with pandas + dask
dfd = dd.read_csv(filename,
                  delimiter="\t",
                  names=["coming_from", "article", "referrer_type", "n"],
                  dtype={"referrer_type": "category",
                         "n": "uint32"},
                  blocksize=64000000  # = 64 Mb chunks
                  )


# Finally, let’s limit the data frame size to the first 100k rows for the sake of speed.
# Note that this is usually a bad idea
# when sampling a subset, it’s far more appropriate to sample every nth row to get as much uniform sampling as possible.
# But since we’re only using it to demonstrate the analysis process, we’re not going to bother:

# the panda way
#df = df.iloc[:100000]

# Q1: Which links do people click on most often in a given article?

# To answer this question, we need to create a table where we can see the aggregated sum of visitors per article and
# per source of origin(coming_from column).
# So, let’s aggregate the table over the article, the coming_from columns, sum up the ’n’ values,
# and then order the rows according to the ’n’ sums. Here’s how we approach it in Pandas:

# the panda way
'''
top_links = df.loc[
    df['referrer_type'].isin(['link']),
    ['coming_from', 'article', 'n']
]\
    .groupby(['coming_from', 'article'])\
    .sum()\
    .sort_values(by='n', ascending=False)
print(top_links)
'''

# ==== the panda + dask way
# this won’t do any calculations yet, the top_links_grouped_dask will be a Dask delayed dataframe object.
# We can then launch it to be computed via the .compute() method.
top_links_grouped_dask = dfd.loc[
    dfd["referrer_type"].isin(["link"]),
    ["coming_from", "article", "n"]]\
    .groupby(["coming_from", "article"])


# But we don’t want to clog our memory, so let’s save it directly to hard drive. We will use the hdf5 file format to do that.
# Let’s declare the hdf5 store then:
store = pd.HDFStore("clickstream_store.h5")

# And compute the data frame into it.
# Note that ordering column values with Dask isn’t that easy(after all, the data is read one chunk at a time),
# so we cannot use the sort_values() method like we did in the Pandas example.
# Instead, we need to use the nlargest() Dask method and specify the number of top values we’d like to determine:
top_links_dask = top_links_grouped_dask.sum().nlargest(20, "n")

# It too returns a delayed Dask object, so to finally compute it (and save it to the store) we run the following:
store.put("top_links_dask",
          top_links_dask.compute(),
          format="table",
          data_columns=True)
for k in store.keys():
    print(k)
print(store['top_links_dask'])

# end the panda and dask way

# the panda way (results)
'''
Cardi_B                                  Invasion_of_Privacy_(album)         28250
List_of_Bollywood_films_of_2018          Zero_(2018_film)                    24835
Rashida_Jones                            Kidada_Jones                        24616
Shah_Rukh_Khan_filmography               Zero_(2018_film)                    18435
Peggy_Lipton                             Kidada_Jones                        17483
...                                                                            ...
Campaigns_of_the_American_Civil_War      Battle_of_Spotsylvania_Court_House     10
George_Allen_(American_football_coach)   Pro_Football_Hall_of_Fame              10
FDI_World_Dental_Federation_notation     ISO_28000                              10
George_Allen_(American_football_coach)   Clark_Shaughnessy                      10
Victims_of_Communism_Memorial_Foundation Vladimir_Bukovsky                      10

[61104 rows x 1 columns]

'''

# the panda+dask way (results)
# In this case, the result is different from the values in the Pandas example since here we work on the entire dataset,
# not just the first 100k rows:
'''
coming_from       article
Jason_Momoa       Lisa_Bonet                             1166522
Priyanka_Chopra   Nick_Jonas                              596798
Bird_Box          Bird_Box_(film)                         508241
Nick_Jonas        Priyanka_Chopra                         493898
George_H._W._Bush George_W._Bush                          453809
Pauline_Robinson_Bush                   419132
Barbara_Bush                            412565
George_W._Bush    George_H._W._Bush                       393452
George_H._W._Bush Dorothy_Bush_Koch                       377785
Emily_Atack       Kate_Robbins                            354577
Macaulay_Culkin   Brenda_Song                             346110
George_H._W._Bush Marvin_Bush                             339241
Neil_Bush                               330132
Lisa_Bonet        Jason_Momoa                             321970
Bird_Box_(film)   Trevante_Rhodes                         309028
Penny_Marshall    Tracy_Reiner                            281911
George_H._W._Bush Prescott_Bush                           253973
Welcome_to_Marwen Marwencol_(film)                        253955
Lisa_Bonet        Zoë_Kravitz                             250392
2.0_(film)        List_of_highest-grossing_Indian_films   249322
'''
