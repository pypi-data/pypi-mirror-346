 <img src="https://www.salabim.org/xlwings_utils_logo2.png">  

## Introduction

This module provides some useful functions to be used in xlwings lite.

## Installation

Just add xlwings-utils to the *requirement.txt* tab. It might be required to add ssl.

In the script, add

```ìmport xlwings_utils as xwu```

## Dropbox support

The xlwings lite system does not provide access to the local file system. With this module, files can be copied between Dropbox and the local pyodide file system, making it possible to indirectly use the local file system.

It is only possible, as of now, to use full-access Dropbox apps.

The easiest way to use the Dropbox functionality is to add the credentials to the environment variables. Add REFRESH_TOKEN, APP_KEY and APP_SECRET with their corresponding values to the environment variables.

Then, it is possible to list all files in a specified folder with the function `list_dropbox`.
It is also possible to get the folders and to access all underlying folders.

The function `read_dropbox` can be used to read a Dropbox file's contents (bytes).

The function `write_dropbox` can be used to write contents (bytes) to a Dropbox file.

The functions `list_local`, `read_local` and `write_local` offer similar functionality for the local file system (on pyodide).

So, a way to access a file on the system's drive (mapped to Dropbox) as a local file is:

```
contents = xlwings_utils.read_dropbox('/downloads/file1.xls')
xlwings_utils.write_local('file1.xlsx')
df = pandas.read_excel"file1.xlsx")
...
```
And the other direction:
```
contents = xlwings_utils.read_local('file1.gif')
xlwings_utils.write_dropbox('/downloads/file1.gif')
```

## Block support

The module contains a useful 2-dimensional data structure: *block*.
This can be useful to manipulate a range without accessing the range directly, which is expensive in terms of memory and execution time.
The advantage over an ordinary list of lists is that a block is index one-based, in line with range and addressing is done with a row, column tuple.
So, `my_block(lol)[row, col]` is roughly equivalent to `lol[row-1][col-1]`

A block stores the values internally as a dictionary and will only convert these to a list of lists when using `block.value`. 

Converting the value of a range (usually a list of lists, but can also be a list or scalar) to a block can be done with

```
my_block = xwu.block.from_value(range.value)
```
The dimensions (number of rows and number of columns) are automatically set.

Setting of an individual item (one-based, like range) can be done like
```
my_block[row, column] = x
```
And, likewise, reading an individual item can be done like
```
x = my_block[row, column]
```
It is not allowed t,o read or write outside the block dimensions.

It is also possible to define an empty block, like
```
block = xlwings_utils.block(number_of_rows, number_columns)
```
The dimensions can be queried or redefined with `block.number_of_rows` and 
`block.number_of_columns`.

To assign a block to range, use
```
range.value = block.value
```

The property `block.highest`_used_row_number returns the

The method `block.minimized()` returns a block that has the dimensions of (highest_used_row_number, highest_used_column_number). 

## Capture stdout support

The module has support for capturing stdout and -later- using showing the captured output on a sheet.

To do that:

```makes it possible to capture stdout writes, which
with xwu.capture_stdout():
    ...
```
and then the captured output can be copied to the screen, like

```can then be copied to a worksheet in a later stage.
sheet.range(4,5).value = xwu.captured_stdout_as_value()
```

Clearing the captured stdout buffer can be done with `xwu.clear_captured_std_out`.

Normally, stdout will be also sent to the xlwings lite UI panel. This can be suppressed with

```
with xwu.capture_stdout(include_print=False):
    ...
```

## Badges

![PyPI](https://img.shields.io/pypi/v/xlwings-utils) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/xlwings-utils) ![PyPI - Implementation](https://img.shields.io/pypi/implementation/xlwings-utils)
![PyPI - License](https://img.shields.io/pypi/l/xlwings-utils) ![ruff](https://img.shields.io/badge/style-ruff-41B5BE?style=flat) 
![GitHub last commit](https://img.shields.io/github/last-commit/salabim/peek)

