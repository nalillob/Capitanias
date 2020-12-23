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
net install datazoom_censo.pkg

* Get list of subdirectories:
local dirlist : dir "`source_dir'" dirs "??", respect

* Loop through dirs, converting txt files to dtas:
foreach subdir of local dirlist {
	cd "`source_dir'"
	display "`subdir'"
	
	datazoom_censo, years(2000) ufs("`subdir'") original("`source_dir'/`subdir'") ///
		saving("`destin_dir'") pes
		
	datazoom_censo, years(2000) ufs("`subdir'") original("`source_dir'/`subdir'") ///
		saving("`destin_dir'") fam
		
	datazoom_censo, years(2000) ufs("`subdir'") original("`source_dir'/`subdir'") ///
		saving("`destin_dir'") dom
	
	datazoom_censo, years(2000) ufs("`subdir'") original("`source_dir'/`subdir'") ///
		saving("`destin_dir'") all
		
	datazoom_censo, years(2000) ufs("`subdir'") original("`source_dir'/`subdir'") ///
		saving("`destin_dir'") both
	
	datazoom_censo, years(2000) ufs("`subdir'") original("`source_dir'/`subdir'") ///
		saving("`destin_dir'") comp pes
		
	datazoom_censo, years(2000) ufs("`subdir'") original("`source_dir'/`subdir'") ///
		saving("`destin_dir'") comp dom
		
	datazoom_censo, years(2000) ufs("`subdir'") original("`source_dir'/`subdir'") ///
		saving("`destin_dir'") comp both
}
