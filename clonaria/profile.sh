#!/bin/bash

python -m cProfile -o cprofile.out ./main.py -d

python -c "import pstats; p = pstats.Stats('cprofile.out'); p.sort_stats('cumulative').print_stats(20)" | less
