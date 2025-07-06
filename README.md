# Dt-modules
This repository provides building blocks (or modules) for quickly creating Plotly visualizations.

## Setup
1. install the `uv` package manager.
1. install the correct font: `RijksoverheidSansText`
1. use `uv sync`

## Generate export files
- use: `uv run .\src\main.py`

## Examples

### Module usage:
```python
    import pandas as pd
    from dt_modules import BarChart

    # Collect data to visualize.
    data = {
        'sectoren': ['A', 'B', 'C', 'D', 'E'],
        'uitstroom': [63589, 7615, 689794, 22133, 34755],
    }

    # Create a dataframe.
    df = pd.DataFrame(data)

    # Create an instance of the BarChart module and set the correct parameters.
    bar_chart = BarChart(df, x="sectoren", y="uitstroom", column_to_color="sectoren")

    # Export the visualization to a file.
    bar_chart.save_json("./exports/bar_chart.export.json")
```

#### Overwriting values
```python
    from dt_modules import BarChart, government_theme

    # Overwrite the default colors with values from the government theme.
    colors = [government_theme["Lintblauw"][100], government_theme["Oranje"][100], government_theme["Mosgroen"][100]]

    bar_chart = BarChart(df, x="sectoren", y="uitstroom", column_to_color="sectoren", colors=colors)
    bar_chart.save_json("./exports/bar_chart.export.json")
```

### Access the plotly visual
```python
    # Get the underlying plotly figure.
    figure = bar_chart.get_figure()

    # Shows the figure in the browser.
    figure.show()
```

## Create a custom module
```python
from dt_modules import Figure, fill, fill_default_colors, government_theme, quantitative_colors
import json

class CustomChart(Figure):
    def __init__(
        self,
        data,
        x: str,
        y: str,
        values: str,
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

        figure = px.sunburst(
            data,
            names=x,
            parents=y,
            values=values,
            color=column_to_color,
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
            "chartType": "custom",
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
```

### Export the custom module
```python
data = dict(
    character=["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
    parent=["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve" ],
    value=[10, 14, 12, 10, 2, 6, 6, 4, 4])

df_custom = pd.DataFrame(data)
custom_chart = CustomChart(data=df_custom, x='character', y='parent', values='value', column_to_color='character')
custom_chart.save_json("./exports/sunburst_chart.export.json")
```
