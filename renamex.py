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
Mister Riley
sorzkode@proton.me
https://github.com/sorzkode

MIT License
Copyright (c) 2024 Mister Riley
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

# Dependencies
import os
from tkinter import filedialog
from tkinter import *
import pyfiglet
import pathlib
import time
import click

# Main class
class Renamex:
    def __init__(self):

        '''Initializes the script and creates a root window for the file dialog'''

        self.root = Tk()
        self.root.withdraw()
        self.reb_banner = pyfiglet.figlet_format("Renamomicon Ex-Bulkus")

    def start_script(self):

        '''Starts the script and asks for a directory to work in'''
        
        print(self.reb_banner)
        print("The script of the dead...")
        print("AKA an Evil Dead themed bulk file renaming utility :)")
        dir_select = filedialog.askdirectory()
        files = os.listdir(dir_select)
        return dir_select, files

    @click.group()
    def main(self):
        '''Renamomicon Ex-Bulkus...The script of the dead. AKA an Evil Dead bulk file renaming utility :)'''
        pass

    @main.command(
        name='xspaces',
        help='Obliterates spaces from filenames in any directory using your trusty boomstick!'
    )
    def remove_spaces(self):
        try:
            dir_select, files = self.start_script()
            for file in files:
                file_name = pathlib.Path(str(file)).stem
                verify_files = os.path.isfile(os.path.join(dir_select, file))
                bool_count = [verify_files].count(True)
                if verify_files is False:
                    pass
                elif verify_files is True:
                    space_counter = "".join(file_name).count(" ")
                    if space_counter >= 1:
                        os.rename(
                            os.path.join(dir_select, file),
                            os.path.join(dir_select, file.replace(' ', ''))
                        )
                        print(f"Obliterated {space_counter} space(s) from your filenames...")
                    else:
                        print(f"The filenames in {dir_select} don't contain any spaces. Better go to S-Mart and buy ya some.")
                        break
            if bool_count == 0:
                print(f"Hey numbnuts, {dir_select} doesn't contain any valid files to rename.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    @main.command(
        name='replacer',
        help='Roses are red, violets are blue, out with the old, in with the new. Replace part of a filename with whatever you want (case sensitive).'
    )
    def replacer(self):
        try:
            dir_select, files = self.start_script()
            to_replace = input("Give me some sugar baby, I mean, tell me what you want to replace (case sensitive): ")
            replaced = input(f"What do you want to put in place of {to_replace}? ")
            for file in files:
                file_name = pathlib.Path(str(file)).stem
                extensions = file.split('.')[-1]
                verify_files = os.path.isfile(os.path.join(dir_select, file))
                bool_count = [verify_files].count(True)
                if verify_files is False:
                    pass
                elif verify_files is True:
                    file_checker = "".join(file_name).count(to_replace)
                    if file_checker >= 1:
                        os.rename(
                            os.path.join(dir_select, file_name + '.' + extensions),
                            os.path.join(dir_select, file_name.replace(to_replace, replaced) + '.' + extensions)
                        )
                        print(f"Groovy! {file_checker} {to_replace}'s are now {replaced}'s...")
                    else:
                        print(f"Go back and read the manual. The files in {dir_select} don't contain {to_replace} in their names.")
                        break
            if bool_count == 0:
                print(f"Something's wrong with your incantation. {dir_select} doesn't have any valid files to rename.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    @main.command(
        name='upper',
        help='UPgrade those pathetic filenames with shiny new uppercase lettering.'
    )
    def uppercase(self):
        try:
            dir_select, files = self.start_script()
            for idx, file in enumerate(files):
                extensions = file.split('.')[-1]
                file_name = pathlib.Path(str(file)).stem
                verify_files = os.path.isfile(os.path.join(dir_select, file))
                bool_count = [verify_files].count(True)
                upper_checker = file_name.isupper()
                upper_count = [upper_checker].count(False)
                if (verify_files is False) and (upper_checker is True):
                    pass
                elif (verify_files is True) and (upper_checker is False):
                    os.rename(
                        os.path.join(dir_select, file_name + '.' + extensions),
                        os.path.join(dir_select, file_name.upper() + '.' + extensions)
                    )
                    print(f"UPgraded {idx} file(s)...")
            if bool_count == 0:
                print(f"Stop yanking my chain. {dir_select} doesn't contain any valid files to UPgrade.")
            elif upper_count == 0:
                print(f"The filenames in {dir_select} can't be upgraded anymore than they already are boss.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    @main.command(
        name='lower',
        help='Your filenames a little too loud? This will cut them down to size and make them all lowercase.'
    )
    def lowercase(self):
        try:
            dir_select, files = self.start_script()
            for idx, file in enumerate(files):
                extensions = file.split('.')[-1]
                file_name = pathlib.Path(str(file)).stem
                verify_files = os.path.isfile(os.path.join(dir_select, file))
                bool_count = [verify_files].count(True)
                lower_checker = file_name.islower()
                lower_count = [lower_checker].count(True)
                if (verify_files is False) and (lower_checker is True):
                    pass
                elif (verify_files is True) and (lower_checker is False):
                    os.rename(
                        os.path.join(dir_select, file_name + '.' + extensions),
                        os.path.join(dir_select, file_name.lower() + '.' + extensions)
                    )
                    print(f"Chopped {idx} filename(s) down to size...")
            if bool_count == 0:
                print(f"Stop yanking my chain. {dir_select} doesn't contain any valid files to downgrade.")
            elif lower_count == 0:
                print(f"The filenames in {dir_select} can't be downgraded anymore than they already are boss.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    @main.command(
        name='date',
        help='Time to tell those filenames what time it is. Add the date to the end of your filenames with a custom delimiter.'
    )
    def add_date(self):
        try:
            dir_select, files = self.start_script()
            date_splitter = input("What do you want between the filenames and today's date? (leave blank for none): ")
            for idx, file in enumerate(files):
                extensions = file.split('.')[-1]
                file_name = pathlib.Path(str(file)).stem
                date_string = time.strftime("%m%d%Y")
                verify_files = os.path.isfile(os.path.join(dir_select, file))
                bool_count = [verify_files].count(True)
                if verify_files is False:
                    pass
                elif verify_files is True:
                    os.rename(
                        os.path.join(dir_select, file_name + '.' + extensions),
                        os.path.join(dir_select, file_name + date_splitter + date_string + '.' + extensions)
                    )
                    print(f"Added {date_string} to {idx} file(s)...")
            if bool_count == 0:
                print(f"Yo, deadite, check again, {dir_select} doesn't contain any valid files to rename.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def run(self):
        if __name__ == "__main__":
            self.main()

renamex = Renamex()
renamex.run()

