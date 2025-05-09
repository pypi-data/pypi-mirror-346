.. _field:

Field
=====

.. currentmodule:: canopy.core.field

**canopy** works with :class:`Field` object, which is:

- a self-describing data container, with indexed data, metadata and grid information
- an interface between user and data
- meant for both model and observational data

Open and read data
------------------

You can read data from a DGVM or a LSM in two different ways

First, you can read the data directly from a file with :meth:`Field.from_file`:

.. code-block:: python

    cpool = cp.Field.from_file('/run/path/cpool.out.gz')

.. currentmodule:: canopy.sources.registry

Alternatively, by getting the source of a run path and load the desired fields with :func:`get_source` and ``load_field``:

.. code-block:: python

    #  Getting source of the run
    run = cp.get_source('/run/path/', 'lpjguess')

    # Load field for example carbon pool
    cpool = run.load_field('cpool')

Data manipulation
=================

Grid operations
---------------

Data reductions
---------------

.. currentmodule:: canopy.core.field.Field

You can reduce your data through the time dimension with :meth:`red_time`:

.. code-block:: python

    cpool_timeav = run.cpool.red_time('av')

and through the spatial dimension with :meth:`red_space`:

.. code-block:: python

    cpool_spaceav = run.cpool.red_space('av')

Combine Fields
--------------

Utilities
=========

.. currentmodule:: canopy.util.fieldops

Create raster 
-------------

After reducing your data with a time average, you can make a raster pandas.DataFrame with :func:`make_raster`:

.. code-block:: python

    cpool_raster = cp.make_raster(cpool_timeav, 'Total')

Create "lines" object
---------------------

After reducing your data with a spatial average, you can make "lines" pandas.DataFrame with :func:`make_lines`:

.. code-block:: python

    cpool_lines = cp.make_lines(cpool_timeav, 'Total')