from abc import ABC, abstractmethod
from typing import Any
import plotly.express as px
import json


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
    """Holds data to visualize the plotly figure."""

    def __init__(self, figure):
        self.figure = figure

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
        figure.update_layout(plot_bgcolor="white")

        super().__init__(figure)


class PieChart(Figure):
    pass


class Table(Figure):
    pass
