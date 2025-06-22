import pandas as pd
import plotly.express as px


from dt_modules import BarChart, LineChart, PieChart, Table, ScatterPlot, Histogram, BoxPlot, HeatMap


def start():
    data = {
        'sectoren': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U'],
        'uitstroom': [63589, 7615, 689794, 22133, 34755, 335913, 894066, 304780, 162482, 198830, 234537, 57592, 409602, 493306, 472004, 398288, 884573, 74078, 103002, 12192, 630],
        'sector_namen': get_sectors(),
    }

    df = pd.DataFrame(data)

    # Bar
    bar_df = df.sort_values(by=["uitstroom"])
    bar_chart = BarChart(bar_df.head(5), x="sectoren", y="uitstroom", column_to_color="sectoren")
    bar_chart.save_json_v2("./exports/bar_chart.export.json")

    # Pie
    pie_chart = PieChart(data=df, values="uitstroom", names="sectoren")
    pie_chart.save_json_v2("./exports/pie_chart.export.json")

    # Line
    df = px.data.gapminder().query("continent == 'Oceania'")
    line_chart = LineChart(df, x="year", y="lifeExp", column_to_color="country")
    line_chart.save_json_v2("./exports/line_chart.export.json")
    line_chart.data.to_excel("exports/line_chart.export.xlsx")

    # Scatter
    scatter_df = pd.DataFrame(data={"x": [0, 1, 2, 3, 4], "y": [0, 1, 4, 9, 16]})
    scatter = ScatterPlot(scatter_df, x="x", y="y")
    scatter.save_json_v2("./exports/scatter.export.json")
    # scatter.data.to_excel("exports/scatter.export.xlsx")

    # Histogram
    df = px.data.tips()
    histogram = Histogram(df, x="total_bill", nbins=10, title="test title", y_label="cost", colors=["#CA005D"])
    histogram.save_json_v2("./exports/histogram.export.json")
    # histogram.data.to_excel("exports/histogram.export.xlsx")

    # Boxplot
    box_plot = BoxPlot(df, x="time", column_to_color="time", y="total_bill")
    box_plot.save_json_v2("./exports/box_plot.export.json")
    box_plot.data.to_excel("exports/box_plot.export.xlsx")

    heatmap_data = get_heatmap_data()
    df = pd.DataFrame(heatmap_data)
    heatmap = HeatMap(df, x="provincie", y="sector", value_column="werkloosheid")
    heatmap.save_json_v2("exports/heatmap.export.json")
    heatmap.data.to_excel("exports/heatmap.export.xlsx")

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
