import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from typing import List, Optional, Any

class GraphGenerator:
    def __init__(self):
        self.fig = None
        self.ax = None

    def generate_graph(self, data: pd.DataFrame, graph_type: str, x_column: Optional[str] = None, 
                       y_column: Optional[str] = None, columns: Optional[List[str]] = None, 
                       title: Optional[str] = None, x_label: Optional[str] = None, 
                       y_label: Optional[str] = None, color: Optional[str] = None, 
                       ax: Optional[plt.Axes] = None, **kwargs: Any) -> None:
        if ax is None:
            self.fig, self.ax = plt.subplots(figsize=(10, 6))
        else:
            self.ax = ax
            self.fig = ax.figure

        graph_functions = {
            'line_plot': self._line_plot,
            'bar_chart': self._bar_plot,
            'scatter_plot': self._scatter_plot,
            'histogram': self._histogram,
            'box_plot': self._box_plot,
            'pie_chart': self._pie_chart,
            'heatmap': self._heatmap,
            'area_plot': self._area_plot
        }
        
        if graph_type in graph_functions:
            graph_functions[graph_type](data, x_column, y_column, columns, color, **kwargs)
        else:
            raise ValueError(f"Unsupported graph type: {graph_type}")

        self._set_labels(title, x_label, y_label)
        self.ax.tick_params(axis='x', rotation=45)

    def _line_plot(self, data, x_column, y_column, columns, color, **kwargs):
        self.ax.plot(data[x_column], data[y_column], color=color, **kwargs)

    def _bar_plot(self, data, x_column, y_column, columns, color, **kwargs):
        self.ax.bar(data[x_column], data[y_column], color=color, **kwargs)

    def _scatter_plot(self, data, x_column, y_column, columns, color, **kwargs):
        self.ax.scatter(data[x_column], data[y_column], color=color, **kwargs)

    def _histogram(self, data, x_column, y_column, columns, color, **kwargs):
        self.ax.hist(data[x_column], bins=kwargs.get('bins', 20), color=color, **kwargs)

    def _box_plot(self, data, x_column, y_column, columns, color, **kwargs):
        sns.boxplot(x=data[x_column], y=data[y_column], ax=self.ax, color=color, **kwargs)

    def _pie_chart(self, data, x_column, y_column, columns, color, **kwargs):
        self.ax.pie(data[y_column], labels=data[x_column], autopct='%1.1f%%', colors=color, **kwargs)

    def _heatmap(self, data, x_column, y_column, columns, color, **kwargs):
        pivot_data = data.pivot(x_column, y_column, columns[0] if columns else 'value')
        sns.heatmap(pivot_data, ax=self.ax, cmap=color or 'coolwarm', **kwargs)

    def _area_plot(self, data, x_column, y_column, columns, color, **kwargs):
        data.plot.area(x=x_column, y=columns or y_column, ax=self.ax, stacked=False, **kwargs)

    def _set_labels(self, title, x_label, y_label):
        if title:
            self.ax.set_title(title)
        if x_label:
            self.ax.set_xlabel(x_label)
        if y_label:
            self.ax.set_ylabel(y_label)

    def generate_standard_graph(self, data: pd.DataFrame, x_axis: str, y_axis: str, graph_type: str) -> None:
        graph_type_mapping = {
            "Line Plot": "line_plot",
            "Bar Chart": "bar_chart",
            "Scatter Plot": "scatter_plot",
            "Histogram": "histogram",
            "Box Plot": "box_plot"
        }
        
        mapped_graph_type = graph_type_mapping.get(graph_type)
        if not mapped_graph_type:
            raise ValueError(f"Unsupported graph type: {graph_type}")
        
        self.generate_graph(
            data=data,
            graph_type=mapped_graph_type,
            x_column=x_axis,
            y_column=y_axis,
            title=f"{graph_type}: {y_axis} vs {x_axis}",
            x_label=x_axis,
            y_label=y_axis
        )
        
        plt.show()