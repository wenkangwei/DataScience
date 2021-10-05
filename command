#!/bin/bash

module load courses/cpsc6300
IP=$(hostname -I | awk '{print $1}')
cd ~/CPSC6300DataScience; jupyter-notebook --ip=$IP --no-browser
