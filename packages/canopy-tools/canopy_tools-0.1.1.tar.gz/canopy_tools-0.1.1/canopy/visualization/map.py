import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.patches import Rectangle
import cartopy.feature as feature
import cartopy.crs as ccrs
import seaborn as sns
import jenkspy
from typing import Optional, List
from pathlib import Path
import canopy as cp
from canopy.visualization.projections import projections
from canopy.visualization.plot_functions import get_color_palette, make_dark_mode, save_figure_png

def calculate_bins(raster, n_classes, classification, force_zero=False, diff_map=False):
    """
    Calculate bin edges based on the maximum value and desired scales.
    """
    def center_zero(bins): # take the closest bin to zero and force it to be zero
        bins = np.array(bins)
        bins[np.argmin(np.abs(bins))] = 0
        return bins

    max_val = np.nanmax(raster)
    min_val = np.nanmin(raster)

    if max_val == 0:
        raise ValueError("Maximum value is 0, raster likely empty.")
    if diff_map and n_classes % 2 != 0:
        raise ValueError("with diff_map, n_classes should be an even number.")

    if isinstance(classification, list):
        if len(classification)-1 != n_classes:
            raise ValueError(f"Custom bin edges must have {len(classification)-1} values.")
        bin_edges = np.array(classification)

    elif classification == "linear":
        # Linear classification
        scale = 10 ** np.floor(np.log10(max_val))  # Find the largest power of 10 less than or equal to max_value
        bin_max = scale * np.ceil(max_val / scale)  # Round up to the nearest multiple of scale
        if bin_max - max_val > scale / 2:
            bin_max -= scale / 2  # Adjust by subtracting half the scale
        
        bin_edges = np.linspace(min_val, bin_max, n_classes + 1)

    elif classification == "quantile":
        bin_edges = np.nanpercentile(raster, np.linspace(0, 100, n_classes + 1))

    elif classification == "jenks":
        flat = raster[np.isfinite(raster)].flatten()
        bin_edges = jenkspy.jenks_breaks(flat, n_classes)

    elif classification == "std":
        mean = np.nanmean(raster)
        std = np.nanstd(raster)
        if n_classes % 2 != 0:
            raise ValueError("n_classes should be even for 'std' classification.")
        half = n_classes // 2
        bin_edges = [mean + i * std for i in range(-half, half + 1)]

    else:
        raise ValueError("Invalid classification. Use 'linear', 'quantile', 'jenks', 'std', or a list.")

    if diff_map and force_zero:
        bin_edges = center_zero(bin_edges)
    if force_zero:
        bin_edges[0] = 0

    return np.array(bin_edges)

def add_map_features(ax):
    """
    Add land, coastlines, and gridlines to the map.
    """
    # Draw land and ocean
    ax.add_feature(feature.LAND, facecolor="silver")
    ax.coastlines(linewidth=0.5, color='black')
    # Gridlines labels
    gridlines = ax.gridlines(draw_labels={"top": True, "left": True, "right": False, "bottom": False})

    return ax, gridlines

def format_numbers(numbers):
    """
    Format bin values for better readability
    """
    formatted_numbers = []
    for value in numbers:
        if value == 0:
            formatted_numbers.append('0')
        elif abs(value) > 999 or abs(value) < 0.01:
            # Use scientific notation for values > 999 or < 0.01
            formatted_numbers.append(f'{value:.1e}')
        else:
            # Round rest values to 2 decimal places
            rounded_value = round(value, 2)
            if rounded_value.is_integer():
                formatted_numbers.append(f'{int(rounded_value)}')
            else:
                formatted_numbers.append(f'{rounded_value:.2f}')
    
    return formatted_numbers

def add_colorbar_quant(fig, ax, filled, bins, orientation, extend):
    """
    Add a quantitative colorbar to the map.
    """    
    cbar = fig.colorbar(filled, ax=ax, orientation=orientation, ticks=bins, shrink=0.7, pad=0.01, extend=extend)
    cbar.set_ticklabels(format_numbers(bins))
    
    return cbar

def add_colorbar_quali(fig, ax, filled, bins, orientation, labels):
    """
    Add a qualitative colorbar to the map.
    """
    cbar = fig.colorbar(filled, ax=ax, orientation=orientation, shrink=0.7, pad=0.03)
    midpoints = (bins[:-1] + bins[1:]) / 2
    tick_labels = [labels.get(i, '') for i in range(len(bins) - 1)]
    cbar.set_ticks(midpoints)
    cbar.set_ticklabels(tick_labels)
    # Hide the colorbar edges ticks
    cbar.ax.xaxis.set_ticks_position('none')
    
    return cbar

def plot_palette_hist(raster, output_file, cb_label, unit, bins, palette, dark_mode):
    """
    Creates and saves an histogram plot of the raster compared to the palette choosen.
    """
    # Make 2d raster, 1d
    flattened_raster = raster.flatten()

    fig = plt.figure(constrained_layout=True)
    ax = fig.add_subplot(1, 1, 1)

    # Dark mode
    if dark_mode is True:
        fig, ax = make_dark_mode(fig, ax)

    # Add colored rectangles for each bin
    for i in range(len(bins) - 1):
        ax.add_patch(Rectangle((bins[i], 0), bins[i + 1] - bins[i], 1, 
                     color=palette[i], alpha=0.3, transform=ax.get_xaxis_transform()))
    
    ax.set_xticks(bins)
    ax.set_xticklabels(format_numbers(bins))

    # Create the histogram
    sns.histplot(flattened_raster, kde=False, ax=ax)

    # Add labels
    ax.set_ylabel("Frequency", fontsize="large")
    if unit:
        ax.set_title(cb_label + " (in "+ unit +")", fontsize="x-large")
    else:
        ax.set_title(cb_label, fontsize="x-large")

    output_path = Path(output_file)
    output_file_modified = output_path.with_stem(output_path.stem + "_hist")
    save_figure_png(output_file_modified)

    plt.close()

def plot_map(xx, yy, raster, labels, output_file, cb_label, title, unit,
             n_classes, bins, palette, custom_palette, orientation, extend, proj, dark_mode, transparent, x_fig, y_fig, hist):
    """
    Creates and saves a map plot.
    """
    # Check if raster is 2D
    if not isinstance(raster, np.ndarray) or raster.ndim != 2:
        raise ValueError("raster must be a 2D NumPy array")
    
    # Extend palette if needed
    if extend != "neither":
        if extend == "both":
            n_classes += 2
        else:
            n_classes += 1

    # Create a colormap based on the provided palette
    palette, palette_dict = get_color_palette(n_classes, palette=palette, custom_palette=custom_palette)
    cmap = colors.ListedColormap(palette)
    
    # Discretize the data into bins
    norm = colors.BoundaryNorm(boundaries=bins, ncolors=n_classes, extend=extend)
    
    # Create histogram
    if hist is True and output_file:
        plot_palette_hist(raster, output_file, cb_label, unit, bins, palette, dark_mode)

    # Create the figure and axis with projection
    fig = plt.figure(figsize=[x_fig, y_fig], constrained_layout=True)
    ax = fig.add_subplot(1, 1, 1, projection=projections[proj]())

    # Plot data
    filled = ax.pcolormesh(xx, yy, raster, cmap=cmap, norm=norm, shading='auto',
                           transform=ccrs.PlateCarree())

    # Add title, map features, colorbar, and colorbar label
    if title:
        ax.set_title(title, fontsize="xx-large", pad=15)

    ax, gridlines = add_map_features(ax)

    if labels is False: # Quantitative map
        cbar = add_colorbar_quant(fig, ax, filled, bins, orientation, extend)
        if unit:
            cbar.set_label(cb_label + " (in " + unit + ")", fontsize="large", labelpad=10)
        else:
            cbar.set_label(cb_label, fontsize="large", labelpad=10)
        cbar.ax.xaxis.set_label_position('top')

    else:               # Qualitative map
        cbar = add_colorbar_quali(fig, ax, filled, bins, orientation, labels)

    # Dark mode
    if dark_mode is True:
        fig, ax = make_dark_mode(fig, ax, cbar=cbar, gridlines=gridlines)

    if output_file:
        save_figure_png(output_file, transparent=transparent)
    else:
        plt.show()

    plt.close()

def make_simple_map(field: cp.Field, layer: str,  categorical: Optional[bool] = False, output_file: Optional[str] = None, redop: Optional[str] = 'av', 
                    cb_label: Optional[str] = None, title: Optional[str] = None, unit: Optional[str] = None,
                    n_classes: Optional[int] = 4, classification: List[float] | str = "linear", palette: Optional[str] = None,
                    custom_palette: Optional[str] = None, orientation: Optional[str] = 'horizontal', extend: Optional[str] = "neither", proj: Optional[str] = "Robinson",
                    force_zero: Optional[bool] = False, dark_mode: Optional[bool] = False, transparent: Optional[bool] =  False, x_fig: Optional[float] = 10, y_fig: Optional[float] = 10):
    """
    Create a map from a given Field object (apply time reduction) and save it to a file.

    Parameters
    ----------
    field : cp.Field
        Field object.
    layer : str
        layer name to display.
    categorical : bool, optional
        Set to True for categorical data mapping. Default False.
    output_file : str
        File path for saving the plot.
    redop : str, optional
        The reduction operation. Either 'sum' or 'av'. Default is 'av'.
    cb_label : str, optional
        Label of the colour bar, ideally the name of the variable.
    unit : str, optional
        Unit of the variable used.
    title : str, optional
        Title of the map.
    n_classes : int, optional
        Number of discrete color classes to use. Default is 4.
    classification : List[float] | str, optional
        Method to classify the data into different classes. One of 'linear', 'quantile', 'jenks', 'std'
        (https://gisgeography.com/choropleth-maps-data-classification/) or a list. Default is 'linear'.
    palette : str, optional
        Seaborn color palette to use for the line colors (https://seaborn.pydata.org/tutorial/color_palettes.html, recommended palette are in https://colorbrewer2.org).
    custom_palette : str, optional
        Path of custom color palette .txt file to use.
    orientation: str, optional
        Orientation of the legend. Either 'horizontal' or 'vertical'. Default is 'horizontal'.
    extend : str, optional
        Extend colourbar to maximum and minimum value. One of 'neither', 'min', 'max' or 'both'. Default is 'neither'.
    proj : str, optional
        Cartopy projection to use for the map (https://scitools.org.uk/cartopy/docs/v0.15/crs/projections.html).
        Default is 'Robinson'.
    force_zero : bool, optional
        If True, force the first (or the closest in diff_map) bin to zero. Default is False.
    dark_mode : bool, optional
        If True, apply dark mode styling. Default is False.
    transparent: bool, optional
        If True, make the figure transparent. Default is False.
    x_fig : float, optional
        Width of the figure in inches. Default is 10.
    y_fig : float, optional
        Height of the figure in inches. Default is 10.
    """
    # Retrieve metadata
    cb_label = cb_label or field.metadata['name']
    unit = unit or field.metadata['units']

    # Data processing pipeline
    if categorical:
        raster = cp.make_raster(field, layer)
        n_classes = len(raster.labels)
        bins = np.arange(n_classes)
        labels = raster.labels
    else:
        field_red = field.red_time(redop, inplace=False)
        raster = cp.make_raster(field_red, layer)
        bins = calculate_bins(raster.vmap, n_classes, classification, force_zero)
        labels = False

    plot_map(raster.xx, raster.yy, raster.vmap, labels, output_file,
             cb_label, title, unit, n_classes, bins, palette, custom_palette, 
             orientation, extend, proj, dark_mode, transparent, 
             x_fig, y_fig, hist=not categorical)

def make_diff_map(field_a: cp.Field, field_b: cp.Field, layer: str, output_file: Optional[str] = None, redop: Optional[str] = 'av', 
                  cb_label: Optional[str] = None, title: Optional[str] = None, unit: Optional[str] = None,
                  n_classes: Optional[int] = 4, classification: List[float] | str = "linear", palette: Optional[str] = None,
                  custom_palette: Optional[str] = None, orientation: Optional[str] = 'horizontal', extend: Optional[str] = "neither", proj: Optional[str] = "Robinson",
                  force_zero: Optional[bool] = False, dark_mode: Optional[bool] = False, transparent: Optional[bool] =  False, 
                  x_fig: Optional[float] = 10, y_fig: Optional[float] = 10, percentage: bool = False):
    """
    Create a difference map from two fields

    Parameters
    ----------
    field_a : cp.Field
        First Field object for computing the difference.
    field_b : cp.Field
        Second Field object for computing the difference.
    percentage : bool, optional
        If True, compute proportional difference in %. Default is False.
    """
    # Retrieve metadata
    cb_label = cb_label or field_a.metadata['name']
    unit = unit or field_a.metadata['units']

    # Apply space reduction to both fields
    field_a_red = field_a.red_time(redop, inplace=False)
    field_b_red = field_b.red_time(redop, inplace=False)
    raster_a = cp.make_raster(field_a_red, layer)
    raster_b = cp.make_raster(field_b_red, layer)

    # Compute the difference
    if percentage:
        with np.errstate(divide='ignore', invalid='ignore'):
            diff = np.where(raster_a.vmap != 0, (raster_b.vmap - raster_a.vmap) / raster_a.vmap * 100, 0)
    else:
        diff = raster_b.vmap - raster_a.vmap

    # Calculate bins for the difference map
    bins = calculate_bins(np.abs(diff), n_classes, classification, force_zero, diff_map=True)

    # Plot the map
    plot_map(raster_a.xx, raster_a.yy, diff, False, output_file, cb_label, title, unit,
             n_classes, bins, palette, custom_palette, orientation, extend, proj, 
             dark_mode, transparent, x_fig, y_fig, hist=True)