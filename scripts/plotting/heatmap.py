import pandas as pd
import numpy as np
import sys
import json


def histogram(res=0.05):
    longitudes = np.arange(df.longitude.min(), df.longitude.max(), res)
    latitudes = np.arange(df.latitude.min(), df.latitude.max(), res)
    xx, yy = np.meshgrid(longitudes, latitudes)
    squares = np.array([xx.ravel(), (xx + res).ravel(), yy.ravel(), (yy + res).ravel()]).T
    return np.apply_along_axis(average_value_rating, 1, squares).reshape(xx.shape), longitudes, latitudes

def average_value_rating(square):
    def value_rating(row):
        # TODO
        return row.price
    points = points_in_square(square)
    if points.empty:
        center = (square[:2].mean(), square[2:].mean())
        points = nearest_points(5, center)
    return points.apply(value_rating, axis=1).mean()

def points_in_square(square):
    left, right, lower, upper = square.tolist()
    return df[(left <= df.longitude) &
              (df.longitude <= right) &
              (lower <= df.latitude) &
              (df.latitude <= upper)]

def nearest_points(num, point):
    return df.assign(distance=(df.longitude-point[0])**2+(df.latitude-point[1])**2) \
             .sort_values('distance').iloc[:num]


import argparse

parser = argparse.ArgumentParser(description='Generate a heatmap of housing price values.')
group = parser.add_mutually_exclusive_group()
parser.add_argument('data', type=open, help='the file containing listings data')
group.add_argument('--offline', action='store_const',
                    const=True, default=False,
                    help='run in offline mode')
group.add_argument('-o', dest='filename',
                    help='save output to .png file')

args = parser.parse_args()

data = json.load(args.data)
df = pd.DataFrame(data)
h, x, y = histogram()

import plotly.plotly as py
import plotly.graph_objs as go
from plotly.grid_objs import Column
import plotly.offline as ol

layout = go.Layout(
    title='Housing Price Heatmap',
    xaxis=dict(
        title='Longitude',
        ticktext=np.char.mod('%.5f', x),
        tickvals=range(len(x))
    ),
    yaxis=dict(
        title='Latitude',
        ticktext=np.char.mod('%.5f', y),
        tickvals=range(len(y))
    ),
    margin=dict(
        b=150,
        l=125
    )
)
data = [ go.Heatmap(z=h) ]
fig = go.Figure(data=data, layout=layout)

if args.offline:
    ol.plot(fig, filename='heatmap.html')
elif args.filename:
    py.image.save_as(fig, args.filename)
else:
    py.plot(fig, filename='heatmap')
