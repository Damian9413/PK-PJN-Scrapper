"""Charts saved as PNG files (no window is opened)."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # render to files only, works without a display
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

DPI = 150


def _save(figure: plt.Figure, path: Path) -> Path:
    figure.tight_layout()
    figure.savefig(path, dpi=DPI)
    plt.close(figure)
    return path


def histogram(products: pd.DataFrame, column: str, bins: int, path: Path) -> Path:
    figure, axes = plt.subplots(figsize=(7, 4))
    axes.hist(products[column].dropna(), bins=bins, edgecolor="white")
    axes.set_title(f"Histogram: {column}")
    axes.set_xlabel(column)
    axes.set_ylabel("liczba produktów")
    return _save(figure, path)


def boxplot_by(products: pd.DataFrame, column: str, group: str, path: Path) -> Path:
    """One box per group value, e.g. price per currency."""
    groups = sorted(products[group].dropna().unique())
    data = [products.loc[products[group] == g, column].dropna() for g in groups]
    figure, axes = plt.subplots(figsize=(7, 4))
    axes.boxplot(data, tick_labels=groups)
    axes.set_title(f"Box-plot: {column} wg {group}")
    axes.set_xlabel(group)
    axes.set_ylabel(column)
    return _save(figure, path)


def correlation_heatmap(correlation: pd.DataFrame, path: Path) -> Path:
    """Pearson correlation matrix with values written in each cell."""
    figure, axes = plt.subplots(figsize=(8, 6.5))
    image = axes.imshow(correlation, cmap="coolwarm", vmin=-1, vmax=1)
    labels = list(correlation.columns)
    axes.set_xticks(range(len(labels)), labels, rotation=45, ha="right")
    axes.set_yticks(range(len(labels)), labels)
    for i in range(len(labels)):
        for j in range(len(labels)):
            axes.text(j, i, f"{correlation.iat[i, j]:.2f}", ha="center", va="center", fontsize=8)
    figure.colorbar(image, ax=axes, label="współczynnik Pearsona")
    axes.set_title("Macierz korelacji cech liczbowych")
    return _save(figure, path)
