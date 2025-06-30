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

