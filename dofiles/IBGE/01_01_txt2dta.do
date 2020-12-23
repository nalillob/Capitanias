clear all
set more off

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

