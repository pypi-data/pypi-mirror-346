====
Main
====

.. automodule:: bilby_pipe.main

Command line interface
----------------------

The primary user-interface for this code is a command line tool
:code:`bilby_pipe`, for an overview of this see `the user interface
<user-interface.txt>`_.

Main function
-------------
Functionally, the main command line tool is
calling the function :code:`bilby_pipe.main.main()`, which is transcribed here:

.. code-block:: python

   def main():
       """ Top-level interface for bilby_pipe """
       args, unknown_args = parse_args(sys.argv[1:], create_parser())
       inputs = MainInput(args, unknown_args)
       # Create a Directed Acyclic Graph (DAG) of the workflow
       Dag(inputs)

As you can see, there 3 steps. First the command line arguments are parsed, the
:code:`args` object stores the user inputs and any defaults (see `Command line
interface`_) while :code:`unknown_args` is a list of any unknown arguments.

The logic of handling the user input (in the form of the :code:`args` object)
is handled by the `Main Input`_ object. Following this, the logic of generated a DAG
given that user input is handled by the Dag_ object.

Main Input
----------

.. autoclass:: bilby_pipe.main.MainInput

Dag
---

#.. autoclass:: bilby_pipe.job_creation.dag.Dag
