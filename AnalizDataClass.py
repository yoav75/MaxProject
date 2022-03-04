import pandas as pd
import seaborn as sns
import plotly.graph_objs as go
import numpy as np


class ADC:
    def __init__(self, csv):
        self.csv = csv
        self.df = pd.read_csv(self.csv)

    def PieChart(self):
        dist = self.df['WYR'].value_counts()
        colors = ['mediumturquoise', 'darkorange']
        trace = go.Pie(values=(np.array(dist)), labels=dist.index)
        layout = go.Layout(title='Would you recommend')
        fig = go.Figure(trace, layout)
        fig.update_traces(marker=dict(colors=colors, line=dict(color='#000000', width=2)))
        fig.show()