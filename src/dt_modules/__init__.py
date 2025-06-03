import plotly.express as px
import plotly.graph_objects as go

from abc import ABC, abstractmethod
from typing import Any
import json

from dt_modules.coloring import government_theme, quantitative_colors


# TODO: remove all occurrences of these colors.
blue_colors = ["#154273", "#4F7196", "#738EAB", "#95A9C0", "#B8C6D5", "#DCE3EA"]
rubine_red = ["#CA005D", "#D74085", "#DF669D", "#E78CB6", "#EFB2CE", "#F7D9E7"]


def fill(to: int, colors: list[str]) -> list[str]:
    """Creates a list filled with items form the `colors` list. Will repeat values so the new list's length will equal `to`"""

    length = len(colors)
    new_colors = []

    for i in range(0, to):
        new_colors.append(colors[i % length])

    return new_colors


def fill_default_colors(
    to: int, theme: dict[str, dict[str, str]], color_names: list[str]
) -> list[str]:
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

    # TODO: implement this.
    # @abstractmethod
    # def get_data(self):
    #     """Returns the data which is used to create the plotly figure."""
    #     pass

    # TODO: implement this.
    # @abstractmethod
    # def get_chart_type(self) -> str:
    #     """Returns what chart will can created."""
    #     pass

    def save_image(self, location: str):
        """Saves the current figure as an image."""

        self.get_figure().write_image(location)

    def save_json(self, location: str):
        """Saves a json representation of the current figure, which can be uploaded to the data portal."""

        figure_contents = json.loads(self.get_figure().to_json())

        with open(location, "w") as f:
            json.dump(figure_contents, f)

    # TODO: implement this.
    # def save_json_v2(self, location: str):
    #     """Saves a json representation of the current figure, which can be uploaded to the data portal."""

    #     data = self.get_data()

    #     portal_data = {
    #         "chartType": self.get_chart_type(),
    #         "dataframe": data.to_dict(),
    #         "columns": list(data.columns),
    #     }

    #     figure_contents = json.loads(self.get_figure().to_json())
    #     export_contents = { "portalData": portal_data, "figureContents": figure_contents }

    #     with open(location, "w") as f:
    #         json.dump(export_contents, f)


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
            colors = fill_default_colors(
                len(data[x]), government_theme, quantitative_colors
            )
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

        self.data = data
        self.colors = colors
        self.column_to_color = column_to_color
        self.x = x
        self.y = y
        super().__init__(figure)

    def save_json_v2(self, location: str):
        parameters = {
            "chartType": "bar",
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


class PieChart(Figure):
    def __init__(
        self, data, values: str, names: str, colors: list[str] = None, **kwargs
    ):
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
            color_discrete_sequence=colors,
            **kwargs,
        )

        self.data = data
        self.colors = colors
        self.column_to_color = names
        self.x = values
        self.y = names
        super().__init__(figure)

    def save_json_v2(self, location: str):
        parameters = {
            "chartType": "pie",
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

        self.headers = headers
        super().__init__(figure)

    def save_json_v2(self, location: str):
        portal_data = {
            "chartType": "table",
            "columns": list(self.headers),
        }

        figure_contents = json.loads(self.get_figure().to_json())
        export_contents = { "portalData": portal_data, "figureContents": figure_contents }

        with open(location, "w") as f:
            json.dump(export_contents, f)


class ScatterPlot(Figure):
    def __init__(self, x: str | list = [], y: str | list = [], colors: list = None, **kwargs):
        if colors is None:
            colors = fill_default_colors(
                len(x), government_theme, quantitative_colors
            )

        figure = px.scatter(
            x=x,
            y=y,
            color=colors,
            color_discrete_map="identity",
            **kwargs,
        )

        super().__init__(figure)


class Histogram(Figure):
    def __init__(self, data, x: str, nbins: int = 10, colors: list = None, x_label: str = None, y_label: str = None, **kwargs):
        if colors is None:
            colors = fill(len(data), [government_theme["Lintblauw"][100]])

        figure = px.histogram(
            data,
            x=x,
            nbins=nbins,
            color=colors,
            color_discrete_map="identity",
            **kwargs,
        )

        # Set axis labels.
        figure.update_layout(
            xaxis_title=x_label or x,
            yaxis_title=y_label
        )

        super().__init__(figure)


class LineChart(Figure):
    def __init__(self, data, x: str, y: str, column_to_color: str, colors: list = None, **kwargs):
        if colors is None:
            colors = fill_default_colors(
                len(data[y]), government_theme, quantitative_colors
            )

        figure = px.line(
            data,
            x=x,
            y=y,
            color=column_to_color,
            color_discrete_sequence=colors,
            **kwargs,
        )

        self.data = data
        self.length = data[column_to_color].unique().shape[0]
        self.colors = colors
        self.column_to_color = column_to_color
        self.x = x
        self.y = y
        super().__init__(figure)

    def save_json_v2(self, location: str):
        parameters = {
            "chartType": "line",
            "dataframe": self.data.to_dict(),
            "length": self.length,
            "columns": list(self.data.columns),
            "colors": self.colors,
            "columnToColor": self.column_to_color,
            "x": self.x,
            "y": self.y,
        }

        figure_contents = json.loads(self.get_figure().to_json())
        export_contents = { "parameters": parameters, "figureContents": figure_contents }

        self.data.to_excel("line_chart.exports.xlsx")

        with open(location, "w") as f:
            json.dump(export_contents, f)


class BoxPlot(Figure):
    def __init__(self, data, x: str, column_to_color: str, colors: list = None, **kwargs):
        if colors is None:
            colors = fill_default_colors(
                len(data[column_to_color]), government_theme, quantitative_colors
            )

        figure = px.box(
            data,
            x=x,
            color=column_to_color,
            color_discrete_sequence=colors,
            **kwargs,
        )

        super().__init__(figure)
