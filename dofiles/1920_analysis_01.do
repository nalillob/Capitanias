clear all
set more off


* Change working directory:
cd "$capdata/dta/processed"

* Load data:
use "1920_merged.dta", clear

********************************************************************************
* CREATE VARIABLES:
* Fiscal expenditures:
gen ln_total_exp = log(Total_Exp)
gen tot_exp_pcap = Total_Exp/pop_1920
gen ln_tot_exp_pcap = log(tot_exp_pcap)

gen ln_pub_ins_exp = log(Pub_Instruction_Exp)
gen pub_ins_pcap = Pub_Instruction_Exp/pop_1920
gen ln_pub_ins_pcap = log(pub_ins_pcap)

gen ln_pub_hlth_exp = log(Pub_Health_Exp)
gen pub_hlth_pcap = Pub_Health_Exp/pop_1920
gen ln_pub_hlth_pcap = log(pub_hlth_pcap)

gen ln_pub_wrks_exp = log(Pub_Works_Exp)
gen pub_wrks_pcap = Pub_Works_Exp/pop_1920
gen ln_pub_wrks_pcap = log(pub_wrks_pcap)

gen ln_illum_exp = log(Illum_Exp)
gen illum_pcap = Illum_Exp/pop_1920
gen ln_illum_pcap = log(illum_pcap)

* Population:
gen ln_pop_1920 = log(pop_1920)
gen pcnt_foreign = 100*foreign_pop/pop_1920
gen ln_pcnt_foreign = log(pcnt_foreign)
gen ln_pcnt_foreign1 = log(pcnt_foreign + 1)
gen dv_pcnt_foreign1 = pcnt_foreign > 0 & pcnt_foreign != .

gen popden_1920 = pop_1920/(mun_poly_arm2*1000000)
gen ln_popden_1920 = log(popden_1920)

* Land inequality:
* PENDING

* Encode:
encode mun_seat_cap_poly_name, gen(capitania)
encode mun_poly_uf, gen(mun_uf)

* Simplify labels:
label var mun_treat "Treated"
label var mun_poly_runvarkm "Dist. to Treat"

label var Total_Exp "Total Expenditure"
label var ln_total_exp "Log(Total Expenditure)"
label var tot_exp_pcap "Total Expenditure per capita (1920 pop.)"
label var ln_tot_exp_pcap "Log(Total Expenditure per capita) (1920 pop.)"

label var Pub_Instruction_Exp "Public Instruction Expenditure"
label var ln_pub_ins_exp "Log(Public Instruction Expenditure)"
label var pub_ins_pcap "Public Instruction Expenditure per capita (1920 pop.)"
label var ln_pub_ins_pcap "Log(Public Instruction Expenditure per capita) (1920 pop.)"

label var Pub_Health_Exp "Public Health Expenditure"
label var ln_pub_hlth_exp "Log(Public Health Expenditure)"
label var pub_hlth_pcap "Public Health Expenditure per capita (1920 pop.)"
label var ln_pub_hlth_pcap "Log(Public Health Expenditure per capita) (1920 pop.)"

label var Pub_Works_Exp "Public Works Expenditure"
label var ln_pub_wrks_exp "Log(Public Works Expenditure)"
label var pub_wrks_pcap "Public Works Expenditure per capita (1920 pop.)"
label var ln_pub_wrks_pcap "Log(Public Works Expenditure per capita) (1920 pop.)"

label var Illum_Exp "Illumination Expenditure"
label var ln_illum_exp "Log(Illumination Expenditure)"
label var illum_pcap "Illumination Expenditure per capita (1920 pop.)"
label var ln_illum_pcap "Log(Illumination Expenditure per capita) (1920 pop.)"

label var pop_1920 "Population, 1920"
label var ln_pop_1920 "Log(Population), 1920"
label var popden_1920 "Population Density, 1920, persons per km2"
label var ln_popden_1920 "Log(Population Density), 1920"

label var pcnt_foreign "Percent Foreign Population, 1920"
label var ln_pcnt_foreign "Log(Percent Foreign Population), 1920"
label var ln_pcnt_foreign1 "Log(1 + Percent Foreign Population), 1920"

label var a7_14percent_literate "Literacy Rate, ages 7-14"
label var a15percent_literate "Literacy Rate, age 15+"

********************************************************************************
* VARLISTS:
* fiscal:
global total_exp Total_Exp ln_total_exp tot_exp_pcap ln_tot_exp_pcap
global pub_instr Pub_Instruction_Exp ln_pub_ins_exp pub_ins_pcap ln_pub_ins_pcap
global pub_helth Pub_Health_Exp ln_pub_hlth_exp pub_hlth_pcap ln_pub_hlth_pcap
global pub_works Pub_Works_Exp ln_pub_wrks_exp pub_wrks_pcap ln_pub_wrks_pcap
global illum_exp Illum_Exp ln_illum_exp illum_pcap ln_illum_pcap

* other:
global demo_1920 pop_1920 ln_pop_1920 popden_1920 ln_popden_1920
global foreign pcnt_foreign ln_pcnt_foreign ln_pcnt_foreign1
global literacy a7_14percent_literate a15percent_literate


********************************************************************************
* SIMPLE REGRESSIONS:
foreach var of varlist $total_exp $pub_instr $pub_helth $pub_works $illum_exp ///
	$demo_1920 $foreign $literacy {
	
	* Treated/Untreated:
	reg `var' i.mun_treat, vce(robust)
	est store `var'_11
	reg `var' i.mun_treat i.mun_uf, vce(robust)
	est store `var'_12
	reg `var' i.mun_treat i.capitania, vce(robust)
	est store `var'_13
	reg `var' i.mun_treat i.mun_uf i.capitania, vce(robust)
	est store `var'_14
	
	* Treated x Distance:
	reg `var' i.mun_treat##c.mun_poly_runvarkm, vce(robust)
	est store `var'_21
	reg `var' i.mun_treat##c.mun_poly_runvarkm i.mun_uf, vce(robust)
	est store `var'_22
	reg `var' i.mun_treat##c.mun_poly_runvarkm i.capitania, vce(robust)
	est store `var'_23
	reg `var' i.mun_treat##c.mun_poly_runvarkm i.mun_uf i.capitania, vce(robust)
	est store `var'_24
}

********************************************************************************
* TABLES:
log using "$results/preliminary_01", replace name(log_01) text
foreach var of varlist $total_exp $pub_instr $pub_helth $pub_works $illum_exp ///
	$demo_1920 $foreign $literacy {
	
	local depvar_label : variable label `var'
	
	esttab `var'_*, se nobase r2 label star(* .1 ** .05 *** .01) var(30) ///
		indicate("State FE = *.mun_uf" "Capitania FE = *.capitania") nocons ///
		title("`depvar_label'")
}
log close log_01
