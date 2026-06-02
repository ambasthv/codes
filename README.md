write easy python code for vs code, dont write big codes and fucntion. make it easy, easy to read, easy to interpret, and easy to run. 
For performing our first step of segmentation analysis we would be using the following selected.


1.	Filter main df with “ID /BSD” in “model_routing” column
2.	Create new data frame df_filt. And use this dataframe across the below codes. 
3.	Identify Key Columns and its unique records
4.	
5.	Identify the lifestage and nichecode and naics_code code fields.
6.	lifestage mapping needs to be done as table given below 
7.	# Original variations → Clean Mapped Name
8.	    "Angel / Seed Firm": "Other",
9.	    "Angel/Seed Firm": "Other",
10.	    "Angel/Seed Fund": "Other",
11.	    "Corp Tech": "Corp Tech",
12.	    "ET": "Emerging Tech",
13.	    "Early Stage": "Early Stage",
14.	    "Emerging Tech": "Emerging Tech",
15.	    "Emerging Tech or ET": "Emerging Tech",
16.	    "Large Corp": "Large Corporate",
17.	    "Large Corporate": "Large Corporate",
18.	    "Late Stage": "Late Stage",
19.	    "Mid Stage": "Mid Stage",
20.	    "Non-Niche": "Other",
21.	    "PCS": "Other",
22.	    "Private Bank": "Other",
23.	    "Private Equity": "Other",
24.	    "Private Equity Fiem": "Other",
25.	    "Private Equity Firm": "Other",
26.	    "Sponsor Led Buyout": "Other",
27.	    "VC Firm": "Other",
28.	    "Venture Capital Firm": "Other",
29.	    "Wine": "Other"

Clean and map the above list with lifestage, create new column with “lifestage_mapped”
Show mapped lifestage distribution 
Verify it “verification = df_filt[['lifestage_original', 'lifestage_clean', 'lifestage_mapped']].drop_duplicates().head(20)
“

3.	Identify the following target ratios within 
Operating Performance columns name:
grossmargin
netmargin
netsales
totalassets
Correlation between ratios (explain them, heatmap)
Trend over Grade Year
Trend over lifestage_mapped


whenever your using above rations, in y axis or anywhere, explain that means, explain plots you create, box and histogram, whatever you create, explain in code as commented lines, withproper explanation,  what it means, how to interpret it  

4.	Produce data distributions for each of the ratios “Operating Performance columns name”  segmented  by lifestage_mapped(we start with this and layer on other segments later)
5.	Produce summary statistics table by segment for each ratio and lifestage_mapped
6.	Produce charts for the distributions (box plots and histograms to begin with), make it lite so it can run, last code ran for about 7 hrs and didn’t result anything.
7.	Produce interactive charts (something like is done in Tableau- but less code), same make it lite and quick run
8.	 Use “grade_date” (year and month column) for above analysis. lifestage_mapped
9.	Use column “cif” for unique counts, and against lifestage_mapped and nichecode and naics_code,
10.	“balance” and “commitment” (dollar value col) analysis against lifestage_mapped and nichecode and naics_code, (show the table in full number and in billions, 
11.	Create stacked bar chart using balance and commitment for lifestage_mapped.
12.	Created stacked basr chart using balance and commitment by grade year. 
13.	Correlation between ratios
14.	Save correlation heatmap
15.	Trend over Grade Year
16.	Trend over Grade Year and Month
17.	SHOW ALL CHARTS IN VS CODE, 
18.	SHOW ALL TABLES IN VS CODE
19.	SAVE ALL CHARTS AND TABLES IN EXCEL IN SAME FOLDER AS PARQUET FILE.
20.	DON’T CREATE ANY FOLDER, JUST SAVE EXCEL AND CHARTS, to_excel.
