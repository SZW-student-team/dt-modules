import plotly.express as px
import plotly.graph_objects as go

from abc import ABC, abstractmethod
from typing import Any
import json


blue_colors = ["#154273", "#4F7196", "#738EAB", "#95A9C0", "#B8C6D5", "#DCE3EA"]
rubine_red = ["#CA005D", "#D74085", "#DF669D", "#E78CB6", "#EFB2CE", "#F7D9E7"]


def fill(to: int, colors: list[str]) -> list[str]:
    """Creates a list filled with items form the `colors` list. Will repeat values so the new list's length will equal `to`"""

    length = len(colors)
    new_colors = []

    for i in range(0, to):
        new_colors.append(colors[i % length])

    return new_colors


# TODO: add the correct font: https://www.rijkshuisstijl.nl/publiek/modules/product/DigitalStyleGuide/default/index.aspx?ItemId=6745
def apply_default_style(figure):
    """Applies the default font and a white background to the given `figure`."""

    figure.update_layout(
        font_family="Arial",
        plot_bgcolor="white",
    )


class Savable(ABC):
    """Denotes classes which can be saved to disk"""

    @abstractmethod
    def get_figure(self):
        """Returns a plotly figure, so the caller has full control over it's settings."""

        pass

    def save_image(self, location: str):
        """Saves the current figure as an image."""

        self.get_figure().write_image(location)

    def save_json(self, location: str):
        """Saves a json representation of the current figure, which can be uploaded to the data portal."""

        figure_contents = json.loads(self.get_figure().to_json())

        with open(location, "w") as f:
            json.dump(figure_contents, f)


class Figure(Savable):
    """Holds the plotly figure."""

    def __init__(self, figure):
        self.figure = figure
        apply_default_style(self.figure)

    @classmethod
    def from_figure(cls, figure):
        """Creates the `Figure` instance from the given plotly figure."""

        return Figure(figure)

    def get_figure(self):
        return self.figure


class BarChart(Figure):
    def __init__(
        self, data: Any, x: str, y: str, column_to_color: str, colors: list[str]
    ):
        figure = px.bar(
            data,
            x=x,
            y=y,
            color=data[column_to_color],
            color_discrete_sequence=fill(len(x), colors),
        )

        super().__init__(figure)


class PieChart(Figure):
    def __init__(self, data: Any, values: str, names: str, colors: list[str]):
        figure = px.pie(
            data,
            values=values,
            names=names,
            color=data[names],
            color_discrete_sequence=fill(len(values), colors),
        )

        super().__init__(figure)


class Table(Figure):
    def __init__(
        self,
        headers=None,
        cells=None,
        header_color=blue_colors[0],
        cells_color=blue_colors[4],
        line_color="darkslategray",
        alternate_row_color=False,
        background_color="white",
    ):
        row_colors = background_color
        if alternate_row_color:
            row_amount = len(cells[0])
            row_colors = [[background_color, cells_color] * row_amount]

        figure = go.Figure(
            data=[
                go.Table(
                    header=dict(
                        values=headers,
                        line_color=line_color,
                        fill_color=header_color,
                        font=dict(color=background_color),
                    ),
                    cells=dict(
                        values=cells,
                        line_color=line_color,
                        fill_color=row_colors,
                    ),
                )
            ]
        )

        super().__init__(figure)
