# NewsStatisticsCompiler
 Python project to get statistical data from jl files

Project Information:

See directory "ProjectBackground" for initial project request and detailed output file information.
See directory "TestData" for examples of typical input and corresponding output.

Basic usage:

WordStatGenerator.py -newssource "[news source]" where news source is the prefix of one or more .jl files containing article information scanned from a given news site. Currently acceptable values are "ap", "reuters", and "npr".

Input:

Input is a file named with the following format: [news source][subject].jl, where news source is the name of a given news site, and subject is the subject of various articles on the news site.

The jl file should contain the following data:

At least one JSON dictionary having keys "title", "articleDate", and "articleBodyText". Additional keys are acceptable, but if any one of these three keys are missing, the script will fail

Setup:

WordStatGenerator.py, wordCountController.py, wordCountModel.py, and wordCountView.py should all be placed in the same folder, along with the jl files to be scanned.
