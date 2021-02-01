clear all
set more off

* Load and standardise municipality polygon geographic data:
use "$capdata/dta/IBGE/from_csv/1920/T05_malha_municipal_1920.dta", clear
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
save "$capdata/dta/processed/1920_municipality_polygon.dta", replace

* Load and standardise municipality seat geographic data:
use "$capdata/dta/IBGE/from_csv/1920/T03_sede_municipal_1920.dta", clear
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



save "$capdata/dta/processed/1920_municipality_seat.dta", replace

* Load and standardise border geographic data:
import delimited "$capdata\csv\IBGE\1920\capitanias_GCS_WGS_1984_line.csv", ///
	case(preserve) asdouble encoding(utf8) stringcols(_all) 
replace Shape = subinstr(Shape, "(", "", .)
replace Shape = subinstr(Shape, ")", "", .)
replace Shape = subinstr(Shape, ",", "", .)
gen Shape_X = word(Shape,1)
gen Shape_Y = word(Shape,2)
drop Shape


save "$capdata/dta/processed/1920_capitania_borders.dta", replace


