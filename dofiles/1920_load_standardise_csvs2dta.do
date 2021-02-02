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
gen Shape_X = word(Shape, 1)
gen Shape_Y = word(Shape, 2)
drop Shape

destring OBJECTID Shape_*, replace

rename OBJECTID 	mun_poly_fid
rename codigo 		mun_poly_codi
rename nome 		mun_poly_nome
rename Shape_Length mun_poly_lenm
rename Shape_Area 	mun_poly_arm2
rename Shape_X 		mun_poly_cenx
rename Shape_Y 		mun_poly_ceny

label var mun_poly_fid 	"Municipality polygon feature id"
label var mun_poly_codi "Municipality polygon code (IBGE)"
label var mun_poly_nome "Municipality polygon name (IBGE)"
label var mun_poly_lenm "Municipality polygon perimeter length (metres)"
label var mun_poly_arm2 "Municipality polygon area (metres-sqrd)"
label var mun_poly_cenx "Municipality polygon centroid x-coordinate (SIRGAS)"
label var mun_poly_ceny "Municipality polygon centroid y-coordinate (SIRGAS)"

label data "1920 political-administrative division (DAP), municipalities"
note: Source: IBGE
save "`destin_dir'/1920_municipality_polygon.dta", replace

********************************************************************************
* Load and standardise municipality seat geographic data:
use "`source_dir'/T03_sede_municipal_1920.dta", clear
replace Shape = subinstr(Shape, "(", "", .)
replace Shape = subinstr(Shape, ")", "", .)
replace Shape = subinstr(Shape, ",", "", .)
gen Shape_X = word(Shape, 1)
gen Shape_Y = word(Shape, 2)
drop Shape

destring OBJECTID Shape_*, replace

rename OBJECTID mun_seat_fid
rename codigo 	mun_seat_codi
rename nome 	mun_seat_nome
rename Shape_X 	mun_seat_pntx
rename Shape_Y 	mun_seat_pnty

label var mun_seat_fid 	"Municipality seat feature id"
label var mun_seat_codi "Municipality seat code (IBGE)"
label var mun_seat_nome "Municipality seat name (IBGE)"
label var mun_seat_pntx "Municipality seat x-coordinate (SIRGAS)"
label var mun_seat_pnty "Municipality seat y-coordinate (SIRGAS)"

label data "1920 municipality seats"
note: Source: IBGE
save "`destin_dir'/1920_municipality_seat.dta", replace

********************************************************************************
* Load and standardise capitania border geographic data:
use "`source_dir'/capitanias_GCS_WGS_1984_line.dta", clear
replace Shape = subinstr(Shape, "(", "", .)
replace Shape = subinstr(Shape, ")", "", .)
replace Shape = subinstr(Shape, ",", "", .)
gen Shape_X = word(Shape, 1)
gen Shape_Y = word(Shape, 2)
drop Shape

destring OBJECTID *_FID Shape_*, replace

rename OBJECTID 	bdr_line_fid
rename LEFT_FID 	bdr_line_left_fid
rename RIGHT_FID 	bdr_line_right_fid
rename Shape_Length bdr_line_lend
rename Shape_X 		bdr_line_linx
rename Shape_Y 		bdr_line_liny

label var bdr_line_fid 			"Capitania border feature id"
label var bdr_line_left_fid 	"Capitania border left polygon municipality fid"
label var bdr_line_right_fid 	"Capitania border right polygon municipality fid"
label var bdr_line_lend 		"Capitania border length (degrees)"
label var bdr_line_linx 		"Capitania border midpoint x-coordinate (SIRGAS)"
label var bdr_line_liny 		"Capitania border midpoint y-coordinate (SIRGAS)"

label data "1920 Capitania Borders"
save "`destin_dir'/1920_capitania_borders.dta", replace

********************************************************************************
* Load and standardise capitania polygon geographic data:
use "`source_dir'/capitanias_GCS_WGS_1984.dta", clear
	
replace Shape = subinstr(Shape, "(", "", .)
replace Shape = subinstr(Shape, ")", "", .)
replace Shape = subinstr(Shape, ",", "", .)
gen Shape_X = word(Shape, 1)
gen Shape_Y = word(Shape, 2)
drop Shape

destring OBJECTID Shape_*, replace

rename OBJECTID 	cap_poly_fid
rename Name_ascii 	cap_poly_name
rename Code 		cap_poly_code
rename Abbrev 		cap_poly_abbr
rename Donatario	cap_poly_dnam
rename Limite 		cap_poly_limt
rename Category 	cap_poly_type
rename Shape_Length cap_poly_lenm
rename Shape_Area 	cap_poly_arm2
rename Shape_X 		cap_poly_cenx
rename Shape_Y 		cap_poly_ceny

label var cap_poly_fid 	"Capitania polygon feature id"
label var cap_poly_name "Capitania name according to Cintra (2013)"
label var cap_poly_code "Capitania code according to Cintra (2013)"
label var cap_poly_abbr "Capitania abbreviation according to Cintra (2013)"
label var cap_poly_dnam "Capitania donatario's name according to Cintra (2013)"
label var cap_poly_limt "Capitania limit according to Cintra (2013)"
label var cap_poly_type "Capitania polygon category"
label var cap_poly_lenm "Capitania polygon perimeter length (metres)"
label var cap_poly_arm2 "Capitania polygon area (metres-sqrd)"
label var cap_poly_cenx "Capitania polygon centroid x-coordinate"
label var cap_poly_ceny "Capitania polygon centroid y-coordinate"

label data "1920 Capitania Geographic Data"
note: Source: Cintra (2013)
save "`destin_dir'/1920_capitania_geodata.dta", replace

********************************************************************************
* Load and standardise Capitania historical data:
import excel "$capdata\raw\capitanias_hist_data.xlsx", ///
	sheet("Sheet1") firstrow case(preserve) allstring clear

rename NAME_ASCII cap_poly_name
rename CODE cap_poly_code
rename ABBREV cap_poly_abbr
rename DONATARIO cap_poly_dnam
rename LIMITE cap_poly_limt
rename CATEGORY cap_poly_type

rename YearDonatarioDeath 			cap_don_death_year
rename CircumstancesDonatarioDeath 	cap_don_death_type
rename CartadeDoacao 				cap_don_letter_date
rename Foral 						cap_foral_date
rename OutrosDocumentos 			cap_otherdocs_date
rename DateofGrantAV 				cap_grant_date
rename YearTransfer 				cap_trnsfr_year
rename YearCrown 					cap_crown_year
rename YearSettlement 				cap_settle_year
rename Populationc1536Portuguese 	cap_pop1536_prtgs
rename Populationc1546Portuguese 	cap_pop1546_prtgs
rename Populationc1546AfricansAV 	cap_pop1546_afrcns
rename Povoados15301549AV 			cap_povs_1530_1549
rename Vilas15301549AV 				cap_vilas_1530_1549

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
destring, replace	
drop OBJECTID

rename IN_FID 		mun_poly_fid
rename NEAR_FID 	bdr_line_fid
rename NEAR_DIST 	mun_poly_bdr_line_distm
rename NEAR_RANK 	mun_poly_bdr_line_rankn
rename FROM_X 		mun_poly_bdr_line_fromx
rename FROM_Y 		mun_poly_bdr_line_fromy
rename NEAR_X 		mun_poly_bdr_line_nearx
rename NEAR_Y 		mun_poly_bdr_line_neary
rename NEAR_ANGLE 	mun_poly_bdr_line_angle

label var mun_poly_fid 				"Municipality polygon feature id"
label var bdr_line_fid 				"Capitania border feature id"
label var mun_poly_bdr_line_distm 	"Distance from municipality polygon to capitania border (metres)"
label var mun_poly_bdr_line_rankn 	"Distance from municipality polygon to capitania border (rank)"
label var mun_poly_bdr_line_fromx 	"X-coord. origin distance municipality polygon to capitania border"
label var mun_poly_bdr_line_fromy 	"Y-coord. origin distance municipality polygon to capitania border"
label var mun_poly_bdr_line_nearx 	"X-coord. destination distance municipality polygon to capitania border"
label var mun_poly_bdr_line_neary 	"Y-coord. destination distance municipality polygon to capitania border"
label var mun_poly_bdr_line_angle 	"Distance from municipality polygon to capitania border (angle)"

label data "1920 Distance from each municipality polygon to each capitania border"
notes drop _all
save "`destin_dir'/1920_munipoly2capbrdrs.dta", replace

********************************************************************************
* Load and standardise distances between municipality seat and capitania borders:
use "`source_dir'/ntable_muni_seat_to_cap_brdr_1920.dta", clear
	
drop OBJECTID

rename IN_FID 		mun_seat_fid
rename NEAR_FID 	bdr_line_fid
rename NEAR_DIST 	mun_seat_bdr_line_distm
rename NEAR_RANK 	mun_seat_bdr_line_rankn
rename FROM_X 		mun_seat_bdr_line_fromx
rename FROM_Y 		mun_seat_bdr_line_fromy
rename NEAR_X 		mun_seat_bdr_line_nearx
rename NEAR_Y 		mun_seat_bdr_line_neary
rename NEAR_ANGLE 	mun_seat_bdr_line_angle

label var mun_seat_fid 				"Municipality seat feature id"
label var bdr_line_fid 				"Capitania border feature id"
label var mun_seat_bdr_line_distm 	"Distance from municipality seat to capitania border (metres)"
label var mun_seat_bdr_line_rankn 	"Distance from municipality seat to capitania border (rank)"
label var mun_seat_bdr_line_fromx 	"X-coord. origin distance municipality seat to capitania border"
label var mun_seat_bdr_line_fromy 	"Y-coord. origin distance municipality seat to capitania border"
label var mun_seat_bdr_line_nearx 	"X-coord. destination distance municipality seat to capitania border"
label var mun_seat_bdr_line_neary 	"Y-coord. destination distance municipality seat to capitania border"
label var mun_seat_bdr_line_angle 	"Distance from municipality seat to capitania border (angle)"

label data "1920 Distance from each municipality seat to each capitania border"
notes drop _all
save "`destin_dir'/1920_muniseat2capbrdrs.dta", replace

********************************************************************************
* Load and standardise municipality seat spatially joined with capitania polygons:
use "`source_dir'/T02_capital_estadual_1920_spj_caps_poly.dta", clear

replace Shape = subinstr(Shape, "(", "", .)
replace Shape = subinstr(Shape, ")", "", .)
replace Shape = subinstr(Shape, ",", "", .)
gen Shape_X = word(Shape, 1)
gen Shape_Y = word(Shape, 2)
drop Shape

destring OBJECTID Join_Count *_FID Shape_*, replace
drop Join_Count TARGET_FID

rename OBJECTID 	prv_seat_fid
rename NOME 		prv_seat_nome
rename codigo 		prv_seat_codi
rename Shape_X 		prv_seat_pntx
rename Shape_Y 		prv_seat_pnty
rename Name_ascii 	cap_poly_name
rename Code 		cap_poly_code
rename Abbrev 		cap_poly_abbr
rename Donatario 	cap_poly_dnam
rename Limite 		cap_poly_limt
rename Category 	cap_poly_type

label var prv_seat_fid 	"Province/State capital feature id"
label var prv_seat_codi "Province/State capital code (IBGE)"
label var prv_seat_nome "Province/State capital name (IBGE)"
label var prv_seat_pntx "Province/State capital x-coordinate (SIRGAS)"
label var prv_seat_pnty "Province/State capital y-coordinate (SIRGAS)"
label var cap_poly_name "Capitania name according to Cintra (2013)"
label var cap_poly_code "Capitania code according to Cintra (2013)"
label var cap_poly_abbr "Capitania abbreviation according to Cintra (2013)"
label var cap_poly_dnam "Capitania donatario's name according to Cintra (2013)"
label var cap_poly_limt "Capitania limit according to Cintra (2013)"
label var cap_poly_type "Capitania polygon category"

label data "1920 state capitals spatially joined to capitanias"
save "`destin_dir'/1920_provseats_spj_cap_polys.dta", replace

********************************************************************************
* Load and standardise municipality seat spatially joined with capitania polygons:
use "`source_dir'/T03_sede_municipal_1920_spj_caps_poly.dta", clear

replace Shape = subinstr(Shape, "(", "", .)
replace Shape = subinstr(Shape, ")", "", .)
replace Shape = subinstr(Shape, ",", "", .)
gen Shape_X = word(Shape, 1)
gen Shape_Y = word(Shape, 2)
drop Shape

destring OBJECTID Join_Count *_FID Shape_*, replace
drop Join_Count TARGET_FID

rename OBJECTID		mun_seat_fid
rename codigo 		mun_seat_codi
rename nome 		mun_seat_nome
rename Shape_X 		mun_seat_pntx
rename Shape_Y 		mun_seat_pnty
rename Name_ascii 	cap_poly_name
rename Code 		cap_poly_code
rename Abbrev 		cap_poly_abbr
rename Donatario 	cap_poly_dnam
rename Limite 		cap_poly_limt
rename Category 	cap_poly_type

label var mun_seat_fid 	"Municipality seat feature id"
label var mun_seat_codi "Municipality seat code (IBGE)"
label var mun_seat_nome "Municipality seat name (IBGE)"
label var mun_seat_pntx	"Municipality seat x-coordinate (SIRGAS)"
label var mun_seat_pnty	"Municipality seat y-coordinate (SIRGAS)"
label var cap_poly_name "Capitania name according to Cintra (2013)"
label var cap_poly_code "Capitania code according to Cintra (2013)"
label var cap_poly_abbr "Capitania abbreviation according to Cintra (2013)"
label var cap_poly_dnam "Capitania donatario's name according to Cintra (2013)"
label var cap_poly_limt "Capitania limit according to Cintra (2013)"
label var cap_poly_type "Capitania is actual or placebo"

label data "1920 municipality seats spatially joined to capitanias"
save "`destin_dir'/1920_muniseats_spj_cap_polys.dta", replace
********************************************************************************
