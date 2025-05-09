============
Installation
============

Installing bilby_pipe from release
----------------------------------

.. tabs::

   .. tab:: conda

      To install the latest :code:`bilby_pipe` release from `conda-forge
      <https://anaconda.org/conda-forge/bilby_pipe>`_, run

      .. code-block:: console

         $ conda install -c conda-forge bilby_pipe

      Note, this is the recommended installation process as it ensures all
      dependencies are met.

   .. tab:: pypi

      To install the latest :code:`bilby_pipe` release from `PyPi
      <https://pypi.org/project/bilby-pipe/>`_, run

      .. code-block:: console

         $ pip install --upgrade bilby_pipe

      WARNING: this is not the recommended installation process, some
      dependencies (see below) are only automatically installed by using the
      conda installation method.


Install bilby_pipe for development
----------------------------------

:code:`bilby_pipe` is developed and tested for Python 3.8, and 3.9. In the
following, we demonstrate how to install a development version of
:code:`bilby_pipe` on a LIGO Data Grid (LDG) cluster.

First off, clone the repository

.. code-block:: console

   $ git clone git@git.ligo.org:lscsoft/bilby_pipe.git
   $ cd bilby_pipe/

.. note::
   If you receive an error message:

   .. code-block:: console

      git@git.ligo.org: Permission denied (publickey,gssapi-keyex,gssapi-with-mic).
      fatal: Could not read from remote repository.

   Then this indicates you have not correctly authenticated with your
   git.ligo account. It is recommended to resolve the authentication issue, but
   you can alternatively use the HTTPS URL: replace the first line above with

   .. code-block:: console

      $ git clone https://git.ligo.org/lscsoft/bilby.git

Once you have cloned the repository, you need to install the software. How you
do this will depend on the python installation you intend to use. Below are
several easy-to-use options. Feel free to disregard these should you already
have an alternative.

Python installation
===================

.. tabs::

   .. tab:: conda

      :code:`conda` is a recommended package manager which allows you to manage
      installation and maintenance of various packages in environments. For
      help getting started, see the `IGWN Conda Distribution documentation
      <https://computing.docs.ligo.org/conda/>`_.

      For detailed help on creating and managing environments see `these help pages
      <https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html>`_.
      Here is an example of creating and activating an environment named  bilby

      .. code-block:: console

         $ conda create -n bilby python=3.9
         $ conda activate bilby

   .. tab:: virtualenv

      :code`virtualenv` is a similar tool to conda. To obtain an environment, run

      .. code-block:: console

         $ virtualenv --python=/usr/bin/python3.9 $HOME/virtualenvs/bilby_pipe
         $ source virtualenvs/bilby_pipe/bin/activate


   .. tab:: CVMFS

      To source a :code:`Python 3.9` installation on the LDG using CVMFS, run the
      commands

      .. code-block:: console

         $ source /cvmfs/software.igwn.org/conda/etc/profile.d/conda.sh
         $ conda activate igwn-py39

     Documentation for this conda setup can be found here: https://computing.docs.ligo.org/conda/



Installing bilby_pipe
=====================

Once you have a working version of :code:`python`, you can install
:code:`bilby_pipe` with the command

.. code-block:: console

   $ pip install --upgrade git+file://${HOME}/PATH/TO/bilby_pipe

Or, alternatively

.. code-block:: console

   $ python setup.py install

The former (using :code:`pip`) is preferred as it makes it easier to uninstall,
but many people use the direct installation method out of habit.

Be careful to check any warning messages about where the code has been
installed.

Additionally, if you receive error messages about read-only file systems you
can add :code:`--user` to the installation call. This will install the software
in a local directory, usually :code:`~/.local`. Be aware that this may not be
on your :code:`PATH` and also, that this will effect all python environments.

Once you have run these steps, you have :code:`bilby_pipe` installed. However,
you will also need to install `bilby <https://git.ligo.org/lscsoft/bilby>`_.
Installation instructions can be found `here
<https://lscsoft.docs.ligo.org/bilby/installation.html>`_.

Whilst the code is developed, we expect to find many bugs. These can either be
in bilby_pipe or in bilby. To debug the problem it is useful to know which
version of the code you are using.

To see which version of the code you are using, call

.. code-block:: console

  $ bilby_pipe --version

If the output of :code:`bilby_pipe --version` contains something like

.. code-block:: console

  bilby_pipe 0.0.1: (UNCLEAN) 3fd2820 2019-01-01 15:08:26 -0800

rather than

.. code-block:: console

  bilby_pipe 0.0.1:

Then you have installed :code:`bilby_pipe` from source. This information is
also printed every time the code is called and therefore will be at the top of
your log files.


Dependencies
------------

:code:`bilby_pipe` handles data from the interferometers using the `gwpy
<https://gwpy.github.io/docs/stable/timeseries/remote-access.html>`_ library.
When requesting data, we first look for local frame-files, then use the `NDS2
<https://www.lsc-group.phys.uwm.edu/daswg/projects/nds-client/doc/manual/>`_
library to fetch proprietary data remotely, finally we search the open data.

To best utilise this tool, you should ensure your python installation has
access to `LDAStools-frameCPP
<https://anaconda.org/conda-forge/python-ldas-tools-framecpp>`_
for local frame-file lookup and `the NDS2 library
<https://anaconda.org/conda-forge/python-nds2-client>`_ for proprietary remote
data look up. These libraries are typically part of most LIGO data stacks and
can be installed with conda using the commands

.. code-block:: console

   $ conda install -c conda-forge python-ldas-tools-framecpp
   $ conda install -c conda-forge python-nds2-client
