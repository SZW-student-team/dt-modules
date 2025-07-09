import pandas as pd
import plotly.express as px
import json


from dt_modules import BarChart, LineChart, PieChart, ScatterPlot, Histogram, BoxPlot, HeatMap, Figure, fill, fill_default_colors, government_theme, quantitative_colors


def get_heatmap_data():
    return [
        # Zuid-Holland
        {"provincie": "Zuid-Holland", "sector": "Bouw", "werkloosheid": 5.2},
        {"provincie": "Zuid-Holland", "sector": "Zorg", "werkloosheid": 3.1},
        {"provincie": "Zuid-Holland", "sector": "Onderwijs", "werkloosheid": 2.8},
        {"provincie": "Zuid-Holland", "sector": "ICT", "werkloosheid": 4.0},

        # Noord-Holland
        {"provincie": "Noord-Holland", "sector": "Bouw", "werkloosheid": 4.9},
        {"provincie": "Noord-Holland", "sector": "Zorg", "werkloosheid": 2.7},
        {"provincie": "Noord-Holland", "sector": "Onderwijs", "werkloosheid": 2.5},
        {"provincie": "Noord-Holland", "sector": "ICT", "werkloosheid": 3.8},

        # Utrecht
        {"provincie": "Utrecht", "sector": "Bouw", "werkloosheid": 4.5},
        {"provincie": "Utrecht", "sector": "Zorg", "werkloosheid": 2.9},
        {"provincie": "Utrecht", "sector": "Onderwijs", "werkloosheid": 2.6},
        {"provincie": "Utrecht", "sector": "ICT", "werkloosheid": 3.2},

        # Noord-Brabant
        {"provincie": "Noord-Brabant", "sector": "Bouw", "werkloosheid": 5.5},
        {"provincie": "Noord-Brabant", "sector": "Zorg", "werkloosheid": 3.3},
        {"provincie": "Noord-Brabant", "sector": "Onderwijs", "werkloosheid": 3.0},
        {"provincie": "Noord-Brabant", "sector": "ICT", "werkloosheid": 4.4},
    ]

def get_sectors():
    sectors = [
        "Landbouw, bosbouw en visserij",
        "Winning van delfstoffen",
        "Industrie",
        "Productie en distributie van en handel in elektriciteit, aardgas, stoom en gekoelde lucht",
        "Winning en distributie van water, afval- en afvalwaterbeheer en sanering",
        "Bouwnijverheid",
        "Groot- en detailhandel, reparatie van auto’s",
        "Vervoer en opslag",
        "Logies-, maaltijd- en drankverstrekking",
        "Informatie en communicatie",
        "Financiële instellingen",
        "Verhuur van en handel in onroerend goed",
        "Advisering, onderzoek en overige specialistische zakelijke dienstverlening",
        "Verhuur van roerende goederen en overige zakelijke dienstverlening",
        "Openbaar bestuur, overheidsdiensten en verplichte sociale verzekeringen",
        "Onderwijs",
        "Gezondheids- en welzijnszorg",
        "Cultuur, sport en recreatie",
        "Overige dienstverlening",
        "Huishoudens als werkgever, niet-gedifferentieerde productie van goederen en diensten door huishoudens voor eigen gebruik",
        "Extraterritoriale organisaties en lichamen"
    ]

    return sectors

class CustomChart(Figure):
    def __init__(
        self,
        data,
        x: str,
        y: str,
        values: str,
        column_to_color: str,
        colors: list[str] | None = None,
        **kwargs,
    ):

        if colors is None:
            colors = fill_default_colors(
                len(data[x]), government_theme, quantitative_colors
            )
        else:
            colors = fill(len(data[x]), colors)

        figure = px.sunburst(
            data,
            names=x,
            parents=y,
            values=values,
            color=column_to_color,
            color_discrete_sequence=colors,
            **kwargs,
        )

        self.data = data
        self.colors = colors
        self.column_to_color = column_to_color
        self.x = x
        self.y = y
        super().__init__(figure)

    def save_json(self, location: str):
        parameters = {
            "chartType": "custom",
            "dataframe": self.data.to_dict(),
            "length": self.data.shape[0],
            "columns": list(self.data.columns),
            "colors": self.colors,
            "columnToColor": self.column_to_color,
            "x": self.x,
            "y": self.y,
        }

        figure_contents = json.loads(self.get_figure().to_json())
        export_contents = { "parameters": parameters, "figureContents": figure_contents }

        with open(location, "w") as f:
            json.dump(export_contents, f)

def main():
    data = {
        'sectoren': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U'],
        'uitstroom': [63589, 7615, 689794, 22133, 34755, 335913, 894066, 304780, 162482, 198830, 234537, 57592, 409602, 493306, 472004, 398288, 884573, 74078, 103002, 12192, 630],
        'sector_namen': get_sectors(),
    }

    df = pd.DataFrame(data)

    # Bar
    bar_df = df.sort_values(by=["uitstroom"])
    bar_chart = BarChart(bar_df.head(5), x="sectoren", y="uitstroom", column_to_color="sectoren")
    bar_chart.save_json("./exports/bar_chart.export.json")

    # Pie
    pie_chart = PieChart(data=df, values="uitstroom", names="sectoren")
    pie_chart.save_json("./exports/pie_chart.export.json")

    # Line
    df = px.data.gapminder().query("continent == 'Oceania'")
    line_chart = LineChart(df, x="year", y="lifeExp", column_to_color="country")
    line_chart.save_json("./exports/line_chart.export.json")
    line_chart.data.to_excel("exports/line_chart.export.xlsx")

    # Scatter
    scatter_df = pd.DataFrame(data={"x": [0, 1, 2, 3, 4], "y": [0, 1, 4, 9, 16]})
    scatter = ScatterPlot(scatter_df, x="x", y="y")
    # scatter.get_figure().show()
    scatter.save_json("./exports/scatter.export.json")
    scatter.data.to_excel("exports/scatter.export.xlsx")

    # Histogram
    df = px.data.tips()
    histogram = Histogram(df, x="total_bill", nbins=10, title="test title", y_label="cost", colors=["#CA005D"])
    histogram.save_json("./exports/histogram.export.json")
    histogram.data.to_excel("exports/histogram.export.xlsx")

    # Boxplot
    box_plot = BoxPlot(df, x="time", column_to_color="time", y="total_bill")
    # box_plot.get_figure().show()
    box_plot.save_json("./exports/box_plot.export.json")
    box_plot.data.to_excel("exports/box_plot.export.xlsx")

    # Heatmap
    heatmap_data = get_heatmap_data()
    df = pd.DataFrame(heatmap_data)
    heatmap = HeatMap(df, x="provincie", y="sector", value_column="werkloosheid")
    heatmap.save_json("exports/heatmap.export.json")
    heatmap.data.to_excel("exports/heatmap.export.xlsx")

    # Custom chart
    data = dict(
        character=["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
        parent=["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve" ],
        value=[10, 14, 12, 10, 2, 6, 6, 4, 4])
    df_custom = pd.DataFrame(data)
    custom_chart = CustomChart(data=df_custom, x='character', y='parent', values='value', column_to_color='character')
    custom_chart.save_json("./exports/sunburst_chart.export.json")

if __name__ == "__main__":
    main()
