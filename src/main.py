# TODO: exporteren, huisstijl, lettertype,

import pandas as pd

from dt_modules import PlotlyBarChart, blue_colors


def main():
    data = {
        'sectoren': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U'],
        'uitstroom': [63589, 7615, 689794, 22133, 34755, 335913, 894066, 304780, 162482, 198830, 234537, 57592, 409602, 493306, 472004, 398288, 884573, 74078, 103002, 12192, 630],
    }

    df = pd.DataFrame(data)

    bar_chart = PlotlyBarChart(df, x="sectoren", y="uitstroom", column_to_color="sectoren", colors=blue_colors)
    bar_chart.save("./exports/bar_chart.png")
    bar_chart.save_json("./exports/bar_chart.export.json")


if __name__ == "__main__":
    main()
