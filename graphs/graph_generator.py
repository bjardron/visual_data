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
            'line': self._line_plot,
            'scatter': self._scatter_plot,
            'bar': self._bar_plot,
            'histogram': self._histogram,
            'box': self._box_plot,
            'violin': self._violin_plot,
            'heatmap': self._heatmap,
            'pie': self._pie_chart,
            'area': self._area_plot,
            'density': self._density_plot
        }
        
        if graph_type in graph_functions:
            graph_functions[graph_type](data, x_column, y_column, columns, color, **kwargs)
        else:
            raise ValueError(f"Unsupported graph type: {graph_type}")

        self._set_labels(title, x_label, y_label)
        self.fig.tight_layout()
        
        # Return the figure instead of showing it
        return self.fig

    def _line_plot(self, data, x_column, y_column, columns, color, **kwargs):
        self.ax.plot(data[x_column], data[y_column], color=color, **kwargs)

    def _scatter_plot(self, data, x_column, y_column, columns, color, **kwargs):
        self.ax.scatter(data[x_column], data[y_column], color=color, **kwargs)

    def _bar_plot(self, data, x_column, y_column, columns, color, **kwargs):
        if y_column:
            self.ax.bar(data[x_column], data[y_column], color=color, **kwargs)
        else:
            data[columns].sum().plot(kind='bar', ax=self.ax, color=color, **kwargs)

    def _histogram(self, data, x_column, y_column, columns, color, **kwargs):
        self.ax.hist(data[columns or y_column], bins=kwargs.get('bins', 20), color=color, **kwargs)

    def _box_plot(self, data, x_column, y_column, columns, color, **kwargs):
        sns.boxplot(data=data[columns or y_column], ax=self.ax, color=color, **kwargs)

    def _violin_plot(self, data, x_column, y_column, columns, color, **kwargs):
        sns.violinplot(x=x_column, y=y_column, data=data, ax=self.ax, **kwargs)

    def _heatmap(self, data, x_column, y_column, columns, color, **kwargs):
        sns.heatmap(data[columns].corr(), ax=self.ax, cmap=color or 'coolwarm', annot=True, **kwargs)

    def _pie_chart(self, data, x_column, y_column, columns, color, **kwargs):
        self.ax.pie(data[y_column], labels=data[x_column], autopct='%1.1f%%', colors=color, **kwargs)

    def _area_plot(self, data, x_column, y_column, columns, color, **kwargs):
        data[columns].plot.area(ax=self.ax, stacked=False, **kwargs)

    def _density_plot(self, data, x_column, y_column, columns, color, **kwargs):
        sns.kdeplot(data=data[columns or y_column], ax=self.ax, **kwargs)

    def _set_labels(self, title, x_label, y_label):
        if title:
            self.ax.set_title(title)
        if x_label:
            self.ax.set_xlabel(x_label)
        if y_label:
            self.ax.set_ylabel(y_label)
        self.ax.tick_params(axis='x', rotation=45)

    def save_graph(self, filename: str, dpi: int = 300) -> None:
        if self.fig:
            self.fig.savefig(filename, dpi=dpi, bbox_inches='tight')
        else:
            raise ValueError("No graph has been generated yet.")

    def get_preview(self) -> np.ndarray:
        if self.fig:
            self.fig.canvas.draw()
            return np.frombuffer(self.fig.canvas.tostring_rgb(), dtype=np.uint8).reshape(self.fig.canvas.get_width_height()[::-1] + (3,))
        else:
            raise ValueError("No graph has been generated yet.")

    def show_graph(self) -> None:
        if self.fig:
            plt.show()
        else:
            raise ValueError("No graph has been generated yet.")