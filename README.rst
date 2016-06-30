==================
SVG Batch Exporter
==================

Inkscape based Python 3 script/module for batch exporting SVG files. It
supports exporting to wide variety of image/document formats. Also,
rules (size, format etc) can be declared (in a JSON-formatted-file_) for
each svg file while batch exporting.

Supported formats
=================

-  png
-  jpeg (or) jpg
-  bmp
-  gif
-  pdf
-  ps
-  eps
-  im
-  pcx
-  tiff

**Note**

-  'pdf', 'ps', 'eps' does not support exporting SVG to custom width,
   height via Inkscape

Requirements
============

1. Python 3
2. `Inkscape <https://inkscape.org>`__
3. `Pillow (PIL fork) <https://python-pillow.org/>`__ library

    .. code:: bash

        pip3 install pillow

Install
=======

1. Clone the repository:

   ::

       >> git clone https://github.com/anselm94/inkscape-svg-batch-exporter.git

2. ``cd`` into the directory:

   ::

       >> cd inkscape-svg-batch-exporter

3. Run setup script (if needed to be installed):

   ::

       >> python3 setup.py install

Usage
=====

Can be used either as a command-line_ script or as a python module_

.. _command-line:
1. Command-line Script:
-----------------------

**Command**

.. code:: bash

    svg_batch_exporter.py srcdir outdir [--rules RULES] [--size SIZE] [--format FORMAT] [--drawing_only DRAWING_ONLY] [--inkscape INKSCAPE]

**Note**

``--rules``, ``--size``, ``--format``, ``--drawing_only``,
``--inkscape`` are optional

Use ``-h`` or ``--help`` to get help

.. code:: usage: svg_batch_exporter.py [-h] [--rules RULES] [--size SIZE]
                              [--format FORMAT] [--drawing_only DRAWING_ONLY]
                              [--inkscape INKSCAPE]
                              srcdir outdir

    Inkscape powered rule-based SVG batch exporter to multiple image formats

    positional arguments:
      srcdir                Path to directory containing SVG files
      outdir                Path to directory to output image files

    optional arguments:
      -h, --help            show this help message and exit
      --rules RULES         JSON rules file
      --size SIZE           'width,size' (without space) Size of exported images
                            in pixels. E.g 50,50 If --rules is supplied, files not
                            mentioned in the JSON file will be exported with SIZE
      --format FORMAT       Image format to be exported. Formats supported: png,
                            jpeg, jpg, pdf, bmp, gif, ps, eps, im, pcx, tiff
      --drawing_only DRAWING_ONLY
                            'yes' or 'y' -> Drawing area alone should be exported.
                            'no' or 'n' -> Whole page should be exported
      --inkscape INKSCAPE   Inkscape custom executable path. Leave it if default
                            Inkscape installation is to be used

    See https://github.com/anselm94/inkscape-svg-batch-exporter for more help

**Example**

.. code:: bash

    svg_batch_exporter.py /home/userx/svg_dir /home/userx/out_dir --rules /home/userx/rules.json --size 50,50 --format jpg --drawing_only yes

.. _module:
2. Module:
----------

1. Import ``export_svg`` from ``svg_batch_exporter`` module

.. code:: python

    >> from svg_batch_exporter import export_svg

2. Call the function

.. code:: python

    >> export_svg(src_dir, out_dir, json_rules_file = None, file_format = None, size = None, drawing_only = None, inkscape_path = "default")

**Example**

.. code:: python

    >> from svg_batch_exporter import export_svg
     >> export_svg("/home/userx/svg_dir", "/home/userx/out_dir",
                   json_rules_file = "/home/userx/rules.json", file_format = "jpeg",
                   size = [50, 50], drawing_only = True, inkscape_path="default")

--------------

Notes
=====

.. _JSON-formatted-file:
1. JSON formatted Rules file
----------------------------

Rules for each image exported has following parameters:

-  format
-  size
-  drawing\_only

These parametric rules can be declared in a JSON formatted file.

.. code:: python

    {
        # '_globalrule_' can be defined without the need of defining local rule for each svg file or programmatically
        "_globalrule_" :
        {
          "size" : [300, 300],
          "format" : "jpg"
          # Parameters can be dropped
        },
         # local rule
        "svg_file_1": # SVG filename without .svg extension
        {
          "size": "default", # 'default' if actual size of the SVG image is to be used
          "format": "gif",
          "drawing_only": true
        },
        # local rule
        "svg_file_2":
        {
          "drawing_only": true
          # Parameters can be dropped
        }
        # Local rules for other SVG files can be dropped
    }

Parameters for each file are assigned in the following priority:

+-------------------------------------------------------------------------+
| ``Default rules -> Global rules -> Programmatic rules -> Local Rules``  |
+=========================================================================+
| ``---- (1) ---- || ---- (2) --- || ------- (3) ------ || --- (4) ---``  |
+-------------------------------------------------------------------------+

Parameter, if found in a rule of higher priority will be used, else
default parameters (priority 1) will be used.

-  **Default Rules** has following parameters:

   -  size: "default" (i.e. Actual size of the SVG file is to be used)
   -  format: "png"
   -  drawing\_only: True

-  **Global rules** and **Local rules** can be defined in a JSON rules
   file
-  **Programmatic Rules** are the global parameters supplied to the
   ``export_svg()`` module function or as arguments for the command line
   script

License
=======

.. code::

    The MIT License (MIT)

    Copyright (c) 2016 Merbin J Anselm

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
