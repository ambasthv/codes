1.	check required columns in dataframe df
RATIO_COLS  = ["grossmargin", "netmargin","Net Sales/Total Assets"] 

1.	cif
2.	grade_date
3.	totalassets
4.	netsales
5.	grossprofit
6.	netprofit
7.	lifestage
8.	balance
9.	rbs
10.	commitment
these colums are imp for my analysis. But for ratio calculation you need to use 
1.	totalassets
2.	netsales
3.	grossprofit
4.	netprofit
5.	NOW, I HAVE df. With those culmn. So you start writing the code from here. 
o	Do Ratio calculation as shown below.  
Gross margin=	(Gross Profit / Net Sales ) x 100
Net margin=	(Net Profit /Net Sales) x 100
Net Sales/Total Assets=	Net Sales/Total Assets
Apply the formula given earlier, no mistake in applying. 
Writing RULE for you reference. NO MISTAKE IN RULES. DON’T ASSUME ANYTHING.
•	DON’T ASSUME GENERAL RULES. WHAT I AM WRITING BELOW IS ONLY RULE FOR YOU NOW.
•	ALL IMP COL CAN HAVE NEGATIVE, ZERO, POSITIVE. SO SET RULE IN SUCH A WAY THAT IT READS EVERYTHING AND APPLY THE BEST SUITABLE.  
•	Ex -ve/-ve = +ve  (put the min/max as per rules), create flag column and say both num & denom were -ve.
•	0/0, handle based on rules, but in flag col, mention it, 
•	Do such thing for right rules given below and flag them
1.	create a flag column for negative denominator & numerator and then handle accordingly as below, once we calculate the ratio
2.	Negative handling:
a.	If only the denominator has potential for being negative: set to MAX
b.	If both the numerator and denominator have potential for being negative: set to MIN if the denominator is negative
3.	Zero handling:
a.	If the numerator is not expected to have a zero value: set to null
4.	Infinite handling (waterfall logic):
a.	If both the numerator and denominator have potential for being negative: none (inf handled through capping and flooring)
b.	If the denominator is not expected to have a zero value: set to null
c.	If neither of the conditions above are met: set to max
5.	Save all output in excel, (cif,	grade_date,	lifestage_original	,lifestage_clean	lifestage_mapped,	totalassets,	netsales,	grossprofit,	netprofit,	grossmargin,	netmargin,	sales_to_assets)
