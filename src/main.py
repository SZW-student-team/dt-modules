import pandas as pd
import plotly.express as px

from dt_modules import BarChart, PieChart, Table, blue_colors, rubine_red, ScatterPlot, fill, Histogram, LineChart, BoxPlot

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

def main():
    sectors = get_sectors()
    data = {
        'sectoren': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U'],
        'uitstroom': [63589, 7615, 689794, 22133, 34755, 335913, 894066, 304780, 162482, 198830, 234537, 57592, 409602, 493306, 472004, 398288, 884573, 74078, 103002, 12192, 630],
        'sector_namen': sectors,
    }

    df = pd.DataFrame(data)

    bar_chart = BarChart(df, x="sectoren", y="uitstroom", column_to_color="sectoren")
    # bar_chart.save_image("./exports/bar_chart.png")
    bar_chart.save_json("./exports/bar_chart.export.json")

    pie_chart = PieChart(data=df, values="uitstroom", names="sectoren")
    # pie_chart.save_image("./exports/pie_chart.png")
    pie_chart.save_json("./exports/pie_chart.export.json")

    headers = ["Letters", "Beschrijvingen"]
    cells = [df["sectoren"].head(5), df["sector_namen"].head(5)]
    table = Table(headers=headers, cells=cells, alternate_row=True)
    table.save_json("./exports/table.export.json")

    # figure = px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16], color=fill(5, [blue_colors[2], rubine_red[2]]), color_discrete_map='identity')
    scatter = ScatterPlot(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16])
    # scatter = ScatterPlot.figure(figure)
    scatter.save_json("./exports/scatter.export.json")

    df = px.data.tips()
    histogram = Histogram(df, x="total_bill", nbins=10, title="test title", y_label="cost")
    histogram.get_figure().show()
    # histogram.save_image("./exports/histogram.png")
    histogram.save_json("./exports/histogram.export.json")

    df = px.data.gapminder().query("continent == 'Oceania'")
    line_chart = LineChart(df, x="year", y="lifeExp", column_to_color="country")
    line_chart.save_json("./exports/line_chart.export.json")
    # line_chart.get_figure().show()

    df = px.data.tips()
    # fig = px.box(df, x="time", y="total_bill", points="all")
    # fig.show()
    box_plot = BoxPlot(df, x="time", column_to_color="time", y="total_bill")
    # box_plot.save_image("./exports/box_plot.png")
    box_plot.save_json("./exports/box_plot.export.json")


if __name__ == "__main__":
    main()
