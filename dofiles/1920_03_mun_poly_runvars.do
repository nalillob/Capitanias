cls
clear all
set more off
set type double

* Change to working directory:
cd "$capdata/dta/processed"

* Load data:
use "1920_munipoly_capbrdr_muniseat_matrix_full.dta", clear

* Assign treatment to municipality:
gen mun_treat = mun_seat_cap_treat
label var mun_treat "`: variable label mun_seat_cap_treat'"

* Determine if treatment changes at a given border:
gen bdr_line_treat_chng = left_cap_treat != right_cap_treat ///
	if left_cap_treat != . & right_cap_treat != .
label var bdr_line_treat_chng "Treatment status changes at this border yes/no"

* Calculate municipality's distance to nearest border where the treatment changes:
gen mun_dist_to_treat_chng = mun_poly_bdr_line_distm if bdr_line_treat_chng == 1
label var mun_dist_to_treat_chng "Distance from municipality polygon to border where treatment changes"
sort mun_poly_fid bdr_line_treat_chng mun_poly_bdr_line_rankn
by mun_poly_fid bdr_line_treat_chng: gen mun_min_dist_to_treat_chng = mun_dist_to_treat_chng[1]
label var mun_min_dist_to_treat_chng "Minimum distance from municipality polygon to border where treatment changes"

* Create treatment running variable:
gen mun_poly_runvarm = .
sort mun_poly_fid bdr_line_treat_chng mun_poly_bdr_line_rankn
by mun_poly_fid bdr_line_treat_chng: replace mun_poly_runvarm = mun_min_dist_to_treat_chng if mun_treat == 1
by mun_poly_fid bdr_line_treat_chng: replace mun_poly_runvarm = -mun_min_dist_to_treat_chng if mun_treat == 0
label var mun_poly_runvarm "Municipality polygon dist. to treatment (running variable, metres)"

* Calculate running variable in kilometers:
gen mun_poly_runvarkm = mun_poly_runvarm / 1000
label var mun_poly_runvarkm "Municipality polygon dist. to treatment (running variable, kilometres)"

* Per municipality, keep only the nearest border where treatment changes:
keep if mun_poly_bdr_line_distm == mun_dist_to_treat_chng  & mun_poly_bdr_line_distm == mun_min_dist_to_treat_chng & bdr_line_treat_chng == 1
duplicates drop mun_poly_fid, force

* Calculate absolute value of the running variable:
gen mun_poly_runvarm_abs = abs(mun_poly_runvarm)
label var mun_poly_runvarm_abs "Municipality polygon dist. to treatment (running variable, metres, absolute)"
gen mun_poly_runvarkm_abs = abs(mun_poly_runvarkm)
label var mun_poly_runvarkm_abs "Municipality polygon dist. to treatment (running variable, kilometres, absolute)"

* Final things:
gen mun_poly_uf = substr(mun_poly_codi, 1, 2)
label var mun_poly_uf "Municipality federal unit (unidade federal)"

* Select variables, compress, label, and save:
keep mun_poly_* mun_seat_* mun_treat
compress
label data "1920 municipality polygon running variables"
save "1920_mun_poly_runvars.dta", replace

* Export to csv (for mapping):
export delimited using "$mapsdir/1920_mun_poly_runvars.csv", replace
