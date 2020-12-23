cls
clear all
set more off
set min_memory 0 // reset min memory to default

macro drop _all
program drop _all

* DIRECTORIES DECEMBER 2020
* User directories:
global dbxdir "C:/Users/nicol/Dropbox"
global research "$dbxdir/Research Projects"
global datadir "$dbxdir/Data"

* Define project directories:
global maindir 	"$research/Capitanias"
global capdata 	"$maindir/data"
global dodir 	"$maindir/dofiles"
global results	"$maindir/results"

* MACRO FOR THIS DO-FILE
global macrodo "$dodir/MACROS_2020_12.do"

* Drop local macros:
macro drop _*

* Show list of global macros:
cls
macro dir

* Change directory to main project directory:
cd "$maindir"
