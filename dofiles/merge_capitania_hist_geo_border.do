clear all
set more off

* Setup directories:
local working_dir "$capdata/dta/processed"

********************************************************************************
* CONSOLIDATED CAPITANIA DATA:
* Merge geographic and historical capitania data:
use "`working_dir'/1920_capitania_geodata.dta", clear
merge 1:1 cap_poly_name ///
	using "`working_dir'/capitanias_hist_data.dta", nogen

label data "Capitanias Consolidated Dataset"
notes drop _all
note: Sources: Cintra (2013), Augeron and Vidal (2007)
save "`working_dir'/1920_capitanias_consolidated.dta", replace

********************************************************************************
* CONSOLIDATED CAPITANIA BORDER DATA:
* Merge consolidated capitania data to capitania borders:
use "`working_dir'/1920_capitania_borders.dta", clear

* Merge in capitania info for polygons on left side of borders:
rename bdr_line_left_fid cap_poly_fid
merge m:1 cap_poly_fid using "`working_dir'/1920_capitanias_consolidated.dta", ///
	gen(mrg_capleft2capbrdrs) keep(1 3)
	
foreach var of varlist cap_* {
	rename `var' `=subinstr("`var'", "cap_", "left_cap_", 1)'
}

* Merge in capitania info for polygons on right side of borders:
rename bdr_line_right_fid cap_poly_fid
merge m:1 cap_poly_fid using "`working_dir'/1920_capitanias_consolidated.dta", ///
	gen(mrg_capright2capbrdrs) keep(1 3)
	
foreach var of varlist cap_* {
	rename `var' `=subinstr("`var'", "cap_", "right_cap_", 1)'
}

compress
label data "1920 Capitania borders (with capitania historical and geographic data)"
save "`working_dir'/1920_capitania_borders_full.dta", replace

********************************************************************************
* CONSOLIDATED MUNICIPALITY POLYGON-CAPITANIA BORDER MATRIX (LONG FORMAT):
* Load "lean" municipality-capitania border matrix:
use "`working_dir'/1920_munipoly2capbrdrs.dta", clear

* Merge in capitania border data (including capitania historical and geo. vars):
merge m:1 bdr_line_fid ///
	using "`working_dir'/1920_capitania_borders_full.dta", nogen

* Merge in municipality polygon data:
merge m:1 mun_poly_fid ///
	using "`working_dir'/1920_municipality_polygon.dta", nogen

* Compress, label, and save:
compress
label data "1920 Municipality-Capitania border matrix with full "
save "`working_dir'/1920_munipoly_capbrdr_matrix_full.dta", replace

********************************************************************************
* CONSOLIDATED PROVINCE/STATE CAPITAL DATA:
use "`working_dir'/1920_provseats_spj_cap_polys.dta", clear

merge m:1 cap_poly_name ///
	using "`working_dir'/1920_capitanias_consolidated.dta", ///
	gen(mrg_capsfull2provseats)
	
gen prv_seat_uf = substr(prv_seat_codi, 1, 2)
label var prv_seat_uf "Province/State capital federal unit (unidade federal)"
order prv_seat_uf, after(prv_seat_codi)

foreach var of varlist cap_* {
	rename `var' prv_seat_`var'
}

label data "1920 state capitals spatially joined to capitanias, with all capitania info"
save "`working_dir'/1920_provseats_with_capinfo.dta", replace

********************************************************************************

