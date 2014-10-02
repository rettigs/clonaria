Clonaria
========
Clonaria is an open source sidescrolling block-based platformer inspired by [Terraria](http://terraria.org/) written in Python that is intended to serve as a fun programming exercise and learning experience.  This is not meant to be "good" code; while cleaniness and flexibility are goals, the primary focus is on exploring both Python itself and the concepts behind game development.  Pull requests are welcome!

The original Java version of Clonaria has been renamed to [Clonaria-Java](https://github.com/rettigs/clonaria-java) and there are no plans to update it any further.

System Dependencies
-------------------
* cpython/pypy 2.7
* python-dev
* swig

Installation
------------
    # In a virtualenv or as root:
    git clone https://github.com/rettigs/clonaria.git
    cd clonaria
    pip install -r requirements.txt
    cd clonaria
    ./main.py

Controls
--------
* Movement: `WASD`/`arrow keys`
* Jump: `spacebar`
* Zoom: `+`/`-`
* Reset zoom: `=`
* Break blocks: `left click`
* Place blocks: `right click`/`middle click`

Notes
-----
main.py may be passed the -h or --help flags to view available command line options.
