Installation
============

This installation guide includes only the GeoCAT-examples installation instructions.
Please refer to `GeoCAT Contributor's Guide <https://geocat.ucar.edu/pages/contributing.html>`_ for installation of
the whole GeoCAT project.

Create a GeoCAT-examples Conda environment
------------------------------------------
GeoCAT-examples is not distributed as a conda package; thus, there is no conda installation for it.

The easiest way to access GeoCAT-examples is by cloning the repo and then using a `Conda <http://conda.pydata.org/docs/>`_
environment and then building file of which is provided in this repo as follows:

From the root directory of the cloned geocat-examples repository, run the following commands:

.. code-block:: bash

   $ conda env create -f conda_environment.yml -n geocat-examples
   $ conda activate geocat-examples

Note that the Conda package manager automatically installs all the required
dependencies of GeoCAT-examples listed under ``conda_environment.yml`` file (such as ``geocat-comp``,
``geocat-datafiles``, ``cartopy``, ``matplotlib``, ``netcdf4``, etc.); therefore, there is no need to
explicitly install those packages.

If you need to make use of other software packages with GeoCAT-examples, you may wish
to install them into your ``geocat-examples`` environment at anytime with a command as in the
following example (assuming your ``geocat-examples`` environment is already activated):

.. code-block:: bash

   $ conda install -c bokeh bokeh

If you are interested in learning more about how Conda environments work, please visit
the `managing environments <https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html>`_
page of the Conda documentation.
