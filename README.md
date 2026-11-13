# metrics-starter-collector

## What this tool is

metrics-starter-collector is an offline command line collector. It reads one build record tree once and prints the 17 metric starter set rows in the settled report form.

The tool works offline. It uses only the Python standard library. It reads the tree you name, prints a report, and does not change the tree it reads.

Each of the 17 rows is shown as present, present but not derivable, or missing, with its figure or its reason and a pointer to the record it rests on. The report also carries a header, a coverage statement, a piece inventory, and a data quality section. The report carries no score and no grade.

## How to install

You need Python 3.12.

From the root of this repo, run:

    python3 -m pip install .

That command installs the package and creates a console script named:

    metrics-starter-collector

You can then run the tool by that name from any folder.

## How to run

The command grammar is:

    metrics-starter-collector ROOT [--report PATH]

In words:

* The first part is the command name, metrics-starter-collector.
* ROOT is one argument, the path of the build record tree to read.
* The optional part is --report followed by its file path. With no --report part, the report is printed to standard output. With --report PATH, the report is written to the file named by PATH.
* A report destination inside the tree being read is refused as a usage error and nothing is written.

Exit numbers:

* 0 means a completed report.
* 2 means a usage error, such as no root argument, an extra argument, an unknown option, a repeated --report part, a --report part with no file path after it, or a report destination inside the tree being read.
* 1 means unreadable input, such as a root that does not stand or cannot be read.

Examples:

Print the report for a tree to standard output:

    metrics-starter-collector path/to/design

Write the report for a tree to a file outside that tree:

    metrics-starter-collector path/to/design --report path/to/report.txt

## How to run the tests

From the root of this repo, run the single test command:

    python3 -m unittest discover -s tests -v

## Potential problem causers

This section lists known potential issues for someone installing or running this tool later, in plain language.

* Python version matters. The tool is built and tested on Python 3.12. A result from another Python version may differ and should not be treated as the tested result.
* The tool is offline and reads local files only. If a record tree is on a drive or folder the tool cannot read, the run will fail or the affected pieces will be reported as not read in full.
* The tool reads the tree once and in one pass. Very large trees can hit the built in limits. Pieces over a limit, malformed pieces, and pieces that are not valid UTF-8 text are listed in the data quality section and are not used as if they had been read in full.
* Links need care. A link whose target sits outside the tree being read is not followed. A link target inside the tree is followed at most once.
* A sparse tree may have too few usable records to support a report. In that case the tool prints a short no usable records report and still exits 0.
* Record forms matter. Rows depend on records standing in the forms the tool knows. A record in a near match form, with a slightly different name or shape, is listed as a near match and is not counted as found. Changing a record form can change a row from present to present but not derivable or missing.
* Unknown definitions versions are refused. If a record tree states a definitions version the tool does not know, the affected rows are shown as present but not derivable with that reason named, rather than being derived under the wrong rules.
* A report file needs a writable home outside the tree. If the folder named for the report file does not stand, or the file cannot be written, the run reports a usage error, writes no partial file, and does not fall back to standard output.
* Figures rest on the records in the one tree named. The tool does not join records across two trees or across separate locations. If part of a build record stands elsewhere, that part is not read and the affected rows will show it as missing.
* In short, the collector was proven on one real record tree and that other trees rest on the synthetic fixtures. A new tree with record forms unlike either may produce more missing or not derivable rows until its forms are understood.

## Licence

This project is licensed under the Apache License 2.0. See the LICENSE file for the full text.
