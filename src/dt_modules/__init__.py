from abc import ABC, abstractmethod
from typing import Any
import plotly.express as px
import json


blue_colors = ["#154273", "#4F7196", "#738EAB", "#95A9C0", "#B8C6D5", "#DCE3EA"]
rubine_red = ["#CA005D", "#D74085", "#DF669D", "#E78CB6", "#EFB2CE", "#F7D9E7"]


# TODO: implement this with these colors: https://www.rijkshuisstijl.nl/publiek/modules/product/DigitalStyleGuide/default/index.aspx?ItemId=9247
def fill(to: int, colors: list[str]) -> list[str]:
    """Creates a list filled with items form the `colors` list. Will repeat values so the new list's length will equal `to`"""

    length = len(colors)
    new_colors = []

    for i in range(0, to):
        new_colors.append(colors[i % length])

    return new_colors


class Savable(ABC):
    """Denotes classes which can be saved to disk"""

    @abstractmethod
    def save(location: str):
        pass

    @abstractmethod
    def save_json(location: str):
        pass


class BarChart(ABC):
    @abstractmethod
    def __init__(self, data: Any, x: str, y: str, visual, colors: list[str]):
        self.data = data
        self.x = x
        self.y = y
        self.visual = visual
        self.colors = colors

    def get_visual(self):
        return self.visual


class PieChart(ABC):
    @abstractmethod
    def __init__(self, data: Any, values: str, names: str, visual, colors: list[str]):
        self.data = data
        self.value = values
        self.names = names
        self.visual = visual
        self.colors = colors

    def get_visual(self):
        return self.visual


class PlotlyBarChart(BarChart, Savable):
    def __init__(
        self, data: Any, x: str, y: str, column_to_color: str, colors: list[str]
    ):
        visual = px.bar(
            data,
            x=x,
            y=y,
            color=data[column_to_color],
            color_discrete_sequence=fill(len(x), colors),
        )
        visual.update_layout(plot_bgcolor="white")
        self.column_to_color = column_to_color

        super().__init__(data, x, y, visual, colors)

    def save(self, location: str):
        print("saving the bar chart")
        self.visual.write_image(location)

    def save_json(self, location: str):
        print("exporting the bar chart")
        export = {
            "visual_type": "bar_chart",
            "renderer": "plotly",
            "visual": json.loads(
                self.visual.to_json()
            ),  # This isn't optimal but it works, for now.
            "x": self.x,
            "y": self.y,
            "column_to_color": self.column_to_color,
            "colors": self.colors,
        }

        with open(location, "w") as f:
            json.dump(export, f)


class PlotlyPieChart(PieChart, Savable):
    def __init__(self, data: Any, values: str, names: str, colors: list[str]):
        visual = px.pie(
            data,
            values=values,
            names=names,
            color=data[names],
            color_discrete_sequence=fill(len(values), colors),
        )
        visual.update_layout(plot_bgcolor="white")

        super().__init__(data, values, names, visual, colors)

    def save(self, location: str):
        print("saving the pie chart")
        self.visual.write_image(location)

    def save_json(self, location):
        print("exporting the bar chart")

        export = {
            "visual_type": "pie_chart",
            "renderer": "plotly",
            "visual": json.loads(
                self.visual.to_json()
            ),  # This isn't optimal but it works, for now.
        }

        with open(location, "w") as f:
            json.dump(export, f)
