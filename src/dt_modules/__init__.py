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

    @abstractmethod
    def save_json(self, location: str):
        """Saves a json representation of the current figure, which can be uploaded to the data portal."""

        pass


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

    def save_json(self, location: str):
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

    def save_json(self, location: str):
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

    def save_json(self, location: str):
        portal_data = {
            "chartType": "table",
            "columns": list(self.headers),
        }

        figure_contents = json.loads(self.get_figure().to_json())
        export_contents = { "portalData": portal_data, "figureContents": figure_contents }

        with open(location, "w") as f:
            json.dump(export_contents, f)


class ScatterPlot(Figure):
    def __init__(self, data, x: str, y: str, colors: list = None, **kwargs):
        if colors is None:
            colors = fill_default_colors(
                1, government_theme, quantitative_colors
            )

        figure = px.scatter(
            x=data[x],
            y=data[y],
            color_discrete_sequence=colors,
            **kwargs,
        )

        self.data = data
        self.colors = colors
        self.x = x
        self.y = y
        super().__init__(figure)

    def save_json(self, location: str):
        parameters = {
            "chartType": "scatter",
            "dataframe": self.data.to_dict(),
            "length": self.data.shape[0],
            "colors": self.colors,
            "columns": [self.x, self.y],
            "x": self.x,
            "y": self.y,
        }

        figure_contents = json.loads(self.get_figure().to_json())
        export_contents = { "parameters": parameters, "figureContents": figure_contents }

        with open(location, "w") as f:
            json.dump(export_contents, f)


class Histogram(Figure):
    def __init__(self, data, x: str, nbins: int = 10, colors: list = None, x_label: str = None, y_label: str = None, **kwargs):
        if colors is None:
            colors = [government_theme["Lintblauw"][100]]

        figure = px.histogram(
            data,
            x=x,
            nbins=nbins,
            color_discrete_sequence=colors,
            **kwargs,
        )

        # Set axis labels.
        figure.update_layout(
            xaxis_title=x_label or x,
            yaxis_title=y_label
        )

        self.data = data
        self.colors = colors
        self.nbins = nbins
        self.x = x
        self.x_label = x_label or x
        self.y_label = y_label
        super().__init__(figure)

    def save_json(self, location: str):
        parameters = {
            "chartType": "histogram",
            "dataframe": self.data.to_dict(),
            "columns": list(self.data.columns),
            "nbins": self.nbins,
            "colors": self.colors,
            "x": self.x,
            "xLabel": self.x_label,
            "yLabel": self.y_label,
        }

        figure_contents = json.loads(self.get_figure().to_json())
        export_contents = { "parameters": parameters, "figureContents": figure_contents }

        with open(location, "w") as f:
            json.dump(export_contents, f)


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

    def save_json(self, location: str):
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

        with open(location, "w") as f:
            json.dump(export_contents, f)


class BoxPlot(Figure):
    def __init__(self, data, x: str, y: str, column_to_color: str, colors: list = None, **kwargs):
        length = data[column_to_color].unique().shape[0]

        if colors is None:
            colors = fill_default_colors(
                length, government_theme, quantitative_colors
            )

        figure = px.box(
            data,
            x=x,
            y=y,
            color=column_to_color,
            color_discrete_sequence=colors,
            **kwargs,
        )

        self.data = data
        self.length = length
        self.colors = colors
        self.column_to_color = column_to_color
        self.x = x
        self.y = y
        super().__init__(figure)

    def save_json(self, location: str):
        parameters = {
            "chartType": "box",
            "dataframe": self.data.to_dict(),
            "columns": list(self.data.columns),
            "length": self.length,
            "colors": self.colors,
            "columnToColor": self.column_to_color,
            "x": self.x,
            "y": self.y,
        }

        figure_contents = json.loads(self.get_figure().to_json())
        export_contents = { "parameters": parameters, "figureContents": figure_contents }

        with open(location, "w") as f:
            json.dump(export_contents, f)


class HeatMap(Figure):
    def __init__(self, data, x: str, y: str, value_column: str, color_continuous_scale: str | list = None, **kwargs):
        if color_continuous_scale is None:
            color_continuous_scale = "Viridis"

        heatmap_data = data.pivot(index=x, columns=y, values=value_column)
        figure = px.imshow(
            heatmap_data,
            labels=dict(x=x, y=y, color=value_column),
            color_continuous_scale=color_continuous_scale,
        )

        self.data = data
        self.x = x
        self.y = y
        self.value_column = value_column
        self.color_continuous_scale = color_continuous_scale
        super().__init__(figure)

    def save_json(self, location: str):
        parameters = {
            "chartType": "heatmap",
            "dataframe": self.data.to_dict(),
            "length": self.data.shape[0],
            "columns": list(self.data.columns),
            "x": self.x,
            "y": self.y,
            "valueColumn": self.value_column,
            "colorContinuousScale": self.color_continuous_scale,
        }

        figure_contents = json.loads(self.get_figure().to_json())
        export_contents = { "parameters": parameters, "figureContents": figure_contents }

        with open(location, "w") as f:
            json.dump(export_contents, f)