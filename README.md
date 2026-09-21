get sql code for this one as well. only sql.
# %% [markdown]
# #### Importing libraries 

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
from pandas.tseries.offsets import DateOffset

from sklearn.metrics import log_loss, roc_auc_score, recall_score, precision_score
from sklearn.metrics import average_precision_score, f1_score, classification_report
from sklearn.metrics import accuracy_score

from sklearn.metrics import roc_curve
from warnings import filterwarnings

filterwarnings("ignore", category=UserWarning, message='.*pandas only supports SQLAlchemy connectable.*')
start = datetime.now()
#print(start)



# %%
#drivers = pyodbc.drivers()
#print("Available ODBC Drivers:", drivers)

# %% [markdown]
# #### Function to convert month to quarter

# %%
def month_to_quarter (month):
    if month in [1,2,3]:
        return 'Q1'
    elif month in [4,5,6]:
        return 'Q2'
    elif month in [7,8,9]:
        return 'Q3'
    else: return 'Q4'

# %% [markdown]
# #### Create dates to be used for generating performance monitoring KPIs

# %%


current_date = date.today()
month_end = current_date + relativedelta(day=31)
last_month_end = month_end - relativedelta(months = 2)

last_month_end = last_month_end + pd.offsets.MonthEnd(n=0)
year = last_month_end.strftime("_%Y")
last_month_end1 = last_month_end.strftime("%m/%d/%Y")

month_end_3m_prior = month_end -relativedelta(months=4)

month_end_3m_prior = month_end_3m_prior + pd.offsets.MonthEnd(n=0)
month_end_3m_prior = month_end_3m_prior.strftime("%m/%d/%Y")

month_end_12m_prior = month_end - relativedelta(months=14)

month_end_12m_prior = month_end_12m_prior + pd.offsets.MonthEnd(n=0)
month_end_12m_prior = month_end_12m_prior.strftime("%m/%d/%Y")

last_month = last_month_end.month
kpi_quarter = month_to_quarter(last_month)



eval_dates = [month_end_3m_prior, last_month_end1  ]

model_name = ['Innovation Large Corp', 'Innovation Mid Size', 'Innovation Early Stage', 'GFB CCLOC', 'GFB NAV', 'GFB Firm']


# %%
print(last_month_end1, month_end_12m_prior, kpi_quarter)

# %%
#create function for getting the last 12 month end dates

def get_last_12_month_end_dates(last_month_end):
    """
    Generates a list of the last 12 month-end dates.
    """
    
    month_end_dates = []

    # Start from the end of the previous month

    
    

    for _ in range(12):
        month_end_dates.append(last_month_end)
        # Move to the end of the previous month
        last_month_end = last_month_end.replace(day=1) - relativedelta(days=1)
        # Sort to get them in chronological order
        sorted(month_end_dates)
        me_date_string_list = list(map(lambda x: x.strftime("%m/%d/%Y"), month_end_dates))

    return me_date_string_list 




# %% [markdown]
# #### Create a KPI dictionary with the KPIs that are being processed in this segment of the KPI code 

# %%
kpi_dict1 = {'KPI 1'	: 'Number of Overrides',

'KPI 2' :	'Accuracy',
'KPI 3':	'Gini',
'KPI 4'	: 'KS Statistic' 
 }




# %% [markdown]
# #### Check the quarter end date and quarter being processed in this run 

# %% [markdown]
# #### Establish connection to SQL server

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



# %% [markdown]
# #### This code segment is to extract dataset for troubleshooting in case a deep dive into the KPIs is required

# %%
# extracting data for troubleshooting. Not used for calculations of KPIs

sql_override_all = """


select distinct  a.CIF,  b.DATE_APPROVED,a.CALCULATED_ORR, a.FINAL_ORR, 				
                a.DIFFERENCE_OF_CALC_AND_FINAL_ORR, a.OVERRIDE_REASON, a.risk_grade_template	
				
							
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'Innovation > $75MM & Sponsor – CF', 
    'Innovation > $75MM & Sponsor – ID/BS', 'Innovation > $15MM up to $75MM',
      'Innovation up to $15MM','CCLOC', 'NAV', 'GFB Firm' )	

     	
      		
				
				and b.DATE_APPROVED < '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
                
                
    
    
    """.format(month_end_12m_prior=month_end_12m_prior)


# %%
# data only used for troubleshooting. Not used for calculation of KPIs

override_all = pd.DataFrame(pd.read_sql_query(sql_override_all, conn))

print(override_all.shape)
override_all.to_csv('override_all_innovation_v2.csv')

# %% [markdown]
# #### Portfolio Data for ORR for each Month End in 12M Evaluation Period

# %%
last_12_month_ends = get_last_12_month_end_dates(last_month_end)
last_12_month_ends1 = "', '".join(last_12_month_ends)


sql_port_12m = """SET NOCOUNT ON

select  loaddt as MonthEnd, CIF, max(CL_OBLIGOR_RISK_RATING) as orr1 


from [CRDADMPRD].[dbo].[CDM_CREDIT_LINES_VIEW]

where loaddt in ('{last_12_month_ends1}')

group by loaddt, cif










""".format(last_12_month_ends1=last_12_month_ends1)


last_12_ports = pd.DataFrame(pd.read_sql_query(sql_port_12m, conn))

last_12_ports['MonthEnd'] = pd.to_datetime(last_12_ports['MonthEnd']).dt.strftime("%m/%d/%Y")

# %% [markdown]
# #### Section 1: PD Models Override - In this segment data is extracted for overrides per risk template for the evaluation period.  

# %%
# calculating overrides for DRR Large Corp

large_corp_kpi = []
num_override_tot = []
# DRR Large Corp 



sql_override = """

select distinct  a.CIF,  b.DATE_APPROVED,a.CALCULATED_ORR, a.FINAL_ORR, 				
                a.DIFFERENCE_OF_CALC_AND_FINAL_ORR, a.OVERRIDE_REASON, a.risk_grade_template	
				
							
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'Innovation > $75MM & Sponsor – CF', 
    'Innovation > $75MM & Sponsor – ID/BS')	

     	
      		
				
				and b.DATE_APPROVED > '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
        
    """.format(month_end_12m_prior=month_end_12m_prior)


# using sql code above to extract data to calculate override KPI

override_large_corp_raw = pd.DataFrame(pd.read_sql_query(sql_override, conn))

#saving list of unique cifs in the evaluation period for calculation of other KPIs 

cif_list_large_kpi = override_large_corp_raw.CIF.unique()

print(override_large_corp_raw.shape)



#create  a month end column for the most proximate month end for each date approved

override_large_corp_raw['DATE_APPROVED'] = pd.to_datetime(override_large_corp_raw['DATE_APPROVED'])
override_large_corp_raw['MonthEnd'] = override_large_corp_raw['DATE_APPROVED'] + pd.offsets.MonthEnd(1)
override_large_corp_raw['MonthEnd'] = override_large_corp_raw['MonthEnd'].dt.strftime("%m/%d/%Y")

combined_override_large = pd.merge(override_large_corp_raw, last_12_ports, on=['CIF', 'MonthEnd'], how='left')


#subset the data that doesn't occur in the portfolio (Nan value for ORR) or where the final ORR is 
#not the same as portfolio ORR

override_large_corp = combined_override_large[combined_override_large['orr1'].notna()]
override_large_corp = override_large_corp[override_large_corp.orr1 == override_large_corp.FINAL_ORR]
    
#calculate override percentage based on difference_of_calc_and_final_orr field


override_large_corp['OVERRIDE_INDICATOR'] = 0
    
override_large_corp.loc[override_large_corp['DIFFERENCE_OF_CALC_AND_FINAL_ORR'] != 0, 'OVERRIDE_INDICATOR'] = 1
override_by_drr_large = override_large_corp.groupby("FINAL_ORR")["OVERRIDE_INDICATOR"].mean()
override_by_drr_large = override_by_drr_large.reset_index()
override_by_drr_large['FINAL_ORR'] = override_by_drr_large['FINAL_ORR'].astype(int)
override_by_drr_large = override_by_drr_large.sort_values(by='FINAL_ORR')
override_by_drr_large2 = list(override_by_drr_large['OVERRIDE_INDICATOR'])


num_of_overrides = override_large_corp[override_large_corp.DIFFERENCE_OF_CALC_AND_FINAL_ORR != 0]
total_override = num_of_overrides.shape[0]
print(total_override)
num_override_tot.append(total_override)

total_override1 = total_override/override_large_corp.shape[0]
try: 
    total_override_mid1 = total_override/override_large_corp.shape[0]
except ZeroDivisionError:
    total_override1 = 0
    
large_corp_kpi.append(total_override1)


# %%
cif_list_large_df = pd.DataFrame(cif_list_large_kpi)
cif_list_large_df.to_csv('cif_list_large_df.csv')
override_large_corp.to_csv('override_large_corp_reasons.csv')
override_by_drr_large.to_csv('override_by_drr_large.csv')

# %%
# DRR Mid Size 
mid_kpi = []

sql_override3 = """

select distinct  a.CIF,  b.DATE_APPROVED,a.CALCULATED_ORR, a.FINAL_ORR, 				
                a.DIFFERENCE_OF_CALC_AND_FINAL_ORR, a.OVERRIDE_REASON, a.risk_grade_template	
				
							
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in (  'Innovation > $15MM up to $75MM' )	

     	
      		
				
				and b.DATE_APPROVED > '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
        
    """.format(month_end_12m_prior = month_end_12m_prior)



override_mid_raw = pd.read_sql_query(sql_override3, conn)
cif_list_mid_kpi = override_mid_raw.CIF.unique()

    


#create  a month end column for the most proximate month end for each date APPROVED

override_mid_raw['DATE_APPROVED'] = pd.to_datetime(override_mid_raw['DATE_APPROVED'])
override_mid_raw['MonthEnd'] = override_mid_raw['DATE_APPROVED'] + pd.offsets.MonthEnd(1)
override_mid_raw['MonthEnd'] = override_mid_raw['MonthEnd'].dt.strftime("%m/%d/%Y")

combined_override_mid = pd.merge(override_mid_raw, last_12_ports, on=['CIF', 'MonthEnd'], how='left')


#subset the data that doesn't occur in the portfolio (Nan value for ORR) or where the final ORR is 
#not the same as portfolio ORR

override_mid = combined_override_mid[combined_override_mid['orr1'].notna()]
override_mid = override_mid[override_mid.orr1 == override_mid.FINAL_ORR]

   
override_mid['OVERRIDE_INDICATOR'] = 0
    
override_mid.loc[override_mid['DIFFERENCE_OF_CALC_AND_FINAL_ORR'] != 0, 'OVERRIDE_INDICATOR'] = 1
override_by_drr_mid = override_mid.groupby("FINAL_ORR")["OVERRIDE_INDICATOR"].mean()
override_by_drr_mid = override_by_drr_mid.reset_index()
override_by_drr_mid['FINAL_ORR'] = override_by_drr_mid['FINAL_ORR'].astype(int)
override_by_drr_mid = override_by_drr_mid.sort_values(by='FINAL_ORR')
override_by_drr_mid2 = list(override_by_drr_mid['OVERRIDE_INDICATOR'])
    
num_of_overrides_mid = override_mid[override_mid.DIFFERENCE_OF_CALC_AND_FINAL_ORR != 0]
total_override_mid = num_of_overrides_mid.shape[0]
    
try: 
    total_override_mid1 = total_override_mid/override_mid.shape[0]
except ZeroDivisionError:
    total_override_mid1 = 0
    
mid_kpi.append(total_override_mid1)
num_override_tot.append(total_override_mid)



# %%
cif_list_mid_df = pd.DataFrame(cif_list_mid_kpi)
cif_list_mid_df.to_csv('cif_list_mid_df.csv')
override_mid.to_csv('override_mid_reasons.csv')
override_by_drr_mid.to_csv('override_by_drr_mid.csv')

# %%
# DRR Early Stage 

early_kpi = []

sql_override2 = """

select distinct  a.CIF,  b.DATE_APPROVED,a.CALCULATED_ORR, a.FINAL_ORR, 				
                a.DIFFERENCE_OF_CALC_AND_FINAL_ORR, a.OVERRIDE_REASON, a.risk_grade_template	
				
							
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'Innovation up to $15MM' )	

     	
      		
				
				and b.DATE_APPROVED > '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
        
    """.format(month_end_12m_prior=month_end_12m_prior)


override_early_stage_raw = pd.read_sql_query(sql_override2, conn)
cif_list_early_kpi = override_early_stage_raw.CIF.unique()

#create  a month end column for the most proximate month end for each date approved

override_early_stage_raw['DATE_APPROVED'] = pd.to_datetime(override_early_stage_raw['DATE_APPROVED'])
override_early_stage_raw['MonthEnd'] = override_early_stage_raw['DATE_APPROVED'] + pd.offsets.MonthEnd(1)
override_early_stage_raw['MonthEnd'] = override_early_stage_raw['MonthEnd'].dt.strftime("%m/%d/%Y")

combined_override_early = pd.merge(override_early_stage_raw, last_12_ports, on=['CIF', 'MonthEnd'], how='left')


#subset the data that doesn't occur in the portfolio (Nan value for ORR) or where the final ORR is 
#not the same as portfolio ORR

override_early_stage = combined_override_early[combined_override_early['orr1'].notna()]
override_early_stage = override_early_stage[override_early_stage.orr1 == override_early_stage.FINAL_ORR]


override_early_stage['OVERRIDE_INDICATOR'] = 0
    
override_early_stage.loc[override_early_stage['DIFFERENCE_OF_CALC_AND_FINAL_ORR'] != 0, 'OVERRIDE_INDICATOR'] = 1
override_by_drr_early = override_early_stage.groupby("FINAL_ORR")["OVERRIDE_INDICATOR"].mean()

override_by_drr_early = override_by_drr_early.reset_index()
override_by_drr_early['FINAL_ORR'] = override_by_drr_early['FINAL_ORR'].astype(int)
override_by_drr_early = override_by_drr_early.sort_values(by='FINAL_ORR')
override_by_drr_early2 = list(override_by_drr_early['OVERRIDE_INDICATOR'])

num_of_overrides_early_stage = override_early_stage[override_early_stage.DIFFERENCE_OF_CALC_AND_FINAL_ORR != 0]
total_override_early_stage = num_of_overrides_early_stage.shape[0]
num_override_tot.append(total_override_early_stage)

try: 
    total_override_early_stage1 = total_override_early_stage/override_early_stage.shape[0]
except ZeroDivisionError: 
    total_override_early_stage1 = 0

early_kpi.append(total_override_early_stage1)
 



# %%
cif_list_early_df = pd.DataFrame(cif_list_early_kpi)
cif_list_early_df.to_csv('cif_list_early_df.csv')
override_early_stage.to_csv('override_early_reasons.csv')
override_by_drr_early.to_csv('override_by_drr_early.csv')

# %%
# DRR GFB Firm 

firm_kpi = []

sql_override4 = """

select distinct  a.CIF,  b.DATE_APPROVED,a.CALCULATED_ORR, a.FINAL_ORR, 				
                a.DIFFERENCE_OF_CALC_AND_FINAL_ORR, a.OVERRIDE_REASON, a.risk_grade_template	
				
							
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'GFB Firm' )	

     	
      		
				
				and b.DATE_APPROVED > '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
        
""".format(month_end_12m_prior=month_end_12m_prior)

override_Firm_raw = pd.read_sql_query(sql_override4, conn)
cif_list_firm_kpi = override_Firm_raw.CIF.unique()

#create  a month end column for the most proximate month end for each date approved

override_Firm_raw['DATE_APPROVED'] = pd.to_datetime(override_Firm_raw['DATE_APPROVED'])
override_Firm_raw['MonthEnd'] = override_Firm_raw['DATE_APPROVED'] + pd.offsets.MonthEnd(1)
override_Firm_raw['MonthEnd'] = override_Firm_raw['MonthEnd'].dt.strftime("%m/%d/%Y")

combined_override_Firm = pd.merge(override_Firm_raw, last_12_ports, on=['CIF', 'MonthEnd'], how='left')


#subset the data that doesn't occur in the portfolio (Nan value for ORR) or where the final ORR is 
#not the same as portfolio ORR

override_Firm = combined_override_Firm[combined_override_Firm['orr1'].notna()]
override_Firm = override_Firm[override_Firm.orr1 == override_Firm.FINAL_ORR]


override_Firm['OVERRIDE_INDICATOR'] = 0
    
override_Firm.loc[override_Firm['DIFFERENCE_OF_CALC_AND_FINAL_ORR'] != 0, 'OVERRIDE_INDICATOR'] = 1
override_by_drr_Firm = override_Firm.groupby("FINAL_ORR")["OVERRIDE_INDICATOR"].mean()

override_by_drr_Firm = override_by_drr_Firm.reset_index()
override_by_drr_Firm['FINAL_ORR'] = override_by_drr_Firm['FINAL_ORR'].astype(int)
override_by_drr_Firm = override_by_drr_Firm.sort_values(by='FINAL_ORR')
override_by_drr_Firm2 = list(override_by_drr_Firm['OVERRIDE_INDICATOR'])

num_of_overrides_Firm = override_Firm[override_Firm.DIFFERENCE_OF_CALC_AND_FINAL_ORR != 0]
total_override_Firm = num_of_overrides_Firm.shape[0]


try: 
    total_override_Firm1 = total_override_Firm/override_Firm.shape[0]
except ZeroDivisionError: 
    total_override_Firm1 = 0

firm_kpi.append(total_override_Firm1)
num_override_tot.append(total_override_Firm)



# %%
cif_list_firm_df = pd.DataFrame(cif_list_firm_kpi)
cif_list_firm_df.to_csv('cif_list_firm_df.csv')
override_Firm.to_csv('override_firm_reasons.csv')
override_by_drr_Firm.to_csv('override_by_drr_Firm.csv')

# %%
# DRR GFB CCLOC 

ccloc_kpi = []

sql_override4 = """

select distinct  a.CIF,  b.DATE_APPROVED,a.CALCULATED_ORR, a.FINAL_ORR, 				
                a.DIFFERENCE_OF_CALC_AND_FINAL_ORR, a.OVERRIDE_REASON, a.risk_grade_template	
				
							
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'CCLOC' )	

     	
      		
				
				and b.DATE_APPROVED > '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
        
""".format(month_end_12m_prior=month_end_12m_prior)

override_CCLOC_raw = pd.read_sql_query(sql_override4, conn)
cif_list_ccloc_kpi = override_CCLOC_raw.CIF.unique()

#create  a month end column for the most proximate month end for each date approved

override_CCLOC_raw['DATE_APPROVED'] = pd.to_datetime(override_CCLOC_raw['DATE_APPROVED'])
override_CCLOC_raw['MonthEnd'] = override_CCLOC_raw['DATE_APPROVED'] + pd.offsets.MonthEnd(1)
override_CCLOC_raw['MonthEnd'] = override_CCLOC_raw['MonthEnd'].dt.strftime("%m/%d/%Y")

combined_override_CCLOC = pd.merge(override_CCLOC_raw, last_12_ports, on=['CIF', 'MonthEnd'], how='left')


#subset the data that doesn't occur in the portfolio (Nan value for ORR) or where the final ORR is 
#not the same as portfolio ORR

override_CCLOC = combined_override_CCLOC[combined_override_CCLOC['orr1'].notna()]
override_CCLOC = override_CCLOC[override_CCLOC.orr1 == override_CCLOC.FINAL_ORR]


override_CCLOC['OVERRIDE_INDICATOR'] = 0
    
override_CCLOC.loc[override_CCLOC['DIFFERENCE_OF_CALC_AND_FINAL_ORR'] != 0, 'OVERRIDE_INDICATOR'] = 1
override_by_drr_CCLOC = override_CCLOC.groupby("FINAL_ORR")["OVERRIDE_INDICATOR"].mean()

override_by_drr_CCLOC = override_by_drr_CCLOC.reset_index()
override_by_drr_CCLOC['FINAL_ORR'] = override_by_drr_CCLOC['FINAL_ORR'].astype(int)
override_by_drr_CCLOC2 = override_by_drr_CCLOC.sort_values(by='FINAL_ORR')
override_by_drr_CCLOC = list(override_by_drr_CCLOC['OVERRIDE_INDICATOR'])

num_of_overrides_CCLOC = override_CCLOC[override_CCLOC.DIFFERENCE_OF_CALC_AND_FINAL_ORR != 0]
total_override_CCLOC = num_of_overrides_CCLOC.shape[0]


try: 
    total_override_CCLOC1 = total_override_CCLOC/override_CCLOC.shape[0]
except ZeroDivisionError: 
    total_override_CCLOC1 = 0

ccloc_kpi.append(total_override_CCLOC1)
num_override_tot.append(total_override_CCLOC)



# %%
cif_list_ccloc_df = pd.DataFrame(cif_list_ccloc_kpi)
cif_list_ccloc_df.to_csv('cif_list_ccloc_df.csv')
override_CCLOC.to_csv('override_ccloc_reasons.csv')
override_by_drr_CCLOC2.to_csv('override_by_drr_CCLOC2.csv')

# %%
# DRR GFB NAV

nav_kpi = []

sql_override5 = """ 

select distinct  a.CIF,  b.DATE_APPROVED,a.CALCULATED_ORR, a.FINAL_ORR, 				
                a.DIFFERENCE_OF_CALC_AND_FINAL_ORR, a.OVERRIDE_REASON, a.risk_grade_template	
				
							
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'NAV' )	

     	
      		
				
				and b.DATE_APPROVED > '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
        
""".format(month_end_12m_prior=month_end_12m_prior)



override_NAV_raw = pd.read_sql_query(sql_override5, conn)
cif_list_nav_kpi = override_NAV_raw.CIF.unique()

#create  a month end column for the most proximate month end for each date approved

override_NAV_raw['DATE_APPROVED'] = pd.to_datetime(override_NAV_raw['DATE_APPROVED'])
override_NAV_raw['MonthEnd'] = override_NAV_raw['DATE_APPROVED'] + pd.offsets.MonthEnd(1)
override_NAV_raw['MonthEnd'] = override_NAV_raw['MonthEnd'].dt.strftime("%m/%d/%Y")

combined_override_NAV = pd.merge(override_NAV_raw, last_12_ports, on=['CIF', 'MonthEnd'], how='left')


#subset the data that doesn't occur in the portfolio (Nan value for ORR) or where the final ORR is 
#not the same as portfolio ORR

override_NAV = combined_override_NAV[combined_override_NAV['orr1'].notna()]
override_NAV = override_NAV[override_NAV.orr1 == override_NAV.FINAL_ORR]



override_NAV['OVERRIDE_INDICATOR'] = 0
    
override_NAV.loc[override_NAV['DIFFERENCE_OF_CALC_AND_FINAL_ORR'] != 0, 'OVERRIDE_INDICATOR'] = 1
override_by_drr_NAV = override_NAV.groupby("FINAL_ORR")["OVERRIDE_INDICATOR"].mean()

override_by_drr_NAV = override_by_drr_NAV.reset_index()
override_by_drr_NAV['FINAL_ORR'] = override_by_drr_NAV['FINAL_ORR'].astype(int)
override_by_drr_NAV = override_by_drr_NAV.sort_values(by='FINAL_ORR')
override_by_drr_NAV2 = list(override_by_drr_NAV['OVERRIDE_INDICATOR'])

num_of_overrides_NAV = override_NAV[override_NAV.DIFFERENCE_OF_CALC_AND_FINAL_ORR != 0]
total_override_NAV = num_of_overrides_NAV.shape[0]

try: 
    total_override_NAV1 = total_override_NAV/override_NAV.shape[0]

except ZeroDivisionError: 
    0

try: 
    total_override_NAV1 = total_override_NAV/override_NAV.shape[0]
except ZeroDivisionError: 
    total_override_NAV1 = 0

nav_kpi.append(total_override_NAV1)
num_override_tot.append(total_override_NAV)

# %%
print(total_override_NAV,override_NAV.shape[0])

# %%
cif_list_nav_df = pd.DataFrame(cif_list_nav_kpi)
cif_list_nav_df.to_csv('cif_list_nav_df.csv')
override_NAV.to_csv('override_nav_reasons.csv')
override_by_drr_NAV.to_csv('override_by_drr_NAV.csv')
num_override_tot = pd.DataFrame(num_override_tot)
num_override_tot.to_csv('pd_override_12m.csv')

# %% [markdown]
# #### Section 2: PD Models Accuracy 

# %%
masterscale = pd.read_csv('masterscale.csv')

# %%
#dates when each risk rating template was implemented

large_corp_date = '08-31-2023'

mid_date = '04-30-2024'

early_date = '04-30-2024'

CCLOC_date = '01-31-2022'

NAV_date = '01-31-2022'

firm_date = '08-31-2023'

# %%
#excluding Loss/Grade 17 rating from the evaluation as distance to default is 0

#grade_exclusion = ['15', '16', '17']
grade_exclusion = [ ]

FINAL_ORR = list(range(17))
FINAL_ORR.pop(0)
Predict_Default = [0]*16
dummy_df = list(zip(FINAL_ORR, Predict_Default))
dummy_df1 = pd.DataFrame(dummy_df, columns=['FINAL_ORR', 'Predict_Default'])


# %%
#Default Status Data for all Models

sql_default = """
SELECT distinct cif, loaddt, default_flag

from [CRDADMPRD].[dbo].[CDM_CLIENT_DEFAULT_STATUS_VW]

			where loaddt > '01-01-2024'
        """

all_default = pd.DataFrame(pd.read_sql_query(sql_default, conn))
all_default['loaddt'] = pd.to_datetime(all_default['loaddt'])




# %%
#Determine if default occured within a 12 month window of observation date. If default occured
#indicator is 1 else 0
#as default data is reported on a monthly basis a window size of 12 indicates a 12 month performance window

def distance_to_def(df):
    df['loaddt'] = pd.to_datetime(df['loaddt'])
    df = df.sort_values(by=['cif', 'loaddt'], ascending=[True, True])
    df['reversed_value'] = df.groupby('cif')['default_flag'].transform(lambda x: x[::-1].values)
    window_size = 12
    forward_max_reversed = df.groupby('cif')['reversed_value'].transform(
        lambda x: x.rolling(window=window_size, min_periods=1, closed='left').max())
    
    # 5. Reverse the results back to the original time order
    df['defaulted_within_12mo'] = df.groupby('cif')['reversed_value'].transform(lambda x: forward_max_reversed[::-1])
    
    df.sort_index(inplace=True) 
    df.rename(columns={'loaddt': 'MonthEnd', 'cif':'CIF'}, inplace=True)
    return df 


  


# %%
#Determine if default occured within months prior to risk rating approval date (excluding the actual risk rating/observation date) If default occured
#indicator is 1 else 0
#as default data is reported on a monthly basis a window size of 12 indicates a 12 month performance window

def prior_default(df):
    df['MonthEnd'] = pd.to_datetime(df['MonthEnd'])
    df = df.sort_values(by=['CIF', 'MonthEnd'], ascending=[True, True])
    
    window_size = 12
    df['previous_default'] = df.groupby('CIF')['default_flag'].transform(
        lambda x: x.rolling(window=window_size, min_periods=1, closed='left').max())
       
    df.sort_index(inplace=True) 
    
    return df 

# %%
sql_large = """

select distinct  a.CIF,  b.DATE_APPROVED, a.FINAL_ORR	
				
							
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'Innovation > $75MM & Sponsor – CF', 
    'Innovation > $75MM & Sponsor – ID/BS')	

     	
      		
				
				and b.DATE_APPROVED < '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
        
    """.format(month_end_12m_prior=month_end_12m_prior)

default_large_raw = pd.read_sql_query(sql_large, conn)
default_large_raw = default_large_raw.drop_duplicates()
default_large_raw['DATE_APPROVED'] = pd.to_datetime(default_large_raw['DATE_APPROVED'])
default_large_raw['MonthEnd'] = default_large_raw['DATE_APPROVED'] + pd.offsets.MonthEnd(1)
default_large_raw['MonthEnd'] = default_large_raw['MonthEnd'].dt.strftime("%m/%d/%Y")
default_large_raw['MonthEnd'] = pd.to_datetime(default_large_raw['MonthEnd'])

#excluding the already non-performing accounts from the analysis (can be changed to excluding only defaulted obligors)


default_large_raw = default_large_raw.loc[~default_large_raw.FINAL_ORR.isin(grade_exclusion)]

large_cif = default_large_raw.CIF.unique()





# %%
#extract the default data for obligors rated under the risk rating template under evaluation

default_status_large = all_default.loc[all_default.cif.isin(large_cif)]
default_status_large = default_status_large.loc[default_status_large.loaddt > large_corp_date]

#only use evaluation dates after model implementation



default_large_corp1 = distance_to_def(default_status_large)



default_large_corp = pd.merge(default_large_corp1 ,default_large_raw,on=['CIF', 'MonthEnd'], how='inner' )





# %%
# DRR Large Corp 

default_large_corp = default_large_corp.fillna(0)
default_large_corp['defaulted_within_12mo'] = default_large_corp['defaulted_within_12mo'].astype(int)


large_corp_total = default_large_corp.groupby('FINAL_ORR')['CIF'].count() 
large_corp_total = pd.DataFrame(large_corp_total)
large_corp_total = large_corp_total.reset_index()
large_corp_total['FINAL_ORR'] = large_corp_total['FINAL_ORR'].astype(int)
large_corp_total = large_corp_total.sort_values(by='FINAL_ORR')


large_corp_default = default_large_corp.groupby('FINAL_ORR')['defaulted_within_12mo'].sum()
large_corp_default = pd.DataFrame(large_corp_default)
large_corp_default = large_corp_default.reset_index()
large_corp_default['FINAL_ORR'] = large_corp_default['FINAL_ORR'].astype(int)
large_corp_default = large_corp_default.sort_values(by='FINAL_ORR')

large_corp_acc = pd.merge(large_corp_total, large_corp_default, right_on = 'FINAL_ORR', left_on = 'FINAL_ORR', how = 'inner')

large_corp_acc_v2 = pd.merge(dummy_df1, large_corp_acc, on='FINAL_ORR', how = 'left')
large_corp_acc_v2 = large_corp_acc_v2.fillna(0)
large_corp_acc_v2 = pd.merge(large_corp_acc_v2,masterscale, on = 'FINAL_ORR', how = 'left')
large_corp_acc_v2['Predict_Default'] = large_corp_acc_v2['CIF']*large_corp_acc_v2['PD']

large_corp_acc_v2['Actual_PD'] = np.where(large_corp_acc_v2['CIF'] != 0, large_corp_acc_v2['defaulted_within_12mo'] / large_corp_acc_v2['CIF'], 0)
predicted_rate_large2 = large_corp_acc_v2['Predict_Default'].sum()/large_corp_acc_v2['CIF'].sum()
actual_rate_large2 = large_corp_acc_v2['defaulted_within_12mo'].sum()/large_corp_acc_v2['CIF'].sum()
MAE_large = abs(predicted_rate_large2 - actual_rate_large2)

large_corp_kpi.append(MAE_large)

# %%
large_corp_acc_v2.to_csv('large_corp_actual_predict.csv')

# %%
sql_mid = """

select distinct  a.CIF,  b.DATE_APPROVED, a.FINAL_ORR	
				
							
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'Innovation > $15MM up to $75MM')	

     	
      		
				
				and b.DATE_APPROVED < '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
        
    """.format(month_end_12m_prior=month_end_12m_prior)

default_mid_raw = pd.read_sql_query(sql_mid, conn)
default_mid_raw['DATE_APPROVED'] = pd.to_datetime(default_mid_raw['DATE_APPROVED'])
default_mid_raw['MonthEnd'] = default_mid_raw['DATE_APPROVED'] + pd.offsets.MonthEnd(1)
default_mid_raw['MonthEnd'] = default_mid_raw['MonthEnd'].dt.strftime("%m/%d/%Y")
default_mid_raw['MonthEnd'] = pd.to_datetime(default_mid_raw['MonthEnd'])


#excluding the already non-performing accounts from the analysis (can be changed to excluding only defaulted obligors)


default_mid_raw = default_mid_raw.loc[~default_mid_raw.FINAL_ORR.isin(grade_exclusion)]

mid_cif = default_mid_raw.CIF.unique()



# %%
default_status_mid = all_default.loc[all_default.cif.isin(mid_cif)]

default_status_mid = default_status_mid.loc[default_status_mid.loaddt > mid_date]

default_mid1 = distance_to_def(default_status_mid)


default_mid = pd.merge(default_mid1, default_mid_raw,on=['CIF', 'MonthEnd'], how='inner' )

#exclude obligors that have defaulted before rating decision. 

#default_mid = default_mid2.loc[default_mid2.default_flag != '1']


# %%
default_mid1.to_csv('default_mid.csv')

# %%
# DRR Mid Size 

default_mid = default_mid.fillna(0)
default_mid['defaulted_within_12mo'] = default_mid['defaulted_within_12mo'].astype(int)


mid_total = default_mid.groupby('FINAL_ORR')['CIF'].count() 
mid_total = pd.DataFrame(mid_total)
mid_total = mid_total.reset_index()
mid_total['FINAL_ORR'] = mid_total['FINAL_ORR'].astype(int)
mid_total = mid_total.sort_values(by='FINAL_ORR')


mid_default = default_mid.groupby('FINAL_ORR')['defaulted_within_12mo'].sum()
mid_default = pd.DataFrame(mid_default)
mid_default = mid_default.reset_index()
mid_default['FINAL_ORR'] = mid_default['FINAL_ORR'].astype(int)
mid_default = mid_default.sort_values(by='FINAL_ORR')

mid_acc = pd.merge(mid_total, mid_default, right_on = 'FINAL_ORR', left_on = 'FINAL_ORR', how = 'inner')

mid_acc_v2 = pd.merge(dummy_df1, mid_acc, on='FINAL_ORR', how = 'left')
mid_acc_v2 = mid_acc_v2.fillna(0)
mid_acc_v2 = pd.merge(mid_acc_v2,masterscale, on = 'FINAL_ORR', how = 'left')
mid_acc_v2['Predict_Default'] = mid_acc_v2['CIF']*mid_acc_v2['PD']

mid_acc_v2['Actual_PD'] = np.where(mid_acc_v2['CIF'] != 0, mid_acc_v2['defaulted_within_12mo'] / mid_acc_v2['CIF'], 0)
predicted_rate_mid2 = mid_acc_v2['Predict_Default'].sum()/mid_acc_v2['CIF'].sum()
actual_rate_mid2 = mid_acc_v2['defaulted_within_12mo'].sum()/mid_acc_v2['CIF'].sum()
MAE_mid = abs(predicted_rate_mid2 - actual_rate_mid2)

mid_kpi.append(MAE_mid)


# %%
mid_acc_v2.to_csv('mid_actual_predict.csv')

# %%
sql_firm = """

select distinct  a.CIF,  b.DATE_APPROVED, a.FINAL_ORR	
				
							
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'GFB Firm')	

     	
      		
				
				and b.DATE_APPROVED < '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
        
    """.format(month_end_12m_prior=month_end_12m_prior)

default_firm_raw = pd.read_sql_query(sql_firm, conn)
default_firm_raw['DATE_APPROVED'] = pd.to_datetime(default_firm_raw['DATE_APPROVED'])
default_firm_raw['MonthEnd'] = default_firm_raw['DATE_APPROVED'] + pd.offsets.MonthEnd(1)
default_firm_raw['MonthEnd'] = default_firm_raw['MonthEnd'].dt.strftime("%m/%d/%Y")
default_firm_raw['MonthEnd'] = pd.to_datetime(default_firm_raw['MonthEnd'])


#excluding the already non-performing accounts from the analysis (can be changed to excluding only defaulted obligors)


default_firm_raw = default_firm_raw.loc[~default_firm_raw.FINAL_ORR.isin(grade_exclusion)]

firm_cif = default_firm_raw.CIF.unique()


# %%
default_status_firm = all_default.loc[all_default.cif.isin(firm_cif)]

default_status_firm = default_status_firm.loc[default_status_firm.loaddt > firm_date]

default_firm1 = distance_to_def(default_status_firm)


default_firm = pd.merge(default_firm1, default_firm_raw,on=['CIF', 'MonthEnd'], how='inner' )
#default_firm = default_firm2.loc[default_firm2.default_flag != '1']

# %%
# DRR Firm

default_Firm = default_firm.fillna(0)
default_Firm['defaulted_within_12mo'] = default_Firm['defaulted_within_12mo'].astype(int)


Firm_total = default_Firm.groupby('FINAL_ORR')['CIF'].count() 
Firm_total = pd.DataFrame(Firm_total)
Firm_total = Firm_total.reset_index()
Firm_total['FINAL_ORR'] = Firm_total['FINAL_ORR'].astype(int)
Firm_total = Firm_total.sort_values(by='FINAL_ORR')


Firm_default = default_Firm.groupby('FINAL_ORR')['defaulted_within_12mo'].sum()
Firm_default = pd.DataFrame(Firm_default)
Firm_default = Firm_default.reset_index()
Firm_default['FINAL_ORR'] = Firm_default['FINAL_ORR'].astype(int)
Firm_default = Firm_default.sort_values(by='FINAL_ORR')

Firm_acc = pd.merge(Firm_total, Firm_default, right_on = 'FINAL_ORR', left_on = 'FINAL_ORR', how = 'inner')

Firm_acc_v2 = pd.merge(dummy_df1, Firm_acc, on='FINAL_ORR', how = 'left')
Firm_acc_v2 = Firm_acc_v2.fillna(0)
Firm_acc_v2 = pd.merge(Firm_acc_v2,masterscale, on = 'FINAL_ORR', how = 'left')
Firm_acc_v2['Predict_Default'] = Firm_acc_v2['CIF']*Firm_acc_v2['PD']

Firm_acc_v2['Actual_PD'] = np.where(Firm_acc_v2['CIF'] != 0, Firm_acc_v2['defaulted_within_12mo'] / Firm_acc_v2['CIF'], 0)
predicted_rate_Firm2 = Firm_acc_v2['Predict_Default'].sum()/Firm_acc_v2['CIF'].sum()
actual_rate_Firm2 = Firm_acc_v2['defaulted_within_12mo'].sum()/Firm_acc_v2['CIF'].sum()
MAE_Firm = abs(predicted_rate_Firm2 - actual_rate_Firm2)

firm_kpi.append(MAE_Firm)


# %%
Firm_acc_v2.to_csv('firm_actual_predict.csv')

# %%
sql_ccloc = """

select distinct  a.CIF,  b.DATE_APPROVED, a.FINAL_ORR	
				
							
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'CCLOC')	

     	
      		
				
				and b.DATE_APPROVED < '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
        
    """.format(month_end_12m_prior=month_end_12m_prior)

default_ccloc_raw = pd.read_sql_query(sql_ccloc, conn)
default_ccloc_raw['DATE_APPROVED'] = pd.to_datetime(default_ccloc_raw['DATE_APPROVED'])
default_ccloc_raw['MonthEnd'] = default_ccloc_raw['DATE_APPROVED'] + pd.offsets.MonthEnd(1)
default_ccloc_raw['MonthEnd'] = default_ccloc_raw['MonthEnd'].dt.strftime("%m/%d/%Y")
default_ccloc_raw['MonthEnd'] = pd.to_datetime(default_ccloc_raw['MonthEnd'])


#excluding the already non-performing accounts from the analysis (can be changed to excluding only defaulted obligors)


default_ccloc_raw = default_ccloc_raw.loc[~default_ccloc_raw.FINAL_ORR.isin(grade_exclusion)]

ccloc_cif = default_ccloc_raw.CIF.unique()


# %%
default_status_ccloc = all_default.loc[all_default.cif.isin(ccloc_cif)]

default_status_ccloc = default_status_ccloc.loc[default_status_ccloc.loaddt > CCLOC_date]

default_ccloc1 = distance_to_def(default_status_ccloc)


default_ccloc = pd.merge(default_ccloc1, default_ccloc_raw,on=['CIF', 'MonthEnd'], how='inner' )
#default_ccloc = default_ccloc2.loc[default_ccloc2.default_flag != '1']

# %%
test = default_ccloc1.loc[default_ccloc1.defaulted_within_12mo == 1]

test.to_csv('test_ccloc.csv')

# %%
# DRR CCLOC

default_CCLOC = default_ccloc.fillna(0)
default_CCLOC['defaulted_within_12mo'] = default_CCLOC['defaulted_within_12mo'].astype(int)


CCLOC_total = default_CCLOC.groupby('FINAL_ORR')['CIF'].count() 
CCLOC_total = pd.DataFrame(CCLOC_total)
CCLOC_total = CCLOC_total.reset_index()
CCLOC_total['FINAL_ORR'] = CCLOC_total['FINAL_ORR'].astype(int)
CCLOC_total = CCLOC_total.sort_values(by='FINAL_ORR')


CCLOC_default = default_CCLOC.groupby('FINAL_ORR')['defaulted_within_12mo'].sum()
CCLOC_default = pd.DataFrame(CCLOC_default)
CCLOC_default = CCLOC_default.reset_index()
CCLOC_default['FINAL_ORR'] = CCLOC_default['FINAL_ORR'].astype(int)
CCLOC_default = CCLOC_default.sort_values(by='FINAL_ORR')

CCLOC_acc = pd.merge(CCLOC_total, CCLOC_default, right_on = 'FINAL_ORR', left_on = 'FINAL_ORR', how = 'inner')

CCLOC_acc_v2 = pd.merge(dummy_df1, CCLOC_acc, on='FINAL_ORR', how = 'left')
CCLOC_acc_v2 = CCLOC_acc_v2.fillna(0)
CCLOC_acc_v2 = pd.merge(CCLOC_acc_v2,masterscale, on = 'FINAL_ORR', how = 'left')
CCLOC_acc_v2['Predict_Default'] = CCLOC_acc_v2['CIF']*CCLOC_acc_v2['PD']

CCLOC_acc_v2['Actual_PD'] = np.where(CCLOC_acc_v2['CIF'] != 0, CCLOC_acc_v2['defaulted_within_12mo'] / CCLOC_acc_v2['CIF'], 0)
predicted_rate_CCLOC2 = CCLOC_acc_v2['Predict_Default'].sum()/CCLOC_acc_v2['CIF'].sum()
actual_rate_CCLOC2 = CCLOC_acc_v2['defaulted_within_12mo'].sum()/CCLOC_acc_v2['CIF'].sum()
MAE_CCLOC = abs(predicted_rate_CCLOC2 - actual_rate_CCLOC2)

ccloc_kpi.append(MAE_CCLOC)

# %%
CCLOC_acc_v2.to_csv('ccloc_actual_predict.csv')

# %%
sql_early = """

select distinct  a.CIF,  b.DATE_APPROVED, a.FINAL_ORR	
				
							
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'Innovation up to $15MM')	

     	
      		
				
				and b.DATE_APPROVED < '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
        
    """.format(month_end_12m_prior=month_end_12m_prior)

default_early_raw = pd.read_sql_query(sql_early, conn)
default_early_raw['DATE_APPROVED'] = pd.to_datetime(default_early_raw['DATE_APPROVED'])
default_early_raw['MonthEnd'] = default_early_raw['DATE_APPROVED'] + pd.offsets.MonthEnd(1)
default_early_raw['MonthEnd'] = default_early_raw['MonthEnd'].dt.strftime("%m/%d/%Y")
default_early_raw['MonthEnd'] = pd.to_datetime(default_early_raw['MonthEnd'])


#excluding the already non-performing accounts from the analysis (can be changed to excluding only defaulted obligors)


default_early_raw = default_early_raw.loc[~default_early_raw.FINAL_ORR.isin(grade_exclusion)]

early_cif = default_early_raw.CIF.unique()


# %%
default_status_early = all_default.loc[all_default.cif.isin(early_cif)]

default_status_early = default_status_early.loc[default_status_early.loaddt > early_date]

default_early1 = distance_to_def(default_status_early)


default_early = pd.merge(default_early1, default_early_raw,on=['CIF', 'MonthEnd'], how='inner' )
#default_early = default_early2.loc[default_early2.default_flag != '1']

# %%
# DRR Early Stage

default_early_stage = default_early.fillna(0)
default_early_stage['defaulted_within_12mo'] = default_early_stage['defaulted_within_12mo'].astype(int)


early_stage_total = default_early_stage.groupby('FINAL_ORR')['CIF'].count() 
early_stage_total = pd.DataFrame(early_stage_total)
early_stage_total = early_stage_total.reset_index()
early_stage_total['FINAL_ORR'] = early_stage_total['FINAL_ORR'].astype(int)
early_stage_total = early_stage_total.sort_values(by='FINAL_ORR')


early_stage_default = default_early_stage.groupby('FINAL_ORR')['defaulted_within_12mo'].sum()
early_stage_default = pd.DataFrame(early_stage_default)
early_stage_default = early_stage_default.reset_index()
early_stage_default['FINAL_ORR'] = early_stage_default['FINAL_ORR'].astype(int)
early_stage_default = early_stage_default.sort_values(by='FINAL_ORR')

early_stage_acc = pd.merge(early_stage_total, early_stage_default, right_on = 'FINAL_ORR', left_on = 'FINAL_ORR', how = 'inner')

early_stage_acc_v2 = pd.merge(dummy_df1, early_stage_acc, on='FINAL_ORR', how = 'left')
early_stage_acc_v2 = early_stage_acc_v2.fillna(0)
early_stage_acc_v2 = pd.merge(early_stage_acc_v2,masterscale, on = 'FINAL_ORR', how = 'left')
early_stage_acc_v2['Predict_Default'] = early_stage_acc_v2['CIF']*early_stage_acc_v2['PD']

early_stage_acc_v2['Actual_PD'] = np.where(early_stage_acc_v2['CIF'] != 0, early_stage_acc_v2['defaulted_within_12mo'] / early_stage_acc_v2['CIF'], 0)
predicted_rate_early2 = early_stage_acc_v2['Predict_Default'].sum()/early_stage_acc_v2['CIF'].sum()
actual_rate_early2 = early_stage_acc_v2['defaulted_within_12mo'].sum()/early_stage_acc_v2['CIF'].sum()
MAE_early = abs(predicted_rate_early2 - actual_rate_early2)
early_kpi.append(MAE_early)


# %%
early_stage_acc_v2.to_csv('early_stage_actual_predict.csv')

# %%
sql_nav = """

select distinct  a.CIF,  b.DATE_APPROVED, a.FINAL_ORR	
				
							
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'NAV')	

     	
      		
				
				and b.DATE_APPROVED < '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
        
    """.format(month_end_12m_prior=month_end_12m_prior)

default_nav_raw = pd.read_sql_query(sql_nav, conn)
default_nav_raw['DATE_APPROVED'] = pd.to_datetime(default_nav_raw['DATE_APPROVED'])
default_nav_raw['MonthEnd'] = default_nav_raw['DATE_APPROVED'] + pd.offsets.MonthEnd(1)
default_nav_raw['MonthEnd'] = default_nav_raw['MonthEnd'].dt.strftime("%m/%d/%Y")
default_nav_raw['MonthEnd'] = pd.to_datetime(default_nav_raw['MonthEnd'])


#excluding the already non-performing accounts from the analysis (can be changed to excluding only defaulted obligors)


default_nav_raw = default_nav_raw.loc[~default_nav_raw.FINAL_ORR.isin(grade_exclusion)]

nav_cif = default_nav_raw.CIF.unique()


# %%
default_status_nav = all_default.loc[all_default.cif.isin(nav_cif)]

default_status_nav = default_status_nav.loc[default_status_nav.loaddt > NAV_date]

default_nav1 = distance_to_def(default_status_nav)


default_nav = pd.merge(default_nav1, default_nav_raw,on=['CIF', 'MonthEnd'], how='inner' )
#default_nav = default_nav2.loc[default_nav2.default_flag != '1']

# %%
# DRR NAV

default_NAV = default_nav.fillna(0)
default_NAV['defaulted_within_12mo'] = default_NAV['defaulted_within_12mo'].astype(int)


NAV_total = default_NAV.groupby('FINAL_ORR')['CIF'].count() 
NAV_total = pd.DataFrame(NAV_total)
NAV_total = NAV_total.reset_index()
NAV_total['FINAL_ORR'] = NAV_total['FINAL_ORR'].astype(int)
NAV_total = NAV_total.sort_values(by='FINAL_ORR')


NAV_default = default_NAV.groupby('FINAL_ORR')['defaulted_within_12mo'].sum()
NAV_default = pd.DataFrame(NAV_default)
NAV_default = NAV_default.reset_index()
NAV_default['FINAL_ORR'] = NAV_default['FINAL_ORR'].astype(int)
NAV_default = NAV_default.sort_values(by='FINAL_ORR')

NAV_acc = pd.merge(NAV_total, NAV_default, right_on = 'FINAL_ORR', left_on = 'FINAL_ORR', how = 'inner')

NAV_acc_v2 = pd.merge(dummy_df1, NAV_acc, on='FINAL_ORR', how = 'left')
NAV_acc_v2 = NAV_acc_v2.fillna(0)
NAV_acc_v2 = pd.merge(NAV_acc_v2,masterscale, on = 'FINAL_ORR', how = 'left')
NAV_acc_v2['Predict_Default'] = NAV_acc_v2['CIF']*NAV_acc_v2['PD']

NAV_acc_v2['Actual_PD'] = np.where(NAV_acc_v2['CIF'] != 0, NAV_acc_v2['defaulted_within_12mo'] / NAV_acc_v2['CIF'], 0)
predicted_rate_NAV2 = NAV_acc_v2['Predict_Default'].sum()/NAV_acc_v2['CIF'].sum()
actual_rate_NAV2 = NAV_acc_v2['defaulted_within_12mo'].sum()/NAV_acc_v2['CIF'].sum()
MAE_NAV = abs(predicted_rate_NAV2 - actual_rate_NAV2)

nav_kpi.append(MAE_NAV)

# %%
NAV_acc_v2.to_csv('NAV_actual_predict.csv')

# %% [markdown]
# #### Section 3: Gini

# %%
# GINI calculations for all DRR models

#DRR Large Corp
 
default_large_corp['FINAL_ORR'] = default_large_corp['FINAL_ORR'].astype(int)
large_corp_gini = pd.merge(default_large_corp,masterscale, on = 'FINAL_ORR', how = 'left') 
large_corp_gini = large_corp_gini.fillna(0)

predicted_rate_large = large_corp_gini['PD']
actual_rate_large = large_corp_gini['defaulted_within_12mo']

auc_large = roc_auc_score(actual_rate_large, predicted_rate_large)
gini_large = 2*auc_large -1 

large_corp_kpi.append(gini_large)

#DRR Mid Size 

default_mid['FINAL_ORR'] = default_mid['FINAL_ORR'].astype(int)
mid_gini = pd.merge(default_mid,masterscale, on = 'FINAL_ORR', how = 'left') 
mid_gini = mid_gini.fillna(0)

predicted_rate_mid = mid_gini['PD']
actual_rate_mid = mid_gini['defaulted_within_12mo']

auc_mid = roc_auc_score(actual_rate_mid, predicted_rate_mid)
gini_mid = 2*auc_mid -1

mid_kpi.append(gini_mid)

#DRR Early Stage

default_early_stage['FINAL_ORR'] = default_early_stage['FINAL_ORR'].astype(int)
early_stage_gini = pd.merge(default_early_stage,masterscale, on = 'FINAL_ORR', how = 'left')
early_stage_gini = early_stage_gini.fillna(0)

predicted_rate_early = early_stage_gini['PD']
actual_rate_early = early_stage_gini['defaulted_within_12mo']

auc_early = roc_auc_score(actual_rate_early,predicted_rate_early)
gini_early = 2*auc_early - 1 

early_kpi.append(gini_early)


#DRR GFB Firm


default_Firm['FINAL_ORR'] = default_Firm['FINAL_ORR'].astype(int)
Firm_gini = pd.merge(default_Firm,masterscale, on = 'FINAL_ORR', how = 'left')
Firm_gini = Firm_gini.fillna(0)

predicted_rate_Firm = Firm_gini['PD']
actual_rate_Firm = Firm_gini['defaulted_within_12mo']

auc_Firm = roc_auc_score(actual_rate_Firm,predicted_rate_Firm)
gini_Firm = 2*auc_Firm - 1 

firm_kpi.append(gini_Firm)



#DRR CCLOC 

default_CCLOC['FINAL_ORR'] = default_CCLOC['FINAL_ORR'].astype(int)
CCLOC_gini = pd.merge(default_CCLOC,masterscale, on = 'FINAL_ORR', how = 'left') 
CCLOC_gini = CCLOC_gini.fillna(0)


predicted_rate_CCLOC = CCLOC_gini['PD']
actual_rate_CCLOC = CCLOC_gini['defaulted_within_12mo']

auc_ccloc = roc_auc_score(actual_rate_CCLOC, predicted_rate_CCLOC)
gini_ccloc = 2*auc_ccloc - 1

ccloc_kpi.append(gini_ccloc)

#DRR NAV

default_NAV['FINAL_ORR'] = default_NAV['FINAL_ORR'].astype(int)
NAV_gini = pd.merge(default_NAV,masterscale, on = 'FINAL_ORR', how = 'left') 
NAV_gini = NAV_gini.fillna(0)


predicted_rate_NAV = NAV_gini['PD']
actual_rate_NAV = NAV_gini['defaulted_within_12mo']
try: 
    auc_nav = roc_auc_score(actual_rate_NAV, predicted_rate_NAV)
except ValueError: 
    auc_nav = 0
gini_nav = 2*auc_nav - 1


nav_kpi.append(gini_nav)

# %% [markdown]
# #### Section 4: KS 

# %%
# KS calculations for all DRR models



#DRR Large Corp 

fpr_large, tpr_large, large_thresholds = roc_curve(actual_rate_large,predicted_rate_large)
ks_large = max(tpr_large - fpr_large) 

large_corp_kpi.append(ks_large)

#DRR Mid Size 
fpr_mid, tpr_mid, mid_thresholds = roc_curve(actual_rate_mid,predicted_rate_mid)
ks_mid = max(tpr_mid - fpr_mid) 
mid_kpi.append(ks_mid)

#DRR Early Stage

fpr_early, tpr_early, early_thresholds = roc_curve(actual_rate_early,predicted_rate_early)
ks_early = max(tpr_early - fpr_early) 
early_kpi.append(ks_early)

#DRR GFB Firm

fpr_Firm, tpr_Firm, Firm_thresholds = roc_curve(actual_rate_Firm,predicted_rate_Firm)
ks_Firm = max(tpr_Firm - fpr_Firm) 
firm_kpi.append(ks_Firm)



#DRR CCLOC 

fpr_ccloc, tpr_ccloc, ccloc_thresholds = roc_curve(actual_rate_CCLOC,predicted_rate_CCLOC)
ks_ccloc = max(tpr_ccloc - fpr_ccloc) 
ccloc_kpi.append(ks_ccloc)


#DRR NAV
try:
    fpr_nav, tpr_nav, nav_thresholds = roc_curve(actual_rate_NAV,predicted_rate_NAV)
except ValueError:
    fpr_nav = 0
    tpr_nav = 0

try: 
    ks_nav = max(tpr_nav - fpr_nav) 
except TypeError: 
    ks_nav = 0
nav_kpi.append(ks_nav)

# %%

table_cols = ['KPI NUMBER','KPI NAME','MODEL','LOADDT','QUARTER','KPI VALUE']

kpi_ref = {model_name[0]: large_corp_kpi, model_name[1] : mid_kpi, model_name[2] : early_kpi, model_name[3] : ccloc_kpi, model_name[4] : nav_kpi, model_name[5] : firm_kpi}

kpi_table = []

for model in model_name: 
   for i in range(4):
      print(kpi_ref[model][i])
      row = [list(kpi_dict1.keys())[i],list(kpi_dict1.values())[i],model,last_month_end1,kpi_quarter,kpi_ref[model][i]]
      kpi_table.append(row)


kpi_table1 = pd.DataFrame(kpi_table, columns = table_cols)
kpi_table1_v2 = kpi_table1.explode('KPI VALUE')

# %% [markdown]
# #### Section 6: Calculation of Thresholds for Accuracy for all Models

# %%
import math

data_list = [default_large_corp, default_mid, default_early_stage, default_CCLOC, default_NAV, default_Firm]

accuracy_threshold = []
perc_threshold_hard1 = []
perc_threshold_soft1 = []

for j in range(6):
    for i in range(1000):
        n_1 = math.ceil(data_list[j].shape[0]*0.8)
        df = data_list[j].sample(n=n_1, replace=True)
        df = df.fillna(0)
        df['default_flag'] = df['default_flag'].astype(int)


        df1 = df.groupby('FINAL_ORR')['CIF'].count() 
        df1 = pd.DataFrame(df1)
        df1 = df1.reset_index()
        df1['FINAL_ORR'] = df1['FINAL_ORR'].astype(int)
        df1 = df1.sort_values(by='FINAL_ORR')


        df2 = df.groupby('FINAL_ORR')['default_flag'].sum()
        df2 = pd.DataFrame(df2)
        df2 = df2.reset_index()
        df2['FINAL_ORR'] = df2['FINAL_ORR'].astype(int)
        df2 = df2.sort_values(by='FINAL_ORR')


        df3 = pd.merge(df2, df1, right_on = 'FINAL_ORR', left_on = 'FINAL_ORR', how = 'inner')
        
        df4 = pd.merge(dummy_df1, df3, on='FINAL_ORR', how = 'left')
        
        df4 = df4.fillna(0)
        df4 = pd.merge(df4,masterscale, on = 'FINAL_ORR', how = 'left')
        df4['Predict_Default'] = df4['CIF']*df4['PD']

        df4['Actual_PD'] = np.where(df4['CIF'] != 0, df4['default_flag'] / df4['CIF'], 0)
        predicted_rate = df4['Predict_Default'].sum()/df4['CIF'].sum()
        actual_rate = df4['default_flag'].sum()/df4['CIF'].sum()
        MAE_df = abs(predicted_rate - actual_rate)
        accuracy_threshold.append(MAE_df)
    
    perc_threshold_hard = np.percentile(accuracy_threshold, 98)
    perc_threshold_soft = np.percentile(accuracy_threshold, 80)
    perc_threshold_hard1.append(perc_threshold_hard)
    perc_threshold_soft1.append(perc_threshold_soft)




# %%
#Exporting thresholds

perc_threshold_soft2 = pd.DataFrame(list(zip(model_name, perc_threshold_soft1)), columns=['Model_Name', 'Soft_Breach'])
perc_threshold_soft2.to_csv('Soft_Breach_Accuracy_Threshold.csv')

perc_threshold_hard2 = pd.DataFrame(list(zip(model_name, perc_threshold_hard1)), columns=['Model_Name', 'Hard_Breach'])
perc_threshold_hard2.to_csv('Hard_Breach_Accuracy_Threshold.csv')

# %%
now = datetime.now()


timestamp_string = now.strftime("_%m_%d_%Y")




table_name = 'all_kpi_' + kpi_quarter + year + '_updated' + timestamp_string + '.csv'

kpi_table1_v2.to_csv(table_name)


