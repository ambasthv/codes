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

month_end_12m_prior = month_end - relativedelta(months=12)

month_end_12m_prior = month_end_12m_prior + pd.offsets.MonthEnd(n=-1)
month_end_12m_prior = month_end_12m_prior.strftime("%m/%d/%Y")

last_month = last_month_end.month
kpi_quarter = month_to_quarter(last_month)



eval_dates = [month_end_3m_prior, last_month_end1  ]

model_name = ['GFB CCLOC', 'GFB NAV', 'GFB Firm','Innovation Large Corp', 'Innovation Mid Size', 'Innovation Early Stage' ]


# %%
print(last_month_end1, month_end_3m_prior, month_end_12m_prior, kpi_quarter)

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

     	
      		
				
				and b.DATE_APPROVED > '{month_end_12m_prior}'
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

select  loaddt as MonthEnd, CIF, FINAL_LGD, FACILITY_TYPE, max(CL_OBLIGOR_RISK_RATING) as orr1


from [CRDADMPRD].[dbo].[CDM_CREDIT_LINES_VIEW]

where loaddt in ('{last_12_month_ends1}')

group by loaddt, cif, FACILITY_TYPE, FINAL_LGD










""".format(last_12_month_ends1=last_12_month_ends1)


last_12_ports = pd.DataFrame(pd.read_sql_query(sql_port_12m, conn))

last_12_ports['MonthEnd'] = pd.to_datetime(last_12_ports['MonthEnd']).dt.strftime("%m/%d/%Y")

# %% [markdown]
# #### Section 1: LGD Models Override - In this segment data is extracted for overrides per risk template for the evaluation period.  

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
override_large_corp = override_large_corp[override_large_corp['FINAL_LGD'].notna()]
    
print(override_large_corp.shape)




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
override_mid = combined_override_mid[combined_override_mid['FINAL_LGD'].notna()]

   




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
override_early_stage = combined_override_early[combined_override_early['FINAL_LGD'].notna()]






# %%
# DRR CCLOC

ccloc_kpi = []

sql_override2 = """

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


override_ccloc_raw = pd.read_sql_query(sql_override2, conn)
cif_list_ccloc_kpi = override_ccloc_raw.CIF.unique()

#create  a month end column for the most proximate month end for each date approved

override_ccloc_raw['DATE_APPROVED'] = pd.to_datetime(override_ccloc_raw['DATE_APPROVED'])
override_ccloc_raw['MonthEnd'] = override_ccloc_raw['DATE_APPROVED'] + pd.offsets.MonthEnd(1)
override_ccloc_raw['MonthEnd'] = override_ccloc_raw['MonthEnd'].dt.strftime("%m/%d/%Y")

combined_override_early = pd.merge(override_ccloc_raw, last_12_ports, on=['CIF', 'MonthEnd'], how='left')


#subset the data that doesn't occur in the portfolio (Nan value for ORR) or where the final ORR is 
#not the same as portfolio ORR

override_ccloc = combined_override_early[combined_override_early['orr1'].notna()]
override_ccloc = override_ccloc[override_ccloc.orr1 == override_ccloc.FINAL_ORR]
override_ccloc = combined_override_early[combined_override_early['FINAL_LGD'].notna()]






# %%
# DRR NAV

nav_kpi = []

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


override_nav_raw = pd.read_sql_query(sql_override2, conn)
cif_list_nav_kpi = override_nav_raw.CIF.unique()

#create  a month end column for the most proximate month end for each date approved

override_nav_raw['DATE_APPROVED'] = pd.to_datetime(override_nav_raw['DATE_APPROVED'])
override_nav_raw['MonthEnd'] = override_nav_raw['DATE_APPROVED'] + pd.offsets.MonthEnd(1)
override_nav_raw['MonthEnd'] = override_nav_raw['MonthEnd'].dt.strftime("%m/%d/%Y")

combined_override_early = pd.merge(override_nav_raw, last_12_ports, on=['CIF', 'MonthEnd'], how='left')


#subset the data that doesn't occur in the portfolio (Nan value for ORR) or where the final ORR is 
#not the same as portfolio ORR

override_nav = combined_override_early[combined_override_early['orr1'].notna()]
override_nav = override_nav[override_nav.orr1 == override_nav.FINAL_ORR]
override_nav = combined_override_early[combined_override_early['FINAL_LGD'].notna()]






# %%
#DRR GFB Firm

firm_kpi = []

sql_override2 = """

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


override_firm_raw = pd.read_sql_query(sql_override2, conn)
cif_list_firm_kpi = override_firm_raw.CIF.unique()

#create  a month end column for the most proximate month end for each date approved

override_firm_raw['DATE_APPROVED'] = pd.to_datetime(override_firm_raw['DATE_APPROVED'])
override_firm_raw['MonthEnd'] = override_firm_raw['DATE_APPROVED'] + pd.offsets.MonthEnd(1)
override_firm_raw['MonthEnd'] = override_firm_raw['MonthEnd'].dt.strftime("%m/%d/%Y")

combined_override_ccloc = pd.merge(override_firm_raw, last_12_ports, on=['CIF', 'MonthEnd'], how='left')


#subset the data that doesn't occur in the portfolio (Nan value for ORR) or where the final ORR is 
#not the same as portfolio ORR

override_firm = combined_override_ccloc[combined_override_ccloc['orr1'].notna()]
override_firm = override_firm[override_firm.orr1 == override_firm.FINAL_ORR]
override_firm = combined_override_ccloc[combined_override_ccloc['FINAL_LGD'].notna()]






# %%
grade_map = {'BGC' : 'F',
'BSL' : 'D',
'CFD' : 'C',
'CHT' : 'D',
'FOL' : 'D',
'FOT' : 'E',
'GCT' : 'F',
'GUD' : 'D',
'IRR' : 'E',
'MEZ' : 'F',
'MRR' : 'C',
'NFL' : 'E',
'NFT' : 'F',
'SFD' : 'D',
'SFR' : 'E',
'UNL' : 'G',
'PCC' : 'C',
'NAV' : 'D',
'SFT' : 'A',
'REL' : 'B',
'RET' : 'B',
'SSL' : 'B',
'PAW' : 'C',
'EOF' : 'D',
'LFL' : 'D',
'BAC' : 'D'


}

# %%
"""

LGD by Facility Type Logic (sorry for the formatting)
IF(
CONTAINS("#SFT#", Facility_Type__c),"A",
IF(
CONTAINS("#REL#RET#SSL#", Facility_Type__c),"B",
IF(
CONTAINS("#PCC#PAW#CFD#MRR#", Facility_Type__c),"C",
IF(
CONTAINS("#NAV#FOL#EOF#LFL#CHT#SFD#BAC#BSL#GUD#WHL#NVS#", Facility_Type__c),"D",
IF(
CONTAINS("#FOT#NFL#IRR#PSL#SFR#ICC#APP#CMR#", Facility_Type__c),"E",
IF(
CONTAINS("#BGC#GCT#NFT#BRL#BRT#GCC#MEZ#CFR#", Facility_Type__c),"F",
IF(
CONTAINS("#CFT#UNL#UNT#", Facility_Type__c),"G"

"""


# %%
def is_consistent(row):
    grade = row['FACILITY_TYPE']
    description = row['FINAL_LGD']
    # Check if the description is in the list of acceptable words for that grade
    if grade in grade_map and description in grade_map[grade]:
        return True
    else:
        return False

# Create a new 'is_consistent' column with boolean results
override_large_corp['is_consistent'] = override_large_corp.apply(is_consistent, axis=1)
override_mid['is_consistent'] = override_mid.apply(is_consistent, axis=1)
override_early_stage['is_consistent'] = override_early_stage.apply(is_consistent, axis=1)
override_ccloc['is_consistent'] = override_ccloc.apply(is_consistent, axis=1)
override_nav['is_consistent'] = override_nav.apply(is_consistent, axis=1)
override_firm['is_consistent'] = override_firm.apply(is_consistent, axis=1)

# %%
override_ccloc = override_ccloc.loc[override_ccloc.FACILITY_TYPE.isin(['PCC'])]
override_nav = override_nav.loc[override_nav.FACILITY_TYPE.isin(['NAV'])]
override_firm = override_firm.loc[~override_firm.FACILITY_TYPE.isin(['GUD', 'BSL', 'PCC', 'CMG','SFT'])]
override_large_corp = override_large_corp.loc[~override_large_corp.FACILITY_TYPE.isin(['GUD', 'BSL', 'PCC', 'CMG','SFT'])]
override_mid = override_mid.loc[~override_mid.FACILITY_TYPE.isin(['GUD', 'BSL', 'PCC', 'CMG','SFT'])]
override_early_stage = override_early_stage.loc[~override_early_stage.FACILITY_TYPE.isin(['GUD', 'BSL', 'PCC', 'CMG','SFT'])]

# %%
override_calc = []
override_calc3 = []
override_ccloc2 = 1-(override_ccloc['is_consistent'].sum()/override_ccloc.shape[0])
override_calc.append(override_ccloc2)
override_calc3.append(override_ccloc.shape[0]-override_ccloc['is_consistent'].sum())
override_nav2 = 1-(override_nav['is_consistent'].sum()/override_nav.shape[0])
override_calc.append(override_nav2)
override_calc3.append(override_nav.shape[0]-override_nav['is_consistent'].sum())
override_firm2 = 1-(override_firm['is_consistent'].sum()/override_firm.shape[0])
override_calc.append(override_firm2)
override_calc3.append(override_firm.shape[0]-override_firm['is_consistent'].sum())
override_large_corp2 = 1-(override_large_corp['is_consistent'].sum()/override_large_corp.shape[0])
override_calc.append(override_large_corp2)
override_calc3.append(override_large_corp.shape[0]-override_large_corp['is_consistent'].sum())
override_mid2 = 1-(override_mid['is_consistent'].sum()/override_mid.shape[0])
override_calc.append(override_mid2)
override_calc3.append(override_mid.shape[0]-override_mid['is_consistent'].sum())
override_early_stage2 = 1-(override_early_stage['is_consistent'].sum()/override_early_stage.shape[0])
override_calc.append(override_early_stage2)
override_calc3.append(override_early_stage.shape[0]-override_early_stage['is_consistent'].sum())

override_calc2 = pd.DataFrame({'Model':model_name, 'Override': override_calc })
override_calc2.to_csv('LGD_Override_All_Models.csv')

override_calc4 = pd.DataFrame({'Model':model_name, 'Override': override_calc3 })
override_calc4.to_csv('LGD_Override_All_Models_Total_Numbers.csv')

# %%
override_large_corp.shape

# %%
override_large_corp.to_csv('large_corp_lgd1.csv')
override_mid.to_csv('mid_lgd1.csv')
override_early_stage.to_csv('early_stage_lgd1.csv')
override_ccloc.to_csv('ccloc_lgd2.csv')
override_firm.to_csv('firm_lgd2.csv')
override_nav.to_csv('nav_lgd2.csv')




