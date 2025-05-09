import seaborn as sns
import matplotlib.pyplot as plt
import warnings
import os

def get_color_palette(n_classes, palette=None, custom_palette=None):
    """
    Generate a color palette for plotting based on either a ColorBrewer palette or a custom palette file.
    
    Parameters
    ----------
    n_classes : int
        Number of colors/classes needed.
    palette : str, optional
        Name of the seaborn palette to use (e.g., "YlGnBu").
    custom_palette : str, optional
        Path of custom color palette .txt file to use.

    Returns
    -------
    List[str]
        A color palette (list of color values).
    """
    if custom_palette:
        palette_dict = {}
        with open(custom_palette, 'r') as file:
            lines = file.readlines()
            if len(lines) != n_classes:
                raise ValueError(f"Custom palette file has {len(lines)} lines, but {n_classes} classes are required.")
            for line in lines:
                parts = line.strip().split()
                if len(parts) == 2:
                    label, color = parts
                    palette_dict[label] = color
                else:
                    raise ValueError("Custom palette provided should have two elements maximum per line.")
        
        # Extract colors from the dictionary
        palette = [palette_dict[label] for label in palette_dict]

    else:
        if palette:
            palette = sns.color_palette(palette, n_colors=n_classes)
        else:
            if n_classes > 20:
                raise ValueError("A maximum of 20 classes is recommended. Use your own palette with custom_palette.")
            palette = sns.color_palette("tab20", n_colors=n_classes)
        palette_dict = None
    
    return palette, palette_dict

def make_dark_mode(fig, ax, legend_style=None, cbar=None, gridlines=None):
    dark_gray = '#1F1F1F'
    fig.patch.set_facecolor(dark_gray)
    ax.set_facecolor(dark_gray)
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.title.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    for spine in ax.spines.values():
        spine.set_edgecolor('white')

    if gridlines:
        gridlines.xlabel_style = {'color': 'white'}
        gridlines.ylabel_style = {'color': 'white'}
    
    if cbar:
        cbar.ax.xaxis.label.set_color('white')
        cbar.ax.tick_params(axis='x', colors='white')
        cbar.outline.set_edgecolor('white')
    
    legend = ax.get_legend()
    if legend and legend_style == 'default':
        for text in legend.get_texts():
            text.set_color('white')
    
    return fig, ax

def save_figure_png(output_file, bbox_inches=None, transparent=False):
    """
    Save the current matplotlib figure as a PNG file.

    Parameters:
    - output_file (str): File path for saving the plot.
    - bbox_inches (str or None): Set to 'tight' to trim white space, or None for default.
    - transparent (bool): If True, the background of the saved figure will be transparent.
    """
    # Ensure the extension is .png
    base, _ = os.path.splitext(output_file)
    output_file = f"{base}.png"
    
    # Create directory if it doesn't exist
    directory = os.path.dirname(output_file)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    
    # Save the figure
    plt.savefig(output_file, format="png", dpi=300, bbox_inches=bbox_inches, transparent=transparent)