import pandas as pd
import seaborn as sns
import plotly.graph_objs as go
import numpy as np
import plotly.express as px


class ADC:
    def AvrageByParm(self, data, Parm, value, field):
        sum = 0
        index = 0
        for i in data:
            if i[Parm] == value:
                sum += i[field]
                index += 1

        return sum / index

    def PieChart(self, col, data):
        dist = data[col].value_counts()
        colors = ['mediumturquoise', 'darkorange']
        trace = go.Pie(values=(np.array(dist)), labels=dist.index)
        layout = go.Layout(title=col)
        fig = go.Figure(trace, layout)
        fig.update_traces(marker=dict(colors=colors, line=dict(color='#000000', width=2)))
        fig.write_image("static/fig1.png")



    def giga_avg(self,data):
        giga_avg = 0
        artist_rating = []
        for i in self.get_all_artist(data):
            artist_rating.append((i, round((self.AvrageByParm(data, "Artist Name", i, "WouldYouDoItAgain") +
                                            self.AvrageByParm(data, "Artist Name", i, "WouldYouRec")) / 2)))
        for i in artist_rating:
            giga_avg += i[1]

        return artist_rating, giga_avg / len(artist_rating)

    def lineChart(self, data, field):
        df = pd.DataFrame(dict(
            x=self.xy(data, "date", field)[0],
            y=self.xy(data, "date", field)[1]
        ))
        if field == "WouldYouDoItAgain":
            labels = {
                "y": "average answer to:Would You Do It Again" ,
                "x": "Date",
            }
        else:
            labels = {
                "y": "average answer to: How often would You Recommend" ,
                "x": "Date",
            }
        df = df.sort_values(by="x")
        fig = px.line(df, x="x", y="y", labels=labels)
        fig.add_shape(  # add a horizontal "target" line
            type="line", line_color="salmon", line_width=3, opacity=1, line_dash="dot",
            x0=0, x1=1, xref="paper", y0=self.giga_avg(data)[1], y1=self.giga_avg(data)[1], yref="y"
        )
        print(self.giga_avg(data))
        return fig

    def xy(self, data, Parm, field):


        parmlist = []
        xaxis = []
        for i in data:
            if not i[Parm] in parmlist:
                parmlist.append(i[Parm])
        for i in parmlist:
            avg = self.AvrageByParm(data, Parm, i, field)
            xaxis.append(avg)

        return parmlist, xaxis

    def BarChart(self, Parm, data):

        df = pd.DataFrame(dict(
            x=self.xy(data, Parm, "WouldYouDoItAgain")[0],
            y=self.xy(data, Parm, "WouldYouDoItAgain")[1]
        ))
        labels = {
            "y": "average satisfaction (avg)",
            "x": "Date (Day/Month/Year)",
        }
        fig = px.bar(df, labels=labels, x="x", y="y")
        fig.add_shape(  # add a horizontal "target" line
            type="line", line_color="salmon", line_width=3, opacity=1, line_dash="dot",
            x0=0, x1=1, xref="paper", y0=self.giga_avg(data)[1], y1=self.giga_avg(data)[1], yref="y"
        )
        return fig

    def get_all_concerts_(self, data):
        concert_list = []
        for i in data:
            if not (i["date"] + '/' + i["Artist Name"] + '/' + str(i["audience number"]) + '/' + i[
                "Show Name"]) in concert_list:
                concert_list.append(
                    i["date"] + '/' + i["Artist Name"] + '/' + str(i["audience number"]) + '/' + i["Show Name"])
        return concert_list

    def get_all_artist(self, data):
        artist_list = []
        for i in data:
            if not (i["Artist Name"]) in artist_list:
                artist_list.append(i["Artist Name"])
        return artist_list
