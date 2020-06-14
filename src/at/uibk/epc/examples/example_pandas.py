import folium
from folium import plugins
import matplotlib.pyplot as plt
import datetime
import numpy as np
import pandas as pd
import ijson
import os

# https://www.dataquest.io/blog/python-json-tutorial/
# ijson will iteratively parse the json file instead of reading it all in at once.
# This is slower than directly reading the whole file in, but it enables us to work with large files that can’t fit in memory.
# To use ijson, we specify a file we want to extract data from, then we specify a key path to extract:

here = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(here, 'md_traffic.json')

with open(filename, 'r') as f:
    objects = ijson.items(f, 'meta.view.columns.item')
    columns = list(objects)

# we should see {'renderTypeName': 'meta_data', 'name': 'sid', 'fieldName': ':sid', 'position': 0, 'id': -1, 'format': {}, 'dataTypeName': 'meta_data'}
# print(columns[0])

column_names = [col["fieldName"] for col in columns]
# print(column_names)

# Extracting the data
# You may recall that the data is locked away in a list of lists inside the data key. We’ll need to read this data into memory to manipulate
# it. Fortunately, we can use the column names we just extracted to only grab the columns that are relevant. This will save a ton of space.
# If the dataset was larger, you could iteratively process batches of rows. So read in the first 10000000 rows, do some processing,
# then the next 10000000, and so on. In this case, we can define the columns we care about, and again use ijson to iteratively process the JSON
# file: )

good_columns = [
    "date_of_stop",
    "time_of_stop",
    "agency",
    "subagency",
    "description",
    "location",
    "latitude",
    "longitude",
    "vehicle_type",
    "year",
    "make",
    "model",
    "color",
    "violation_type",
    "race",
    "gender",
    "driver_state",
    "driver_city",
    "dl_state",
    "arrest_type"]
data = []
with open(filename, 'r') as f:
    objects = ijson.items(f, 'data.item')
    for row in objects:
        selected_row = []
        for item in good_columns:
            selected_row.append(row[column_names.index(item)])
            data.append(selected_row)

# reading the data into pandas
# Now that we have the data as a list of lists, and the column headers as a list, we can create a Pandas Dataframe to analyze the data.
# If you’re unfamiliar with Pandas, it’s a data analysis library that uses an efficient, tabular data structure called a Dataframe to represent
# your data. Pandas allows you to convert a list of lists into a Dataframe and specify the column names separately.
stops = pd.DataFrame(data, columns=good_columns)

# Now that we have our data in a Dataframe, we can do some interesting analysis.
# Here’s a table of how many stops are made by car color:
# print(stops["color"].value_counts())
# print(stops["arrest_type"].value_counts())

# Converting columns
# We’re now almost ready to do some time and location based analysis, but we need to convert the longitude, latitude,
# and date columns from strings to floats first. We can use the below code to convert latitude and longitude:


def parse_float(x):
    try:
        x = float(x)
    except Exception:
        x = 0
    return x


stops["longitude"] = stops["longitude"].apply(parse_float)
stops["latitude"] = stops["latitude"].apply(parse_float)


def parse_full_date(row):
    date = datetime.datetime.strptime(row["date_of_stop"], "%Y-%m-%dT%H:%M:%S")
    time = row["time_of_stop"].split(":")
    date = date.replace(hour=int(time[0]), minute=int(
        time[1]), second=int(time[2]))
    return date


stops["date"] = stops.apply(parse_full_date, axis=1)

# We can now make a plot of which days result in the most traffic stops:
#figDays = plt.hist(stops["date"].dt.weekday, bins=6)
# plt.savefig("figDays.png")

# We can also plot out the most common traffic stop times:
#figHours = plt.hist(stops["date"].dt.hour, bins=24)
# plt.savefig("figHours.png")

# Subsetting the stops
# Now that we’ve converted the location and date columns, we can map out the traffic stops.
# Because mapping is very intensive in terms of CPU resources and memory, we’ll need to filter down the rows we use from stops first:
last_year = stops[stops["date"] >
                  datetime.datetime(year=2015, month=2, day=18)]

# In the above code, we selected all of the rows that came in the past year. We can further narrow this down, and only select rows that occurred during rush hour — the morning period when everyone is going to work:
morning_rush = last_year[(last_year["date"].dt.weekday < 5) & (
    last_year["date"].dt.hour > 5) & (last_year["date"].dt.hour < 10)]
# print(morning_rush.shape)  # 2787280, 21
# print(last_year.shape)  # 21483500, 21

# Using the excellent folium package, we can now visualize where all the stops occurred.
# Folium allows you to easily create interactive maps in Python by leveraging leaflet.
# In order to preserve performance, we’ll only visualize the first 1000 rows of morning_rush:
stops_map = folium.Map(location=[39.0836, -77.1483], zoom_start=11)
marker_cluster = folium.plugins.MarkerCluster().add_to(stops_map)
for name, row in morning_rush.iloc[:1000].iterrows():
    folium.Marker([row["longitude"], row["latitude"]],
                  popup=row["description"]).add_to(marker_cluster)
stops_map.save('stops.html')

# This shows that many traffic stops are concentrated around the bottom right of the county. We can extend our analysis further with a heatmap:
stops_heatmap = folium.Map(location=[39.0836, -77.1483], zoom_start=11)
stops_heatmap.add_children(plugins.HeatMap(
    [[row["longitude"], row["latitude"]] for name, row in morning_rush.iloc[:1000].iterrows()]))
stops_heatmap.save("heatmap.html")
