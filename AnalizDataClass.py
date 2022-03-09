import pandas as pd
import seaborn as sns
import plotly.graph_objs as go
import numpy as np
import plotly.express as px


class ADC:
    def __init__(self, csv):
        self.csv = csv
        self.df = pd.read_csv(self.csv)

    def PieChart(self,col):
        dist = self.df[col].value_counts()
        print(dist.keys())
        print(dist)
        colors = ['mediumturquoise', 'darkorange']
        trace = go.Pie(values=(np.array(dist)), labels=dist.index)
        layout = go.Layout(title=col)
        fig = go.Figure(trace, layout)
        fig.update_traces(marker=dict(colors=colors, line=dict(color='#000000', width=2)))
        fig.show()

    def BarChart(self, col):
       return 0
