import pandas as pd
# Visualization Imports
import matplotlib.pyplot as plt
import seaborn as sns
from IPython import get_ipython
import plotly.offline as py
import plotly.graph_objs as go
import plotly.tools as tls
import plotly.express as px
import numpy as np
df = pd.read_csv(r'C:\Users\User\Desktop\DAT\Data.csv')
df.head()

color = sns.color_palette()
dist = df['WYR'].value_counts()
colors = ['mediumturquoise', 'darkorange']
trace = go.Pie(values=(np.array(dist)), labels=dist.index)

layout = go.Layout(title='Would you recommend')
data = [trace]
fig = go.Figure(trace, layout)
fig.update_traces(marker=dict(colors=colors, line=dict(color='#000000', width=2)))
fig.show()


def df_to_plotly(df):
    return {'z': df.values.tolist(),
            'x': df.columns.tolist(),
            'y': df.index.tolist()}


import plotly.graph_objects as go

dfNew = df.corr()
fig = go.Figure(data=go.Heatmap(df_to_plotly(dfNew)))
fig.show()

fig = px.scatter(df, x='Glucose', y='Insulin')
fig.update_traces(marker_color="turquoise", marker_line_color='rgb(8,48,107)', marker_line_width=1.5)
fig.update_layout(title_text='Glucose and Insulin')
fig.show()
