import pandas as pd
import seaborn as sns
import plotly.graph_objs as go
import numpy as np
import plotly.express as px


class ADC:

    def PieChart(self,col,data):
        dist = data[col].value_counts()
        colors = ['mediumturquoise', 'darkorange']
        trace = go.Pie(values=(np.array(dist)), labels=dist.index)
        layout = go.Layout(title=col)
        fig = go.Figure(trace, layout)
        fig.update_traces(marker=dict(colors=colors, line=dict(color='#000000', width=2)))
        fig.show()


    def lineChart(self,data):
        data = data.sort_values(by="date")
        fig = px.line(data, x="date", y="WouldYouDoItAgain", title='Life expectancy in Canada',)
        fig.show()
    def BarChart(self, col):
        return 0
