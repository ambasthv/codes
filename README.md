# %%
# ### Importing libraries to be used for getting data and KPI calculations


import pandas as pd
import numpy as np
pd.options.display.float_format = '{:.3f}'.format
pd.set_option('display.max_columns',None)

import pyodbc

import os
#print(os.getcwd())

import warnings
warnings.filterwarnings('ignore')

import gc

from datetime import datetime
from datetime import date 
from dateutil.relativedelta import relativedelta 
import timeit

from sklearn.metrics import log_loss, roc_auc_score, recall_score, precision_score
from sklearn.metrics import average_precision_score, f1_score, classification_report
from sklearn.metrics import accuracy_score

from sklearn.metrics import roc_curve
from warnings import filterwarnings

filterwarnings("ignore", category=UserWarning, message='.*pandas only supports SQLAlchemy connectable.*')
start = datetime.now()
#print(start)



# %%
def month_to_quarter (month):
    if month in [1,2,3]:
        return 'Q1'
    elif month in [4,5,6]:
        return 'Q2'
    elif month in [7,8,9]:
        return 'Q3'
    else: return 'Q4'

# %%


current_date = date.today()
month_end = current_date + relativedelta(day=31)
last_month_end = month_end - relativedelta(months = 1)
last_month_end = last_month_end + pd.offsets.MonthEnd(n=0)
year = last_month_end.strftime("_%Y")
last_month_end1 = last_month_end.strftime("%m/%d/%Y")

month_end_3m_prior = month_end -relativedelta(months=4)

month_end_3m_prior = month_end_3m_prior + pd.offsets.MonthEnd(n=0)
month_end_3m_prior = month_end_3m_prior.strftime("%m/%d/%Y")

month_end_12m_prior = month_end - relativedelta(months=13)

month_end_12m_prior = month_end_12m_prior + pd.offsets.MonthEnd(n=0)
month_end_12m_prior = month_end_12m_prior.strftime("%m/%d/%Y")

last_month = last_month_end.month
kpi_quarter = month_to_quarter(last_month)



eval_dates = [month_end_3m_prior, last_month_end1  ]

model_name = ['Innovation Large Corp', 'Innovation Mid Size', 'Innovation Early Stage', 'GFB CCLOC', 'GFB NAV', 'GFB Firm']


# %%
print(last_month_end1, month_end_3m_prior, month_end_12m_prior, kpi_quarter)

# %%
#last_month_end1 = '2025-09-30'

# %%
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=SQLAG-CRDMPRD-L.CORP.SVBANK.COM,1433;'
                      'Database=CRDADMANALYSIS;'
                      'Schema=dbo'
                      'Trusted_Connection=yes;')


conn2 = pyodbc.connect('Driver={SQL Server};'
                      'Server=SQLAG-CRDMPRD-L.CORP.SVBANK.COM,1433;'
                      'Database=CRDADMPRD;'
                      'Schema=dbo'
                      'Trusted_Connection=yes;')

#Step 1
# Connection to sql server
#password = cyberArk_automation_v1.main()
#conn = pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};'
                      #'Server=10.108.24.101,1436;'
                      #'Server=10.108.24.61,1435;'
                      #'Database=CRDADMANALYSIS;'
                      #'UID=svc.cdmdrr;'
                      #'PWD='+password+';'
                      #'Schema=dbo;'
                      #'TrustServerCertificate=yes;')



# %%
sql_balance = """



SELECT Supplementary_Data.*, Filtered_Balances.Balance,
		isnull(SEC_UNFUNDED,0) + isnull(SVB_UTILIZED_EXPOSURE_AMT,0) + isnull([Final Payment],0) AS 'Total Commitment', 
		isnull(SEC_UNFUNDED,0) + isnull(SVB_UTILIZED_EXPOSURE_AMT,0) + isnull([Final Payment],0) -  isnull(Balance,0) AS 'Unfunded Commitment'




FROM
	(
	SELECT  Base.LoadDT, [Entity ID], Base.LECE_FLG, Base.UNDRWRTNG_MTHD, Base.CIF, coalesce(CLIENT_LEGAL_NAME, CLIENT_NM) AS 'CLIENT_NM', CUST_LINE_NBR, 
			RISK_BAS_SEG_CD AS 'RBS Code', FACILITY_TYPE, Facility_Type_DESC, Lifestage, Risk_CD, Base.CL_OBLIGOR_RISK_RATING, Base.FINAL_LGD, Base.DUAL_RISK_RATING, NICHECD, portfolio_segment AS 'segment', BUSINESS_UNIT,
			BP_FLAG,
			Sales_Niche, 
			SEC_UNFUNDED, SVB_UTILIZED_EXPOSURE_AMT 
				

	FROM CRDADMPRD.dbo.CDM_CREDIT_LINES_VIEW Base 

	LEFT JOIN CRDADMPRD.dbo.REF_FACILITY_TYPE Facility_Table
	ON Facility_Table.FACILITY_TYPE_CD = Base.facility_type

	LEFT JOIN 
		(
		SELECT LoadDT, CLIENT_RELATIONSHIP_ENTITYID AS 'Entity ID', CIF, TEAMCODE
		FROM CRDADMPRD.dbo.CDM_CLIENTS
		WHERE 1 = 1
			AND CLIENT_RELATIONSHIP_ENTITYID is NOT NULL
			AND (
			LoadDT = '{last_month_end1}')
		)
	Entity_Table
	ON 1 =1 
		AND Entity_Table.LoadDT = Base.LoadDT 
		AND Entity_Table.CIF = Base.CIF

	LEFT JOIN 
	(
	SELECT team_code, portfolio_segment
	FROM 
		(
		SELECT *, ROW_NUMBER () OVER (PARTITION BY team_code ORDER BY create_date DESC) AS 'Ranking'
		FROM [CRDADMANALYSIS].[dbo].[ref_portfolio_segment_bk_20250105_OBSOLETE]
		)
		Segment_Rankings
		WHERE Ranking = 1
	) Portfolio_Segments
	ON Portfolio_Segments.team_code = Entity_Table.TEAMCODE


	LEFT JOIN ---not joining this qualitative data on CDM_CREDIT_LINES date. (using the max date for both; the dates don't match)
	(
	SELECT distinct Entity_Id, Sales_Niche, Sales_Sector, SCO_Name
	FROM CRDADMPRD.dbo.CDM_ENTITY_RELATIONSHIP
	WHERE 1 = 1
		AND LoadDT = (SELECT max(LoadDT) FROM CRDADMPRD.dbo.CDM_ENTITY_RELATIONSHIP WHERE DATEPART(dw, LoadDT) NOT IN (1, 7))
		AND (Sales_Niche is NOT NULL AND Sales_Sector is NOT NULL AND SCO_NAME is NOT NULL) 
	) Qualitative_Data
	ON Qualitative_Data.Entity_Id = Entity_Table.[Entity ID]

	LEFT JOIN
		(
			SELECT *
			FROM 
				(
				SELECT LoadDT AS 'Client Date', CIF AS 'Client CIF', CLIENT_LEGAL_NAME, 
						row_number () OVER (PARTITION BY LoadDT, CIF ORDER BY BP_FLAG ASC) AS 'Priority'
				FROM CRDADMPRD.dbo.CDM_CLIENTS_VIEW
				) Step_1
			WHERE Priority = 1
		) Clients

	ON 1 = 1
		AND Clients.[Client Date] = Base.LoadDT
		AND Clients.[Client CIF] = Base.CIF

				--------------------------

			LEFT JOIN ( SELECT distinct qtr_start_date, next_qtr_end_date, exclusion_type, exclusion_value, 1 AS 'Flag'
			FROM CRDADMANALYSIS.dbo.ref_FCB_exclusions_OBSOLETE
			WHERE exclusion_type = 'Cust_Line_NBR'
			) Exclusions_1

			ON 1 = 1
				AND Base.LoadDT >= Exclusions_1.qtr_start_date
				AND Base.LoadDT < Exclusions_1.next_qtr_end_date
				AND Base.Cust_Line_NBR = Exclusions_1.exclusion_value

			LEFT JOIN ( SELECT distinct qtr_start_date, next_qtr_end_date, exclusion_type, exclusion_value, 1 AS 'Flag'
			FROM CRDADMANALYSIS.dbo.ref_FCB_exclusions_OBSOLETE
			WHERE exclusion_type = 'BUSINESS_UNIT'
			) Exclusions_2

			ON 1 = 1
				AND Base.LoadDT >= Exclusions_2.qtr_start_date
				AND Base.LoadDT < Exclusions_2.next_qtr_end_date
				AND Base.BUSINESS_UNIT = Exclusions_2.exclusion_value

			--------------------------

	WHERE 1 =1 
		AND (Base.LoadDT = '{last_month_end1}')

		AND Exclusions_1.Flag IS NULL
		AND Exclusions_2.FLAG IS NULL

		AND (UPPER(LINE_STATUS) != 'EXPIRED' OR (UPPER(LINE_STATUS) = 'EXPIRED' AND SVB_UTILIZED_EXPOSURE_AMT > 0 )) 
	)
	Supplementary_Data

LEFT JOIN  
	(
	SELECT LoadDT, CUST_LINE_NBR, 
		   sum(isnull(NOTEPRNCPLBALNET,0) + isnull(LOAN_FEES_RECEIVABLE_AMT,0)) AS 'Balance',
		   sum(isnull(LOAN_FEES_RECEIVABLE_AMT,0)) AS 'Final Payment'

	FROM CRDADMPRD.dbo.CDM_INSTRUMENTS_VIEW Base

				--------------------------

			LEFT JOIN ( SELECT distinct qtr_start_date, next_qtr_end_date, exclusion_type, exclusion_value, 1 AS 'Flag'
			FROM CRDADMANALYSIS.dbo.ref_FCB_exclusions_OBSOLETE
			WHERE exclusion_type = 'ACCTNBR'
			) Exclusions_1

			ON 1 = 1
				AND Base.LoadDT >= Exclusions_1.qtr_start_date
				AND Base.LoadDT < Exclusions_1.next_qtr_end_date
				AND Base.ACCTNBR = Exclusions_1.exclusion_value

			LEFT JOIN ( SELECT distinct qtr_start_date, next_qtr_end_date, exclusion_type, exclusion_value, 1 AS 'Flag'
			FROM CRDADMANALYSIS.dbo.ref_FCB_exclusions_OBSOLETE
			WHERE exclusion_type = 'BUSINESS_UNIT'
			) Exclusions_2

			ON 1 = 1
				AND Base.LoadDT >= Exclusions_2.qtr_start_date
				AND Base.LoadDT < Exclusions_2.next_qtr_end_date
				AND Base.BUSINESS_UNIT = Exclusions_2.exclusion_value

			--------------------------

	WHERE 1 =1 
		AND CUST_LINE_NBR is NOT NULL

		AND applid not in ('MUNI','CORP')	
		AND isnull(status_cd,'None') <>'Inactive'

		AND left(isnull(LOAN_TYPE,0),1) <>'4'	
		AND Exclusions_1.Flag IS NULL
		AND Exclusions_2.Flag IS NULL
		
	GROUP BY  LoadDT, CUST_LINE_NBR
	)
Filtered_Balances 

ON 1 = 1
	AND Supplementary_Data.LoadDT = Filtered_Balances.LoadDT 
	AND Supplementary_Data.CUST_LINE_NBR = Filtered_Balances.CUST_LINE_NBR






""".format(last_month_end1=last_month_end1)



# %%
sql_risk_model = """


select distinct a.cif,b.DATE_APPROVED , a.RISK_GRADE_TEMPLATE, a.DIFFERENCE_OF_CALC_AND_FINAL_ORR

from  [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a  join 

[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
a.credit_req_nbr = b.CREDIT_REQ_NBR
where a.RISK_GRADE_TEMPLATE is not null
and b.CREDIT_REQ_STATUS = 'Booked'

"""



# %%
#pull data on Current Portfolio and Risk Template distribution 

df_current = pd.read_sql_query(sql_balance, conn2)

df_risk_model = pd.read_sql_query(sql_risk_model, conn2)

# %%
#exclude NAV and CCLOC from the risk template data df
#Sort values by date and keep most recent date for unique cif and risk template combinations

model_list = ['NAV', 'CCLOC']

df_rsk1 = df_risk_model.loc[~df_risk_model.RISK_GRADE_TEMPLATE.isin(model_list)]
df_rsk1['DATE_APPROVED'] = pd.to_datetime(df_rsk1['DATE_APPROVED'])
df_rsk1 = df_rsk1.sort_values(by='DATE_APPROVED', ascending=True)
df_rsk2 = df_rsk1.drop_duplicates(subset=['cif', 'RISK_GRADE_TEMPLATE'], keep='last')

# %%
#this shows that there is duplication and the same obligor been rated by two different templates

duplicate_rows = df_rsk2[df_rsk2['cif'].duplicated(keep=False)]
sorted_df = duplicate_rows.sort_values(by='cif')


# %%
#for the purposes of identifying portfolio segment we are only using the most recent
# risk template used for each obligor

df_rsk3 = df_rsk2.drop_duplicates(subset=['cif'], keep='last')
mapping_template = df_rsk3.set_index('cif')['RISK_GRADE_TEMPLATE']
mapping_override = df_rsk3.set_index('cif')['DIFFERENCE_OF_CALC_AND_FINAL_ORR']
df_current['risk_model'] = df_current['CIF'].map(mapping_template)
df_current['override'] = df_current['CIF'].map(mapping_override)

df_current['override_ind'] =((df_current['override'].notna()) & (df_current['override'] != 0)).astype(int)

#assign risk model based on facility type for NAV and CCLOC models (as these apply to only 1 facility type each)

df_current.loc[df_current['FACILITY_TYPE'] == 'NAV', 'risk_model'] = 'NAV'
df_current.loc[df_current['FACILITY_TYPE'] == 'PCC', 'risk_model'] = 'CCLOC'



# %%
#identifying CIFs that are eligible for Innovation Templates but still not converted

df_missing = df_current[df_current['risk_model'].isnull()]

#exclude premium wine and private bank from analysis

rbs_list = ['PW', 'PB']

df_missing = df_missing[~df_missing['RBS Code'].isin(rbs_list)]

facility_count = df_missing.groupby('CIF')['FACILITY_TYPE'].nunique()
facility_count1 = facility_count.to_frame()
facility_count1 = facility_count1.reset_index()
multiple_facility = facility_count1[facility_count1['FACILITY_TYPE'] != 1]
single_facility = facility_count1[facility_count1['FACILITY_TYPE'] == 1]

single_cif = single_facility.CIF.unique()

df_single = df_missing[df_missing['CIF'].isin(single_cif)]

fac_list = ['GUD']

single_facility_exclusions = df_single[~df_single['FACILITY_TYPE'].isin(fac_list)]

# %%
single_cif2 = single_facility_exclusions.CIF.unique()
print(len(single_cif2))
multiple_cif = multiple_facility.CIF.unique()
print(len(multiple_cif))
statement_cif = list(single_cif2) + list(multiple_cif)

statement_cif = "', '".join(statement_cif)

sql_statement = """SET NOCOUNT ON


select 

        a.cif_crm, 
        b.maxdate, 
        a.statementid,   
        a.statementmonths, 
        a.statementtype, 
        a.NETSALES

        into #temp1

        from    [CRDADMPRD].[dbo].[CDM_CLIENT_FINANCIALS_VW] a

        join (select cif_crm, max(statementdate) as maxdate from 
        [CRDADMPRD].[dbo].[CDM_CLIENT_FINANCIALS_VW] group by cif_crm) b

        on a.cif_crm = b.cif_crm and a.statementdate = b.maxdate

        where a.cif_crm in ('{statement_cif}')
        and a.statementdate > '01-01-2020';

WITH RankedRecords AS (
    SELECT
        cif_crm, 
        maxdate, 
        statementid,   
        statementmonths, 
        statementtype, 
        NETSALES,      
        
        ROW_NUMBER() OVER (PARTITION BY cif_crm, maxdate ORDER BY statementid DESC) as rn
    FROM
        #temp1

        )

        SELECT
    cif_crm, 
        maxdate, 
        statementid,  
        statementmonths, 
        statementtype, 
        NETSALES, 
        rn
    
FROM
    RankedRecords
WHERE
    rn = 1;

drop table #temp1 

""".format(statement_cif=statement_cif)

df_statement = pd.read_sql_query(sql_statement, conn2)

df_statement.drop_duplicates(inplace=True)


# %%
#annualized the net sales to segment according to model

df_statement['sales_annualized'] = df_statement['NETSALES']*12*(1/df_statement['statementmonths'])

extra_large_corp = df_statement[df_statement['sales_annualized'] > 75000]
extra_mid_size = df_statement[(df_statement['sales_annualized'] <= 75000) & (df_statement['sales_annualized'] >15000)]
extra_early_stage = df_statement[df_statement['sales_annualized'] <= 15000]

extra_large_corp1 = extra_large_corp.cif_crm.unique()
extra_mid_size1 = extra_mid_size.cif_crm.unique()
extra_early_stage1 = extra_early_stage.cif_crm.unique()


# %%
df_current.loc[df_current.CIF.isin(extra_large_corp1),'risk_model'] = 'Innovation > $75MM & Sponsor – ID/BS'
df_current.loc[df_current.CIF.isin(extra_mid_size1),'risk_model'] = 'Innovation > $15MM up to $75MM'
df_current.loc[df_current.CIF.isin(extra_early_stage1),'risk_model'] = 'Innovation up to $15MM'


# %%
baseline_dist = pd.read_csv('DRR_Testing_Data_Baseline_Rating_Distribution.csv')

# %%
model_dict = {'Innovation up to $15MM': 'Early', 'Innovation > $15MM up to $75MM': 'Mid',
       'GFB Firm' :'Firm', 'CCLOC' :'CCLOC', 'Innovation > $75MM & Sponsor – CF' :'Large',
       'Innovation > $75MM & Sponsor – ID/BS' :'Large', 'NAV': 'NAV'}

# %%
df_current['risk_model'] = df_current['risk_model'].map(model_dict)

risk_model_name = df_current.risk_model.unique().tolist()
risk_model_name = [x for x in risk_model_name if str(x) != 'nan']



# %%
df_current['CL_OBLIGOR_RISK_RATING'] = df_current['CL_OBLIGOR_RISK_RATING'].replace('None', 0)
df_current['CL_OBLIGOR_RISK_RATING'] = df_current['CL_OBLIGOR_RISK_RATING'].astype('Int64')

# %%
def calculate_psi(expected_data, actual_data, num_bins=10):
    """
    Calculates the Population Stability Index (PSI) between two datasets.

    Args:
        expected_data (pd.Series or np.ndarray): The reference or "expected" data.
        actual_data (pd.Series or np.ndarray): The current or "actual" data.
        num_bins (int): The number of bins to use for bucketing the data.

    Returns:
        float: The calculated PSI value.
    """

    # Ensure data is in a numpy array
    expected_counts = np.array(expected_data)
    actual_counts = np.array(actual_data)

   
    # Calculate counts and proportions for each bin
    expected_props = expected_counts / expected_counts.sum()
    actual_props = actual_counts / actual_counts.sum()

    expected_props = np.where(expected_props == 0, 0.0001, expected_props)
    actual_props = np.where(actual_props == 0, 0.0001, actual_props)


  

    # Calculate PSI for each bin
    psi_per_bin = (actual_props - expected_props) * np.log(actual_props / expected_props)

    # Sum the PSI for all bins to get the total PSI
    total_psi = np.sum(psi_per_bin)

    return total_psi


# %%
psi_all = []
model_all = []


for model in risk_model_name:
    df = df_current.loc[df_current.risk_model == model]
    df1 = df.groupby('CL_OBLIGOR_RISK_RATING')['CIF'].count()
    df1 = df1.reset_index()
    
    df2 = pd.merge(df1, baseline_dist, left_on='CL_OBLIGOR_RISK_RATING', right_on = 'CL_OBLIGOR_RISK_RATING')
    df2.sort_values(by='CL_OBLIGOR_RISK_RATING')
    baseline_rating = df2[model]
    actual_rating = df2['CIF']
    psi_calc = calculate_psi(baseline_rating, actual_rating)
    psi_data = pd.DataFrame(list(zip(baseline_rating, actual_rating)), columns = ['Baseline', 'Current Portfolio'])
    name_file = 'output_psi_' + model + '_data.csv'
    psi_data.to_csv(name_file)

    

    psi_all.append(psi_calc)
    model_all.append(model)



psi_all_values = pd.DataFrame(list(zip(psi_all, model_all)), columns=['PSI', 'Model'])
psi_all_values.to_csv('output_psi_all_models.csv')


# %%
baseline_rating


