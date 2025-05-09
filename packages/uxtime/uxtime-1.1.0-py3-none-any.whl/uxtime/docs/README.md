# Unixtime Converter

The Unixtime Converter is a lightweight python program with a Tkinter-GUI. 
It calculates local time or UTC into an unixtimestamp or vice versa. Basically 
it can be used and downloaded by everybody. Unixtime is mainly used in the IT.


# Installation/Setup

## Prerequisites

Make sure that your python setup has minimumversion 3.9 and contains the libraries for tkinter. To get this information you can type in into a terminal the command python (it can be that you have to use python3) and hit enter. You shoud get something like this:

    myuser@xxxx1:~$ python3
    Python 3.11.2 (main, Nov 30 2024, 21:22:50) [GCC 12.2.0] on linux
    ype "help", "copyright", "credits" or "license" for more information.
    >>> 


In the second line of the output you see the current version of python. As next you can type in "import tkinter as tk" and hit enter. If the tkinter libraries are installed nothing will happen - otherwise you will get an error that it can't be imported or found. If you have no issue you can type in the following and you will see the current version of tkinter:

    myuser@xxxx1:~$ python3
    Python 3.11.2 (main, Nov 30 2024, 21:22:50) [GCC 12.2.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import tkinter as tk
    >>> tkversion = tk.TkVersion
    >>> print(tkversion)
    8.6
    >>>

If you can see something like this you are ready for setup.


## Proceed with installation

Currently the setup is only tested on linuxbased os with python3 minimumversion 3.9. It is strongly recommended to install it into a virtual environment (venv).
To start the setup use pip:

    pip install uxtime

A setup Windows 10 or 11 will follow soon.


## Start the application

After installing the application you can start it with "unixtime" from an terminal.


## How it works

The program needs exactly 2 parameters to calculate the requested time:
* select a timezone from the list
* fill in a unixtimestamp or localtime or utc and click on the butten left of the field
All 3 fields for time will be filled/calculated

Basically it's not needed to click on the resetbutton. It's for more clearance for the usage. If you click on it all entriefields for time (localtime, utc-time and unixtime) are cleared.<br><br>
If you change one timefield (and both other timefields containing values) and you click on the button beside of this field all other (time-)fields are recalculated.

done - that's it!

Read the documentation online (including Screenshots):

https://docs.roadrunnerserver.com/unixtime/html/index.html
