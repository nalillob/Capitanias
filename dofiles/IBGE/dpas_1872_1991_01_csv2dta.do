clear all
set more off

* Define source and destination directories:
local top_source_dir "$capdata/csv/IBGE"
local top_destin_dir "$capdata/dta/IBGE/from_csv"

* Make sure top destination directory exists, and if not, create it:
local capdata_split = subinstr("${capdata}", "/", " ", .)
local top_destin_split = subinstr("`top_destin_dir'", "/", " ", .)

cd "$capdata"
forval i = `=wordcount(`"`capdata_split'"') + 1'(1)`=wordcount(`"`top_destin_split'"')' {
	local next_dir : word `i' of `top_destin_split'
	capture cd "./`next_dir'"
	if _rc != 0 {
		mkdir "./`next_dir'"
		cd "./`next_dir'"
	}
}

local csv_year_dirs : dir "`top_source_dir'" dirs "????", respect

foreach csv_year_dir of local csv_year_dirs {
	* Make sure year destination directory exists:
	capture cd "`top_destin_dir'/`csv_year_dir'"
	if _rc != 0 {
		mkdir "`top_destin_dir'/`csv_year_dir'"
	}
	cd "`top_destin_dir'/`csv_year_dir'"
	
	* Get list of files from source:
	local files : dir "`top_source_dir'/`csv_year_dir'" files "*.csv", respect
	
	* Loop over files, importing them and saving them as .dta's:
	foreach file of local files {
		import delimited "`top_source_dir'/`csv_year_dir'/`file'", clear ///
			varnames(1) case(preserve) asdouble encoding(utf8) stringcols(_all)
			
		local filenoext = subinstr("`file'", ".csv", "", .)
		save "`filenoext'.dta", replace
	}
}
