# Python Tkinter Application Manager

## What this does

The purpose of this application is to create an
easy-to-use application manager for Tkinter. I plan to
use this to create some pre-built utilities for doing
calculations and creates graphs etc, but can also be
used to do other things that users can create (with
upcoming documentation on how to use this to it it's
full extent).

## Installation info

Recommended version: Python 3.8.2

However, most/all versions above Python 3.0 should work.

### Required dependencies

[Pillow/PIL](https://pillow.readthedocs.io/en/stable/installation.html)

[Matplotlib](https://matplotlib.org/3.1.1/users/installing.html)

[Sympy](https://docs.sympy.org/latest/install.html)

### Additional requirements for Linux

If tkinter is not installed, run in the terminal
```bash
sudo apt-get install python3-pip
```

If you are running Ubuntu in WSL (Windows Subsystem for Linux), run
```bash
sudo nano ~/.bashrc
```
Then, add to the end of the file
```bash
export DISPLAY:0;
```
Then save and exit (shift+X to exit, Y to confirm save, enter to save to the same filename)

## How to run

### Windows 10

In the installed file
```bash
python main.py
```

### Linux

In the installed file
```bash
python3 main.py
```
