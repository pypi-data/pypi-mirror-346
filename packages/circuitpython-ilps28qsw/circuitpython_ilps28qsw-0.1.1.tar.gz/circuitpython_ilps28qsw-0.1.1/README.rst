Introduction
============


.. image:: https://readthedocs.org/projects/circuitpython-ilps28qsw/badge/?version=latest
    :target: https://circuitpython-ilps28qsw.readthedocs.io/
    :alt: Documentation Status



.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord


.. image:: https://github.com/mrv96/CircuitPython_ILPS28QSW/workflows/Build%20CI/badge.svg
    :target: https://github.com/mrv96/CircuitPython_ILPS28QSW/actions
    :alt: Build Status


.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Code Style: Ruff

CircuitPython module for the ILPS28QSW absolute digital output barometer.

This is a pure-Python porting of:

* `ST's C driver <https://github.com/STMicroelectronics/ilps28qsw-pid>`_
* `ST's C examples <https://github.com/STMicroelectronics/STMems_Standard_C_drivers/tree/master/ilps28qsw_STdC/examples>`_


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.

Installing from PyPI
=====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/circuitpython-ilps28qsw/>`_.
To install for current user:

.. code-block:: shell

    pip3 install circuitpython-ilps28qsw

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install circuitpython-ilps28qsw

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install circuitpython-ilps28qsw

Installing to a Connected CircuitPython Device with Circup
==========================================================

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip3 install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install ilps28qsw

Or the following command to update an existing version:

.. code-block:: shell

    circup update

Usage Example
=============

See examples/ilps28qsw_read_data_polling.py for a demo of the usage.

Documentation
=============
API documentation for this library can be found on `Read the Docs <https://circuitpython-ilps28qsw.readthedocs.io/>`_.

For information on building library documentation, please check out
`this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/mrv96/CircuitPython_ILPS28QSW/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
