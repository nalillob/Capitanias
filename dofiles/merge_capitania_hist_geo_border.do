clear all
set more off

********************************************************************************
* CONSOLIDATED CAPITANIA DATA:
* Merge geographic and historical capitania data:
use "$capdata/dta/processed/1920_capitania_geodata.dta", clear
merge 1:1 cap_poly_name_ascii_cintra ///
	using "$capdata/dta/processed/capitanias_hist_data.dta", nogen

label data "Capitanias Consolidated Dataset"
notes drop _all
note: Sources: Cintra (2013), Augeron and Vidal (2007)
save "$capdata/dta/processed/1920_capitanias_consolidated.dta", replace


********************************************************************************
* CONSOLIDATED CAPITANIA BORDER DATA:
* Merge consolidated capitania data to capitania borders:
use "$capdata/dta/processed/1920_capitania_borders.dta", clear

* Merge in capitania info for polygons on left side of borders:
rename capbrdr_left_poly_fid cap_poly_fid
merge m:1 cap_poly_fid using "$capdata/dta/processed/1920_capitanias_consolidated.dta", ///
	gen(mrg_capleft2capbrdrs) keep(1 3)
	
foreach var of varlist cap_* {
	rename `var' `=subinstr("`var'", "cap_", "left_cap_", 1)'
}

* Merge in capitania info for polygons on right side of borders:
rename capbrdr_right_poly_fid cap_poly_fid
merge m:1 cap_poly_fid using "$capdata/dta/processed/1920_capitanias_consolidated.dta", ///
	gen(mrg_capright2capbrdrs) keep(1 3)
	
foreach var of varlist cap_* {
	rename `var' `=subinstr("`var'", "cap_", "right_cap_", 1)'
}

compress
label data "1920 Capitania borders (with capitania historical and geographic data)"
save "$capdata/dta/processed/1920_capitania_borders_full.dta", replace

********************************************************************************
* CONSOLIDATED MUNICIPALITY POLYGON-CAPITANIA BORDER MATRIX (LONG FORMAT):
* Load "lean" municipality-capitania border matrix:
use "$capdata/dta/processed/1920_munipoly2capbrdrs.dta", clear

* Merge in capitania border data (including capitania historical and geo. vars):
merge m:1 capbrdr_fid ///
	using "$capdata/dta/processed/1920_capitania_borders_full.dta", nogen

* Merge in municipality polygon data:
merge m:1 muni_poly_fid ///
	using "$capdata/dta/processed/1920_municipality_polygon.dta", nogen

* Compress, label, and save:
compress
label data "1920 Municipality-Capitania border matrix with full "
save "$capdata/dta/processed/1920_munipoly_capbrdr_matrix_full.dta", replace
********************************************************************************
