# p-process Research

This is my p-process research for Anna Simon at the University of Notre Dame.

## Getting Started

This project uses Python 3.6.4, so make sure Python is installed.

## Set Up

### Installing TALYS

Go to the following link to download the stable version of TALYS (1.8 in my case).

http://www.talys.eu/download-talys/

Expand talys1.8.tar, and cd into the talys folder.

Edit the "talys.setup" file. You need to download a fortran compiler and add TALYS to your binary source files.

Run the talys.setup file with the below command.

```
./talys.setup
```

After the script finishes running, TALYS should be installed and accesible by scripts on your system.

### After Installing Talys - Jupyter, Packages & Libraries

Firstly, visit http://jupyter.readthedocs.io/en/latest/install.html to install Jupyter to run the notebooks. Make sure you know how to open a Jupyter session with the below function in the command line.

```
jupyter notebook
```

Once Jupyter is installed, make sure the following packages are installed / the following cell executes properly. 

```
import os, glob
import numpy as np
import pandas as pd

import math
import itertools

import matplotlib as mpl
import matplotlib.pyplot as plt
```

### After Installing Talys - Data

Visit the following link to download the data for the element/isotope you care about.

http://www.kadonis.org/pprocess/

Note: The reactions we care about in this case are alpha-gamma and alpha-n, so only use data pertaining to those.

I like to keep these data files in a "kad_files" folder.

## Running the Script / Notebook

In this repository, I have created two different folders: template (which should be used to customize the process to your liking), and 113-indium (an example of the script using silver data and a smaller subset of model parameters).

I will suppose that you are using the template folder for the remainder of this document.

After cd'ing into the folder, open the template.ipynb. 

**Note: If you change the name of the notebook, see the following cell in the "Functions" section.

```
### CHANGE THIS CELL ONLY IF YOU CHANGE THE NAME OF THE NOTEBOOK
def clean_files():
    # clean file system
    ### WHERE YOU SEE 'template.ipynb', ENTER THE NEW NAME OF THE NOTEBOOK
    keeping = [ag_talys_file, an_talys_file, 'output', 'total.tot', 'template.ipynb','input']
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        if(f not in keeping):
            os.remove(f)
    print('Done --- File system clean.')
```

Change the following lines to properly point to the correct files. This corresponds to Cell 6.

```
### CHANGE THIS CELL
# read in files
ag_kad_file = './kad_files/XXXXXXXXXXXXXX'
an_kad_file = './kad_files/XXXXXXXXXXXXXX'
```

Note: Do **not** change anything in the "Imports" or "Functions" sections.

Note 2: If the downloaded data did not contain error bars, the notebook will warn you. 

After the data filenames have been changed, scroll down to the "Talys Portion" section.

The first cell in this section needs to be changed to reflect your element/isotope. It should like the cell below.

```
### CHANGE THIS CELL
# general parameters
symbol = 'xx'
mass = XXX
z = XXX
```

**Note: symbol should be a lower-case string; mass and z should be integers.**  

After changing the above two cells, the bulk of the computations can be executed in the "Talys Loop" section. This process takes a long time, especially when the original kadonis files include lots of data points. Once the loop is done, a message will let you know that the working file system has been cleaned.

The rest of the notebook should not need any more modifications.

You may encounter the following error message when plotting, but you need not worry about it.

```
/usr/local/Cellar/python3/3.6.4/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/matplotlib/scale.py:111: RuntimeWarning: invalid value encountered in less_equal
  out[a <= 0] = -1000
```

**Note: The current working version of this repository has a few flaws; namely, I am not sure why the TALYS calculations are not smooth-looking functions.**

If you run into questions, email me at ptinsley@nd.edu.