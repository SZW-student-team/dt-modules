import plotly.express as px
import plotly.graph_objects as go

from abc import ABC, abstractmethod
from typing import Any
import json

from dt_modules.coloring import government_theme, quantitative_colors


# TODO: add the colors to the coloring module.
blue_colors = ["#154273", "#4F7196", "#738EAB", "#95A9C0", "#B8C6D5", "#DCE3EA"]
rubine_red = ["#CA005D", "#D74085", "#DF669D", "#E78CB6", "#EFB2CE", "#F7D9E7"]


def fill(to: int, colors: list[str]) -> list[str]:
    """Creates a list filled with items form the `colors` list. Will repeat values so the new list's length will equal `to`"""

    length = len(colors)
    new_colors = []

    for i in range(0, to):
        new_colors.append(colors[i % length])

    return new_colors


def fill_default_colors(to: int, theme: dict[str, dict[str, str]], color_names: list[str]) -> list[str]:
    """Generates a list of colors based on a given `theme`, repeating color names and adjusting their intensity."""

    length = len(color_names)
    new_colors = []
    used_colors = {}

    for i in range(0, to):
        color_name = color_names[i % length]

        if color_name not in used_colors:
            used_colors[color_name] = 100
        else:
            if used_colors[color_name] == 100:
                used_colors[color_name] = 75

            elif used_colors[color_name] == 15:
                used_colors[color_name] == 100

            else:
                used_colors[color_name] -= 15

        percentage = used_colors[color_name]
        new_colors.append(theme[color_name][percentage])

    return new_colors


def apply_default_style(figure):
    """Applies the default font (RijksoverheidSansText) to the given `figure`."""

    figure.update_layout(
        font_family="RijksoverheidSansText",
        # font_family="Arial",
        # plot_bgcolor="white",
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
    def figure(cls, figure):
        """Uses the given plotly `figure` without default configuration."""

        return Figure(figure)

    def get_figure(self):
        return self.figure


class BarChart(Figure):
    def __init__(
        self,
        data: Any,
        x: str,
        y: str,
        column_to_color: str,
        colors: list[str] | None = None,
        **kwargs,
    ):
        if colors is None:
            colors = fill_default_colors(len(data[x]), government_theme, quantitative_colors)
        else:
            colors = fill(len(data[x]), colors)

        figure = px.bar(
            data,
            x=x,
            y=y,
            color=data[column_to_color],
            color_discrete_sequence=colors,
            **kwargs,
        )
        figure.update_layout(plot_bgcolor="white")

        super().__init__(figure)


class PieChart(Figure):
    def __init__(self, data, values: str, names: str, colors: list[str] = None, **kwargs):
        length = len(values)

        if colors is None:
            colors = fill_default_colors(length, government_theme, quantitative_colors)
        else:
            colors = fill(length, colors)

        figure = px.pie(
            data,
            values=values,
            names=names,
            color=data[names],
            # color_discrete_sequence=fill(length, colors),
            color_discrete_sequence=colors,
            **kwargs,
        )
        figure.update_layout(plot_bgcolor="white")

        super().__init__(figure)


class Table(Figure):
    def __init__(
        self,
        headers=None,
        cells=None,
        header_color=blue_colors[0],
        cells_color=blue_colors[4],
        line_color="darkslategray",
        alternate_row=False,
        background_color="white",
        **kwargs,
    ):
        row_colors = background_color
        if alternate_row:
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
            ],
            **kwargs,
        )
        figure.update_layout(plot_bgcolor="white")

        super().__init__(figure)


class ScatterPlot(Figure):
    def __init__(self, figure=None, x: str | list = [], y: str | list = [], **kwargs):
        figure = px.scatter(
            x=x,
            y=y,
            color=fill(len(x), [blue_colors[0], rubine_red[0]]),
            color_discrete_map="identity",
            **kwargs,
        )

        super().__init__(figure)


class Histogram(Figure):
    def __init__(self, data, x: str, nbins: int = 10, **kwargs):
        figure = px.histogram(
            data,
            x=x,
            nbins=nbins,
            color=fill(len(data), [blue_colors[0]]),
            color_discrete_map="identity",
            **kwargs,
        )

        super().__init__(figure)


# TODO: make it easier to select a color for a line.
class LineChart(Figure):
    def __init__(self, data, x: str, y: str, color: str, **kwargs):
        figure = px.line(
            data,
            x=x,
            y=y,
            color=color,
            color_discrete_sequence=fill(len(data[y]), [blue_colors[0], rubine_red[0]]),
            **kwargs,
        )

        super().__init__(figure)


class BoxPlot(Figure):
    def __init__(self, data, x: str, color: str, **kwargs):
        figure = px.box(
            data,
            x=x,
            color=color,
            **kwargs,
        )

        super().__init__(figure)
