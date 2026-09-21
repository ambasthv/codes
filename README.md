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
print(last_month_end1, month_end_12m_prior, month_end_3m_prior, kpi_quarter)

# %%
#create function for getting the last 12 month end dates

def get_last_45_month_end_dates(last_month_end):
    """
    Generates a list of the last 45 month-end dates.
    """
    
    month_end_dates = []

    # Start from the end of the previous month

    
    

    for _ in range(45):
        month_end_dates.append(last_month_end)
        # Move to the end of the previous month
        last_month_end = last_month_end.replace(day=1) - relativedelta(days=1)
        # Sort to get them in chronological order
        sorted(month_end_dates)
        me_date_string_list = list(map(lambda x: x.strftime("%m/%d/%Y"), month_end_dates))

    return me_date_string_list 




# %% [markdown]
# #### Create a KPI dictionary with the KPIs that are being processed in this segment of the KPI code 

# %% [markdown]
# #### Check the quarter end date and quarter being processed in this run 

# %%
print(last_month_end1, kpi_quarter,month_end_12m_prior)

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
# #### Portfolio Data for ORR for each Month End in 45M Evaluation Period

# %%
last_45_month_ends = get_last_45_month_end_dates(last_month_end)
last_45_month_ends1 = "', '".join(last_45_month_ends)


sql_port_45m = """SET NOCOUNT ON

select  loaddt as MonthEnd, CIF, max(CL_OBLIGOR_RISK_RATING) as orr1 


from [CRDADMPRD].[dbo].[CDM_CREDIT_LINES_VIEW]

where loaddt in ('{last_45_month_ends1}')

group by loaddt, cif










""".format(last_45_month_ends1=last_45_month_ends1)


last_45_ports = pd.DataFrame(pd.read_sql_query(sql_port_45m, conn))

last_45_ports['MonthEnd'] = pd.to_datetime(last_45_ports['MonthEnd']).dt.strftime("%m/%d/%Y")

# %% [markdown]
# #### Section 1: PD Models Override - In this segment data is extracted for overrides per risk template for the evaluation period.  

# %%
# calculating overrides for DRR Large Corp

large_corp_kpi = []
# DRR Large Corp 



sql_override = """

select distinct  a.CIF,  b.DATE_APPROVED,a.CALCULATED_ORR, a.FINAL_ORR, 				
                a.DIFFERENCE_OF_CALC_AND_FINAL_ORR, a.OVERRIDE_REASON, a.risk_grade_template	
				
							
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'Innovation > $75MM & Sponsor – CF', 
    'Innovation > $75MM & Sponsor – ID/BS')	

     	
      		
				
				--and b.DATE_APPROVED > '{month_end_12m_prior}'
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

combined_override_large = pd.merge(override_large_corp_raw, last_45_ports, on=['CIF', 'MonthEnd'], how='left')


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
override_by_drr_large = list(override_by_drr_large['OVERRIDE_INDICATOR'])


num_of_overrides = override_large_corp[override_large_corp.DIFFERENCE_OF_CALC_AND_FINAL_ORR != 0]
total_override = num_of_overrides.shape[0]
print(total_override)

total_override1 = total_override/override_large_corp.shape[0]
try: 
    total_override_mid1 = total_override/override_large_corp.shape[0]
except ZeroDivisionError:
    total_override1 = 0
    


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

     	
      		
				
				--and b.DATE_APPROVED > '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
        
    """.format(month_end_12m_prior = month_end_12m_prior)



override_mid_raw = pd.read_sql_query(sql_override3, conn)
cif_list_mid_kpi = override_mid_raw.CIF.unique()

    


#create  a month end column for the most proximate month end for each date APPROVED

override_mid_raw['DATE_APPROVED'] = pd.to_datetime(override_mid_raw['DATE_APPROVED'])
override_mid_raw['MonthEnd'] = override_mid_raw['DATE_APPROVED'] + pd.offsets.MonthEnd(1)
override_mid_raw['MonthEnd'] = override_mid_raw['MonthEnd'].dt.strftime("%m/%d/%Y")

combined_override_mid = pd.merge(override_mid_raw, last_45_ports, on=['CIF', 'MonthEnd'], how='left')


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
override_by_drr_mid = list(override_by_drr_mid['OVERRIDE_INDICATOR'])
    
num_of_overrides_mid = override_mid[override_mid.DIFFERENCE_OF_CALC_AND_FINAL_ORR != 0]
total_override_mid = num_of_overrides_mid.shape[0]
    
try: 
    total_override_mid1 = total_override_mid/override_mid.shape[0]
except ZeroDivisionError:
    total_override_mid1 = 0
    


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

     	
      		
				
				--and b.DATE_APPROVED > '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
        
    """.format(month_end_12m_prior=month_end_12m_prior)


override_early_stage_raw = pd.read_sql_query(sql_override2, conn)
cif_list_early_kpi = override_early_stage_raw.CIF.unique()

#create  a month end column for the most proximate month end for each date approved

override_early_stage_raw['DATE_APPROVED'] = pd.to_datetime(override_early_stage_raw['DATE_APPROVED'])
override_early_stage_raw['MonthEnd'] = override_early_stage_raw['DATE_APPROVED'] + pd.offsets.MonthEnd(1)
override_early_stage_raw['MonthEnd'] = override_early_stage_raw['MonthEnd'].dt.strftime("%m/%d/%Y")

combined_override_early = pd.merge(override_early_stage_raw, last_45_ports, on=['CIF', 'MonthEnd'], how='left')


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
override_by_drr_early = list(override_by_drr_early['OVERRIDE_INDICATOR'])

num_of_overrides_early_stage = override_early_stage[override_early_stage.DIFFERENCE_OF_CALC_AND_FINAL_ORR != 0]
total_override_early_stage = num_of_overrides_early_stage.shape[0]

try: 
    total_override_early_stage1 = total_override_early_stage/override_early_stage.shape[0]
except ZeroDivisionError: 
    total_override_early_stage1 = 0




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

     	
      		
				
				--and b.DATE_APPROVED > '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
        
""".format(month_end_12m_prior=month_end_12m_prior)

override_Firm_raw = pd.read_sql_query(sql_override4, conn)
cif_list_firm_kpi = override_Firm_raw.CIF.unique()

#create  a month end column for the most proximate month end for each date approved

override_Firm_raw['DATE_APPROVED'] = pd.to_datetime(override_Firm_raw['DATE_APPROVED'])
override_Firm_raw['MonthEnd'] = override_Firm_raw['DATE_APPROVED'] + pd.offsets.MonthEnd(1)
override_Firm_raw['MonthEnd'] = override_Firm_raw['MonthEnd'].dt.strftime("%m/%d/%Y")

combined_override_Firm = pd.merge(override_Firm_raw, last_45_ports, on=['CIF', 'MonthEnd'], how='left')


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
override_by_drr_Firm = list(override_by_drr_Firm['OVERRIDE_INDICATOR'])

num_of_overrides_Firm = override_Firm[override_Firm.DIFFERENCE_OF_CALC_AND_FINAL_ORR != 0]
total_override_Firm = num_of_overrides_Firm.shape[0]


try: 
    total_override_Firm1 = total_override_Firm/override_Firm.shape[0]
except ZeroDivisionError: 
    total_override_Firm1 = 0




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

     	
      		
				
				--and b.DATE_APPROVED > '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
        
""".format(month_end_12m_prior=month_end_12m_prior)

override_CCLOC_raw = pd.read_sql_query(sql_override4, conn)
cif_list_ccloc_kpi = override_CCLOC_raw.CIF.unique()

#create  a month end column for the most proximate month end for each date approved

override_CCLOC_raw['DATE_APPROVED'] = pd.to_datetime(override_CCLOC_raw['DATE_APPROVED'])
override_CCLOC_raw['MonthEnd'] = override_CCLOC_raw['DATE_APPROVED'] + pd.offsets.MonthEnd(1)
override_CCLOC_raw['MonthEnd'] = override_CCLOC_raw['MonthEnd'].dt.strftime("%m/%d/%Y")

combined_override_CCLOC = pd.merge(override_CCLOC_raw, last_45_ports, on=['CIF', 'MonthEnd'], how='left')


#subset the data that doesn't occur in the portfolio (Nan value for ORR) or where the final ORR is 
#not the same as portfolio ORR

override_CCLOC = combined_override_CCLOC[combined_override_CCLOC['orr1'].notna()]
override_CCLOC = override_CCLOC[override_CCLOC.orr1 == override_CCLOC.FINAL_ORR]


override_CCLOC['OVERRIDE_INDICATOR'] = 0
    
override_CCLOC.loc[override_CCLOC['DIFFERENCE_OF_CALC_AND_FINAL_ORR'] != 0, 'OVERRIDE_INDICATOR'] = 1
override_by_drr_CCLOC = override_CCLOC.groupby("FINAL_ORR")["OVERRIDE_INDICATOR"].mean()

override_by_drr_CCLOC = override_by_drr_CCLOC.reset_index()
override_by_drr_CCLOC['FINAL_ORR'] = override_by_drr_CCLOC['FINAL_ORR'].astype(int)
override_by_drr_CCLOC = override_by_drr_CCLOC.sort_values(by='FINAL_ORR')
override_by_drr_CCLOC = list(override_by_drr_CCLOC['OVERRIDE_INDICATOR'])

num_of_overrides_CCLOC = override_CCLOC[override_CCLOC.DIFFERENCE_OF_CALC_AND_FINAL_ORR != 0]
total_override_CCLOC = num_of_overrides_CCLOC.shape[0]


try: 
    total_override_CCLOC1 = total_override_CCLOC/override_CCLOC.shape[0]
except ZeroDivisionError: 
    total_override_CCLOC1 = 0




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

     	
      		
				
				--and b.DATE_APPROVED > '{month_end_12m_prior}'
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				and a.cif is not null
        
""".format(month_end_12m_prior=month_end_12m_prior)



override_NAV_raw = pd.read_sql_query(sql_override5, conn)
cif_list_nav_kpi = override_NAV_raw.CIF.unique()

#create  a month end column for the most proximate month end for each date approved

override_NAV_raw['DATE_APPROVED'] = pd.to_datetime(override_NAV_raw['DATE_APPROVED'])
override_NAV_raw['MonthEnd'] = override_NAV_raw['DATE_APPROVED'] + pd.offsets.MonthEnd(1)
override_NAV_raw['MonthEnd'] = override_NAV_raw['MonthEnd'].dt.strftime("%m/%d/%Y")

combined_override_NAV = pd.merge(override_NAV_raw, last_45_ports, on=['CIF', 'MonthEnd'], how='left')


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
override_by_drr_NAV = list(override_by_drr_NAV['OVERRIDE_INDICATOR'])

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



# %% [markdown]
# #### Section 2: PD Models Accuracy 

# %%
masterscale = pd.read_csv('masterscale.csv')

# %%
masterscale1 = masterscale.rename(columns={'FINAL_ORR': 'CALCULATED_ORR'})

# %%
CALCULATED_ORR = list(range(18))
CALCULATED_ORR.pop(0)
Predict_Default = [0]*17
dummy_df = list(zip(CALCULATED_ORR, Predict_Default))
dummy_df2 = pd.DataFrame(dummy_df, columns=['CALCULATED_ORR', 'Predict_Default'])


# %%
FINAL_ORR = list(range(18))
FINAL_ORR.pop(0)
Predict_Default = [0]*17
dummy_df = list(zip(FINAL_ORR, Predict_Default))
dummy_df1 = pd.DataFrame(dummy_df, columns=['FINAL_ORR', 'Predict_Default'])

# %%
# DRR Large Corp Default Pull

sql_default1 = """SET NOCOUNT ON
    
    select distinct  a.CIF,  b.DATE_APPROVED,a.CALCULATED_ORR, a.FINAL_ORR, a.OVERRIDE_REASON, 				
                a.DIFFERENCE_OF_CALC_AND_FINAL_ORR, a.risk_grade_template	
				
				into #temp1 			
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'Innovation > $75MM & Sponsor – CF', 'Innovation > $75MM & Sponsor – ID/BS')				
				
				--and b.DATE_APPROVED > '{month_end_12m_prior}'
				
				and a.cif is not null
                
				and b.CREDIT_REQ_STATUS = 'Booked'
				
				
                
                
    SELECT distinct g.*, h.load_date, h.default_flag
 
            FROM #temp1 g 

           left join 

            (select cif, default_flag, max(loaddt) as load_date from [CRDADMPRD].[dbo].[CDM_CLIENT_DEFAULT_STATUS_VW]
            group by cif, default_flag) h

            on g.cif = h.cif

    drop table #temp1, #temp2
			
    """.format(month_end_12m_prior=month_end_12m_prior)

default_large_corp_raw = pd.DataFrame(pd.read_sql_query(sql_default1, conn))
default_large_corp_raw = default_large_corp_raw.drop_duplicates()


# %%
# DRR Large Corp 

default_large_corp = default_large_corp_raw.fillna(0)
default_large_corp['default_flag'] = default_large_corp['default_flag'].astype(int)


large_corp_total = default_large_corp.groupby('FINAL_ORR')['CIF'].count() 
large_corp_total = pd.DataFrame(large_corp_total)
large_corp_total = large_corp_total.reset_index()
large_corp_total['FINAL_ORR'] = large_corp_total['FINAL_ORR'].astype(int)
large_corp_total = large_corp_total.sort_values(by='FINAL_ORR')


large_corp_default = default_large_corp.groupby('FINAL_ORR')['default_flag'].sum()
large_corp_default = pd.DataFrame(large_corp_default)
large_corp_default = large_corp_default.reset_index()
large_corp_default['FINAL_ORR'] = large_corp_default['FINAL_ORR'].astype(int)
large_corp_default = large_corp_default.sort_values(by='FINAL_ORR')

large_corp_acc = pd.merge(large_corp_total, large_corp_default, right_on = 'FINAL_ORR', left_on = 'FINAL_ORR', how = 'inner')

large_corp_acc_v2 = pd.merge(dummy_df1, large_corp_acc, on='FINAL_ORR', how = 'left')
large_corp_acc_v2 = large_corp_acc_v2.fillna(0)
large_corp_acc_v2 = pd.merge(large_corp_acc_v2,masterscale, on = 'FINAL_ORR', how = 'left')
large_corp_acc_v2['Predict_Default'] = large_corp_acc_v2['CIF']*large_corp_acc_v2['PD']

large_corp_acc_v2['Actual_PD_Post'] = np.where(large_corp_acc_v2['CIF'] != 0, large_corp_acc_v2['default_flag'] / large_corp_acc_v2['CIF'], 0)
predicted_rate_large2 = large_corp_acc_v2['Predict_Default'].sum()/large_corp_acc_v2['CIF'].sum()
actual_rate_large2 = large_corp_acc_v2['default_flag'].sum()/large_corp_acc_v2['CIF'].sum()
MAE_large = abs(predicted_rate_large2 - actual_rate_large2)

large_corp_kpi.append(MAE_large)

# %%
#Large Corp Defaults Pre Override

default_large_corp_pre = default_large_corp_raw.fillna(0)
default_large_corp_pre['default_flag'] = default_large_corp_pre['default_flag'].astype(int)


large_corp_total_pre = default_large_corp_pre.groupby('CALCULATED_ORR')['CIF'].count() 
large_corp_total_pre = pd.DataFrame(large_corp_total_pre)
large_corp_total_pre = large_corp_total_pre.reset_index()
large_corp_total_pre['CALCULATED_ORR'] = large_corp_total_pre['CALCULATED_ORR'].astype(int)
large_corp_total_pre = large_corp_total_pre.sort_values(by='CALCULATED_ORR')


large_corp_default_pre = default_large_corp_pre.groupby('CALCULATED_ORR')['default_flag'].sum()
large_corp_default_pre = pd.DataFrame(large_corp_default_pre)
large_corp_default_pre = large_corp_default_pre.reset_index()
large_corp_default_pre['CALCULATED_ORR'] = large_corp_default_pre['CALCULATED_ORR'].astype(int)
large_corp_default_pre = large_corp_default_pre.sort_values(by='CALCULATED_ORR')

large_corp_acc_pre = pd.merge(large_corp_total_pre, large_corp_default_pre, right_on = 'CALCULATED_ORR', left_on = 'CALCULATED_ORR', how = 'inner')

large_corp_acc_v2_pre = pd.merge(dummy_df2, large_corp_acc_pre, on='CALCULATED_ORR', how = 'left')
large_corp_acc_v2_pre = large_corp_acc_v2_pre.fillna(0)
large_corp_acc_v2_pre = pd.merge(large_corp_acc_v2_pre,masterscale1, on = 'CALCULATED_ORR', how = 'left')
large_corp_acc_v2_pre['Predict_Default'] = large_corp_acc_v2_pre['CIF']*large_corp_acc_v2_pre['PD']

large_corp_acc_v2_pre['Actual_PD_Pre'] = np.where(large_corp_acc_v2_pre['CIF'] != 0, large_corp_acc_v2_pre['default_flag'] / large_corp_acc_v2_pre['CIF'], 0)
predicted_rate_large2_pre = large_corp_acc_v2_pre['Predict_Default'].sum()/large_corp_acc_v2_pre['CIF'].sum()
actual_rate_large2_pre = large_corp_acc_v2_pre['default_flag'].sum()/large_corp_acc_v2_pre['CIF'].sum()
MAE_large_pre = abs(predicted_rate_large2_pre - actual_rate_large2_pre)



# %%
# DRR Mid Size Default Pull

sql_default2 = """SET NOCOUNT ON
             
               
			   
	select distinct  a.CIF, b.DATE_APPROVED,a.CALCULATED_ORR, a.FINAL_ORR, a.OVERRIDE_REASON,				
    a.DIFFERENCE_OF_CALC_AND_FINAL_ORR, a.risk_grade_template	
				
	into #temp4			
                				
    from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
	[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
	a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'Innovation > $15MM up to $75MM')				
				
	--and b.DATE_APPROVED > '{month_end_12m_prior}'
				
	and a.cif is not null
    and b.CREDIT_REQ_STATUS = 'Booked'


    select #temp4.*

    into #temp5 
    from  (
        SELECT MAX(DATE_APPROVED) as Date_CIF, CIF, FINAL_ORR 
        FROM #temp4
        GROUP BY CIF, FINAL_ORR
    ) max_date_per_cif 

    inner join #temp4 

    on max_date_per_cif.Date_CIF = #temp4.date_approved

    and max_date_per_cif.cif = #temp4.cif


    


    

    SELECT distinct g.*, h.load_date, h.default_flag
 
            FROM #temp5 g 

           left join 

            (select cif, default_flag, max(loaddt) as load_date from [CRDADMPRD].[dbo].[CDM_CLIENT_DEFAULT_STATUS_VW]
            group by cif, default_flag) h

            on g.cif = h.cif

    drop table #temp4, #temp5
			
    """.format(month_end_12m_prior = month_end_12m_prior)



default_mid = pd.read_sql_query(sql_default2, conn)
default_mid = default_mid.drop_duplicates()


# %%
# DRR Mid Size 

default_mid = default_mid.fillna(0)
default_mid['default_flag'] = default_mid['default_flag'].astype(int)


mid_total = default_mid.groupby('FINAL_ORR')['CIF'].count() 
mid_total = pd.DataFrame(mid_total)
mid_total = mid_total.reset_index()
mid_total['FINAL_ORR'] = mid_total['FINAL_ORR'].astype(int)
mid_total = mid_total.sort_values(by='FINAL_ORR')


mid_default = default_mid.groupby('FINAL_ORR')['default_flag'].sum()
mid_default = pd.DataFrame(mid_default)
mid_default = mid_default.reset_index()
mid_default['FINAL_ORR'] = mid_default['FINAL_ORR'].astype(int)
mid_default = mid_default.sort_values(by='FINAL_ORR')

mid_acc = pd.merge(mid_total, mid_default, right_on = 'FINAL_ORR', left_on = 'FINAL_ORR', how = 'inner')

mid_acc_v2 = pd.merge(dummy_df1, mid_acc, on='FINAL_ORR', how = 'left')
mid_acc_v2 = mid_acc_v2.fillna(0)
mid_acc_v2 = pd.merge(mid_acc_v2,masterscale, on = 'FINAL_ORR', how = 'left')
mid_acc_v2['Predict_Default'] = mid_acc_v2['CIF']*mid_acc_v2['PD']

mid_acc_v2['Actual_PD_Post'] = np.where(mid_acc_v2['CIF'] != 0, mid_acc_v2['default_flag'] / mid_acc_v2['CIF'], 0)
predicted_rate_mid2 = mid_acc_v2['Predict_Default'].sum()/mid_acc_v2['CIF'].sum()
actual_rate_mid2 = mid_acc_v2['default_flag'].sum()/mid_acc_v2['CIF'].sum()
MAE_mid = abs(predicted_rate_mid2 - actual_rate_mid2)

mid_kpi.append(MAE_mid)


# %%
#Mid Size Defaults Pre Override

default_mid_pre = default_mid.fillna(0)
default_mid_pre['default_flag'] = default_mid_pre['default_flag'].astype(int)


mid_total_pre = default_mid_pre.groupby('CALCULATED_ORR')['CIF'].count() 
mid_total_pre = pd.DataFrame(mid_total_pre)
mid_total_pre = mid_total_pre.reset_index()
mid_total_pre['CALCULATED_ORR'] = mid_total_pre['CALCULATED_ORR'].astype(int)
mid_total_pre = mid_total_pre.sort_values(by='CALCULATED_ORR')


mid_default_pre = default_mid_pre.groupby('CALCULATED_ORR')['default_flag'].sum()
mid_default_pre = pd.DataFrame(mid_default_pre)
mid_default_pre = mid_default_pre.reset_index()
mid_default_pre['CALCULATED_ORR'] = mid_default_pre['CALCULATED_ORR'].astype(int)
mid_default_pre = mid_default_pre.sort_values(by='CALCULATED_ORR')

mid_acc_pre = pd.merge(mid_total_pre, mid_default_pre, right_on = 'CALCULATED_ORR', left_on = 'CALCULATED_ORR', how = 'inner')

mid_acc_v2_pre = pd.merge(dummy_df2, mid_acc_pre, on='CALCULATED_ORR', how = 'left')
mid_acc_v2_pre = mid_acc_v2_pre.fillna(0)
mid_acc_v2_pre = pd.merge(mid_acc_v2_pre,masterscale1, on = 'CALCULATED_ORR', how = 'left')
mid_acc_v2_pre['Predict_Default'] = mid_acc_v2_pre['CIF']*mid_acc_v2_pre['PD']

mid_acc_v2_pre['Actual_PD_Pre'] = np.where(mid_acc_v2_pre['CIF'] != 0, mid_acc_v2_pre['default_flag'] / mid_acc_v2_pre['CIF'], 0)
predicted_rate_mid_pre = mid_acc_v2_pre['Predict_Default'].sum()/mid_acc_v2_pre['CIF'].sum()
actual_rate_mid_pre = mid_acc_v2_pre['default_flag'].sum()/mid_acc_v2_pre['CIF'].sum()
MAE_large_pre = abs(predicted_rate_mid_pre - actual_rate_mid_pre)


# %%
# DRR Firm Default Pull

sql_default2 = """SET NOCOUNT ON
             
               
			   
	select distinct  a.CIF, b.DATE_APPROVED,a.CALCULATED_ORR, a.FINAL_ORR, a.OVERRIDE_REASON,				
    a.DIFFERENCE_OF_CALC_AND_FINAL_ORR, a.risk_grade_template	
				
	into #temp4			
                				
    from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
	[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
	a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'GFB Firm')				
				
	--and b.DATE_APPROVED > '{month_end_12m_prior}'
				
	and a.cif is not null
    and b.CREDIT_REQ_STATUS = 'Booked'


    select #temp4.*

    into #temp5 
    from  (
        SELECT MAX(DATE_APPROVED) as Date_CIF, CIF, FINAL_ORR 
        FROM #temp4
        GROUP BY CIF, FINAL_ORR
    ) max_date_per_cif 

    inner join #temp4 

    on max_date_per_cif.Date_CIF = #temp4.date_approved

    and max_date_per_cif.cif = #temp4.cif


    


    

    SELECT distinct g.*, h.load_date, h.default_flag
 
            FROM #temp5 g 

           left join 

            (select cif, default_flag, max(loaddt) as load_date from [CRDADMPRD].[dbo].[CDM_CLIENT_DEFAULT_STATUS_VW]
            group by cif, default_flag) h

            on g.cif = h.cif

    drop table #temp4, #temp5
			
    """.format(month_end_12m_prior = month_end_12m_prior)



default_Firm = pd.read_sql_query(sql_default2, conn)
default_Firm = default_Firm.drop_duplicates()


# %%
# DRR Firm

default_Firm = default_Firm.fillna(0)
default_Firm['default_flag'] = default_Firm['default_flag'].astype(int)


Firm_total = default_Firm.groupby('FINAL_ORR')['CIF'].count() 
Firm_total = pd.DataFrame(Firm_total)
Firm_total = Firm_total.reset_index()
Firm_total['FINAL_ORR'] = Firm_total['FINAL_ORR'].astype(int)
Firm_total = Firm_total.sort_values(by='FINAL_ORR')


Firm_default = default_Firm.groupby('FINAL_ORR')['default_flag'].sum()
Firm_default = pd.DataFrame(Firm_default)
Firm_default = Firm_default.reset_index()
Firm_default['FINAL_ORR'] = Firm_default['FINAL_ORR'].astype(int)
Firm_default = Firm_default.sort_values(by='FINAL_ORR')

Firm_acc = pd.merge(Firm_total, Firm_default, right_on = 'FINAL_ORR', left_on = 'FINAL_ORR', how = 'inner')

Firm_acc_v2 = pd.merge(dummy_df1, Firm_acc, on='FINAL_ORR', how = 'left')
Firm_acc_v2 = Firm_acc_v2.fillna(0)
Firm_acc_v2 = pd.merge(Firm_acc_v2,masterscale, on = 'FINAL_ORR', how = 'left')
Firm_acc_v2['Predict_Default'] = Firm_acc_v2['CIF']*Firm_acc_v2['PD']

Firm_acc_v2['Actual_PD_Post'] = np.where(Firm_acc_v2['CIF'] != 0, Firm_acc_v2['default_flag'] / Firm_acc_v2['CIF'], 0)
predicted_rate_Firm2 = Firm_acc_v2['Predict_Default'].sum()/Firm_acc_v2['CIF'].sum()
actual_rate_Firm2 = Firm_acc_v2['default_flag'].sum()/Firm_acc_v2['CIF'].sum()
MAE_Firm = abs(predicted_rate_Firm2 - actual_rate_Firm2)

firm_kpi.append(MAE_Firm)


# %%
#Firm Defaults Pre Override

default_Firm_pre = default_Firm.fillna(0)
default_Firm_pre['default_flag'] = default_Firm_pre['default_flag'].astype(int)


Firm_total_pre = default_Firm_pre.groupby('CALCULATED_ORR')['CIF'].count() 
Firm_total_pre = pd.DataFrame(Firm_total_pre)
Firm_total_pre = Firm_total_pre.reset_index()
Firm_total_pre['CALCULATED_ORR'] = Firm_total_pre['CALCULATED_ORR'].astype(int)
Firm_total_pre = Firm_total_pre.sort_values(by='CALCULATED_ORR')


Firm_default_pre = default_Firm_pre.groupby('CALCULATED_ORR')['default_flag'].sum()
Firm_default_pre = pd.DataFrame(Firm_default_pre)
Firm_default_pre = Firm_default_pre.reset_index()
Firm_default_pre['CALCULATED_ORR'] = Firm_default_pre['CALCULATED_ORR'].astype(int)
Firm_default_pre = Firm_default_pre.sort_values(by='CALCULATED_ORR')

Firm_acc_pre = pd.merge(Firm_total_pre, Firm_default_pre, right_on = 'CALCULATED_ORR', left_on = 'CALCULATED_ORR', how = 'inner')

Firm_acc_v2_pre = pd.merge(dummy_df2, Firm_acc_pre, on='CALCULATED_ORR', how = 'left')
Firm_acc_v2_pre = Firm_acc_v2_pre.fillna(0)
Firm_acc_v2_pre = pd.merge(Firm_acc_v2_pre,masterscale1, on = 'CALCULATED_ORR', how = 'left')
Firm_acc_v2_pre['Predict_Default'] = Firm_acc_v2_pre['CIF']*Firm_acc_v2_pre['PD']

Firm_acc_v2_pre['Actual_PD_Pre'] = np.where(Firm_acc_v2_pre['CIF'] != 0, Firm_acc_v2_pre['default_flag'] / Firm_acc_v2_pre['CIF'], 0)
predicted_rate_Firm_pre = Firm_acc_v2_pre['Predict_Default'].sum()/Firm_acc_v2_pre['CIF'].sum()
actual_rate_Firm_pre = Firm_acc_v2_pre['default_flag'].sum()/Firm_acc_v2_pre['CIF'].sum()
MAE_Firm_pre = abs(predicted_rate_Firm_pre - actual_rate_Firm_pre)


# %%
# DRR CCLOC Default Pull

sql_default3 = """SET NOCOUNT ON
             
               
			   
			   select distinct  a.CIF, b.DATE_APPROVED,a.CALCULATED_ORR, a.FINAL_ORR, a.OVERRIDE_REASON, 				
                a.DIFFERENCE_OF_CALC_AND_FINAL_ORR,a.OVERRIDE_COMMENTS, a.risk_grade_template	
				
				into #temp7 			
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'CCLOC')	

    --and b.DATE_APPROVED > '{month_end_12m_prior}'			
				
				
				
				and a.cif is not null
                and b.CREDIT_REQ_STATUS = 'Booked'


select #temp7.*

into #temp8
from  (
    SELECT MAX(DATE_APPROVED) as Date_CIF, CIF, FINAL_ORR 
    FROM #temp7
    GROUP BY CIF, FINAL_ORR
) max_date_per_cif 

inner join #temp7 

on max_date_per_cif.Date_CIF = #temp7.date_approved

and max_date_per_cif.cif = #temp7.cif





SELECT distinct g.*, h.load_date, h.default_flag
 
            FROM #temp8 g 

           left join 

            (select cif, default_flag, max(loaddt) as load_date from [CRDADMPRD].[dbo].[CDM_CLIENT_DEFAULT_STATUS_VW]
            group by cif, default_flag) h

            on g.cif = h.cif

drop table #temp7, #temp8
			
""".format(month_end_12m_prior=month_end_12m_prior)

default_CCLOC = pd.read_sql_query(sql_default3, conn)
default_CCLOC = default_CCLOC.drop_duplicates()



# %%
# DRR CCLOC

default_CCLOC = default_CCLOC.fillna(0)
default_CCLOC['default_flag'] = default_CCLOC['default_flag'].astype(int)


CCLOC_total = default_CCLOC.groupby('FINAL_ORR')['CIF'].count() 
CCLOC_total = pd.DataFrame(CCLOC_total)
CCLOC_total = CCLOC_total.reset_index()
CCLOC_total['FINAL_ORR'] = CCLOC_total['FINAL_ORR'].astype(int)
CCLOC_total = CCLOC_total.sort_values(by='FINAL_ORR')


CCLOC_default = default_CCLOC.groupby('FINAL_ORR')['default_flag'].sum()
CCLOC_default = pd.DataFrame(CCLOC_default)
CCLOC_default = CCLOC_default.reset_index()
CCLOC_default['FINAL_ORR'] = CCLOC_default['FINAL_ORR'].astype(int)
CCLOC_default = CCLOC_default.sort_values(by='FINAL_ORR')

CCLOC_acc = pd.merge(CCLOC_total, CCLOC_default, right_on = 'FINAL_ORR', left_on = 'FINAL_ORR', how = 'inner')

CCLOC_acc_v2 = pd.merge(dummy_df1, CCLOC_acc, on='FINAL_ORR', how = 'left')
CCLOC_acc_v2 = CCLOC_acc_v2.fillna(0)
CCLOC_acc_v2 = pd.merge(CCLOC_acc_v2,masterscale, on = 'FINAL_ORR', how = 'left')
CCLOC_acc_v2['Predict_Default'] = CCLOC_acc_v2['CIF']*CCLOC_acc_v2['PD']

CCLOC_acc_v2['Actual_PD_Post'] = np.where(CCLOC_acc_v2['CIF'] != 0, CCLOC_acc_v2['default_flag'] / CCLOC_acc_v2['CIF'], 0)
predicted_rate_CCLOC2 = CCLOC_acc_v2['Predict_Default'].sum()/CCLOC_acc_v2['CIF'].sum()
actual_rate_CCLOC2 = CCLOC_acc_v2['default_flag'].sum()/CCLOC_acc_v2['CIF'].sum()
MAE_CCLOC = abs(predicted_rate_CCLOC2 - actual_rate_CCLOC2)

ccloc_kpi.append(MAE_CCLOC)

# %%
#CCLOC Defaults Pre Override

default_CCLOC_pre = default_CCLOC.fillna(0)
default_CCLOC_pre['default_flag'] = default_CCLOC_pre['default_flag'].astype(int)


CCLOC_total_pre = default_CCLOC_pre.groupby('CALCULATED_ORR')['CIF'].count() 
CCLOC_total_pre = pd.DataFrame(CCLOC_total_pre)
CCLOC_total_pre = CCLOC_total_pre.reset_index()
CCLOC_total_pre['CALCULATED_ORR'] = CCLOC_total_pre['CALCULATED_ORR'].astype(int)
CCLOC_total_pre = CCLOC_total_pre.sort_values(by='CALCULATED_ORR')


CCLOC_default_pre = default_CCLOC_pre.groupby('CALCULATED_ORR')['default_flag'].sum()
CCLOC_default_pre = pd.DataFrame(CCLOC_default_pre)
CCLOC_default_pre = CCLOC_default_pre.reset_index()
CCLOC_default_pre['CALCULATED_ORR'] = CCLOC_default_pre['CALCULATED_ORR'].astype(int)
CCLOC_default_pre = CCLOC_default_pre.sort_values(by='CALCULATED_ORR')

CCLOC_acc_pre = pd.merge(CCLOC_total_pre, CCLOC_default_pre, right_on = 'CALCULATED_ORR', left_on = 'CALCULATED_ORR', how = 'inner')

CCLOC_acc_v2_pre = pd.merge(dummy_df2, CCLOC_acc_pre, on='CALCULATED_ORR', how = 'left')
CCLOC_acc_v2_pre = CCLOC_acc_v2_pre.fillna(0)
CCLOC_acc_v2_pre = pd.merge(CCLOC_acc_v2_pre,masterscale1, on = 'CALCULATED_ORR', how = 'left')
CCLOC_acc_v2_pre['Predict_Default'] = CCLOC_acc_v2_pre['CIF']*CCLOC_acc_v2_pre['PD']

CCLOC_acc_v2_pre['Actual_PD_Pre'] = np.where(CCLOC_acc_v2_pre['CIF'] != 0, CCLOC_acc_v2_pre['default_flag'] / CCLOC_acc_v2_pre['CIF'], 0)
predicted_rate_CCLOC_pre = CCLOC_acc_v2_pre['Predict_Default'].sum()/CCLOC_acc_v2_pre['CIF'].sum()
actual_rate_CCLOC_pre = CCLOC_acc_v2_pre['default_flag'].sum()/CCLOC_acc_v2_pre['CIF'].sum()
MAE_large_pre = abs(predicted_rate_CCLOC_pre - actual_rate_CCLOC_pre)


# %%
# DRR Early Stage Default Pull

sql_default4 = """SET NOCOUNT ON
    select distinct  a.CIF, b.DATE_APPROVED,a.CALCULATED_ORR, a.FINAL_ORR, a.OVERRIDE_REASON, 				
    a.DIFFERENCE_OF_CALC_AND_FINAL_ORR, a.risk_grade_template	
				
	into #temp1 			
                				
    from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
    [CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
	a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'Innovation up to $15MM')				
				
	--and b.DATE_APPROVED > '{month_end_12m_prior}'
				
	and a.cif is not null
    and b.CREDIT_REQ_STATUS = 'Booked'


    select #temp1.*

    into #temp2 
    from  (
        SELECT MAX(DATE_APPROVED) as Date_CIF, CIF, FINAL_ORR 
        FROM #temp1
        GROUP BY CIF, FINAL_ORR
    ) max_date_per_cif 

    inner join #temp1 

    on max_date_per_cif.Date_CIF = #temp1.date_approved

    and max_date_per_cif.cif = #temp1.cif

   

    SELECT distinct g.*, h.load_date, h.default_flag
 
            FROM #temp2 g 

           left join 

            (select cif, default_flag, max(loaddt) as load_date from [CRDADMPRD].[dbo].[CDM_CLIENT_DEFAULT_STATUS_VW]
            group by cif, default_flag) h

            on g.cif = h.cif

    drop table #temp1, #temp2
			
    """.format(month_end_12m_prior=month_end_12m_prior)

default_early_stage = pd.read_sql_query(sql_default4, conn)
default_early_stage = default_early_stage.drop_duplicates()


# %%
# DRR Early Stage

default_early_stage = default_early_stage.fillna(0)
default_early_stage['default_flag'] = default_early_stage['default_flag'].astype(int)


early_stage_total = default_early_stage.groupby('FINAL_ORR')['CIF'].count() 
early_stage_total = pd.DataFrame(early_stage_total)
early_stage_total = early_stage_total.reset_index()
early_stage_total['FINAL_ORR'] = early_stage_total['FINAL_ORR'].astype(int)
early_stage_total = early_stage_total.sort_values(by='FINAL_ORR')


early_stage_default = default_early_stage.groupby('FINAL_ORR')['default_flag'].sum()
early_stage_default = pd.DataFrame(early_stage_default)
early_stage_default = early_stage_default.reset_index()
early_stage_default['FINAL_ORR'] = early_stage_default['FINAL_ORR'].astype(int)
early_stage_default = early_stage_default.sort_values(by='FINAL_ORR')

early_stage_acc = pd.merge(early_stage_total, early_stage_default, right_on = 'FINAL_ORR', left_on = 'FINAL_ORR', how = 'inner')

early_stage_acc_v2 = pd.merge(dummy_df1, early_stage_acc, on='FINAL_ORR', how = 'left')
early_stage_acc_v2 = early_stage_acc_v2.fillna(0)
early_stage_acc_v2 = pd.merge(early_stage_acc_v2,masterscale, on = 'FINAL_ORR', how = 'left')
early_stage_acc_v2['Predict_Default'] = early_stage_acc_v2['CIF']*early_stage_acc_v2['PD']

early_stage_acc_v2['Actual_PD_Post'] = np.where(early_stage_acc_v2['CIF'] != 0, early_stage_acc_v2['default_flag'] / early_stage_acc_v2['CIF'], 0)
predicted_rate_early2 = early_stage_acc_v2['Predict_Default'].sum()/early_stage_acc_v2['CIF'].sum()
actual_rate_early2 = early_stage_acc_v2['default_flag'].sum()/early_stage_acc_v2['CIF'].sum()
MAE_early = abs(predicted_rate_early2 - actual_rate_early2)
early_kpi.append(MAE_early)


# %%
#Early Defaults Pre Override

default_early_pre = default_early_stage.fillna(0)
default_early_pre['default_flag'] = default_early_pre['default_flag'].astype(int)


early_total_pre = default_early_pre.groupby('CALCULATED_ORR')['CIF'].count() 
early_total_pre = pd.DataFrame(early_total_pre)
early_total_pre = early_total_pre.reset_index()
early_total_pre['CALCULATED_ORR'] = early_total_pre['CALCULATED_ORR'].astype(int)
early_total_pre = early_total_pre.sort_values(by='CALCULATED_ORR')


early_default_pre = default_early_pre.groupby('CALCULATED_ORR')['default_flag'].sum()
early_default_pre = pd.DataFrame(early_default_pre)
early_default_pre = early_default_pre.reset_index()
early_default_pre['CALCULATED_ORR'] = early_default_pre['CALCULATED_ORR'].astype(int)
early_default_pre = early_default_pre.sort_values(by='CALCULATED_ORR')

early_acc_pre = pd.merge(early_total_pre, early_default_pre, right_on = 'CALCULATED_ORR', left_on = 'CALCULATED_ORR', how = 'inner')

early_acc_v2_pre = pd.merge(dummy_df2, early_acc_pre, on='CALCULATED_ORR', how = 'left')
early_acc_v2_pre = early_acc_v2_pre.fillna(0)
early_acc_v2_pre = pd.merge(early_acc_v2_pre,masterscale1, on = 'CALCULATED_ORR', how = 'left')
early_acc_v2_pre['Predict_Default'] = early_acc_v2_pre['CIF']*early_acc_v2_pre['PD']

early_acc_v2_pre['Actual_PD_Pre'] = np.where(early_acc_v2_pre['CIF'] != 0, early_acc_v2_pre['default_flag'] / early_acc_v2_pre['CIF'], 0)
predicted_rate_early_pre = early_acc_v2_pre['Predict_Default'].sum()/early_acc_v2_pre['CIF'].sum()
actual_rate_early_pre = early_acc_v2_pre['default_flag'].sum()/early_acc_v2_pre['CIF'].sum()
MAE_large_pre = abs(predicted_rate_early_pre - actual_rate_early_pre)


# %%
# DRR NAV Default Pull

sql_default5 = """ SET NOCOUNT ON
             
               
			   
			   select distinct  a.CIF, b.DATE_APPROVED,a.CALCULATED_ORR, a.FINAL_ORR, a.OVERRIDE_REASON, 				
                a.DIFFERENCE_OF_CALC_AND_FINAL_ORR,a.OVERRIDE_COMMENTS, a.risk_grade_template	
				
				into #temp10			
                				
                from [CRDADMPRD].[dbo].[CDM_LOS_FACILITY_ENTITY_INVOLVEMENT_VW] a join  				
				[CRDADMPRD].[dbo].[CDM_LOS_CREDIT_REQUEST_ATTRIBUTES_VW] b on 
				a.credit_req_nbr = b.CREDIT_REQ_NBR
				
    and a.risk_grade_template in ( 'NAV')				
				
				--and b.DATE_APPROVED > '{month_end_12m_prior}'
				
				and a.cif is not null
                and b.CREDIT_REQ_STATUS = 'Booked'


select #temp10.*

into #temp11 
from  (
    SELECT MAX(DATE_APPROVED) as Date_CIF, CIF, FINAL_ORR 
    FROM #temp10
    GROUP BY CIF, FINAL_ORR
) max_date_per_cif 

inner join #temp10

on max_date_per_cif.Date_CIF = #temp10.date_approved

and max_date_per_cif.cif = #temp10.cif








SELECT distinct g.*, h.load_date, h.default_flag
 
            FROM #temp11 g 

           left join 

            (select cif, default_flag, max(loaddt) as load_date from [CRDADMPRD].[dbo].[CDM_CLIENT_DEFAULT_STATUS_VW]
            group by cif, default_flag) h

            on g.cif = h.cif

Drop table #temp10, #temp11
			
""".format(month_end_12m_prior=month_end_12m_prior)



default_NAV = pd.read_sql_query(sql_default5, conn)
default_NAV = default_NAV.drop_duplicates()

# %%
# DRR NAV

default_NAV = default_NAV.fillna(0)
default_NAV['default_flag'] = default_NAV['default_flag'].astype(int)


NAV_total = default_NAV.groupby('FINAL_ORR')['CIF'].count() 
NAV_total = pd.DataFrame(NAV_total)
NAV_total = NAV_total.reset_index()
NAV_total['FINAL_ORR'] = NAV_total['FINAL_ORR'].astype(int)
NAV_total = NAV_total.sort_values(by='FINAL_ORR')


NAV_default = default_NAV.groupby('FINAL_ORR')['default_flag'].sum()
NAV_default = pd.DataFrame(NAV_default)
NAV_default = NAV_default.reset_index()
NAV_default['FINAL_ORR'] = NAV_default['FINAL_ORR'].astype(int)
NAV_default = NAV_default.sort_values(by='FINAL_ORR')

NAV_acc = pd.merge(NAV_total, NAV_default, right_on = 'FINAL_ORR', left_on = 'FINAL_ORR', how = 'inner')

NAV_acc_v2 = pd.merge(dummy_df1, NAV_acc, on='FINAL_ORR', how = 'left')
NAV_acc_v2 = NAV_acc_v2.fillna(0)
NAV_acc_v2 = pd.merge(NAV_acc_v2,masterscale, on = 'FINAL_ORR', how = 'left')
NAV_acc_v2['Predict_Default'] = NAV_acc_v2['CIF']*NAV_acc_v2['PD']

NAV_acc_v2['Actual_PD_Post'] = np.where(NAV_acc_v2['CIF'] != 0, NAV_acc_v2['default_flag'] / NAV_acc_v2['CIF'], 0)
predicted_rate_NAV2 = NAV_acc_v2['Predict_Default'].sum()/NAV_acc_v2['CIF'].sum()
actual_rate_NAV2 = NAV_acc_v2['default_flag'].sum()/NAV_acc_v2['CIF'].sum()
MAE_NAV = abs(predicted_rate_NAV2 - actual_rate_NAV2)

nav_kpi.append(MAE_NAV)

# %%
#NAV Defaults Pre Override

default_NAV_pre = default_NAV.fillna(0)
default_NAV_pre['default_flag'] = default_NAV_pre['default_flag'].astype(int)


NAV_total_pre = default_NAV_pre.groupby('CALCULATED_ORR')['CIF'].count() 
NAV_total_pre = pd.DataFrame(NAV_total_pre)
NAV_total_pre = NAV_total_pre.reset_index()
NAV_total_pre['CALCULATED_ORR'] = NAV_total_pre['CALCULATED_ORR'].astype(int)
NAV_total_pre = NAV_total_pre.sort_values(by='CALCULATED_ORR')


NAV_default_pre = default_NAV_pre.groupby('CALCULATED_ORR')['default_flag'].sum()
NAV_default_pre = pd.DataFrame(NAV_default_pre)
NAV_default_pre = NAV_default_pre.reset_index()
NAV_default_pre['CALCULATED_ORR'] = NAV_default_pre['CALCULATED_ORR'].astype(int)
NAV_default_pre = NAV_default_pre.sort_values(by='CALCULATED_ORR')

NAV_acc_pre = pd.merge(NAV_total_pre, NAV_default_pre, right_on = 'CALCULATED_ORR', left_on = 'CALCULATED_ORR', how = 'inner')

NAV_acc_v2_pre = pd.merge(dummy_df2, NAV_acc_pre, on='CALCULATED_ORR', how = 'left')
NAV_acc_v2_pre = NAV_acc_v2_pre.fillna(0)
NAV_acc_v2_pre = pd.merge(NAV_acc_v2_pre,masterscale1, on = 'CALCULATED_ORR', how = 'left')
NAV_acc_v2_pre['Predict_Default'] = NAV_acc_v2_pre['CIF']*NAV_acc_v2_pre['PD']

NAV_acc_v2_pre['Actual_PD_Pre'] = np.where(NAV_acc_v2_pre['CIF'] != 0, NAV_acc_v2_pre['default_flag'] / NAV_acc_v2_pre['CIF'], 0)
predicted_rate_NAV_pre = NAV_acc_v2_pre['Predict_Default'].sum()/NAV_acc_v2_pre['CIF'].sum()
actual_rate_NAV_pre = NAV_acc_v2_pre['default_flag'].sum()/NAV_acc_v2_pre['CIF'].sum()
MAE_large_pre = abs(predicted_rate_NAV_pre - actual_rate_NAV_pre)


# %%

merged_large_corp = pd.merge(large_corp_acc_v2, large_corp_acc_v2_pre, left_on='FINAL_ORR', right_on='CALCULATED_ORR', suffixes=('_post', '_pre'))
merged_mid = pd.merge(mid_acc_v2, mid_acc_v2_pre, left_on='FINAL_ORR', right_on='CALCULATED_ORR', suffixes=('_post', '_pre'))
merged_early = pd.merge(early_stage_acc_v2, early_acc_v2_pre, left_on='FINAL_ORR', right_on='CALCULATED_ORR', suffixes=('_post', '_pre'))
merged_Firm = pd.merge(Firm_acc_v2, Firm_acc_v2_pre, left_on='FINAL_ORR', right_on='CALCULATED_ORR', suffixes=('_post', '_pre'))
merged_CCLOC = pd.merge(CCLOC_acc_v2, CCLOC_acc_v2_pre, left_on='FINAL_ORR', right_on='CALCULATED_ORR', suffixes=('_post', '_pre'))
merged_NAV = pd.merge(NAV_acc_v2, NAV_acc_v2_pre, left_on='FINAL_ORR', right_on='CALCULATED_ORR', suffixes=('_post', '_pre'))



# %%
columns_to_drop = ['CALCULATED_ORR',  'Actual_PD_Post', 'PD_pre', 'Actual_PD_Pre', 'Predict_Default_pre', 'Predict_Default_post']
merged_large_corp2 = merged_large_corp.drop(columns=columns_to_drop)
merged_mid2 = merged_mid.drop(columns=columns_to_drop)
merged_early2 = merged_early.drop(columns=columns_to_drop)
merged_Firm2 = merged_Firm.drop(columns=columns_to_drop)
merged_CCLOC2 = merged_CCLOC.drop(columns=columns_to_drop)
merged_NAV2 = merged_NAV.drop(columns=columns_to_drop)


rename_dict = {'PD_post': 'PD_Midpoint', 'FINAL_ORR': 'ORR', 'CIF_post': 'Total_with_Override', 'default_flag_post': 'Bads_with_Override', 'CIF_pre': 'Total_without_Override', 'default_flag_pre': 'Bads_without_Override'}



merged_large_corp3 = merged_large_corp2.rename(columns=rename_dict)
merged_mid3 = merged_mid2.rename(columns=rename_dict)
merged_early3 = merged_early2.rename(columns=rename_dict)
merged_Firm3 = merged_Firm2.rename(columns=rename_dict)
merged_CCLOC3 = merged_CCLOC2.rename(columns=rename_dict)
merged_NAV3 = merged_NAV2.rename(columns=rename_dict)



new_order = ['ORR', 'PD_Midpoint', 'Bads_with_Override', 'Total_with_Override', 'Bads_without_Override','Total_without_Override']

merged_large_corp3 = merged_large_corp3[new_order]
merged_mid3 = merged_mid3[new_order]
merged_early3 = merged_early3[new_order]
merged_Firm3 = merged_Firm3[new_order]
merged_CCLOC3 = merged_CCLOC3[new_order]
merged_NAV3 = merged_NAV3[new_order]



merged_large_corp3.to_csv('large_corp_post_override.csv') 
merged_mid3.to_csv('mid_post_override.csv') 
merged_early3.to_csv('early_post_override.csv')  
merged_Firm3.to_csv('Firm_post_override.csv')  
merged_CCLOC3.to_csv('CCLOC_post_override.csv') 
merged_NAV3.to_csv('NAV_post_override.csv')  





