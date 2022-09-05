#!/usr/bin/env python3

'''
██████  ███████ ███    ██  █████  ███    ███  ██████  ███    ███ ██  ██████  ██████  ███    ██ 
██   ██ ██      ████   ██ ██   ██ ████  ████ ██    ██ ████  ████ ██ ██      ██    ██ ████   ██ 
██████  █████   ██ ██  ██ ███████ ██ ████ ██ ██    ██ ██ ████ ██ ██ ██      ██    ██ ██ ██  ██ 
██   ██ ██      ██  ██ ██ ██   ██ ██  ██  ██ ██    ██ ██  ██  ██ ██ ██      ██    ██ ██  ██ ██ 
██   ██ ███████ ██   ████ ██   ██ ██      ██  ██████  ██      ██ ██  ██████  ██████  ██   ████ 
                                                                                               
                                                                                               
███████ ██   ██      ██████  ██    ██ ██      ██   ██ ██    ██ ███████                         
██       ██ ██       ██   ██ ██    ██ ██      ██  ██  ██    ██ ██                              
█████     ███  █████ ██████  ██    ██ ██      █████   ██    ██ ███████                         
██       ██ ██       ██   ██ ██    ██ ██      ██  ██  ██    ██      ██                         
███████ ██   ██      ██████   ██████  ███████ ██   ██  ██████  ███████                         
                                                                                               

The script of the dead....AKA an Evil Dead themed bulk file renaming utility :)
-
Usage: 
cd to script directory (via terminal of choice) and type: python renamex.py --help

Author:
sorzkode
sorzkode@proton.me
https://github.com/sorzkode

MIT License
Copyright (c) 2022 sorzkode
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

# Importing needed modules / libraries.
import os                                       
from tkinter import filedialog                  
from tkinter import *                           
import pyfiglet                                 
import pathlib                                  
import time                                     
import click                                    

# Enables the ability to ask the user for directory input in the 'start_script' function below.
root = Tk() 
root.withdraw() 

# Creates an ASCII art intro banner used in the 'start_script' function.
reb_banner = pyfiglet.figlet_format("Renamomicon Ex-Bulkus") 


# This function is called at the start of every function within the script. 
# It prints the script intro, asks the user to select a directory, and creates a list of files.
# The files list includes subdirectories which is why filenames are split into sections for the other functions.
def start_script(): 
    global dirselect, files 
    print(reb_banner) 
    print("The script of the dead...") 
    print("AKA an Evil Dead themed bulk file renaming utility :)")
    dirselect = filedialog.askdirectory() 
    files = os.listdir(dirselect) 

# Creates a 'main' group in click to tie all functions together. 
# Called each time the script is ran but doesn't actually execute any code.
# The docstring below is used as a descriptor within the click interface.
@click.group() 
def main(): 
    '''Renamomicon Ex-Bulkus...The script of the dead. AKA an Evil Dead bulk file renaming utility :)''' 
    pass 

# Creates the 'xspaces' command within the main click group above.
# Removes spaces from all filenames in a given directory.
@main.command(
    name='xspaces', 
    help='Obliterates spaces from filenames in any directory using your trusty boomstick!'
    )
def remove_spaces():
    start_script()
    for file in files:
        filenames = pathlib.Path(str(file)).stem
        verify_files = os.path.isfile(os.path.join(dirselect, file))
        bool_count = [verify_files].count(True)
        if verify_files is False:
            pass
        elif verify_files is True:
            space_counter = "".join(filenames).count(" ")
            if space_counter >= 1:
                os.rename(
                    os.path.join(dirselect, file), 
                    os.path.join(dirselect, file.replace(' ', ''))
                    )
                print(f"Obliterated {space_counter} space(s) from your filenames...")
            else: 
                print(f"The filenames in {dirselect} don't contain any spaces. Better go to S-Mart and buy ya some.")
                break
    if bool_count == 0:
        print(f"Hey numbnuts, {dirselect} doesn't contain any valid files to rename.")

# Creates the 'replacer' command within the main click group above.
# Replaces any section of a filename with whatever the user wants.
@main.command(
    name='replacer', 
    help='Roses are red, violets are blue, out with the old, in with the new. Replace part of a filename with whatever you want (case sensitive).'
    )
def replacer():
    start_script()
    toreplace = input("Give me some sugar baby, I mean, tell me what you want to replace (case sensitive): ")
    replaced = input(f"What do you want to put in place of {toreplace}? ")
    for file in files:
        filenames = pathlib.Path(str(file)).stem
        extensions = file.split('.')[-1]
        verify_files = os.path.isfile(os.path.join(dirselect, file))
        bool_count = [verify_files].count(True)
        if verify_files is False:
            pass
        elif verify_files is True:
            file_checker = "".join(filenames).count(toreplace)
            if file_checker >= 1:
                os.rename(
                    os.path.join(dirselect, filenames + '.' + extensions), 
                    os.path.join(dirselect, filenames.replace(toreplace, replaced) + '.' + extensions)
                    )
                print(f"Groovy! {file_checker} {toreplace}'s are now {replaced}'s...")
            else:
                print(f"Go back and read the manual. The files in {dirselect} don't contain {toreplace} in their names.")
                break
    if bool_count == 0:
        print(f"Something's wrong with your incantation. {dirselect} doesn't have any valid files to rename.")

# Creates the 'upper' command within the main click group above.
# Makes all filenames in the given directory uppercase.
@main.command(
    name='upper', 
    help='UPgrade those pathetic filenames with shiny new uppercase lettering.'
    )
def uppercase():
    start_script()
    for idx, file in enumerate(files):
        extensions = file.split('.')[-1]
        filenames = pathlib.Path(str(file)).stem
        verify_files = os.path.isfile(os.path.join(dirselect, file))
        bool_count = [verify_files].count(True)
        upper_checker = filenames.isupper()
        upper_count = [upper_checker].count(False)
        if (verify_files is False) and (upper_checker is True):
            pass
        elif (verify_files is True) and (upper_checker is False):
            os.rename(
                os.path.join(dirselect, filenames + '.' + extensions), 
                os.path.join(dirselect, filenames.upper() + '.' + extensions)
                )
            print(f"UPgraded {idx} file(s)...")
    if bool_count == 0:
        print(f"Stop yanking my chain. {dirselect} doesn't contain any valid files to UPgrade.")
    elif upper_count == 0:
        print(f"The filenames in {dirselect} can't be upgraded anymore than they already are boss.")

# Creates the 'lower' command within the main click group above.
# Makes all filenames in the given directory lowercase.
@main.command(
    name='lower',
    help='Your filenames a little too loud? This will cut them down to size and make them all lowercase.'
    )
def lowercase():
    start_script()
    for idx, file in enumerate(files):
        extensions = file.split('.')[-1]
        filenames = pathlib.Path(str(file)).stem
        verify_files = os.path.isfile(os.path.join(dirselect, file))
        bool_count = [verify_files].count(True)
        lower_checker = filenames.islower()
        lower_count = [lower_checker].count(True)
        if (verify_files is False) and (lower_checker is True):
            pass
        elif (verify_files is True) and (lower_checker is False):
            os.rename(
                os.path.join(dirselect, filenames + '.' + extensions),
                os.path.join(dirselect, filenames.lower() + '.' + extensions)
                )
            print(f"Chopped {idx} filename(s) down to size...")
    if bool_count == 0:
        print(f"Stop yanking my chain. {dirselect} doesn't contain any valid files to downgrade.")
    elif lower_count == 0:
        print(f"The filenames in {dirselect} can't be downgraded anymore than they already are boss.")

# Creates the 'date' command within the main click group above.
# Adds today's date to the end of filenames with any given delimeter.
@main.command(
    name='date',
    help='Time to tell those filenames what time it is. Add the date to the end of your filenames with a custom delimeter.'
    )
def add_date():
    start_script()
    date_splitter = input("What do you want between the filenames and today's date? (leave blank for none): ")
    for idx, file in enumerate(files):
        extensions = file.split('.')[-1]
        filenames = pathlib.Path(str(file)).stem
        datestring = time.strftime("%m%d%Y")
        verify_files = os.path.isfile(os.path.join(dirselect, file))
        bool_count = [verify_files].count(True)
        if verify_files is False:
            pass
        elif verify_files is True:
            os.rename(
                os.path.join(dirselect, filenames + '.' + extensions),
                os.path.join(dirselect, filenames + date_splitter + datestring + '.' + extensions)
                )
            print(f"Added {datestring} to {idx} file(s)...")
    if bool_count == 0:
        print(f"Yo, deadite, check again, {dirselect} doesn't contain any valid files to rename.")

# Calls the main function / executes the script
if __name__ == "__main__":
    main()