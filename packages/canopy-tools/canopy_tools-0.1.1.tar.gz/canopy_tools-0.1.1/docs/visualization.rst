.. _visualization:

Visualization
=============

**canopy** includes high-level functions to make figures directly from a Field object using `Seaborn <https://seaborn.pydata.org/index.html>`_ and `Cartopy <https://scitools.org.uk/cartopy/docs/latest/>`_ libraries.

Make a map
----------

.. currentmodule:: canopy.visualization.map

Using a Field object, you can make a simple map with :func:`make_simple_map`:

.. code-block:: python

    # Load your field first
    run_ssp1 = cp.get_source("example_data/ssp1A/","lpjguess")
    run_ssp1.load_field("cpool")

    cp.visualization.make_simple_map(field=run_ssp1.cpool, layer="Total")

You can check the different parameters available in the API reference: :func:`make_simple_map`. 

.. note::

    ``make_simple_map`` is using a Field to produce a figure. 
    
    By doing so, the rasterisation with ``make_raster`` is included in the function.

.. warning::

    In some specific set-ups, the use of "EuroPP" as projection will introduce
    a bug that will produce undesired polygons on the ocean.

    This is coming form **cartopy** and is being discussed in their `github issues <https://github.com/SciTools/cartopy/issues/1685>`_.

    If you encounter such issues, please use "TransverseMercator", 
    an adapted projection for the Europe region

You can also make a difference map between two Field objects using :func:`make_diff_map`:

.. code-block:: python

    cp.visualization.make_diff_map(field_a=run_ssp1.cpool, field_b=run_ssp3.cpool, layer="Total")

Make a time-series
------------------

.. currentmodule:: canopy.visualization.time_series

Using a Field object, you can make a time-series with :func:`make_time_series`:

.. code-block:: python

    cp.visualization.make_time_series(fields=cpool)

You can check the different parameters available in the API reference: :func:`make_time_series`. 

.. note::

    ``make_time_series`` is using a Field to produce a figure. 
    
    By doing so, the linearalization with ``make_lines`` is included in the function.

In addition, you can use kwargs parameters from the `seaborn.lineplot <https://seaborn.pydata.org/generated/seaborn.lineplot.html>`_ and `matplotlib.lines.Line2D <https://matplotlib.org/stable/api/_as_gen/matplotlib.lines.Line2D.html>`_ functions. This allows customization of line aesthetics such as `linewidth`, `linestyle`, `alpha`, etc.

.. code-block:: python

    cp.visualization.make_time_series(fields=cpool, layers="Total", linewidth=3, linestyle='-', alpha=0.3)

.. warning::

    Kwargs parameters are only available for single time series (not multiple), and without the ``rolling_mean`` parameter.

If you want to compare multiple time-series on the same figure, the function parameter `fields` also accepts a list of Field objects:

.. code-block:: python

    import canopy.visualization as cv

    # Let's load first multiple fields
    run_hist = cp.get_source("example_data/hist/","lpjguess")
    run_ssp1 = cp.get_source("example_data/ssp1A/","lpjguess")
    run_ssp3 = cp.get_source("example_data/ssp3A/","lpjguess")
    run_hist.load_field("cpool")
    run_ssp1.load_field("cpool")
    run_ssp3.load_field("cpool")

    # Make a list of your loaded fields
    fields = [run_hist.cpool,run_ssp1.cpool,run_ssp3.cpool]

    cv.make_time_series(fields=fields, 
                        layers=["Total","VegC","SoilC"],
                        ts_labels=["hist","ssp1","ssp3"])

In this case, the function parameter `ts_labels`, the list of labels for the time series, is mandatory.

By default, each time-series will get a different colour, and each layer will get a different line styles (solid, dashed, etc.). 

If you want to be opposite, you can use the the function parameter `reverse_hue_style`:

.. code-block:: python

    cv.make_time_series(fields=fields, 
                        layers=["Total","VegC","SoilC"],
                        ts_labels=["hist","ssp1","ssp3"],
                        reverse_hue_style=True)

Make a static plot
------------------

.. currentmodule:: canopy.visualization.static_plot

You can produce a scatter plot with regression lines and r-scores to compare two Fields objects (which can be reduced spatially, temporally, or both beforehand) with :func:`make_static_plot`:

.. code-block:: python

    cp.visualization.make_static_plot(field_a=run_a, field_b=run_b, layers="Total")

In addition, you can use kwargs parameters from the `seaborn.regplot <https://seaborn.pydata.org/generated/seaborn.regplot.html>`_ function.

Make a comparison plot
----------------------

.. currentmodule:: canopy.visualization.comparison_plot

You can compare a list of Field objects (for example, different runs) with :func:`make_comparison_plot`: 

.. code-block:: python

    cp.visualization.make_comparison_plot(fields=[model_a, model_b, model_c], plot_type="box", layers="Total")

This function can generate boxplot ("box"), strip plot, swarm plot, violin plot, boxen plot, point plot, bar plot or count plot based on the `plot_type` parameter.

In addition, you can use kwargs parameters from the `seaborn.catplot <https://seaborn.pydata.org/generated/seaborn.catplot.html>`_ function.

.. note::

    ``make_comparison_plot`` accept any kind of reduced Fields. 
    
    You can reduce spatially, temporally, or both your fields beforehand.
