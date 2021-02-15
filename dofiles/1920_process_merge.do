clear all
set more off

* Change to working directory:
cd "$capdata/dta/processed"

* Load base dataset:
use "1920_mun_poly_runvars.dta", clear

* Merge in 1920 farmsize data:
destring mun_poly_codi, gen(code_1920)
merge 1:1 code_1920 using "$capdata\raw\Felipe\Censo1920_farmsize.dta", ///
	keep(1 3) gen(mrg_1920_farmsize)

* Merge in 1920 literacy rate:
destring mun_poly_codi, gen(UFMUNDV)
merge 1:1 UFMUNDV using "$capdata\raw\Felipe\1920 Literacy.dta", ///
	keep(1 3) gen(mrg_1920_literacy)

* Merge in 1920 foreign population:
merge 1:1 UFMUNDV using ///
	"$capdata\raw\Felipe\Foreign Population by Municipality 1920.dta", ///
	keep(1 3) gen(mrg_1920_foreignpop)

* Merge in 1926 fiscal expenditures:
* first, prepare fiscal data:
preserve
use "$capdata\raw\Felipe\Public expenditure_1.dta", clear
tostring UFMUNDV, gen(mun_poly_codi) format(%07.0f)
gen mun_poly_nome = nome
gen mun_poly_uf = substr(mun_poly_codi, 1, 2)
duplicates tag mun_poly_nome mun_poly_uf, gen(dups_1)
drop if dups_1 == 1
drop mun_poly_codi dups_1
save "1926_public_expenditure_premerge.dta", replace
restore

* second, merge based on municipality code:
merge 1:1 UFMUNDV using "1926_public_expenditure_premerge.dta", ///
	keep(1 3) gen(mrg_1920_fiscalexp_1) ///
	keepusing(Total_Exp Pub_Instruction_Exp Pub_Health_Exp Pub_Works_Exp ///
		Illum_Exp NEW_CODE_1920_1997 Code Divida_Publica)

* third, merge based on municipality name and province code:
merge 1:1 mun_poly_nome mun_poly_uf ///
	using "1926_public_expenditure_premerge.dta", ///
	gen(mrg_1920_fiscalexp_2) keep(1 3 4) update ///
	keepusing(Total_Exp Pub_Instruction_Exp Pub_Health_Exp Pub_Works_Exp ///
		Illum_Exp NEW_CODE_1920_1997 Code Divida_Publica)
		
save "1920_merged.dta", replace

	

