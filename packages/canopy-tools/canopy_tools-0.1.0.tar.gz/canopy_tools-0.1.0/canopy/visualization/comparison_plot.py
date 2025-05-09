import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from typing import Optional, List
from canopy.visualization.plot_functions import get_color_palette, make_dark_mode, save_figure_png
import canopy as cp

def make_comparison_plot(fields: cp.Field | List[cp.Field], output_file: Optional[str] = None, plot_type: Optional[str] = "box",
                         layers: Optional[List[str]] = None, yaxis_label: Optional[str] = None, field_labels: Optional[List[str]] = None,
                         unit: Optional[List[str]] = None, title: Optional[str] = None, palette: Optional[str] = None,
                         custom_palette: Optional[List[str]] = None, dark_mode: bool = False,
                         transparent: bool = False, x_fig: float = 10, y_fig: float = 10, **kwargs):
    """
    Create a comparative plot from a list of input data Fields from, for example, different runs. The functions can generate
    boxplot, strip or swarm plot, violin plot, boxen plot, point plot, bar plot or count plot based on the `plot_type` parameter.

    Parameters
    ----------
    fields : cp.Field or List[cp.Field]
        Input data Field to display.
    output_file : str, optional
        File path for saving the plot.
    plot_type: str, default="box"
        Type of plot. Either “strip”, “swarm”, “box”, “violin”, “boxen”, “point”, “bar”, or “count”
    layers : List[str], optional
        List of layer names to display.
    yaxis_label : str, optional
        Y-axis label.
    field_labels : List[str], optional
        Names of each series to display in the legend.
    unit : List[str], optional
        Unit of the y-axis variable.
    title : str, optional
        Title of the plot.
    palette : str, optional
        Seaborn color palette to use for the line colors (https://seaborn.pydata.org/tutorial/color_palettes.html, recommended palette are in https://colorbrewer2.org).
    custom_palette : List[str], optional
        A list of color codes to override the default or colorblind palette.
    dark_mode : bool, default=False
        If True, applies dark mode styling to the figure.
    transparent : bool, default=False
        If True, sets the figure background to be transparent when saved.
    x_fig : float, default=10
        Width of the figure in inches.
    y_fig : float, default=10
        Height of the figure in inches.
    **kwargs
        Additional keyword arguments are passed directly to `seaborn.catplot`. This allows customization of
        plot features such as `aspect`, `errorbar`, height`, etc.
    """
    # Force time_series to be a list
    if not isinstance(fields, list):
        fields = [fields]

    # Retrieve metadata
    yaxis_label = yaxis_label or fields[0].metadata['name']
    unit = unit or fields[0].metadata['units']
    layers = layers or fields[0].layers

    # Check valid labels
    if len(fields) > 1 and field_labels is None:
            raise ValueError("field_labels must be defined when there are more than one field.")

    # Convert all series to DataFrames with flattened structure
    combined_data = []
    for i, field in enumerate(fields):
        label = field_labels[i]
        df = cp.make_lines(field)

        for layer in layers:
            data = df[layer].values.flatten()
            combined_data.append(pd.DataFrame({
                "value": data,
                "series": label,
                "layer": layer
            }))

    df_long = pd.concat(combined_data, ignore_index=True)

    # Get color palette
    colors, color_dict = get_color_palette(len(field_labels), palette=palette, custom_palette=custom_palette)
    palette = {label: color for label, color in zip(field_labels, colors)}

    # Base arguments
    plot_kwargs = {
        "data": df_long,
        "x": "layer",
        "y": "value",
        "hue": "series",
        "kind": plot_type,
        "palette": palette,
        "height": y_fig,
        "aspect": x_fig / y_fig
    }

    plot_kwargs.update(kwargs)

    # Recommended arguments
    if plot_type == "box" or plot_type == "boxen":
        plot_kwargs["fill"] = False
        plot_kwargs["showfliers"] = False
        plot_kwargs["gap"] = 0.1
    if plot_type == "violin":
        plot_kwargs["inner"] = None
        plot_kwargs["bw_method"] = 1
        if len(fields) == 2:
            plot_kwargs["split"] = True

    # Create the catplot
    fig = sns.catplot(**plot_kwargs)

    ax = fig.ax  # Extract the main axis

    # Set labels and title
    if unit:
        ax.set_ylabel(f"{yaxis_label} (in {unit})", fontsize=16)
    else:
        ax.set_ylabel(f"{yaxis_label}", fontsize=16)
    ax.set_xlabel("")
    ax.tick_params(labelsize=14)
    if title:
        ax.set_title(title, fontsize=16)

    # Custom legend (colored labels, no box)
    fig._legend.remove()
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles=[plt.Line2D([], [], color=palette[label], marker='', linestyle='') for label in labels],
              labels=labels, handlelength=0, handletextpad=0, labelcolor=[palette[label] for label in labels],
              loc='best', frameon=False, fontsize=14)

    # Apply dark mode
    if dark_mode:
        fig, ax = make_dark_mode(fig.fig, ax)

    # Save or display
    if output_file:
        save_figure_png(output_file, bbox_inches='tight', transparent=transparent)
    else:
        plt.show()

    plt.close()

    ## TODO: Check fields