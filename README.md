1.	I have a data frame, which read a parquet file.
df_main= “Clean Data V1.parquet”  is the main parquet file, contains all data. 
2.	Then I filter this data 
df_filt = df_main[df_main['model_routing'] == 'ID / BSD']
3.	then I check required columns in dataframe df_filt
RATIO_COLS  = ["grossmargin", "netmargin","adjquick","debttotnw"] 

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

5.	then I create a new column “lifestage_mapped” from “lifestage” column using below mapping. These mapping are very imp for further analysis. 

So, create “lifestage_mapped” colum and add it into df_filt

lifestage_mapping = {
    "Angel / Seed Firm": "Other",
    "Angel/Seed Firm": "Other",
    "Angel/Seed Fund": "Other",
    "Corp Tech": "Corp Tech",
    "Early Stage": "Early Stage",
    "Emerging Tech": "Emerging Tech",
    "ET": "Emerging Tech",
    "Large Corp": "Large Corporate",
    "Large Corporate": "Large Corporate",
    "Late Stage": "Late Stage",
    "Mid Stage": "Mid Stage",
    "Mid stage": "Mid Stage",
    "Non-Niche": "Other",
    "Non-niche": "Other",
    "PCS": "Other",
    "Private Bank": "Other",
    "Private Equity": "Other",
    "Private Equity Fiem": "Other",
    "Private Equity Firm": "Other",
    "Sponsor Led Buyout": "Other",
    "VC Firm": "Other",
    "Venture Capital Firm": "Other",
    "Wine": "Other",
    "None": "None"
6.	once these mapping is done, change the df_filt name and create copy to df
7.	Check if both columns exist in new df. Sample data (Original vs Mapped):
8.	NOW, I HAVE df. With those culmn. So you start writing the code from here. 
o	Do Ratio calculation as shown below.  
Gross margin=	(Gross Profit / Net Sales ) x 100
Net margin=	(Net Profit /Net Sales) x 100
Net Sales/Total Assets=	Net Sales/Total Assets
Apply the condition given earlier, no mistake in applying rules. Writing them again for you reference. NO MISTAKE IN RULES. DON’T ASSUME ANYTHING
1.	1 Negative handling:
a.	If only the denominator has potential for being negative: set to max
b.	If both the numerator and denominator have potential for being negative: set to min if the denominator is negative
2.	2 Zero handling:
a.	If the numerator is not expected to have a zero value: set to null
3.	3 Infinite handling (waterfall logic):
a.	If both the numerator and denominator have potential for being negative: none (inf handled through capping and flooring)
b.	If the denominator is not expected to have a zero value: set to null
c.	If neither of the conditions above are met: set to max

SHOW ALL THE OUPPUT IN EACH STEP OF CODE (JUPYTER)
SAVE ALL THE RESULTS IN EXCEL in directory 
