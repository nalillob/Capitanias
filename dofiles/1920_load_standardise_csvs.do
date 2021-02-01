clear all
set more off

* Setup directories:
local source_dir "$capdata/dta/IBGE/from_csv/1920"
local destin_dir "$capdata/dta/processed"

********************************************************************************
* Load and standardise municipality polygon geographic data:
use "`source_dir'/T05_malha_municipal_1920.dta", clear
replace Shape = subinstr(Shape, "(", "", .)
replace Shape = subinstr(Shape, ")", "", .)
replace Shape = subinstr(Shape, ",", "", .)
gen Shape_X = word(Shape,1)
gen Shape_Y = word(Shape,2)
drop Shape

destring OBJECTID Shape_*, replace

rename OBJECTID muni_poly_fid
rename codigo muni_poly_codigo
rename nome muni_poly_nome
rename Shape_Length muni_poly_length_m
rename Shape_Area muni_poly_area_m2
rename Shape_X muni_poly_centroid_x
rename Shape_Y muni_poly_centroid_y

label var muni_poly_fid "Municipality polygon feature id"
label var muni_poly_codigo "Municipality polygon code (IBGE)"
label var muni_poly_nome "Municipality polygon name (IBGE)"
label var muni_poly_length_m "Municipality polygon perimeter length (metres)"
label var muni_poly_area_m2 "Municipality polygon area (metres-sqrd)"
label var muni_poly_centroid_x "Municipality polygon centroid x-coordinate (SIRGAS)"
label var muni_poly_centroid_y "Municipality polygon centroid y-coordinate (SIRGAS)"

label data "1920 political-administrative division (DAP), municipalities"
note: Source: IBGE
save "`destin_dir'/1920_municipality_polygon.dta", replace

********************************************************************************
* Load and standardise municipality seat geographic data:
use "`source_dir'/T03_sede_municipal_1920.dta", clear
replace Shape = subinstr(Shape, "(", "", .)
replace Shape = subinstr(Shape, ")", "", .)
replace Shape = subinstr(Shape, ",", "", .)
gen Shape_X = word(Shape,1)
gen Shape_Y = word(Shape,2)
drop Shape

destring OBJECTID Shape_*, replace

rename OBJECTID muni_seat_fid
rename codigo muni_seat_codigo
rename nome muni_seat_nome
rename Shape_X muni_seat_x
rename Shape_Y muni_seat_y

label var muni_seat_fid "Municipality seat feature id"
label var muni_seat_codigo "Municipality seat code (IBGE)"
label var muni_seat_nome "Municipality seat name (IBGE)"
label var muni_seat_x "Municipality seat x-coordinate (SIRGAS)"
label var muni_seat_y "Municipality seat y-coordinate (SIRGAS)"

label data "1920 municipality seats"
note: Source: IBGE
save "`destin_dir'/1920_municipality_seat.dta", replace

********************************************************************************
* Load and standardise capitania border geographic data:
use "`source_dir'/capitanias_GCS_WGS_1984_line.dta", clear
replace Shape = subinstr(Shape, "(", "", .)
replace Shape = subinstr(Shape, ")", "", .)
replace Shape = subinstr(Shape, ",", "", .)
gen Shape_X = word(Shape,1)
gen Shape_Y = word(Shape,2)
drop Shape

destring OBJECTID *_FID Shape_*, replace

rename OBJECTID capbrdr_fid
rename LEFT_FID capbrdr_left_poly_fid
rename RIGHT_FID capbrdr_right_poly_fid
rename Shape_Length capbrdr_length_degrees
rename Shape_X capbrdr_midpoint_x
rename Shape_Y capbrdr_midpoint_y

label var capbrdr_fid "Capitania border feature id"
label var capbrdr_left_poly_fid "Capitania border left polygon municipality fid"
label var capbrdr_right_poly_fid "Capitania border right polygon municipality fid"
label var capbrdr_length_degrees "Capitania border length (degrees)"
label var capbrdr_midpoint_x "Capitania border midpoint x-coordinate (SIRGAS)"
label var capbrdr_midpoint_y "Capitania border midpoint y-coordinate (SIRGAS)"

label data "1920 Capitania Borders"
save "`destin_dir'/1920_capitania_borders.dta", replace

********************************************************************************
* Load and standardise capitania polygon geographic data:
use "`source_dir'/capitanias_GCS_WGS_1984.dta", clear
	
replace Shape = subinstr(Shape, "(", "", .)
replace Shape = subinstr(Shape, ")", "", .)
replace Shape = subinstr(Shape, ",", "", .)
gen Shape_X = word(Shape,1)
gen Shape_Y = word(Shape,2)
drop Shape

destring OBJECTID Shape_*, replace

rename OBJECTID cap_poly_fid
rename Name_ascii cap_poly_name_ascii_cintra
rename Code cap_poly_code_cintra
rename Abbrev cap_poly_abbrev_cintra
rename Donatario cap_poly_donatario_cintra
rename Limite cap_poly_limite_cintra
rename Category cap_poly_category
rename Shape_Length cap_poly_length_m
rename Shape_Area cap_poly_area_m2
rename Shape_X cap_poly_centroid_x
rename Shape_Y cap_poly_centroid_y

label var cap_poly_fid "Capitania polygon feature id"
label var cap_poly_name_ascii_cintra "Capitania polygon name (Cintra, 2013)"
label var cap_poly_code_cintra "Capitania polygon code (Cintra, 2013)"
label var cap_poly_abbrev_cintra "Capitania polygon abbreviation (Cintra, 2013)"
label var cap_poly_donatario_cintra "Capitania polygon donatario name (Cintra, 2013)"
label var cap_poly_limite_cintra "Capitania polygon limit (Cintra, 2013)"
label var cap_poly_category "Capitania polygon category"
label var cap_poly_length_m "Capitania polygon perimeter length (metres)"
label var cap_poly_area_m2 "Capitania polygon area (metres-sqrd)"
label var cap_poly_centroid_x "Capitania polygon centroid x-coordinate"
label var cap_poly_centroid_y "Capitania polygon centroid y-coordinate"

label data "1920 Capitania Geographic Data"
note: Source: Cintra (2013)
save "`destin_dir'/1920_capitania_geodata.dta", replace

********************************************************************************
* Load and standardise Capitania historical data:
import excel "$capdata\raw\capitanias_hist_data.xlsx", ///
	sheet("Sheet1") firstrow case(preserve) allstring clear

rename NAME_ASCII cap_poly_name_ascii_cintra
rename CODE cap_poly_code_cintra
rename ABBREV cap_poly_abbrev_cintra
rename DONATARIO cap_poly_donatario_cintra
rename LIMITE cap_poly_limite_cintra
rename CATEGORY cap_poly_category

rename YearDonatarioDeath cap_don_death_year
rename CircumstancesDonatarioDeath cap_don_death_type
rename CartadeDoacao cap_don_letter_date
rename Foral cap_foral_date
rename OutrosDocumentos cap_otherdocs_date
rename DateofGrantAV cap_grant_date
rename YearTransfer cap_trnsfr_year
rename YearCrown cap_crown_year
rename YearSettlement cap_settle_year
rename Populationc1536Portuguese cap_pop1536_prtgs
rename Populationc1546Portuguese cap_pop1546_prtgs
rename Populationc1546AfricansAV cap_pop1546_afrcns
rename Povoados15301549AV cap_povs_1530_1549
rename Vilas15301549AV cap_vilas_1530_1549

destring, replace

* Create a variable that measures the time that a capitania was autonomous:
gen double cap_time_auto = cap_crown_year - cap_settle_year
compress cap_time_auto
format %ty cap_time_auto
label var cap_time_auto "Time Capitania was autonomous"

* Define a treatment based on whether time autonomous is greater than median:
sum cap_time_auto, d
local cap_time_auto_p50 = r(p50)
gen cap_treat = cap_time_auto >= `cap_time_auto_p50'  if cap_time_auto!=.
label var cap_treat "Treated if time autonomous >= median (`cap_time_auto_p50')"

* Define a placebo treatment based on extending capitania borders west of the 
* Tordesillas line: (PENDING: automate it)

* Compress and save:
compress
label data "Capitania Historical Data"
note: Sources: Cintra (2013), Augeron and Vidal (2007)
save "`destin_dir'/capitanias_hist_data.dta", replace

********************************************************************************
* Load and standardise distances between municipality and capitania borders:
use "`source_dir'/ntable_muni_brdr_to_cap_brdr_1920.dta", clear
	
drop OBJECTID

rename IN_FID muni_poly_fid
rename NEAR_FID capbrdr_fid
rename NEAR_DIST muni_poly_capbrdr_dist_m
rename NEAR_RANK muni_poly_capbrdr_rank
rename FROM_X muni_poly_capbrdr_fromx
rename FROM_Y muni_poly_capbrdr_fromy
rename NEAR_X muni_poly_capbrdr_nearx
rename NEAR_Y muni_poly_capbrdr_neary
rename NEAR_ANGLE muni_poly_capbrdr_angle

label var muni_poly_fid "Municipality polygon feature id"
label var capbrdr_fid "Capitania border feature id"
label var muni_poly_capbrdr_dist_m "Distance from municipality polygon to capitania border (metres)"
label var muni_poly_capbrdr_rank "Distance from municipality polygon to capitania border (rank)"
label var muni_poly_capbrdr_fromx "X-coord. origin distance municipality polygon to capitania border"
label var muni_poly_capbrdr_fromy "Y-coord. origin distance municipality polygon to capitania border"
label var muni_poly_capbrdr_nearx "X-coord. destination distance municipality polygon to capitania border"
label var muni_poly_capbrdr_neary "Y-coord. destination distance municipality polygon to capitania border"
label var muni_poly_capbrdr_angle "Distance from municipality polygon to capitania border (angle)"

label data "1920 Distance from each municipality polygon to each capitania border"
notes drop _all
save "`destin_dir'/1920_munipoly2capbrdrs.dta", replace

********************************************************************************
* Load and standardise distances between municipality seat and capitania borders:
use "`source_dir'/ntable_muni_seat_to_cap_brdr_1920.dta", clear
	
drop OBJECTID

rename IN_FID muni_seat_fid
rename NEAR_FID capbrdr_fid
rename NEAR_DIST muni_seat_capbrdr_dist_m
rename NEAR_RANK muni_seat_capbrdr_rank
rename FROM_X muni_seat_capbrdr_fromx
rename FROM_Y muni_seat_capbrdr_fromy
rename NEAR_X muni_seat_capbrdr_nearx
rename NEAR_Y muni_seat_capbrdr_neary
rename NEAR_ANGLE muni_seat_capbrdr_angle

label var muni_seat_fid "Municipality seat feature id"
label var capbrdr_fid "Capitania border feature id"
label var muni_seat_capbrdr_dist_m "Distance from municipality seat to capitania border (metres)"
label var muni_seat_capbrdr_rank "Distance from municipality seat to capitania border (rank)"
label var muni_seat_capbrdr_fromx "X-coord. origin distance municipality seat to capitania border"
label var muni_seat_capbrdr_fromy "Y-coord. origin distance municipality seat to capitania border"
label var muni_seat_capbrdr_nearx "X-coord. destination distance municipality seat to capitania border"
label var muni_seat_capbrdr_neary "Y-coord. destination distance municipality seat to capitania border"
label var muni_seat_capbrdr_angle "Distance from municipality seat to capitania border (angle)"

label data "1920 Distance from each municipality seat to each capitania border"
notes drop _all
save "`destin_dir'/1920_muniseat2capbrdrs.dta", replace
********************************************************************************
