import pandas as pd
import numpy as np
import sys
import json


def histogram(res=0.05):
    longitudes = np.arange(df.longitude.min(), df.longitude.max(), res)
    latitudes = np.arange(df.latitude.min(), df.latitude.max(), res)
    xx, yy = np.meshgrid(longitudes, latitudes)
    squares = pd.DataFrame(np.array([xx.ravel(), (xx + res).ravel(), yy.ravel(), (yy + res).ravel()]).T,
                           columns=['left', 'right', 'lower', 'upper'])
    return squares.apply(average_value_rating, axis=1).values.reshape(xx.shape), longitudes, latitudes

def average_value_rating(square):
    def value_rating(row):
        # TODO
        return row.price
    points = points_in_square(square)
    if points.empty:
        center = (square.left + square.right) / 2, (square.lower + square.upper)/2
        points = nearest_neighbours(center, 5)
    return points.apply(value_rating, axis=1).mean()

def points_in_square(square):
    return df[(df.longitude >= square.left) &
              (df.longitude <= square.right) &
              (df.latitude >= square.upper) &
              (df.latitude <= square.upper)]

def nearest_neighbours(point, num):
    return df.assign(distance=(df[['longitude', 'latitude']] - point).apply(np.linalg.norm, axis=1)) \
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
