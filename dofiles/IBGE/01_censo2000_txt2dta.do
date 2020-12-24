/*
DESCRIPTION:
This do-file uses the datazoom_censo program by PUC-Rio to process the 2000
census files.

EXECUTION TIME: ~1h30
*/


clear all
set more off

* Define source and destination directories:
local source_dir "$capdata/raw/IBGE/Censo_2000"
local destin_dir "$capdata/dta/IBGE/Censo_2000"

* Make sure destination directory exists, and if not, create it:
local capdata_split = subinstr("${capdata}", "/", " ", .)
local destin_split = subinstr("`destin_dir'", "/", " ", .)

cd "$capdata"
forval i = `=wordcount(`"`capdata_split'"') + 1'(1)`=wordcount(`"`destin_split'"')' {
	local next_dir : word `i' of `destin_split'
	capture cd "./`next_dir'"
	if _rc != 0 {
		mkdir "./`next_dir'"
		cd "./`next_dir'"
	}
}

cd "`source_dir'"

* Make sure datazoom is installed and updated:
net from "http://www.econ.puc-rio.br/datazoom/english"
net install datazoom_censo.pkg

* Get list of states from list of 2-letter zip files:
local ziplist : dir "`source_dir'" files "??.zip", respect
macro drop _sslist
foreach zipfile of local ziplist {
	local ss = subinstr("`zipfile'", ".zip", "", .)
	local sslist `sslist' `ss'
}

/// Convert txt files to dtas ///
* Individual variables only:
datazoom_censo, years(2000) ufs(`sslist') original("`source_dir'") saving("`destin_dir'") pes

* Family variables only (2000 census only):
datazoom_censo, years(2000) ufs(`sslist') original("`source_dir'") saving("`destin_dir'") fam

* Household variables only:
datazoom_censo, years(2000) ufs(`sslist') original("`source_dir'") saving("`destin_dir'") dom

* All variable types merged (household, family, and individual) (only available for 2000):
datazoom_censo, years(2000) ufs(`sslist') original("`source_dir'") saving("`destin_dir'") all

* Household and individual merged:
datazoom_censo, years(2000) ufs(`sslist') original("`source_dir'") saving("`destin_dir'") both

* Individual (compatible across waves):
datazoom_censo, years(2000) ufs(`sslist') original("`source_dir'") saving("`destin_dir'") comp pes

* Household (compatible across waves):
datazoom_censo, years(2000) ufs(`sslist') original("`source_dir'") saving("`destin_dir'") comp dom

* Household and individual merged (compatible across waves):
datazoom_censo, years(2000) ufs(`sslist') original("`source_dir'") saving("`destin_dir'") comp both
