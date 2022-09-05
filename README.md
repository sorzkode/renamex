[[PyPI Package](https://pypi.org/project/renamex/)]
[[MIT Licence](https://en.wikipedia.org/wiki/MIT_License)]


![alt text](https://raw.githubusercontent.com/sorzkode/renamex/master/assets/reblogo.png)

# Renamomicon Ex-Bulkus

The script of the dead...AKA an Evil Dead themed bulk renaming utility.

![alt text](https://raw.githubusercontent.com/sorzkode/renamex/master/assets/help.png)

## Example

![alt text](https://raw.githubusercontent.com/sorzkode/renamex/master/assets/example.png)

## Installation

The script is packaged with PyPI and you can install using:
```
pip install renamex
```

Alternatively, you can download from Github, changedir (cd) to the script directory and run the following:
```
pip install -e .
```
*This will install the renamex package locally 

Installation isn't required to run the script but you will need to ensure the requirements below are met.

## Requirements

  [[Python 3](https://www.python.org/downloads/)]

  [[pyfiglet module](https://pypi.org/project/pyfiglet/)]

  [[click module](https://pypi.org/project/click/)]

## Usage

```
Usage: renamex.py [OPTIONS] COMMAND [ARGS]...

  Renamomicon Ex-Bulkus...The script of the dead. AKA an Evil Dead bulk file
  renaming utility :)

Options:
  --help  Show this message and exit.

Commands:
  date      Allows you to add today's date to end of filenames with specified delimiter before date.
  lower     Renames all filenames to lowercase.
  replacer  Allows you to replace any section of a filename with whatever you choose.
  upper     Renames all filenames to uppercase.
  xspaces   Removes spaces from all filenames.
```
If renamex is installed you can use the following command syntax:
```
python -m renamex --help

python -m renamex date
python -m renamex lower
python -m renamex replacer
python -m renamex upper
python -m renamex xspaces
```
Otherwise you can run the script directly by changing directory (cd) in a terminal of your choice to the renamex directory and using the following syntax:
```
python renamex.py --help

python renamex.py date
python renamex.py lower
python renamex.py replacer
python renamex.py upper
python renamex.py xspaces
```




