So, lets re-write the code again form scratch. You missed the main essence of the analysis. So idea is, 
Do and show the mathematical distribution analysis, 
Produce and show data distributions for each of the ratios segmented 
Produce and show summary statistics table by segment for each ratio 
Produce and show charts for the distributions (box plots and histograms to begin with)
show the chart (no fail chart), show the table, keep saving each table in separate sheets of excel and save in df_path. Simply save, don’t create folder.
Imp columns to use for analysis are below,
•	cif
•	grade_date
•	commitment
•	balance
•	totalassets
•	netsales
•	grossmargin
•	netmargin
•	naics_code
•	lifestage
•	nichecode
Now ask is: 
1.	dataframe to use for all analysis is df_filt
2.	do mapping of lifestage to lifestage_mapped (create this column), below is the mapping table, 
    "Angel / Seed Firm": "Other",
    "Angel/Seed Firm": "Other",
    "Angel/Seed Fund": "Other",
    "Corp Tech": "Corp Tech",
    "ET": "Emerging Tech",
    "Early Stage": "Early Stage",
    "Emerging Tech": "Emerging Tech",
    "Emerging Tech or ET": "Emerging Tech",
    "Large Corp": "Large Corporate",
    "Large Corporate": "Large Corporate",
    "Late Stage": "Late Stage",
    "Mid Stage": "Mid Stage",
    "Non-Niche": "Other",
    "PCS": "Other",
    "Private Bank": "Other",
    "Private Equity": "Other",
    "Private Equity Fiem": "Other",
    "Private Equity Firm": "Other",
    "Sponsor Led Buyout": "Other",
    "VC Firm": "Other",
    "Venture Capital Firm": "Other",
    "Wine": "Other"
•	Clean and Map Lifestage
•	Mapped Lifestage Distribution
•	Verification

3.	with the above lifestage_mapped, do further analysis as below,
a.	do (Distributions & Summary Stats) mathematical distribution and statistical analysis lifestage_mapped, year, balance. Create chart/histogram/boxplot
b.	do (Distributions & Summary Stats) mathematical distribution and statistical analysis lifestage_mapped, year, commitment. Create chart/histogram/boxplot
c.	do (Distributions & Summary Stats) mathematical distribution and statistical analysis lifestage_mapped, year, and each ratios separately. Create chart/histogram/boxplot
d.	Unique CIF Count year wise for lifestage_mapped
e.	Correlation of ratios, heatmap 
f.	Each separate trend chart for balance , commitment over year, lifestage_mapped, ratios, over years.


