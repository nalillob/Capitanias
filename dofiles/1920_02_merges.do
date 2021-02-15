clear all
set more off

* Change to working directory:
cd "$capdata/dta/processed"

********************************************************************************
* CONSOLIDATED CAPITANIA DATA:
* Merge geographic and historical capitania data:
use "1920_capitania_geodata.dta", clear
merge 1:1 cap_poly_name ///
	using "capitanias_hist_data.dta", nogen

label data "Capitanias Consolidated Dataset"
notes drop _all
note: Sources: Cintra (2013), Augeron and Vidal (2007)
save "1920_capitanias_consolidated.dta", replace

********************************************************************************
* CONSOLIDATED CAPITANIA BORDER DATA:
* Merge consolidated capitania data to capitania borders:
use "1920_capitania_borders.dta", clear

* Merge in capitania info for polygons on left side of borders:
rename bdr_line_left_fid cap_poly_fid
merge m:1 cap_poly_fid using "1920_capitanias_consolidated.dta", ///
	gen(mrg_capleft2capbrdrs) keep(1 3)
	
foreach var of varlist cap_* {
	rename `var' `=subinstr("`var'", "cap_", "left_cap_", 1)'
}

* Merge in capitania info for polygons on right side of borders:
rename bdr_line_right_fid cap_poly_fid
merge m:1 cap_poly_fid using "1920_capitanias_consolidated.dta", ///
	gen(mrg_capright2capbrdrs) keep(1 3)
	
foreach var of varlist cap_* {
	rename `var' `=subinstr("`var'", "cap_", "right_cap_", 1)'
}

compress
label data "1920 Capitania borders (with capitania historical and geographic data)"
save "1920_capitania_borders_full.dta", replace

********************************************************************************
* CONSOLIDATED PROVINCE/STATE CAPITAL DATA:
* Load province/state capital data spatially joined with capitanias:
use "1920_provseats_spj_cap_polys.dta", clear

* Merge in consolidated capitania variables:
merge m:1 cap_poly_name using "1920_capitanias_consolidated.dta", ///
	gen(mrg_capsfull2provseats)
	
* Create unidade federal variable:
gen prv_seat_uf = substr(prv_seat_codi, 1, 2)
label var prv_seat_uf "Province/State capital federal unit (unidade federal)"
order prv_seat_uf, after(prv_seat_codi)

* Assign corresponding prefix to capitania variables:
foreach var of varlist cap_* {
	rename `var' prv_seat_`var'
}

* Compress, label, and save:
compress
label data "1920 state capitals spatially joined to capitanias, with all capitania info"
save "1920_provseats_with_capinfo.dta", replace

********************************************************************************
* CONSOLIDATED MUNICIPALITY SEAT DATA:
* Load municipality seat data spatially joined with capitanias:
use "1920_muniseats_spj_cap_polys.dta", clear

* Merge in historical capitania variables:
merge m:1 cap_poly_name using "1920_capitanias_consolidated.dta", nogen

* Assign corresponding prefix to capitania variables:
foreach var of varlist cap_* {
	rename `var' mun_seat_`var'
}

* Compress, label, and save:
compress
label data "1920 municipality seats spatially joined to capitanias, with all capitania info"
save "1920_muniseats_with_capinfo.dta", replace

********************************************************************************
* CONSOLIDATED MUNICIPALITY POLYGON-CAPITANIA BORDER MATRIX (LONG FORMAT):
* Load "lean" municipality-capitania border matrix:
use "1920_munipoly2capbrdrs.dta", clear

* Merge in capitania border data (including capitania historical and geo. vars):
merge m:1 bdr_line_fid using "1920_capitania_borders_full.dta", nogen

* Merge in municipality polygon data:
merge m:1 mun_poly_fid using "1920_municipality_polygon.dta", nogen

* Merge in municipality seat data:
gen mun_seat_codi = mun_poly_codi
label var mun_seat_codi "Municipality seat code (IBGE)"
merge m:1 mun_seat_codi using "1920_muniseats_with_capinfo.dta", nogen keep(1 3)

* Compress, label, and save:
compress
label data "1920 Municipality-Capitania border matrix with full info"
save "1920_munipoly_capbrdr_muniseat_matrix_full.dta", replace

********************************************************************************
