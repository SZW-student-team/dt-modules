import pandas as pd
import plotly.express as px


from dt_modules import BarChart, LineChart, PieChart, Table, ScatterPlot, Histogram, BoxPlot


def start_old():
    data = {
        'sectoren': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U'],
        'uitstroom': [63589, 7615, 689794, 22133, 34755, 335913, 894066, 304780, 162482, 198830, 234537, 57592, 409602, 493306, 472004, 398288, 884573, 74078, 103002, 12192, 630],
        'sector_namen': get_sectors(),
    }

    df = pd.DataFrame(data)

    bar_chart = BarChart(df, x="sectoren", y="uitstroom", column_to_color="sectoren")
    bar_chart.save_json("./exports/bar_chart.export.json")

    pie_chart = PieChart(data=df, values="uitstroom", names="sectoren")
    pie_chart.save_json("./exports/pie_chart.export.json")

    headers = ["Letters", "Beschrijvingen"]
    cells = [df["sectoren"].head(5), df["sector_namen"].head(5)]
    table = Table(headers=headers, cells=cells, alternate_row=True)
    table.save_json("./exports/table.export.json")

    scatter = ScatterPlot(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16])
    scatter.save_json("./exports/scatter.export.json")

    df = px.data.tips()
    histogram = Histogram(df, x="total_bill", nbins=10, title="Rekening en kosten", y_label="cost")
    histogram.save_json("./exports/histogram.export.json")

    df = px.data.tips()
    box_plot = BoxPlot(df, x="time", column_to_color="time", y="total_bill")
    box_plot.save_json("./exports/box_plot.export.json")


def start():
    data = {
        'sectoren': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U'],
        'uitstroom': [63589, 7615, 689794, 22133, 34755, 335913, 894066, 304780, 162482, 198830, 234537, 57592, 409602, 493306, 472004, 398288, 884573, 74078, 103002, 12192, 630],
        'sector_namen': get_sectors(),
    }

    df = pd.DataFrame(data)

    # # Pie
    # pie_chart = PieChart(data=df, values="uitstroom", names="sectoren")
    # pie_chart.save_json_v2("./exports/pie_chart_v2.export.json")

    # # Bar
    # bar_chart = BarChart(df.head(3), x="sectoren", y="uitstroom", column_to_color="sectoren")
    # bar_chart.save_json_v2("./exports/bar_chart_v2.export.json")
    # # bar_chart.save_json("./exports/bar_chart.export.json")

    # # Table
    # headers = ["Letters", "Beschrijvingen"]
    # cells = [df["sectoren"].head(5), df["sector_namen"].head(5)]
    # table = Table(headers=headers, cells=cells, alternate_row=True)
    # table.save_json_v2("./exports/table.export.json")

    # # Line
    # df = px.data.gapminder().query("continent == 'Oceania'")
    # line_chart = LineChart(df, x="year", y="lifeExp", column_to_color="country")
    # line_chart.save_json_v2("./exports/line_chart_v2.export.json")

    # # Scatter
    # scatter_df = pd.DataFrame(data={"x": [0, 1, 2, 3, 4], "y": [0, 1, 4, 9, 16]})
    # scatter = ScatterPlot(scatter_df, x="x", y="y")
    # # scatter.get_figure().show()
    # scatter.save_json_v2("./exports/scatter_v2.export.json")

    # Histogram
    df = px.data.tips()
    # histogram = Histogram(df, x="total_bill", nbins=10, title="test title", y_label="cost", colors=["#CA005D"])
    # histogram.save_json_v2("./exports/histogram_v2.export.json")

    # Boxplot
    box_plot = BoxPlot(df, x="time", column_to_color="time", y="total_bill")
    # box_plot.get_figure().show()
    # box_plot.save_image("./exports/box_plot.png")
    box_plot.save_json_v2("./exports/box_plot_v2.export.json")

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
